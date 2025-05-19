from .edit import *
from .table import *

class MainPage(QWidget):
    """
    主页
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.editInterface = EditInterface(self)
        self.tableInterface= TableInterface(self)

        self.hBoxLayout.addWidget(self.tableInterface, 2)
        self.hBoxLayout.addWidget(self.editInterface, 0)

        self.setLayout(self.hBoxLayout)
