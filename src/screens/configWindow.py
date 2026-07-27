from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QCheckBox, QComboBox, QDateTimeEdit, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget, QListWidget, QToolButton, QDialog, QDialogButtonBox, QMessageBox

class ConfigWindow(QMainWindow):
    windowHidden = Signal()
    settingsConfirmed = Signal()
    eventsChanged = Signal(object)

    def __init__(self):
        super().__init__()

        self.events = []
        
        self.setWindowTitle("Date Tracker | Setup")
        self.resize(400, 500)

        self.createInterface()

    def createInterface(self):
        centralWidget = QWidget()
        mainLayout = QVBoxLayout()

        titleLabel = QLabel("Date Tracker - Configuration")
        titleLabel.setStyleSheet("font-size: 22px; font-weight: bold;")

        descriptionLabel = QLabel("Configure the appearance, layout and behavior of the app.")

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)

        trackerTitleLabel = QLabel("Name: ")
        self.trackerTitleInput = QLineEdit()
        self.trackerTitleInput.setPlaceholderText("Example: Dog's Birthday")

        targetDateLabel = QLabel("Date and time: ")
        self.targetDateInput = QDateTimeEdit()
        self.targetDateInput.setCalendarPopup(True)
        self.targetDateInput.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.targetDateInput.setDateTime(QDateTime.currentDateTime())

        displayModeLabel = QLabel("Counter display mode: ")
        self.displayModeCombobox = QComboBox()
        self.displayModeCombobox.addItems(["Single-line", "Multi-line", "Compact Single-line"])

        secondaryCountersLabel = QLabel("Secondary counters: ")
        secondaryCountersLabel.setStyleSheet("font-weight: bold;")
        self.weeksCounterCheckbox = QCheckBox("Weeks counter")
        self.hoursCounterCheckbox = QCheckBox("Hours counter")
        self.eventsCheckbox = QCheckBox("Track events until then")
        self.weeksCounterCheckbox.setChecked(True)

        self.eventsContainer = QWidget()
        eventsLayout = QVBoxLayout(self.eventsContainer)
        eventsLayout.setContentsMargins(20, 0, 0, 0)
        eventsLayout.setSpacing(6)

        eventsHeaderLayout = QHBoxLayout()

        eventsLabel = QLabel("Upcoming events")
        eventsLabel.setStyleSheet("font-weight: bold;")

        self.addEventButton = QToolButton()
        self.addEventButton.setText("+")
        self.addEventButton.setFixedSize(28, 28)

        eventsHeaderLayout.addWidget(eventsLabel)
        eventsHeaderLayout.addStretch()
        eventsHeaderLayout.addWidget(self.addEventButton)

        self.eventsListWidget = QListWidget()
        self.eventsListWidget.setMaximumHeight(170)
        self.eventsListWidget.setAlternatingRowColors(True)

        eventsLayout.addLayout(eventsHeaderLayout)
        eventsLayout.addWidget(self.eventsListWidget)

        self.eventsContainer.setVisible(False)

        positionLabel = QLabel("Widget position: ")
        self.positionCombobox = QComboBox()
        self.positionCombobox.addItems(["Top Left", "Top Right", "Bottom Left", "Bottom Right"])

        monitorLabel = QLabel("Screen: ")
        self.monitorCombobox = QComboBox()

        for index, screen in enumerate(QGuiApplication.screens()):
            screenName = screen.name()
            self.monitorCombobox.addItem(f"Monitor {index + 1} - {screenName}", index)

        positionLayout = QHBoxLayout()
        positionColumnLayout = QVBoxLayout()
        positionColumnLayout.addWidget(positionLabel)
        positionColumnLayout.addWidget(self.positionCombobox)

        monitorColumnLayout = QVBoxLayout()
        monitorColumnLayout.addWidget(monitorLabel)
        monitorColumnLayout.addWidget(self.monitorCombobox)

        positionLayout.addLayout(positionColumnLayout)
        positionLayout.addLayout(monitorColumnLayout)

        opacityLabelLayout = QHBoxLayout()
        opacityLabel = QLabel("Background opacity: ")
        self.opacityValueLabel = QLabel("80%")
        opacityLabelLayout.addWidget(opacityLabel)
        opacityLabelLayout.addStretch()
        opacityLabelLayout.addWidget(self.opacityValueLabel)
        self.opacitySlider = QSlider(Qt.Orientation.Horizontal)
        self.opacitySlider.setRange(5, 100)
        self.opacitySlider.setValue(80)

        closeButton = QPushButton("Done")
        closeButton.clicked.connect(self.confirmSettings)


        mainLayout.addWidget(titleLabel)
        mainLayout.addWidget(descriptionLabel)

        mainLayout.addWidget(separator)

        mainLayout.addWidget(trackerTitleLabel)
        mainLayout.addWidget(self.trackerTitleInput)

        mainLayout.addWidget(targetDateLabel)
        mainLayout.addWidget(self.targetDateInput)

        mainLayout.addWidget(displayModeLabel)
        mainLayout.addWidget(self.displayModeCombobox)

        mainLayout.addSpacing(0)
        mainLayout.addWidget(secondaryCountersLabel)
        mainLayout.addWidget(self.weeksCounterCheckbox)
        mainLayout.addWidget(self.hoursCounterCheckbox)
        mainLayout.addWidget(self.eventsCheckbox)
        mainLayout.addWidget(self.eventsContainer)

        self.eventsCheckbox.toggled.connect(self.eventsContainer.setVisible)
        self.addEventButton.clicked.connect(self.openAddEventDialog)
        self.eventsListWidget.itemDoubleClicked.connect(self.removeEventFromList)

        mainLayout.addLayout(positionLayout)

        mainLayout.addLayout(opacityLabelLayout)
        mainLayout.addWidget(self.opacitySlider)

        mainLayout.addStretch()
        mainLayout.addWidget(closeButton)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.resize(400, 650)

    def confirmSettings(self):
        self.settingsConfirmed.emit()
        self.close()

    def openAddEventDialog(self):
        if len(self.events) >= 10:
            QMessageBox.warning(self, "Event limit reached", "You can only add up to 10 events.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add event")
        dialog.setMinimumWidth(360)

        dialogLayout = QVBoxLayout(dialog)

        eventNameLabel = QLabel("Event name:")
        eventNameInput = QLineEdit()
        eventNameInput.setPlaceholderText("Example: Buy tickets")

        eventDateLabel = QLabel("Date and time:")
        eventDateInput = QDateTimeEdit()
        eventDateInput.setCalendarPopup(True)
        eventDateInput.setDisplayFormat("dd/MM/yyyy HH:mm")
        eventDateInput.setMinimumDateTime(QDateTime.currentDateTime())
        eventDateInput.setMaximumDateTime(self.targetDateInput.dateTime())
        eventDateInput.setDateTime(QDateTime.currentDateTime().addDays(1))

        dialogButtons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        dialogButtons.accepted.connect(dialog.accept)
        dialogButtons.rejected.connect(dialog.reject)

        dialogLayout.addWidget(eventNameLabel)
        dialogLayout.addWidget(eventNameInput)
        dialogLayout.addWidget(eventDateLabel)
        dialogLayout.addWidget(eventDateInput)
        dialogLayout.addWidget(dialogButtons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        eventName = eventNameInput.text().strip()
        eventDate = eventDateInput.dateTime()

        if not eventName:
            QMessageBox.warning(self, "Invalid event", "Enter an event name.")
            return

        if eventDate <= QDateTime.currentDateTime():
            QMessageBox.warning(self, "Invalid date", "The event must be in the future.")
            return

        if eventDate > self.targetDateInput.dateTime():
            QMessageBox.warning(self, "Invalid date", "The event cannot be after the main event.")
            return

        self.events.append({
            "name": eventName,
            "date": eventDate,
        })

        self.events.sort(key=lambda event: event["date"].toSecsSinceEpoch())
        self.refreshEventsList()

    def refreshEventsList(self):
        currentDate = QDateTime.currentDateTime()

        self.events = [
            event
            for event in self.events
            if event["date"] > currentDate
        ]

        self.events.sort(key=lambda event: event["date"].toSecsSinceEpoch())

        self.eventsListWidget.clear()

        for event in self.events:
            eventName = event["name"]
            eventDate = event["date"].toString("dd/MM/yyyy HH:mm")

            self.eventsListWidget.addItem(f"{eventName} — {eventDate}")

        self.eventsChanged.emit(self.events.copy())

    def removeEventFromList(self, item):
        eventIndex = self.eventsListWidget.row(item)

        confirmation = QMessageBox.question(
            self,
            "Remove event",
            f"Remove '{self.events[eventIndex]['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        self.events.pop(eventIndex)
        self.refreshEventsList()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.windowHidden.emit()