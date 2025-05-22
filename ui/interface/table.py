from .widget import *


class TableInterface(HeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.listWidget = ListWidget(self)
        self.listWidget.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.listWidget)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.setTitle("预览区")

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.setTable()

    def setTable(self):

        for i in range(7):  # 行
            for j in range(11):  # 列
                if j % 3 == 2:
                    self.gridLayout.addWidget(QWidget(self), i, j,1,1)
                    self.gridLayout.setRowStretch(i, 1)
                    self.gridLayout.setColumnStretch(j, 1)
                    continue
                self.gridLayout.addWidget(PeopleWidgetTableBase(self), i, j, 1, 1)
                self.gridLayout.setRowStretch(i, 2)
                self.gridLayout.setColumnStretch(j, 2)

        self.viewLayout.addLayout(self.gridLayout)
