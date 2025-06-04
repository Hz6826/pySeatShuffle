import core
from ..program import *


class PeopleWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(30, 20)
        self._people = None

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)

        self.label = SubtitleLabel("", self)
        self.label.setWordWrap(True)

        self.vBoxLayout.addWidget(self.label)

        self.setLayout(self.vBoxLayout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            return

        drag_pixmap = QPixmap(self.size())
        drag_pixmap.fill(Qt.transparent)
        self.render(drag_pixmap)

        painter = QPainter(drag_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        painter.fillRect(drag_pixmap.rect(), QColor(255, 255, 255, 128))  # 设置50%透明度
        painter.end()

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(self._people))
        mime_data.setData("PeopleWidget", QByteArray(self._people.get_name().encode("utf-8")))
        drag.setMimeData(mime_data)

        drag.setPixmap(drag_pixmap)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        # 执行拖拽操作
        drag.exec_(Qt.MoveAction)

    def getPeople(self):
        return self._people

    def setPeople(self, people: core.Person):
        self._people = people
        self.label.setText(self.getPeople().get_name())


class PeopleWidgetTableBase(CardWidget):
    def __init__(self, parent=None, r: int = 0, c: int = 0):
        super().__init__(parent)
        self._people = None

        self._pos = (r, c)

        self.setAcceptDrops(True)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.vBoxLayout)

        self.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasFormat("PeopleWidget"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasFormat("PeopleWidget"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasFormat("PeopleWidget"):
            people_name = bytes(event.mimeData().data("PeopleWidget")).decode()
            if manager.hasPeople(people_name):
                self.setPeople(manager.getPeopleWidget(people_name))
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def getPeople(self):
        return self._people

    def setPeople(self, people: PeopleWidget):
        old_people = self._people
        old_parent = people.parent()
        if old_people:
            if isinstance(old_parent, PeopleWidgetTableBase):
                self.removePeople()
                old_parent.setPeople(old_people)
            else:
                return
        else:
            if isinstance(old_parent, PeopleWidgetTableBase):
                old_parent.removePeople()

            elif isinstance(old_parent, PeopleWidgetBase):
                old_parent.removePeople()
        self.removePeople()
        self._people = people
        self.vBoxLayout.addWidget(people)
        zbw.setToolTip(self, "\n".join([self._people._people.get_name()] + [f"{k}：{v}" for k, v in self._people._people.get_properties().items()]))

    def removePeople(self):
        self.vBoxLayout.removeWidget(self._people)
        self._people, people = None, self._people
        return people

    def deletePeople(self):
        self.removePeople()

    def clearPeople(self):
        self.removePeople()


class PeopleWidgetBase(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._people = None

        self.setMaximumHeight(40)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.vBoxLayout)

    def getPeople(self):
        return self._people

    def setPeople(self, people: PeopleWidget):
        self._people = people
        self.vBoxLayout.addWidget(people)
        zbw.setToolTip(self, "\n".join([self._people._people.get_name()] + [f"{k}：{v}" for k, v in self._people._people.get_properties().items()]))

    def removePeople(self):
        self.parent().removeCard(self._people._people.get_name())
        self.deleteLater()

    def deletePeople(self):
        self.removePeople()

    def clearPeople(self):
        self.removePeople()


class TableManager:
    PEOPLE_PARSER = core.PeopleParser()
    XLSX_PARSER = core.SeatTableParserXlsx()
    JSON_PARSER = core.SeatTableParserJson()
    EXPORTER = core.SeatTableExporter()

    def __init__(self):
        self._table: core.SeatTable | None = None
        self._people: dict = {}
        self._instance: core.Instance = (
            core.Instance("default", [], self._table, core.parse_ruleset(".test/config/ruleset/default.json"))
        )
        self._shuffler = core.Shuffler(self._instance)

    def setTable(self, table):
        self._table = table
        self._instance.set_seat_table(table)

    def getTable(self):
        return self._table

    def setPeople(self, widget: list | dict):
        if isinstance(widget, list):
            for i in widget:
                self._people[i.getPeople()] = i
        elif isinstance(widget, dict):
            for k, v in widget:
                self._people[k] = v

    def getPeople(self):
        return self._people

    def getPeopleWidget(self, name):
        for k, v in self._people.items():
            if k.get_name() == name:
                return v

    def hasPeople(self, name):
        return name in [i.get_name() for i in self._people.keys()]

    def removePeople(self, name):
        for k in list(self._people.keys()):
            if k.get_name() == name:
                widget = self._people.pop(k)
                if isinstance(widget.parent(), PeopleWidgetBase):
                    widget.parent().removePeople()
                elif isinstance(widget.parent(), PeopleWidgetTableBase):
                    widget.parent().removePeople()
                widget.deleteLater()

    def clearPeople(self):
        for k, v in self._people.items():
            if isinstance(v.parent(), PeopleWidgetBase):
                v.parent().removePeople()
            elif isinstance(v.parent(), PeopleWidgetTableBase):
                v.parent().removePeople()
            v.deleteLater()
        self._people = {}

    def getShuffler(self):
        return self._shuffler


manager = TableManager()
