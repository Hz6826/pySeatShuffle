from ui import *


if os.environ.get("PSS_ENV").lower() == "dev":
    import faulthandler
    faulthandler.enable()

window = Window()
if program.isStartup and setting.read("autoHide"):
    window.hide()
    logging.info("程序主窗口隐藏！")
else:
    window.show()
    logging.info("程序主窗口展示！")
app.exec()

