from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QDateTime, QSettings
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from src.screens.configWindow import ConfigWindow
from src.screens.trackerWidget import TrackerWidget
from src.rsc import getResourcePath

class AppController:
    def __init__(self, app: QApplication):
        self.app = app

        self.settings = QSettings("RickDev", "DateTracker")

        self.configWindow = ConfigWindow()
        self.trackerWidget = TrackerWidget()

        self.loadSettings()

        self.configWindow.trackerTitleInput.textChanged.connect(self.trackerWidget.setTrackerTitle)
        self.configWindow.weeksCounterCheckbox.toggled.connect(self.trackerWidget.setWeeksCounterVisible)
        self.configWindow.hoursCounterCheckbox.toggled.connect(self.trackerWidget.setHoursCounterVisible)
        self.configWindow.positionCombobox.currentTextChanged.connect(self.trackerWidget.setWidgetPosition)
        self.configWindow.opacitySlider.valueChanged.connect(self.trackerWidget.setBackgroundOpacity)
        self.configWindow.opacitySlider.valueChanged.connect(lambda value: self.configWindow.opacityValueLabel.setText(f"{value}%"))
        self.configWindow.targetDateInput.dateTimeChanged.connect(self.trackerWidget.setTargetDate)
        self.configWindow.displayModeCombobox.currentTextChanged.connect(self.trackerWidget.setDisplayMode)
        self.configWindow.settingsConfirmed.connect(self.saveSettings)
        self.configWindow.monitorCombobox.currentIndexChanged.connect(self.trackerWidget.setMonitor)

        self.trackerWidget.setWeeksCounterVisible(self.configWindow.weeksCounterCheckbox.isChecked())
        self.trackerWidget.setHoursCounterVisible(self.configWindow.hoursCounterCheckbox.isChecked())
        self.trackerWidget.setWidgetPosition(self.configWindow.positionCombobox.currentText())
        self.trackerWidget.setBackgroundOpacity(self.configWindow.opacitySlider.value())
        self.trackerWidget.setTargetDate(self.configWindow.targetDateInput.dateTime())
        self.trackerWidget.setDisplayMode(self.configWindow.displayModeCombobox.currentText())
        self.trackerWidget.setMonitor(self.configWindow.monitorCombobox.currentIndex())

        self.trackerWidget.setTrackerTitle(self.configWindow.trackerTitleInput.text())
        self.trackerWidget.setTargetDate(self.configWindow.targetDateInput.dateTime())
        self.trackerWidget.setDisplayMode(self.configWindow.displayModeCombobox.currentText())
        self.trackerWidget.setWeeksCounterVisible(self.configWindow.weeksCounterCheckbox.isChecked())
        self.trackerWidget.setHoursCounterVisible(self.configWindow.hoursCounterCheckbox.isChecked())
        self.trackerWidget.setWidgetPosition(self.configWindow.positionCombobox.currentText())
        self.trackerWidget.setBackgroundOpacity(self.configWindow.opacitySlider.value())

        self.trayIcon = None
        self.trayMenu = None

        self.openConfigAction = None
        self.exitAction = None

        self.configWindow.windowHidden.connect(self.showTrackerWidget)

    def start(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            raise RuntimeError("The Windows' system tray is not available.")

        self.createTrayIcon()
        self.trackerWidget.show()
        self.trackerWidget.updateWidgetSize()

    def createTrayIcon(self):
        icon = QIcon(getResourcePath("src/icon.png"))

        self.trayIcon = QSystemTrayIcon(icon, self.app)
        self.trayIcon.setToolTip("Date Tracker")

        self.trayMenu = QMenu()

        openConfigAction = QAction("Configure", self.trayMenu)
        openConfigAction.triggered.connect(self.showConfigWindow)

        exitAction = QAction("Quit app", self.trayMenu)
        exitAction.triggered.connect(self.exitApplication)

        self.trayMenu.addAction(openConfigAction)
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(exitAction)

        self.trayIcon.setContextMenu(self.trayMenu)
        self.trayIcon.activated.connect(self.handleTrayActivation)

        self.trayIcon.show()

    def showConfigWindow(self):
        self.configWindow.show()
        self.configWindow.raise_()
        self.configWindow.activateWindow()

    def showTrackerWidget(self):
        self.configWindow.hide()

        self.trackerWidget.show()
        self.trackerWidget.raise_()

    def handleTrayActivation(self, activationReason):
        if activationReason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showConfigWindow()
        elif activationReason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showConfigWindow()

    def saveSettings(self):
        self.settings.setValue("trackerTitle", self.configWindow.trackerTitleInput.text())
        self.settings.setValue("targetDate", self.configWindow.targetDateInput.dateTime())
        self.settings.setValue("displayMode", self.configWindow.displayModeCombobox.currentText())
        self.settings.setValue("showWeeksCounter", self.configWindow.weeksCounterCheckbox.isChecked())
        self.settings.setValue("showHoursCounter", self.configWindow.hoursCounterCheckbox.isChecked())
        self.settings.setValue("widgetPosition", self.configWindow.positionCombobox.currentText())
        self.settings.setValue("backgroundOpacity", self.configWindow.opacitySlider.value())
        self.settings.setValue("monitorIndex", self.configWindow.monitorCombobox.currentIndex())
        self.settings.sync()

    def loadSettings(self):
        trackerTitle = self.settings.value("trackerTitle", "Untitled Counter", type=str)
        displayMode = self.settings.value("displayMode", "Single-line", type=str)
        showWeeksCounter = self.settings.value("showWeeksCounter", True, type=bool)
        showHoursCounter = self.settings.value("showHoursCounter", True, type=bool)
        widgetPosition = self.settings.value("widgetPosition", "Top Left", type=str)
        backgroundOpacity = self.settings.value("backgroundOpacity", 80, type=int)
        targetDate = self.settings.value("targetDate", QDateTime.currentDateTime())
        monitorIndex = self.settings.value("monitorIndex", 0, type=int)

        self.configWindow.trackerTitleInput.setText(trackerTitle)
        self.configWindow.targetDateInput.setDateTime(targetDate)
        self.configWindow.displayModeCombobox.setCurrentText(displayMode)
        self.configWindow.weeksCounterCheckbox.setChecked(showWeeksCounter)
        self.configWindow.hoursCounterCheckbox.setChecked(showHoursCounter)
        self.configWindow.positionCombobox.setCurrentText(widgetPosition)
        self.configWindow.opacitySlider.setValue(backgroundOpacity)
        self.configWindow.opacityValueLabel.setText(f"{backgroundOpacity}%")

        if monitorIndex < self.configWindow.monitorCombobox.count():
            self.configWindow.monitorCombobox.setCurrentIndex(monitorIndex)

    def exitApplication(self):
        self.trayIcon.hide()
        self.app.quit()