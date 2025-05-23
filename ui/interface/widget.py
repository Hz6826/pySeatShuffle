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

        program.PEOPLE_WIDGET.append(self)

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
        mime_data.setData("PeopleWidget", QByteArray(self.getPeople().get_name().encode("utf-8")))
        drag.setMimeData(mime_data)

        drag.setPixmap(drag_pixmap)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        # 执行拖拽操作
        drag.exec_(Qt.MoveAction)

    def getPeople(self):
        return self._people

    def setPeople(self, person: core.Person):
        self._people = person
        self.label.setText(self.getPeople().get_name())
        zbw.setToolTip(self, "\n".join([self.getPeople().get_name()] + [f"{k}：{v}" for k, v in self.getPeople().get_properties().items()]))

    def movePeople(self, new):
        old = self.parent()
        old.removePeople()
        new.setPeople(self)


class PeopleWidgetTableBase(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._people = None

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
            person_name = bytes(event.mimeData().data("PeopleWidget")).decode()
            for i in program.PEOPLE_WIDGET:
                if i.getPeople().get_name() == person_name:
                    self.setPeople(i)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def getPeople(self):
        return self._people

    def setPeople(self, people: PeopleWidget):
        if self._people is not None:
            old_person = self.getPeople()
            old_parent = people.parent()
            if isinstance(old_parent, PeopleWidgetTableBase):
                old_person.movePeople(old_parent)
            else:
                return

        self.removePeople()
        self._people = people
        self.vBoxLayout.addWidget(people)

    def removePeople(self):
        self.vBoxLayout.removeWidget(self.getPeople())
        self._people = None

    def deletePeople(self):
        self.removePeople()

    def clearPeople(self):
        self.removePeople()


class PeopleWidgetBase(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._people = None

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.vBoxLayout)

    def getPeople(self):
        return self._people

    def setPeople(self, people: PeopleWidget):
        if self._people is not None:
            old_person = self.getPeople()
            old_parent = people.parent()
            old_person.movePeople(old_parent)

        self.removePeople()
        self._people = people
        self.vBoxLayout.addWidget(people)

    def removePeople(self):
        self.vBoxLayout.removeWidget(self.getPeople())
        self._people = None

    def deletePeople(self):
        self.removePeople()

    def clearPeople(self):
        self.removePeople()
