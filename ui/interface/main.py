from .edit import *
from .table import *

class MainPage(QWidget):
    """
    主页
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.listPage = EditInterface(self)
        self.tablePage= TableInterface(self)

        self.hBoxLayout.addWidget(self.tablePage,2)
        self.hBoxLayout.addWidget(self.listPage,0)

        self.setLayout(self.hBoxLayout)
