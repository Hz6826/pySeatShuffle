import traceback

from .widget import *


class MainPage(QWidget):
    """
    主页
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.hBoxLayout = QHBoxLayout(self)

        self.editInterface = EditInterface(self)
        self.tableInterface = TableInterface(self)

        self.hBoxLayout.addWidget(self.tableInterface, 2)
        self.hBoxLayout.addWidget(self.editInterface, 0)

        self.setLayout(self.hBoxLayout)


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

        self.viewLayout.addLayout(self.gridLayout)

    def setTable(self):

        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            self.parent().editInterface.listInterface.addPeople(list(manager.getPeople().keys()))

            if widget is not None:
                widget.deleteLater()

        table = manager.getTable()
        for group in table.get_seat_groups():
            for seat in group.get_seats():
                c, r = seat.get_pos()
                self.gridLayout.addWidget(PeopleWidgetTableBase(self), r - 2, c - 1, 1, 1)
                # self.gridLayout.setRowStretch(r-1, 2)
                # self.gridLayout.setColumnStretch(c-1, 2)
        ct, rt = table.get_size()
        for r in range(rt):
            for c in range(ct):
                if not self.gridLayout.itemAtPosition(r, c):
                    self.gridLayout.addWidget(QWidget(self), r, c, 1, 1)
                    # self.gridLayout.setRowStretch(r, 1)
                    # self.gridLayout.setColumnStretch(c, 1)


class EditInterface(HeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(100)
        self.setMaximumWidth(250)
        self.setTitle("编辑区")

        self.vBoxLayout2 = QVBoxLayout(self.view)
        self.vBoxLayout2.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.addLayout(self.vBoxLayout2)

        self.importFileChooser1 = zbw.FileChooser(self)
        self.importFileChooser1.setSuffix({"表格文件": [".xlsx", ".json"]})
        self.importFileChooser1.setOnlyOne(True)
        self.importFileChooser1.setDefaultPath(setting.read("downloadPath"))
        self.importFileChooser1.setDescription("座位表")
        self.importFileChooser1.setFixedHeight(100)
        self.importFileChooser1.fileChoosedSignal.connect(self.importSeatButtonClicked)

        self.importFileChooser2 = zbw.FileChooser(self)
        self.importFileChooser2.setSuffix({"名单文件": [".csv"]})
        self.importFileChooser2.setOnlyOne(True)
        self.importFileChooser2.setDefaultPath(setting.read("downloadPath"))
        self.importFileChooser2.setDescription("名单")
        self.importFileChooser2.setFixedHeight(100)
        self.importFileChooser2.fileChoosedSignal.connect(self.importPeopleButtonClicked)

        self.exportButton = PushButton("导出", self, FIF.UP)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)

        self.vBoxLayout2.addWidget(self.importFileChooser1, 0, Qt.AlignCenter)
        self.vBoxLayout2.addWidget(self.exportButton)
        self.vBoxLayout2.addWidget(self.pivot)
        self.vBoxLayout2.addWidget(self.stackedWidget)

        self.pivot.currentItemChanged.connect(lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

        self.listInterface = ListInterface(self)
        self.rulesInterface = RulesInterface(self)

        self.listInterface.vBoxLayout.insertWidget(0, self.importFileChooser2, 0, Qt.AlignCenter)

        self.addSubInterface(self.listInterface, "名单", "名单")
        self.addSubInterface(self.rulesInterface, "规则", "规则")

        self.pivot.setCurrentItem("名单")

        setting.signalConnect(self.settingChanged)

    def settingChanged(self, name):
        if name == "downloadPath":
            self.importFileChooser1.setDefaultPath(setting.read("downloadPath"))
            self.importFileChooser2.setDefaultPath(setting.read("downloadPath"))

    def importSeatButtonClicked(self, get):
        try:
            if not get[0]:
                raise FileNotFoundError("未找到文件！")
            if zb.getFileSuffix(get[0]) == ".xlsx":
                manager.setTable(manager.XLSX_PARSER.parse(get[0]))
            elif zb.getFileSuffix(get[0]) == ".json":
                manager.setTable(manager.JSON_PARSER.parse(get[0]))
            self.window().mainPage.tableInterface.setTable()  # FIXME: see GH-2
            setting.save("downloadPath", zb.getFileDir(get[0]))
            logging.info(f"导入座位表格文件{get[0]}成功！")
            infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入座位表格文件{zb.getFileName(get[0])}成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM, self.window().mainPage)
        except Exception:
            logging.error(f"导入座位表格文件{get[0]}失败，报错信息：{traceback.format_exc()}！")
            infoBar = InfoBar(InfoBarIcon.ERROR, "失败", f"导入座位表格文件{zb.getFileName(get[0])}失败！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM, self.window().mainPage)
        infoBar.show()

    def importPeopleButtonClicked(self, get):
        try:
            if not get[0]:
                raise FileNotFoundError("未找到文件！")
            if zb.getFileSuffix(get[0]) == ".csv":
                people = manager.PEOPLE_PARSER.parse(get[0])
            self.listInterface.addPeople(people)
            setting.save("downloadPath", zb.getFileDir(get[0]))
            logging.info(f"导入名单表格文件{get[0]}成功！")
            infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入名单表格文件{zb.getFileName(get[0])}成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM, self.window().mainPage)
        except Exception:
            logging.error(f"导入名单表格文件{get[0]}失败，报错信息：{traceback.format_exc()}！")
            infoBar = InfoBar(InfoBarIcon.ERROR, "失败", f"导入名单表格文件{zb.getFileName(get[0])}失败！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM, self.window().mainPage)
        infoBar.show()

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)


class RulesInterface(zbw.BasicPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class ListInterface(zbw.BasicTab):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.cardGroup = zbw.CardGroup(self)
        self.cardGroup.setShowTitle(False)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.cardGroup)

    def addPeople(self, people: list):
        manager.clearPeople()
        result = []
        for i in people:
            people_widget = PeopleWidget(self)
            people_widget.setPeople(i)
            widget = PeopleWidgetBase(self)
            widget.setPeople(people_widget)
            self.cardGroup.addCard(widget, i.get_name())
            result.append(people_widget)
            widget.layout()
        manager.setPeople(result)
