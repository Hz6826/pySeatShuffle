import traceback

from .widget import *


class EditInterface(HeaderCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumWidth(250)
        self.setTitle("编辑区")

        self.vBoxLayout2 = QVBoxLayout(self.view)
        self.vBoxLayout2.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.addLayout(self.vBoxLayout2)

        self.hBoxLayout = QHBoxLayout(self)

        self.importSeatButton = PrimaryPushButton("导入座位", self, FIF.DOWN)
        self.importSeatButton.clicked.connect(self.importSeatButtonClicked)

        self.importPeopleButton = PrimaryPushButton("导入名单", self, FIF.DOWN)
        self.importPeopleButton.clicked.connect(self.importPeopleButtonClicked)

        self.exportButton = PushButton("导出", self, FIF.UP)

        self.hBoxLayout.addWidget(self.importSeatButton)
        self.hBoxLayout.addWidget(self.importPeopleButton)
        self.hBoxLayout.addWidget(self.exportButton)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)

        self.vBoxLayout2.addLayout(self.hBoxLayout)
        self.vBoxLayout2.addWidget(self.pivot)
        self.vBoxLayout2.addWidget(self.stackedWidget)

        self.pivot.currentItemChanged.connect(lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

        self.listInterface = ListInterface(self)
        self.rulesInterface = RulesInterface(self)

        self.addSubInterface(self.listInterface, "列表", "列表")
        self.addSubInterface(self.rulesInterface, "规则", "规则")

        self.pivot.setCurrentItem("列表")

    def importSeatButtonClicked(self):
        get = QFileDialog.getOpenFileName(self, "选择座位表格", setting.read("downloadPath"), "表格文件 (*.xlsx *.json)")
        try:
            if not get[0]:
                raise FileNotFoundError("未找到文件！")
            if zb.getFileSuffix(get[0], False) == ".xlsx":
                program.TABLE = program.XLSX_PARSER.parse(get[0])
            elif zb.getFileSuffix(get[0], False) == ".json":
                program.TABLE = program.JSON_PARSER.parse(get[0])
            logging.info(f"导入座位表格文件{get[0]}成功！")
            infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入座位表格文件{zb.getFileName(get[0])}成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM_RIGHT, self.window().mainPage)
        except Exception:
            logging.error(f"导入座位表格文件{get[0]}失败，报错信息：{traceback.format_exc()}！")
            infoBar = InfoBar(InfoBarIcon.ERROR, "失败", f"导入座位表格文件{zb.getFileName(get[0])}失败！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM_RIGHT, self.window().mainPage)
        infoBar.show()

    def importPeopleButtonClicked(self):
        get = QFileDialog.getOpenFileName(self, "选择名单表格", setting.read("downloadPath"), "表格文件 (*.csv)")
        try:
            if not get[0]:
                raise FileNotFoundError("未找到文件！")
            if zb.getFileSuffix(get[0], False) == ".csv":
                program.PEOPLE = program.PEOPLE_PARSER.parse(get[0])
            infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入名单表格文件{zb.getFileName(get[0])}成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM_RIGHT, self.window().mainPage)
            logging.info(f"导入名单表格文件{get[0]}成功！")

            self.listInterface.addPeople(program.PEOPLE)

        except Exception:
            logging.error(f"导入名单表格文件{get[0]}失败，报错信息：{traceback.format_exc()}！")
            infoBar = InfoBar(InfoBarIcon.ERROR, "失败", f"导入名单表格文件{zb.getFileName(get[0])}失败！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM_RIGHT, self.window().mainPage)
        infoBar.show()

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)


class RulesInterface(zbw.BasicPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)


class ListInterface(zbw.BasicTab):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.cardGroup = zbw.CardGroup(self)

        self.vBoxLayout.addWidget(self.cardGroup)

        self.setAcceptDrops(True)

    def addPeople(self, people: list):
        self.cardGroup.clearCard()
        for i in people:
            people_widget = PeopleWidget(self)
            people_widget.setPeople(i)
            widget = PeopleWidgetBase(self)
            widget.setPeople(people_widget)
            self.cardGroup.addCard(widget, i.get_name())

    def dragEnterEvent(self, a0):
        if a0.mimeData().hasUrls():
            a0.acceptProposedAction()

    def dropEvent(self, a0):
        if a0.mimeData().hasUrls():
            if len(a0.mimeData().urls()) > 1:
                return
            url = a0.mimeData().urls()[0]
            if zb.getFileSuffix(url.toLocalFile()) in [".csv", ".xlsx", ".json"]:
                program.PEOPLE = program.PEOPLE_PARSER.parse(url.toLocalFile())
                self.addPeople(program.PEOPLE)
                infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入名单表格文件{zb.getFileName(url.toLocalFile())}成功！",
                                  Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM_RIGHT,
                                  self.window().mainPage)
                logging.info(f"导入名单表格文件{zb.getFileName(url.toLocalFile())}成功！")

                self.parent().listInterface.addPeople(program.PEOPLE)
                infoBar.show()
