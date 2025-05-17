from .widget import *


class HelpSettingCard(SettingCard):
    """
    帮助设置卡片
    """
    signalBool = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(FIF.HELP, "帮助", "查看程序相关信息", parent)
        self.button1 = HyperlinkButton(program.INSTALL_PATH, "程序安装路径", self, FIF.FOLDER)
        self.button1.clicked.connect(lambda: zb.showFile(program.INSTALL_PATH))
        self.button1.setToolTip("打开程序安装路径")
        self.button1.installEventFilter(ToolTipFilter(self.button1, 1000))

        self.button2 = HyperlinkButton(program.INSTALL_PATH, "程序数据路径", self, FIF.FOLDER)
        self.button2.clicked.connect(lambda: zb.showFile(program.DATA_PATH))
        self.button2.setToolTip("打开程序数据路径")
        self.button2.installEventFilter(ToolTipFilter(self.button2, 1000))

        self.button3 = HyperlinkButton("", "清理程序缓存", self, FIF.BROOM)
        self.button3.clicked.connect(self.button3Clicked)
        self.button3.setToolTip("清理程序运行过程中生成的缓存文件")
        self.button3.installEventFilter(ToolTipFilter(self.button3, 1000))

        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.button3, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.signalBool.connect(self.threadEvent3)

    def button3Clicked(self):
        self.button3.setEnabled(False)

        program.THREAD_POOL.submit(self.clearCache)

    def clearCache(self):
        zb.clearDir(zb.joinPath(program.DATA_PATH, "cache"))
        program.THREAD_POOL.submit(lambda: self.signalBool.emit(True))

    def threadEvent3(self, msg):
        self.button3.setEnabled(True)
        if msg:
            self.infoBar = InfoBar(InfoBarIcon.SUCCESS, "提示", "清理程序缓存成功！", Qt.Orientation.Vertical, True, 5000, InfoBarPosition.TOP_RIGHT, self.window().aboutPage)
            self.infoBar.show()


class ControlSettingCard(SettingCard):
    """
    控制设置卡片
    """

    def __init__(self, parent=None):
        super().__init__(FIF.ALBUM, "控制", "", parent)
        self.button1 = HyperlinkButton("", "重置设置", self, FIF.SYNC)
        self.button1.clicked.connect(self.button1Clicked)
        self.button1.setToolTip("重启程序设置")
        self.button1.installEventFilter(ToolTipFilter(self.button1, 1000))

        self.button2 = PushButton("关闭", self, FIF.CLOSE)
        self.button2.clicked.connect(program.close)
        self.button2.setToolTip("关闭程序")
        self.button2.installEventFilter(ToolTipFilter(self.button2, 1000))

        self.button3 = PushButton("重启", self, FIF.SYNC)
        self.button3.clicked.connect(program.restart)
        self.button3.setToolTip("重启程序")
        self.button3.installEventFilter(ToolTipFilter(self.button3, 1000))

        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.button3, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def button1Clicked(self):
        self.button5 = PushButton("确认", self, FIF.SEND)
        self.button5.clicked.connect(self.button5Clicked)
        self.infoBar = InfoBar(InfoBarIcon.WARNING, "警告", "是否确认重置设置？该操作不可撤销！", Qt.Orientation.Vertical, True, 10000, InfoBarPosition.TOP_RIGHT, self.window().aboutPage)
        self.infoBar.addWidget(self.button5)
        self.infoBar.show()

    def button5Clicked(self):
        setting.reset()
        self.infoBar.close()


class AboutSettingCard(SettingCard):
    """
    关于设置卡片
    """

    def __init__(self, parent=None):
        super().__init__(FIF.INFO, "关于", f"{program.INFO}\nVersion {program.VERSION}. Powered by zbGuiTemplate {program.CORE_VERSION}.", parent)
        self.button1 = HyperlinkButton(program.URL, "程序官网", self, FIF.LINK)
        self.button1.setToolTip("打开程序官网")
        self.button1.installEventFilter(ToolTipFilter(self.button1, 1000))

        self.button2 = HyperlinkButton(program.GITHUB_URL, "GitHub", self, FIF.GITHUB)
        self.button2.setToolTip("打开程序GitHub页面")
        self.button2.installEventFilter(ToolTipFilter(self.button2, 1000))

        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.button2, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class AboutPage(zbw.BasicPage):
    """
    关于页面
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setViewportMargins(0, 70, 0, 0)
        self.setTitle("关于")
        self.setIcon(FIF.INFO)

        self.cardGroup1 = zbw.CardGroup("关于", self)

        self.helpSettingCard = HelpSettingCard()
        self.controlSettingCard = ControlSettingCard()
        self.aboutSettingCard = AboutSettingCard()

        self.cardGroup1.addCard(self.helpSettingCard, "helpSettingCard")
        self.cardGroup1.addCard(self.controlSettingCard, "controlSettingCard")
        self.cardGroup1.addCard(self.aboutSettingCard, "aboutSettingCard")

        self.vBoxLayout.addWidget(self.cardGroup1, 0, Qt.AlignTop)
