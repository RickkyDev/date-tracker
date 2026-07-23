from PySide6.QtCore import Qt, QDateTime, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QCheckBox, QComboBox, QDateTimeEdit, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget

class ConfigWindow(QMainWindow):
    windowHidden = Signal()
    settingsConfirmed = Signal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Date Tracker | Setup")
        self.resize(600, 450)

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
        self.weeksCounterCheckbox.setChecked(True)

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

        mainLayout.addLayout(positionLayout)

        mainLayout.addLayout(opacityLabelLayout)
        mainLayout.addWidget(self.opacitySlider)

        mainLayout.addStretch()
        mainLayout.addWidget(closeButton)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.resize(520, 650)

    def confirmSettings(self):
        self.settingsConfirmed.emit()
        self.close()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.windowHidden.emit()