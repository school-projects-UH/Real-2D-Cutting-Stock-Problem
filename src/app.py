import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox, QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush, QPen,QFont, QPolygon, QLinearGradient
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
        self.setWindowTitle('App')
        self.window = QWidget() 
        self.formWidgets()
        self.setCentralWidget(self.window)
        self.show()


    def restart(self):  # function connected to when restart button clicked
        QApplication.exit( EXIT_CODE_REBOOT )

    def formWidgets(self):
        total_label = QLabel("Entra la cantidad de tipos diferentes de hojas")
        total = QSpinBox()
        total.setMinimum(1)
        total_button = QPushButton('Aceptar', self)
        total_button.clicked.connect(lambda: self.showDemandForm(total.value(),[total_label,total,total_button]))

        total_hbox = QHBoxLayout()
        total_hbox.addWidget(total_label)
        total_hbox.addWidget(total)
        total_hbox.addWidget(total_button)

        app_form_layout = QFormLayout()
        app_form_layout.addRow(total_hbox)

        self.window.setLayout(app_form_layout)

    def showDemandForm(self, amount, to_remove):

        for w in to_remove:
            w.setParent(None)
        self.window.layout().takeAt(0).setParent(None)

        rect_label = QLabel("Entra la dimensión de la hoja a picar")

        rect_hlabel = QLabel("Altura:")
        rect_hbox = QSpinBox()
        rect_hbox.setMaximum(1000000)
        rect_wlabel = QLabel("Ancho:")
        rect_wbox = QSpinBox()
        rect_wbox.setMaximum(1000000)
        rect_dim_hbox = QHBoxLayout()
        rect_dim_hbox.addWidget(rect_hlabel)
        rect_dim_hbox.addWidget(rect_hbox)
        rect_dim_hbox.addSpacing(40)
        rect_dim_hbox.addWidget(rect_wlabel)
        rect_dim_hbox.addWidget(rect_wbox)

        self.window.layout().addRow(rect_label)
        self.window.layout().addRow(rect_dim_hbox)

        rect_label = QLabel("Entra las dimensiones de la hojas y su demanda")
        self.window.layout().addRow(rect_label)
        layout_list = []

        for _ in range(amount):
            hlabel = QLabel("Altura:")
            hbox = QSpinBox()
            hbox.setMaximum(1000000)
            wlabel = QLabel("Ancho:")
            wbox = QSpinBox()
            wbox.setMaximum(1000000)
            dlabel = QLabel("Demanda:")
            dbox = QSpinBox()
            dbox.setMaximum(1000000)
            rect_dim_hbox = QHBoxLayout()
            rect_dim_hbox.addWidget(hlabel)
            rect_dim_hbox.addWidget(hbox)
            rect_dim_hbox.addSpacing(40)
            rect_dim_hbox.addWidget(wlabel)
            rect_dim_hbox.addWidget(wbox)
            rect_dim_hbox.addSpacing(40)
            rect_dim_hbox.addWidget(dlabel)
            rect_dim_hbox.addWidget(dbox)
            self.window.layout().addRow(rect_dim_hbox)
            layout_list.append((wbox,hbox,dbox))

        back_button = QPushButton('Atras', self)
        back_button.clicked.connect(lambda: self.restart())
        start_button = QPushButton('Aceptar', self)
        start_button.clicked.connect(lambda: self.show_new_window((rect_wbox.value(),rect_hbox.value()), layout_list))
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addWidget(back_button)
        buttons_hbox.addWidget(start_button)

        self.window.layout().addRow(buttons_hbox)    
        self.update()


    def show_new_window(self,rect_dim, sheet_dims):
        if self.w is None:
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
        self.thread = Worker(rect_dim, sheet_dims)
        self.setGeometry(640, 100, 300, 150)
        self.initialize_ui()
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
            print(solution)
        else:
            print("Stopped")
        self.close()
        self.parent.w = None 

    def cancel(self):
        self.thread.interrupt()
        self.close()
        self.parent.w = None 

class PatternWindow(QWidget):
    def __init__(self, rect_dim, sheet_dims):
        super().__init__()
        h,w = rect_dim
        self.setGeometry(640, 100, w*6, h*6)

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

    def drawRectangles(self,painter):
        pen = QPen(QColor(self.black))
        brush = QBrush(QColor(self.black))
        painter.setPen(pen)
        #rect(x,y,w,h)
        painter.drawRect(0, 0, 30, 40)

        pen = QPen(QColor(self.blue))
        brush = QBrush(QColor(self.blue))
        painter.setPen(pen)
        painter.drawRect(0, 40, 40, 30)

        pen = QPen(QColor(self.green))
        brush = QBrush(QColor(self.green))
        painter.setPen(pen)
        painter.drawRect(30, 0, 30, 40)

        pen = QPen(QColor(self.purple))
        brush = QBrush(QColor(self.black))
        painter.setPen(pen)
        painter.drawRect(40, 40, 25, 25)

        pen = QPen(QColor(self.red))
        brush = QBrush(QColor(self.black))
        painter.setPen(pen)
        painter.drawRect(65, 0, 25, 25)

        pen = QPen(QColor(self.orange))
        brush = QBrush(QColor(self.black))
        painter.setPen(pen)
        painter.drawRect(65, 25, 25, 25)
        painter.end()


# Run program
if __name__ == '__main__':
    currentExitCode = EXIT_CODE_REBOOT
    while currentExitCode == EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = MainWindow()
        currentExitCode = app.exec_()
        app = None
