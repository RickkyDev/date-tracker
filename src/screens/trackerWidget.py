from PySide6.QtCore import QDateTime, Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

class TrackerWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.configureWindow()
        self.createInterface()

        self.currentPosition = "Top Left"

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

        self.setFixedWidth(340)
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

        self.mainCounterLabel = QLabel("2 months, 12 days, 14 hours, 54 minutes e 11 seconds")

        self.mainCounterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainCounterLabel.setWordWrap(True)

        self.mainCounterLabel.setStyleSheet(
            """
            QLabel {
                color: white;
                font-size: 22px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 70);
                border-radius: 8px;
                padding: 10px;
            }
            """
        )

        self.weeksCounterLabel = QLabel("2 weeks")
        self.hoursCounterLabel = QLabel("360 hours")

        secondaryLabels = [self.weeksCounterLabel, self.hoursCounterLabel]

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

            self.mainLayout.addWidget(label)

        self.mainLayout.insertWidget(0, self.titleLabel)
        self.mainLayout.insertWidget(1, self.mainCounterLabel)

        self.adjustSize()

        self.titleLabel.setFixedHeight(34)
        self.mainCounterLabel.setFixedHeight(80)
        self.weeksCounterLabel.setFixedHeight(30)
        self.hoursCounterLabel.setFixedHeight(30)

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

    def setWidgetPosition(self, position):
        self.currentPosition = position
        screen = QGuiApplication.primaryScreen()

        if screen is None: return

        availableGeometry = screen.availableGeometry()

        margin = 20

        left = availableGeometry.left() + margin
        top = availableGeometry.top() + margin

        right = (availableGeometry.right() - self.width() - margin + 1)

        bottom = (availableGeometry.bottom() - self.height() - margin + 1)

        positions = {"Top Left": (left, top), "Top Right": (right, top), "Bottom Left": (left, bottom), "Bottom Right": (right, bottom)}

        xPosition, yPosition = positions.get(position, (left, top))

        self.move(xPosition, yPosition)

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