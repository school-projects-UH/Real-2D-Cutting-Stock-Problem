import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox, QAction
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush, QPen,QFont
from PyQt5.QtCore import Qt, QPoint, QRect, QThread, pyqtSignal
from pyqtspinner.spinner import WaitingSpinner
from classes import Rectangle, Sheet, Solution
from genetic_algorithm import Solver


EXIT_CODE_REBOOT = -123

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() # create default constructor for QWidget
        self.initializeUI()

    def initializeUI(self):
        self.w = None
        self.setGeometry(100, 100, 100, 100)
        self.setWindowTitle('Asistente de Cortes')
        self.window = QWidget() 
        self.formWidgets()
        self.createMenu()
        self.setCentralWidget(self.window)
        self.show()


    def restart(self):  # function connected to when restart button clicked
        QApplication.exit( EXIT_CODE_REBOOT )

    def formWidgets(self):
        total_label = QLabel("Entre la cantidad de tipos diferentes de hojas : ")
        total = QSpinBox()
        total.setMinimum(1)
        total_button = QPushButton('Aceptar', self)
        total_button.clicked.connect(lambda: self.showDemandForm(total.value(),[total_label,total,total_button]))
        vbox = QVBoxLayout()
        total_hbox = QHBoxLayout()
        total_hbox.addWidget(total_label)
        total_hbox.addWidget(total)
        total_hbox.addWidget(total_button)

        vbox.addSpacing(15)
        vbox.addItem(total_hbox)
        app_form_layout = QFormLayout()
        app_form_layout.addRow(vbox)

        self.window.setLayout(app_form_layout)

    def createMenu(self):
        # Create actions for file menu
        exit_act = QAction('Instrucciones', self)
        exit_act.setShortcut('F1')
        exit_act.triggered.connect(self.show_help)
        # Create menubar
        menu_bar = self.menuBar()
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('Ayuda')
        file_menu.addAction(exit_act)

    def show_help(self):
        pass

    def showDemandForm(self, amount, to_remove):

        for w in to_remove:
            w.setParent(None)
        self.window.layout().takeAt(0).setParent(None)

        rect_label = QLabel("Entre la dimensión de la hoja a picar: ")

        rect_hlabel = QLabel("Altura:")
        rect_hbox = QSpinBox()
        rect_hbox.setMinimum(1)
        rect_hbox.setMaximum(1000000)
        rect_wlabel = QLabel("Ancho:")
        rect_wbox = QSpinBox()
        rect_wbox.setMinimum(1)
        rect_wbox.setMaximum(1000000)
        rect_dim_hbox = QHBoxLayout()
        rect_dim_hbox.addWidget(rect_hlabel)
        rect_dim_hbox.addWidget(rect_hbox)
        rect_dim_hbox.addSpacing(20)
        rect_dim_hbox.addWidget(rect_wlabel)
        rect_dim_hbox.addWidget(rect_wbox)
        rect_dim_hbox.addSpacing(190)

        self.window.layout().addRow(rect_label)
        self.window.layout().addRow(rect_dim_hbox)

        rect_label = QLabel("Entre las dimensiones de las hojas y la demanda: ")
        self.window.layout().addRow(rect_label)
        layout_list = []

        for _ in range(amount):
            hlabel = QLabel("Altura:")
            hbox = QSpinBox()
            hbox.setMinimum(1)
            hbox.setMaximum(1000000)
            wlabel = QLabel("Ancho:")
            wbox = QSpinBox()
            wbox.setMinimum(1)
            wbox.setMaximum(1000000)
            dlabel = QLabel("Demanda:")
            dbox = QSpinBox()
            dbox.setMinimum(1)
            dbox.setMaximum(100000000)
            rect_dim_hbox = QHBoxLayout()
            rect_dim_hbox.addWidget(hlabel)
            rect_dim_hbox.addWidget(hbox)
            rect_dim_hbox.addSpacing(20)
            rect_dim_hbox.addWidget(wlabel)
            rect_dim_hbox.addWidget(wbox)
            rect_dim_hbox.addSpacing(20)
            rect_dim_hbox.addWidget(dlabel)
            rect_dim_hbox.addWidget(dbox)
            self.window.layout().addRow(rect_dim_hbox)
            layout_list.append((wbox,hbox,dbox))

        back_button = QPushButton('Atrás', self)
        back_button.clicked.connect(lambda: self.restart())
        start_button = QPushButton('Aceptar', self)
        start_button.clicked.connect(lambda: self.show_new_window((rect_wbox.value(),rect_hbox.value()), layout_list))
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(back_button)
        buttons_hbox.addWidget(start_button)

        self.window.layout().addRow(buttons_hbox)    
        self.update()


    def show_new_window(self, rect_dim, sheet_dims):
        error = False
        for sheet in sheet_dims:
            w, h, _ = sheet
            if w.value() > rect_dim[0] and h.value() > rect_dim[1]:
                error = True
        if error:
            QMessageBox.warning(self, "Error", "Las dimensiones a cortar no pueden ser mayores que la hoja principal.", QMessageBox.Ok, QMessageBox.Ok)
        elif self.w is None:
                self.w = SolverWindow(rect_dim, sheet_dims,self)
                self.w.show()


class Worker(QThread):
    output = pyqtSignal(Solution)
    def __init__(self,rect_dim, sheet_dims, parent = None):
        QThread.__init__(self, parent)
        self.rect_dim = rect_dim
        self.solver = Solver()
        self.sheet_dims = sheet_dims

    def run(self):        
        rect = Rectangle(*self.rect_dim)
        sheets = []
        for sheet in self.sheet_dims:
            w,h,d = sheet
            sheets.append(Sheet(w.value(), h.value(),d.value()))
        sol = self.solver.solve(rect, sheets)
        self.output.emit(sol)

    def interrupt(self):
        self.solver.stopped = True


class SolverWindow(QWidget):
    def __init__(self, rect_dim, sheet_dims, parent):
        super().__init__()
        self.parent = parent
        self.rectangle = rect_dim
        self.thread = Worker(rect_dim, sheet_dims)
        self.setGeometry(640, 100, 300, 150)
        self.setWindowTitle(' ')
        self.initialize_ui()
        self.setFixedSize(self.size())
        self.update()
        self.thread.start()
        self.thread.output['PyQt_PyObject'].connect(self.show_solution)

    def initialize_ui(self):
        label = QLabel("El resultado puede demorar varios minutos")
        spinner = WaitingSpinner(self,roundness=70.0, opacity=15.0,fade=70.0, radius=10.0, lines=12,line_length=10.0, line_width=5.0,speed=1.0, color=(0, 0, 0))
        spinner.start()  # starts spinning
        cancel_button = QPushButton('Cancelar', self)
        cancel_button.clicked.connect(lambda: self.cancel())
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(spinner)
        vbox.addWidget(cancel_button)
        self.setLayout(vbox)

    def show_solution(self, solution):
        if not self.thread.solver.stopped:
            self.windows = []
            total = len(solution.bins)
            i = 0
            for bin, k in zip(solution.bins, solution.prints_per_pattern):
                self.windows.append(PatternWindow(self, self.rectangle, i, bin, solution.prints_per_pattern[k], total))
                i += 1
            self.windows[0].show() 
            print(solution)
        else:
            print("Stopped")
        self.close()
        self.parent.w = None 

    def cancel(self):
        self.thread.interrupt()
        self.close()
        self.parent.w = None

    def closeEvent(self,event):
        self.thread.interrupt()

class Canvas(QLabel):
    def __init__(self, parent, bin):
        super().__init__(parent)
        self.parent = parent
        self.bin = bin
        self.setFixedSize(parent.width * 6, parent.height * 6)

        # Create a few pen colors
        self.black = '#000000'
        self.blue = '#2041F1'
        self.green = '#12A708'
        self.purple = '#6512F0'
        self.red = '#E00C0C'
        self.orange = '#FF930A'

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.scale(6,6)
        # Use antialiasing to smooth curved edges
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawRectangles(painter)

    def drawRectangles(self, painter):
        pen = QPen(QColor(self.black))
        brush = QBrush(QColor(self.black))
        painter.setPen(pen)
        painter.setBrush(brush) 
        painter.drawRect(0, 0, self.parent.width, self.parent.height)
        for cut in self.bin.cuts:
            x, y = cut.top_left   
            pen = QPen(QColor(self.black))

            # pen.setStyle(Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.white)
            #rect(x,y,w,h)
           
            painter.drawRect(x, y, cut.width, cut.height)

            text = f'{cut.width}x{cut.height}'
            pen = QPen(QColor(self.red))
            painter.setFont(QFont("Helvetica", cut.width//10))
            painter.setPen(pen)
            painter.drawText(x + cut.width//3, y + cut.height//2, text)

        painter.end()


class PatternWindow(QWidget):
    def __init__(self, parent, rectangle,id,bin,k,n):
        super().__init__()
        w, h = rectangle
        self.setWindowTitle('Patrones de Corte')
        self.width = w
        self.height = h
        self.id = id
        self.bin = bin
        self.k = k
        self.n = n
        self.parent = parent
        self.initialize_ui()
        # self.setFixedSize(self.size().width(), self.size().height() + 20)


    def initialize_ui(self):
        label = QLabel(f'Patrón de Corte {self.id + 1} de {self.n}')
        amount = QLabel(f'Cantidad necesaria de repeticiones del patrón: {self.k}')
        prev_button = QPushButton('Anterior', self)
        if self.id == 0:
            prev_button.setEnabled(False)
        prev_button.clicked.connect(lambda: self.show_prev())
        next_button = QPushButton('Siguiente', self)
        if self.id == self.n - 1:
            next_button.setEnabled(False)
        next_button.clicked.connect(lambda: self.show_next())
        form = QFormLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(prev_button)
        hbox.addWidget(label)
        hbox.addWidget(next_button)
        vbox = QVBoxLayout()
        vbox.addWidget(amount)
        canvas = Canvas(self, self.bin)
        form.addRow(hbox)
        form.addRow(canvas)
        form.addRow(vbox)
        self.setLayout(form)   

    def show_next(self):
        self.parent.windows[self.id + 1].show()
        self.close()

    def show_prev(self):
        self.parent.windows[self.id - 1].show()
        self.close()


# Run program
if __name__ == '__main__':
    currentExitCode = EXIT_CODE_REBOOT
    while currentExitCode == EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = MainWindow()
        currentExitCode = app.exec_()
        app = None
