import time

from .widget import *


class MainPage(zbw.BasicTab):
    """
    主页
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setTitle("主页")
        self.setIcon(FIF.HOME)
