import traceback

from .widget import *


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
                program.TABLE = program.XLSX_PARSER.parse(get[0])
            elif zb.getFileSuffix(get[0]) == ".json":
                program.TABLE = program.JSON_PARSER.parse(get[0])
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
                program.PEOPLE = program.PEOPLE_PARSER.parse(get[0])
            setting.save("downloadPath", zb.getFileDir(get[0]))
            logging.info(f"导入名单表格文件{get[0]}成功！")
            infoBar = InfoBar(InfoBarIcon.SUCCESS, "成功", f"导入名单表格文件{zb.getFileName(get[0])}成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.BOTTOM, self.window().mainPage)
            self.listInterface.addPeople(program.PEOPLE)
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
        self.cardGroup.clearCard()
        for i in people:
            people_widget = PeopleWidget(self)
            people_widget.setPeople(i)
            widget = PeopleWidgetBase(self)
            widget.setPeople(people_widget)
            self.cardGroup.addCard(widget, i.get_name())
