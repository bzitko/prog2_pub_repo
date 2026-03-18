import sys
import nbformat
import io
import contextlib
import re
import keyword
import builtins
import tokenize

import threading
import traceback
import time

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QDockWidget,
    QPushButton, QSplitter, QLabel, QPlainTextEdit, QFileDialog, QTextEdit, QSizePolicy, QComboBox, QToolButton, QFrame
)
from PySide6.QtGui import QAction, QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QKeyEvent, QKeySequence, QShortcut, QPainter, QPalette, QPixmap, QIcon
from PySide6.QtCore import Qt, Signal, QTimer, QProcess, QSize
from PySide6.QtWebEngineWidgets import QWebEngineView

from PySide6 import QtCore
from dataclasses import dataclass, field

@dataclass
class Cell:
    type: str
    source: str
    title: str = field(init=False)
    output: str = field(init=False)
    task: str = field(init=False)

    def __post_init__(self):
        self.title = ""
        self.output = ""
        self.task = ""

def read_nb(file_path):
    nb = nbformat.read(file_path, as_version=4)
    
    cells = []
    for nb_cell in nb.cells:
        if nb_cell.cell_type not in ("markdown", "code"):
            continue

        cell = Cell(type=nb_cell.cell_type, source=nb_cell.source)

        if nb_cell.cell_type == "markdown":
            m = re.search(r"^#+\s+(.+)$", cell.source, re.MULTILINE)
            if m:
                title = m.group() # Fixed: Use m.group(1) to get the captured group without the full match
                n = len(title) - len(title.lstrip("# "))
                title = " " * n + title[n:]
                cell.title = title
                


        if nb_cell.cell_type == "code":
            if nb_cell.outputs and nb_cell.outputs[0].get('text'):
                cell.output = nb_cell.outputs[0]['text']  # Fixed: Access 'text' key in the output dict
            
            if cells and cells[-1].type == "markdown":
                cell.title = cells[-1].title
                
                m = re.search(r"\*\*zada(tak|ci)(:)?\*\*", cells[-1].source, re.IGNORECASE)
                if m:
                    cell.task = cells[-1].source[m.end():]
                    
        cells.append(cell)

    return cells

# -------------------------
# LineNumberArea + CodeEditor
# -------------------------
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    
    def __init__(self, font_size=12):
        super().__init__()
        self.font_size = font_size
        font = QFont()
        font.setFamilies(["Courier New", "Consolas", "Monaco", "monospace"])
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)


        self.setCursorWidth(2)
        QApplication.setCursorFlashTime(0)

        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits  # Povećan razmak od 3 na 10 za više prostora
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self.palette().color(QPalette.Base))  # Koristi istu boju pozadine kao code editor
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#666666"))  # Svijetlo siva boja za brojeve
                painter.drawText(0, int(top), self.line_number_area.width()-5, int(self.fontMetrics().height()),
                                 Qt.AlignRight, number)  # Povećan padding s -2 na -5
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#e0e0e0"))
            cursor = self.textCursor()
            cursor.clearSelection()
            selection.cursor = cursor
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Tab and not event.modifiers():
            cursor = self.textCursor()
            cursor.insertText(" " * 4)
            event.accept()
            return

        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            cursor = self.textCursor()
            text = cursor.block().text()
            
            indent = len(text) - len(text.lstrip())

            if text.rstrip().endswith(":"):
                indent += 4
            

            cursor.insertText("\n" + " " * indent)
            event.accept()
            return

        if event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                
                text = cursor.block().text()
                pos_in_line = cursor.positionInBlock()
                before_cursor = text[:pos_in_line]

                if before_cursor.startswith(" ") and before_cursor.strip() == "":
                    # Izračunaj koliko razmaka treba obrisati do prethodne "tab" granice
                    spaces_to_del = pos_in_line % 4
                    if spaces_to_del == 0:
                        spaces_to_del = 4
                    
                    # Izbriši izračunati broj razmaka
                    for _ in range(spaces_to_del):
                        cursor.deletePreviousChar()
                    
                    event.accept()
                    return

        super().keyPressEvent(event) 

    def setFontSize(self, size):
        self.font_size = size
        font = QFont()
        font.setFamilies(["Courier New", "Consolas", "Monaco", "monospace"])
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.update_line_number_area_width(0)

# -------------------------
# Python syntax highlighter
# -------------------------

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # --- Formats ---
        self.formats = {}

        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            if italic:
                f.setFontItalic(True)
            return f

        self.formats["keyword"] = fmt("#0000FF", bold=True)
        self.formats["builtin"] = fmt("#008000")
        self.formats["string"] = fmt("#BA2121")
        self.formats["comment"] = fmt("#999988", italic=True)
        self.formats["number"] = fmt("#666666")
        self.formats["decorator"] = fmt("#AA22FF")

        self._keywords = set(keyword.kwlist)
        self._builtins = set(dir(__builtins__))

    def highlightBlock(self, text):
        self.setCurrentBlockState(0)

        # Tokenizer requires full lines including newline
        line = text + "\n"
        stream = io.StringIO(line)

        try:
            for tok in tokenize.generate_tokens(stream.readline):
                token_type = tok.type
                token_string = tok.string
                start_col = tok.start[1]
                end_col = tok.end[1]

                length = end_col - start_col

                if token_type == tokenize.STRING:
                    self.setFormat(start_col, length, self.formats["string"])

                elif token_type == tokenize.COMMENT:
                    self.setFormat(start_col, length, self.formats["comment"])

                elif token_type == tokenize.NUMBER:
                    self.setFormat(start_col, length, self.formats["number"])

                elif token_type == tokenize.NAME:
                    if token_string in self._keywords:
                        self.setFormat(start_col, length, self.formats["keyword"])
                    elif token_string in self._builtins:
                        self.setFormat(start_col, length, self.formats["builtin"])
                    else:
                        pass

                elif token_type == tokenize.OP:
                    if token_string == "@":
                        self.setFormat(start_col, length, self.formats["decorator"])

        except tokenize.TokenError:
            # Occurs for incomplete multi-line input; ignore safely
            pass


# -------------------------
# Markdown font update
# -------------------------
def update_markdown_font(view: QWebEngineView, size: int):
    js = f"""
    document.body.style.fontSize='{size}pt';
    document.querySelectorAll('pre, code, td, th').forEach(p => {{ p.style.fontSize='{size}pt'; }});
    """
    view.page().runJavaScript(js)

# -------------------------
# NotebookViewer
# -------------------------
class NotebookViewer(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Notebook Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.cells = []
        self.index = 0
        self.font_size = 12
        self.start_time = None
        self.process = None

        # Get info if OS is in dark mode
        current_scheme = QApplication.styleHints().colorScheme()
        self.dark_mode = None
        if current_scheme == Qt.ColorScheme.Dark:
            self.dark_mode = True
        elif current_scheme == Qt.ColorScheme.Light:
            self.dark_mode = False

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Actions
        def make_unicode_icon(unicode_char, color="black", size=32):
            pixmap = QPixmap(QSize(size, size))
            pixmap.fill(Qt.transparent)
    
            painter = QPainter(pixmap)
            painter.setPen(QColor(color))  # Arrow color
            font = QFont()
            font.setFamilies(["Courier New"])
            #font.setFamilies(["Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji"])
            font.setPointSize(size // 2)
            font.setBold(True)
            painter.setFont(font)
            
            painter.drawText(pixmap.rect(), Qt.AlignCenter, unicode_char)
            painter.end()
            return QIcon(pixmap)


        def make_action(icon, title, shortcut, connect_fn):
            action = QAction(icon, title, self)
            action.setShortcut(shortcut)
            action.setToolTip(f"{title} ({action.shortcut().toString(QKeySequence.NativeText)})")
            action.triggered.connect(connect_fn)
            return action

        self.open_action = make_action(make_unicode_icon("\U0001F4C4"), "Open", "Ctrl+O", self.load_notebook)
        self.reopen_action = make_action(make_unicode_icon("↻"), "Reload", "Ctrl+R", self.reload_notebook)        
        self.prev_action = make_action(make_unicode_icon("⬅"), "Previous", "Ctrl+Left", self.prev_cell)
        self.next_action = make_action(make_unicode_icon("⮕"), "Next", "Ctrl+Right", self.next_cell)


        self.run_action = make_action(make_unicode_icon("▶", "green"), "Run", "Ctrl+B", self.run_current_cell)
        self.stop_action = make_action(make_unicode_icon("⏹", "Red"), "Stop", "Esc", self.stop_execution)

        self.zoom_out_action = make_action(make_unicode_icon("➖"), "Zoom Out", "Ctrl+-", self.zoom_out)
        self.zoom_in_action = make_action(make_unicode_icon("➕"), "Zoom In", "Ctrl++", self.zoom_in)


        # Toolbar with navigation
        toolbar = self.addToolBar("Navigation")
        
        toolbar.addAction(self.prev_action)
        toolbar.addAction(self.next_action)
        toolbar.addSeparator()

        # Title combo in toolbar
        self.title_combo = QComboBox()
        self.title_combo.currentIndexChanged.connect(self.on_title_selected)
        toolbar.addWidget(self.title_combo)

        toolbar.addSeparator()

        # Open dialog in toolbar
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.reopen_action)
        toolbar.addSeparator()

        # Run and Stop buttons in toolbar
        toolbar.addAction(self.run_action)
        toolbar.addAction(self.stop_action)

        # Cell display area
        self.cell_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        self.cell_container.setLayout(container_layout)
        self.cell_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.cell_container, 1)  # Add stretch factor of 1

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Status bar with sections
        statusbar = self.statusBar()
        
        # Left: Cell info
        self.status_cell_info = QLabel("Cell 1/1")
        statusbar.addWidget(self.status_cell_info, 1)
        
        # Middle: Execution status
        self.status_execution = QLabel("")
        statusbar.addWidget(self.status_execution, 0)
        
        # Right: Zoom control (− button | 100% | + button)
        zoom_widget = QWidget()
        zoom_layout = QHBoxLayout()
        zoom_layout.setContentsMargins(0, 0, 0, 0)
        zoom_layout.setSpacing(4)
        
        self.minus_button = QToolButton()
        self.minus_button.setDefaultAction(self.zoom_out_action)
        zoom_layout.addWidget(self.minus_button)
        
        self.status_zoom = QLabel("100%")
        self.status_zoom.setFixedWidth(40)
        self.status_zoom.setAlignment(Qt.AlignCenter)
        zoom_layout.addWidget(self.status_zoom)
        
        self.plus_button = QToolButton()
        self.plus_button.setDefaultAction(self.zoom_in_action)
        zoom_layout.addWidget(self.plus_button)
        
        zoom_widget.setLayout(zoom_layout)
        statusbar.addPermanentWidget(zoom_widget)


        QApplication.instance().focusChanged.connect(self.on_focus_changed)

        # --- Persistent Widgets ---
        self.markdown_view = QWebEngineView()
        self.task_view = QWebEngineView()
        self.code_editor = CodeEditor(self.font_size)
        self.output_view = QPlainTextEdit()
        font = QFont()
        font.setFamilies(["Courier New", "Consolas", "Monaco", "monospace"])
        font.setStyleHint(QFont.Monospace)
        font.setPointSize(self.font_size)
        self.output_view.setFont(font)

        self.output_view.setReadOnly(False)
        self.output_view.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        # Setup Docks once
        self.editor_dock = QDockWidget("Code", self)
        self.editor_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.editor_dock.setWidget(self.code_editor)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.editor_dock)

        self.output_dock = QDockWidget("Output", self)
        self.output_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.output_dock.setWidget(self.output_view)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.output_dock)

        # Set task_view as central (it will show markdown or task info)
        # We can use a QStackedWidget or just toggle between markdown_view and task_view
        self.central_stack = QStackedWidget()
        self.central_stack.addWidget(self.markdown_view)
        self.central_stack.addWidget(self.task_view)
        self.setCentralWidget(self.central_stack)
        
        # Initial state: hide everything until a notebook is loaded
        self.editor_dock.hide()
        self.output_dock.hide()        

        self.load_notebook()
        
    def on_title_selected(self, combo_index):
        if combo_index >= 0 and combo_index < len(self.markdown_indices):
            self.index = self.markdown_indices[combo_index]
            self.show_cell()

    def on_focus_changed(self, old_widget, new_widget):
        if new_widget == self.code_editor or new_widget == self.output_view:
            # Disable the shortcut only, not the action itself
            self.prev_action.setShortcut(QKeySequence()) 
            self.next_action.setShortcut(QKeySequence()) 
        else:
            # Restore the shortcut when leaving the editor
            self.prev_action.setShortcut(QKeySequence("Ctrl+Left")) 
            self.next_action.setShortcut(QKeySequence("Ctrl+Right"))


    def read_notebook(self, index=None):
        self.cells = read_nb(self.file_path)

        # Collect markdown titles and their indices
        self.markdown_titles = []
        self.markdown_indices = []
        for i, cell in enumerate(self.cells):
            if cell.type == "markdown" and cell.title:
                self.markdown_titles.append(cell.title)
                self.markdown_indices.append(i)

        self.title_combo.clear()
        self.title_combo.addItems(self.markdown_titles)

        if index is not None:
            self.index = index

        self.show_cell()

    def load_notebook(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Open Notebook", "", "Jupyter Notebook (*.ipynb)")
        if not self.file_path:
            return
        
        self.read_notebook()

    def reload_notebook(self):
        self.read_notebook(self.index)

    def clear_cell(self):
        # Just clear the content, don't delete the objects
        self.code_editor.clear()
        self.output_view.clear()
        self.markdown_view.setHtml("")
        self.task_view.setHtml("")

    def show_cell(self):
        cell = self.cells[self.index]
        
        if cell.type == "markdown":
            # Update Content
            self.markdown_view.setHtml(self.markdown_to_html(cell.source))
            update_markdown_font(self.markdown_view, self.font_size)
            
            # Visibility
            self.central_stack.setCurrentWidget(self.markdown_view)
            self.editor_dock.hide()
            self.output_dock.hide()

        elif cell.type == "code":
            # Update Content
            if cell.task:
                self.task_view.setHtml(self.markdown_to_html(cell.task))
                self.task_view.show()
            else:
                self.task_view.setHtml("") # Or a placeholder
                
            self.code_editor.setPlainText(cell.source)
            self.output_view.setPlainText(cell.output)
            
            # Ensure highlighter is attached (only needs to happen once if editor is persistent)
            if not hasattr(self, 'highlighter'):
                self.highlighter = PythonHighlighter(self.code_editor.document())

            # Visibility
            self.central_stack.setCurrentWidget(self.task_view)
            self.editor_dock.show()
            self.output_dock.show()

        self.update_ui_state(cell)

    def update_ui_state(self, cell):
        """Helper to handle toolbar and status bar updates"""
        # Update combo box
        if self.index in self.markdown_indices:
            combo_index = self.markdown_indices.index(self.index)
            self.title_combo.blockSignals(True)
            self.title_combo.setCurrentIndex(combo_index)
            self.title_combo.blockSignals(False)
        else:
            self.title_combo.setCurrentIndex(-1)

        # Enable/Disable actions
        is_code = (cell.type == "code")
        self.run_action.setEnabled(is_code)
        self.stop_action.setEnabled(is_code)
        
        # Status text
        title_str = f" : {cell.title.strip()}" if cell.title else ""
        self.status_cell_info.setText(f"Slide {self.index + 1} of {len(self.cells)}{title_str}")

    def markdown_to_html(self, text):
        import markdown
        from pygments.formatters import HtmlFormatter
        
        # Koristi codehilite ekstenziju za bojanje koda
        md_html = markdown.markdown(text, extensions=["extra", "tables", "fenced_code", "codehilite", "sane_lists", "nl2br"])
        
        # Dodaj Pygments CSS za bojanje
        formatter = HtmlFormatter(style='default')
        pygments_css = formatter.get_style_defs('.codehilite')
        
        html = f"""
        <html>
        <head>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script>
        MathJax = {{
            tex: {{inlineMath: [['$', '$']]}},
            svg: {{fontCache: 'global'}}
        }};
        </script>

        <script id="MathJax-script" async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
        </script>
        <style>
        body {{ font-family: sans-serif; font-size: {self.font_size}pt; }}
        code {{ background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; }}
        blockquote {{ margin: 10px 0px 10px 10px; padding: 5px 5px; background-color: #f9f9f9; color: #555; border-radius: 0 4px 4px 0;}}        
        pre {{ background-color: #f0f0f0; padding: 5px; border-radius: 3px; }}
        table {{ border-collapse: collapse; }}
        th, td {{ border: 1px solid black; padding: 3px; }}
        {pygments_css}
        </style>
        </head>
        <body>{md_html}</body>
        </html>
        """
        return html

    def stop_execution(self):
        if self.process and self.process.state() != QProcess.NotRunning:
            self.process.kill()

    def run_current_cell(self):
        if not self.code_editor:
            return

        if self.process and self.process.state() != QProcess.NotRunning:
            return

        self.process = QProcess(self)

        code = self.code_editor.toPlainText()
        self.process.setProgram(sys.executable)
        self.process.setArguments(["-u", "-c", code])
        self.process.finished.connect(self._process_finished)
        
        # Disable all buttons
        self.prev_action.setEnabled(False)
        self.next_action.setEnabled(False)
        self.open_action.setEnabled(False)
        self.reopen_action.setEnabled(False)
        self.run_action.setEnabled(False)
        self.zoom_in_action.setEnabled(False)
        self.zoom_out_action.setEnabled(False)
        self.title_combo.setEnabled(False)

        if self.code_editor:
            self.code_editor.setReadOnly(True)

        self.status_execution.setText("Running...")
        self.start_time = time.time()

        self.output_view.clear()
        self.process.start()

    def _process_finished(self):
        elapsed = time.time() - self.start_time
        self.status_execution.setText(f"Finished in {elapsed:.2f}s")
        self.start_time = None

        out = self.process.readAllStandardOutput().data().decode("utf-8")
        err = self.process.readAllStandardError().data().decode("utf-8")

        self.output_view.setPlainText(out + err)

        self.process = None

        # Re-enable all buttons
        self.prev_action.setEnabled(True)
        self.next_action.setEnabled(True)
        self.open_action.setEnabled(True)
        self.reopen_action.setEnabled(True)
        self.run_action.setEnabled(True)
        self.zoom_in_action.setEnabled(True)
        self.zoom_out_action.setEnabled(True)
        
        self.title_combo.setEnabled(True)
        self.code_editor.setReadOnly(False)

    def next_cell(self):
        if self.index < len(self.cells)-1:
            self.index += 1
            self.show_cell()

    def prev_cell(self):
        if self.index > 0:
            self.index -= 1
            self.show_cell()

    def zoom_in(self):
        self.font_size += 1
        self.status_zoom.setText(f"{100 + (self.font_size - 12) * 10}%")
        self.set_fonts()

    def zoom_out(self):
        if self.font_size > 1:
            self.font_size -= 1
            self.status_zoom.setText(f"{100 + (self.font_size - 12) * 10}%")
            self.set_fonts()

    def set_fonts(self):
        if getattr(self, "code_editor", None):
            self.code_editor.setFontSize(self.font_size)
        if getattr(self, "output_view", None):
            font = self.output_view.font()
            font.setPointSize(self.font_size)
            self.output_view.setFont(font)
        if getattr(self, "markdown_view", None):
            update_markdown_font(self.markdown_view, self.font_size)
        if getattr(self, "task_view", None):
            update_markdown_font(self.task_view, self.font_size)

    def adjust_task_width(self, ok):
        if ok and getattr(self, "task_view", None):
            # Dohvati širinu sadržaja putem JavaScript-a i postavi fiksnu širinu
            self.task_view.page().runJavaScript(
                "document.body.scrollWidth",
                lambda width: self.task_view.setFixedWidth(width + 20)  # +20 za padding/margine
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow::separator {background: palette(window); width: 5px; height: 5px;}
        QSplitter::handle {background: palette(window); width: 5px; height: 5px;}
    """)

    viewer = NotebookViewer()
    viewer.show()
    sys.exit(app.exec())
