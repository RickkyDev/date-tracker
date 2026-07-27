from PySide6.QtCore import QDateTime, Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget

class TrackerWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.configureWindow()
        self.createInterface()

        self.events = []
        self.visibleEventCount = 0

        self.currentPosition = "Top Left"
        self.currentMonitorIndex = 0

        self.targetDate = QDateTime.currentDateTime()
        self.displayMode = "Single-line"

        self.counterTimer = QTimer(self)
        self.counterTimer.setInterval(1000)
        self.counterTimer.timeout.connect(self.updateCounter)
        self.counterTimer.start()

    def configureWindow(self):
        self.setWindowTitle("Date Tracker")

        windowFlags = (Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnBottomHint | Qt.WindowType.Tool)

        self.setWindowFlags(windowFlags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setFixedWidth(320)
        self.move(10, 10)

    def createInterface(self):
        self.outerLayout = QVBoxLayout(self)
        self.outerLayout.setContentsMargins(0, 0, 0, 0)

        self.backgroundFrame = QFrame()
        self.backgroundFrame.setObjectName("backgroundFrame")

        self.mainLayout = QVBoxLayout(self.backgroundFrame)
        self.mainLayout.setContentsMargins(12, 12, 12, 12)
        self.mainLayout.setSpacing(6)

        self.outerLayout.addWidget(self.backgroundFrame)

        self.titleLabel = QLabel("Viagem de Aniversário")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 90);
                border-radius: 8px;
                padding: 6px;
            }
            """
        )

        self.mainCounterFrame = QFrame()
        self.mainCounterFrame.setObjectName("mainCounterFrame")
        self.mainCounterFrame.setStyleSheet(
            """
            QFrame#mainCounterFrame {
                background-color: rgba(0, 0, 0, 70);
                border-radius: 8px;
            }
            """
        )

        self.mainCounterLayout = QVBoxLayout(self.mainCounterFrame)
        self.mainCounterLayout.setContentsMargins(6, 4, 6, 4)
        self.mainCounterLayout.setSpacing(0)

        self.mainCounterLabel = QLabel("2 months, 12 days, 14 hours, 54 minutes and 11 seconds")
        self.mainCounterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainCounterLabel.setWordWrap(True)
        self.mainCounterLabel.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                background-color: transparent;
                padding: 4px;
            }
            """
        )

        self.secondaryCountersWidget = QWidget()
        self.secondaryCountersLayout = QHBoxLayout(self.secondaryCountersWidget)
        self.secondaryCountersLayout.setContentsMargins(0, 0, 0, 0)
        self.secondaryCountersLayout.setSpacing(10)

        self.hoursCounterLabel = QLabel("360 hours")
        self.weeksCounterLabel = QLabel("2 weeks")

        secondaryLabels = [self.hoursCounterLabel, self.weeksCounterLabel]

        for label in secondaryLabels:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 15px;
                    background-color: transparent;
                    padding: 4px;
                }
                """
            )

        self.secondaryCountersLayout.addWidget(self.hoursCounterLabel, 1)
        self.secondaryCountersLayout.addWidget(self.weeksCounterLabel, 1)

        self.mainCounterLayout.addWidget(self.mainCounterLabel)
        self.mainCounterLayout.addWidget(self.secondaryCountersWidget)

        self.eventsFrame = QFrame()
        self.eventsFrame.setObjectName("eventsFrame")
        self.eventsFrame.setStyleSheet(
            """
            QFrame#eventsFrame {
                background-color: rgba(0, 0, 0, 70);
                border-radius: 8px;
            }
            """
        )

        self.eventsLayout = QVBoxLayout(self.eventsFrame)
        self.eventsLayout.setContentsMargins(10, 8, 10, 8)
        self.eventsLayout.setSpacing(4)

        self.eventsTitleLabel = QLabel("Events until then:")
        self.eventsTitleLabel.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
            }
            """
        )

        self.eventsLayout.addWidget(self.eventsTitleLabel)

        self.eventRows = []

        for _ in range(5):
            eventRowLayout = QHBoxLayout()
            eventRowLayout.setContentsMargins(0, 0, 0, 0)

            eventNameLabel = QLabel()
            eventTimeLabel = QLabel()

            eventNameLabel.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 12px;
                }
                """
            )

            eventTimeLabel.setStyleSheet(
                """
                QLabel {
                    color: white;
                    font-size: 12px;
                }
                """
            )

            eventNameLabel.setMinimumWidth(170)
            eventTimeLabel.setAlignment(Qt.AlignmentFlag.AlignRight)

            eventRowLayout.addWidget(eventNameLabel)
            eventRowLayout.addStretch()
            eventRowLayout.addWidget(eventTimeLabel)

            self.eventsLayout.addLayout(eventRowLayout)

            self.eventRows.append({
                "nameLabel": eventNameLabel,
                "timeLabel": eventTimeLabel,
            })

        self.eventsFrame.setVisible(False)

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.mainCounterFrame)
        self.mainLayout.addWidget(self.eventsFrame)

        self.titleLabel.setFixedHeight(36)
        self.mainCounterLabel.setFixedHeight(30)
        self.hoursCounterLabel.setFixedHeight(35)
        self.weeksCounterLabel.setFixedHeight(35)

        self.adjustSize()
        self.setFixedHeight(self.sizeHint().height())

    def setTargetDate(self, targetDate):
        self.targetDate = targetDate
        self.updateCounter()


    def setDisplayMode(self, displayMode):
        self.displayMode = displayMode

        if displayMode == "Multi-line":
            self.mainCounterLabel.setFixedHeight(150)
        else:
            self.mainCounterLabel.setFixedHeight(80)

        self.updateCounter()
        self.updateWidgetSize()


    def updateCounter(self):
        currentDate = QDateTime.currentDateTime()
        remainingTotalSeconds = currentDate.secsTo(self.targetDate)

        if remainingTotalSeconds < 0:
            remainingTotalSeconds = 0

        remainingSeconds = remainingTotalSeconds

        days = remainingSeconds // 86400
        remainingSeconds %= 86400

        hours = remainingSeconds // 3600
        remainingSeconds %= 3600

        minutes = remainingSeconds // 60
        seconds = remainingSeconds % 60

        totalHours = remainingTotalSeconds // 3600
        totalWeeks = remainingTotalSeconds // 604800

        self.mainCounterLabel.setText(self.formatMainCounter(days, hours, minutes, seconds))
        self.weeksCounterLabel.setText(self.formatSimpleCounter(totalWeeks, "week"))
        self.hoursCounterLabel.setText(self.formatSimpleCounter(totalHours, "hour"))
        self.updateEventsDisplay()

    def formatMainCounter(self, days, hours, minutes, seconds):
        if self.displayMode == "Multi-line":
            return (
                f"{days} {self.getUnitName(days, 'day')}\n"
                f"{hours} {self.getUnitName(hours, 'hour')}\n"
                f"{minutes} {self.getUnitName(minutes, 'minute')}\n"
                f"{seconds} {self.getUnitName(seconds, 'second')}"
            )

        if self.displayMode == "Compact Single-line":
            return f"{days} d  {hours} h  {minutes} m  {seconds} s"

        return (
            f"{days} {self.getUnitName(days, 'day')}, "
            f"{hours} {self.getUnitName(hours, 'hour')}, "
            f"{minutes} {self.getUnitName(minutes, 'minute')} and "
            f"{seconds} {self.getUnitName(seconds, 'second')}"
        )
    
    def formatSimpleCounter(self, value, unit):
        return f"{value} {self.getUnitName(value, unit)}"

    def getUnitName(self, value, unit):
        if value == 1:
            return unit

        return f"{unit}s"

    def setEvents(self, events):
        self.events = events
        self.updateEventsDisplay()

    def setEventsVisible(self, visible):
        self.eventsFrame.setVisible(visible)
        self.updateEventsDisplay()
        self.updateWidgetSize()

    def updateEventsDisplay(self):
        currentDate = QDateTime.currentDateTime()

        self.events = [event for event in self.events if event["date"] > currentDate]
        upcomingEvents = sorted(self.events, key=lambda event: event["date"].toSecsSinceEpoch())[:5]

        for index, eventRow in enumerate(self.eventRows):
            if index < len(upcomingEvents):
                event = upcomingEvents[index]
                remainingSeconds = currentDate.secsTo(event["date"])

                days = remainingSeconds // 86400
                remainingSeconds %= 86400

                hours = remainingSeconds // 3600
                remainingSeconds %= 3600

                minutes = remainingSeconds // 60

                eventRow["nameLabel"].setText(event["name"])
                eventRow["timeLabel"].setText(f"{days}d {hours}h {minutes}m")

                eventRow["nameLabel"].show()
                eventRow["timeLabel"].show()
            else:
                eventRow["nameLabel"].clear()
                eventRow["timeLabel"].clear()

                eventRow["nameLabel"].hide()
                eventRow["timeLabel"].hide()

        newVisibleEventCount = len(upcomingEvents)

        if newVisibleEventCount != self.visibleEventCount:
            self.visibleEventCount = newVisibleEventCount
            self.updateWidgetSize()

    def setWidgetPosition(self, position):
        self.currentPosition = position
        screens = QGuiApplication.screens()

        if not screens: return

        if self.currentMonitorIndex >= len(screens):
            self.currentMonitorIndex = 0

        screen = screens[self.currentMonitorIndex]
        availableGeometry = screen.availableGeometry() # add connections

        margin = 20

        left = availableGeometry.left() + margin
        top = availableGeometry.top() + margin
        right = (availableGeometry.right() - self.width() - margin + 1)
        bottom = (availableGeometry.bottom() - self.height() - margin + 1)

        positions = {"Top Left": (left, top), "Top Right": (right, top), "Bottom Left": (left, bottom), "Bottom Right": (right, bottom)}

        xPosition, yPosition = positions.get(position, (left, top))

        self.move(xPosition, yPosition)

    def setMonitor(self, monitorIndex):
        self.currentMonitorIndex = monitorIndex
        self.setWidgetPosition(self.currentPosition)

    def setBackgroundOpacity(self, opacity):
        alpha = round((opacity / 100) * 255)

        self.backgroundFrame.setStyleSheet(
            f"""
            QFrame#backgroundFrame {{
                background-color: rgba(25, 25, 25, {alpha});
                border-radius: 14px;
            }}
            """
        )

    def setTrackerTitle(self, title):
        if title.strip():
            self.titleLabel.setText(title)
        else: self.titleLabel.setText("Untitled Counter")

    def setWeeksCounterVisible(self, visible):
        self.weeksCounterLabel.setVisible(visible)
        self.updateWidgetSize()

    def setHoursCounterVisible(self, visible):
        self.hoursCounterLabel.setVisible(visible)
        self.updateWidgetSize()

    def updateWidgetSize(self):
        QTimer.singleShot(0, self.applyWidgetSize)

    def applyWidgetSize(self):
        self.mainLayout.invalidate()
        self.mainLayout.activate()

        self.backgroundFrame.adjustSize()

        newHeight = self.backgroundFrame.sizeHint().height()

        self.setFixedHeight(newHeight)
        self.setWidgetPosition(self.currentPosition)