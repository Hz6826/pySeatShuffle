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


class Manager(QWidget):
    PEOPLE_PARSER = core.PeopleParser()
    XLSX_PARSER = core.SeatTableParserXlsx()
    JSON_PARSER = core.SeatTableParserJson()
    EXPORTER = core.SeatTableExporter()

    table: core.SeatTable = None
    people: dict = {}  # {name:{"people":core.Person, "widget": PeopleWidget}}
    table_widget: dict = {}

    def __init__(self):
        super().__init__()

    @property
    def editInterface(self):
        return self.parent().mainPage.editInterface

    @property
    def shuffleInterface(self):
        return self.parent().mainPage.shuffleInterface

    @property
    def tableInterface(self):
        return self.parent().mainPage.tableInterface

    @property
    def listInterface(self):
        return self.parent().mainPage.editInterface.listInterface

    @property
    def rulesInterface(self):
        return self.parent().mainPage.editInterface.rulesInterface

    def getTable(self):
        return self.table

    def setTable(self, table):
        self.table = table

    def getPeople(self, name: str | core.Person | PeopleWidget):
        if isinstance(name, str):
            return self.people.get(name, {}).get("people", None)
        elif isinstance(name, core.Person):
            return name
        elif isinstance(name, PeopleWidget):
            return name.getPeople()
        return None

    def getPeopleWidget(self, name: str | core.Person | PeopleWidget):
        if isinstance(name, str):
            return self.people.get(name, {}).get("widget", None)
        elif isinstance(name, core.Person):
            return self.people.get(name.get_name(), {}).get("widget", None)
        elif isinstance(name, PeopleWidget):
            return name
        return None

    def getPeoples(self):
        return [p["people"] for p in self.people.values()]

    def getPeopleWidgets(self):
        return [p["widget"] for p in self.people.values()]

    def setPeople(self, people: core.Person | PeopleWidget):
        if isinstance(people, core.Person):
            people_widget = PeopleWidget()
            people_widget.setPeople(people)
            name = people.get_name()
            if name in self.people.keys():
                existing_widget = self.people[name]["widget"]
                if isinstance(existing_widget.parent(), PeopleWidgetBase):
                    existing_widget.parent().removePeople()
                elif isinstance(existing_widget.parent(), PeopleWidgetTableBase):
                    existing_widget.parent().removePeople()
                existing_widget.deleteLater()
            self.people[name] = {"people": people, "widget": people_widget}
        elif isinstance(people, PeopleWidget):
            name = people.getPeople().get_name()
            if name in self.people.keys():
                existing_widget = self.people[name]["widget"]
                if isinstance(existing_widget.parent(), PeopleWidgetBase):
                    existing_widget.parent().removePeople()
                elif isinstance(existing_widget.parent(), PeopleWidgetTableBase):
                    existing_widget.parent().removePeople()
                existing_widget.deleteLater()
            self.people[name] = {"people": people.getPeople(), "widget": people}

    def setPeoples(self, peoples: list[core.Person | PeopleWidget]):
        for people in peoples:
            self.setPeople(people)

    def hasPeople(self, name: str | core.Person | PeopleWidget):
        if isinstance(name, str):
            return name in self.people.keys()
        elif isinstance(name, core.Person):
            return name.get_name() in self.people.keys()
        elif isinstance(name, PeopleWidget):
            return name.getPeople().get_name() in self.people.keys()
        return False

    def removePeople(self, name: str | core.Person | PeopleWidget):
        if isinstance(name, str):
            if name in self.people.keys():
                name = name
        elif isinstance(name, core.Person):
            if name.get_name() in self.people.keys():
                name = name.get_name()
        elif isinstance(name, PeopleWidget):
            if name.getPeople().get_name() in self.people.keys():
                name = name.getPeople().get_name()
        else:
            return
        v = self.people.pop(name, None)
        if isinstance(v, dict):
            widget = v["widget"]
            if isinstance(widget.parent(), PeopleWidgetBase):
                widget.parent().removePeople()
            elif isinstance(widget.parent(), PeopleWidgetTableBase):
                widget.parent().removePeople()
            widget.deleteLater()

    def clearPeople(self):
        for widget in self.getPeopleWidgets():
            if isinstance(widget.parent(), PeopleWidgetBase):
                widget.parent().removePeople()
            elif isinstance(widget.parent(), PeopleWidgetTableBase):
                widget.parent().removePeople()
            widget.deleteLater()
        self.people = {}

    def setPeopleList(self):
        self.listInterface.cardGroup.clearCard()

        for k, v in self.people.items():
            people_widget: PeopleWidget = v["widget"]
            people_widget.setParent(self.listInterface)
            widget = PeopleWidgetBase(self.listInterface)
            widget.setPeople(people_widget)
            self.listInterface.cardGroup.addCard(widget, k)
            widget.layout()

    def getTableWidgets(self):
        return self.table_widget

    def getTableWidget(self, pos: (int, int)):
        return self.table_widget.get(pos, None)

    def getPeopleAtPos(self, pos: (int, int)):
        """
        获取指定位置的人员
        :return: People
        """
        widget: PeopleWidgetTableBase | None = self.getTableWidget(pos)
        if widget:
            return widget.getPeople().getPeople()
        return None

    def getAllPeopleInTable(self):
        """
        获取所有人员
        :return: dict
        """
        return {k: v.getPeople().getPeople() for k, v in manager.table_widget.items() if v.getPeople() is not None and v.getPeople().getPeople() is not None}


manager = Manager()
