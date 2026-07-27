# Date Tracker

A lightweight and customizable countdown widget for Windows 11, built with Python and PySide6.

Date Tracker stays quietly in the system tray and displays a clean desktop countdown without occupying the taskbar. Its appearance and behavior can be configured through a dedicated settings window.

## Features

- Real-time countdown to a selected date and time
- Windows system tray integration
- Minimal desktop widget that stays below other applications
- Custom tracker title
- Adjustable background opacity
- Three main counter display modes:
  - Single-line
  - Multi-line
  - Compact single-line
- Optional secondary counters:
  - Total weeks
  - Total hours
  - List of dates until the main date
- Persistent settings saved with `QSettings` and Json (for the list of dates)
- Clean dark-mode icon inspired by Windows 11's design

## Requirements to run directly from your IDE:
- Windows 11
- Python 3.12 or newer
- PySide6
#### No need to install anything to run the .exe (compiled) app

---

## While Date Tracker is running:

- The countdown widget remains visible on the desktop.
- The application icon remains available in the system tray, no icon stays on the taskbar.
- Clicking the tray icon opens the configuration window.
- Use the tray context menu to quit the application.


## Project Structure

```text
date-tracker/
├── src/
│   ├── screens/
│   │   ├── configWindow.py
│   │   └── trackerWidget.py
│   ├── appController.py
│   ├── icon.ico
│   ├── icon.png
│   └── rsc.py
├── main.py
├── pyproject.toml
├── compile.bat
└── README.md
```

## Configuration Persistence

Settings are saved when the user clicks **Done** in the configuration window.

The application remembers:

- Tracker title
- Target date and time
- Main counter display mode
- Enabled secondary counters
- Secondary dates being tracked
- Widget position & monitor
- Background opacity

Settings are stored through Qt's `QSettings` and Json, so they remain available after the application is closed or updated.

## Technologies

- [Python](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [Qt](https://www.qt.io/)
- [PyInstaller](https://pyinstaller.org/)
- [JSON](https://www.json.org/json-en.html/)

## License

This project is currently provided without a defined license.
---

Built as a learning project & portfolio building, focused on the use of Python, PySide6, desktop interfaces, application state, and Windows integration.
