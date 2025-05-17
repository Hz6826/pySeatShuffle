from .interface import *


class Window(zbw.Window):
    """
    主窗口
    """

    def __init__(self):
        super().__init__()

        # 托盘组件

        self.mainPage = MainPage(self)
        self.settingPage = SettingPage(self)
        self.aboutPage = AboutPage(self)
        self.addPage(self.mainPage, self.mainPage.title(), self.mainPage.icon(), "top")
        self.addSeparator("top")
        self.addSeparator("bottom")
        self.addPage(self.settingPage, self.settingPage.title(), self.settingPage.icon(), "bottom")
        self.addPage(self.aboutPage, self.aboutPage.title(), self.aboutPage.icon(), "bottom")

        # 外观调整
        self.navigationInterface.setAcrylicEnabled(True)
        # 窗口属性
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon(program.ICON))
        self.setWindowTitle(program.TITLE)
        self.navigationInterface.setReturnButtonVisible(False)
        self.show()
        self.resize(900, 700)
        # 窗口居中
        desktop = QApplication.screens()[0].size()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        # 设置数据异常提醒
        if setting.errorState:
            self.infoBar = InfoBar(InfoBarIcon.ERROR, "错误", "设置文件数据错误，已自动恢复至默认选项，具体错误原因请查看程序日志！", Qt.Orientation.Vertical, True, -1, InfoBarPosition.TOP_RIGHT, self.mainPage)
            self.infoBar.show()

    def keyPressEvent(self, QKeyEvent):
        """
        自定义按键事件
        """
        # Esc键
        if QKeyEvent.key() == Qt.Key.Key_Escape:
            if setting.read("hideWhenClose"):
                self.hide()

    def closeEvent(self, QCloseEvent):
        """
        自定义关闭事件
        """
        QCloseEvent.ignore()
        if setting.read("hideWhenClose"):
            self.hide()
        else:
            program.close()


logging.debug("程序主窗口类初始化成功！")
