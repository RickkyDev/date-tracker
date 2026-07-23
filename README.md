# Date Tracker

A lightweight and customizable countdown widget for Windows 11, built with Python and PySide6.

Date Tracker stays quietly in the system tray and displays a clean desktop countdown without occupying the taskbar. Its appearance and behavior can be configured through a dedicated settings window.

## Features

- Real-time countdown to a selected date and time
- Windows system tray integration
- Minimal desktop widget that stays below other applications
- Custom tracker title
- Four screen positions:
  - Top Left
  - Top Right
  - Bottom Left
  - Bottom Right
- Automatically respects the Windows taskbar area
- Adjustable background opacity
- Optional secondary counters:
  - Total weeks
  - Total hours
- Three main counter display modes:
  - Single-line
  - Multi-line
  - Compact single-line
- Automatic widget resizing when counters are shown or hidden
- Persistent settings saved with `QSettings`
- Clean dark-mode icon inspired by Windows 11 Fluent Design
- No taskbar entry while running as a widget

## Preview

The widget can display the countdown in different formats.

### Single-line

```text
15 days, 9 hours, 15 minutes and 50 seconds
```

### Multi-line

```text
15 days
9 hours
15 minutes
50 seconds
```

### Compact single-line

```text
15 d  9 h  15 m  50 s
```

Secondary counters can also be enabled:

```text
2 weeks
369 hours
```

## Requirements

- Windows 11
- Python 3.12 or newer
- PySide6

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/date-tracker.git
cd date-tracker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bat
venv\Scripts\activate
```

Install the project:

```bash
pip install -e .
```

## Running the App

```bash
python main.py
```

While Date Tracker is running:

- The countdown widget remains visible on the desktop.
- The application icon remains available in the system tray.
- Clicking the tray icon opens the configuration window.
- Closing the configuration window returns to the countdown widget.
- Use the tray context menu to quit the application.

## Building the Executable

The project includes a `compile.bat` file for building a standalone Windows executable with PyInstaller.

Run:

```bat
compile.bat
```

The executable will be generated inside:

```text
dist/
```

Example PyInstaller command:

```bat
pyinstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name "Date Tracker" ^
    --icon "src\icon.ico" ^
    --add-data "src\icon.png;src" ^
    main.py
```

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
- Widget position
- Background opacity

Settings are stored through Qt's `QSettings`, so they remain available after the application is closed or updated.

## Technologies

- [Python](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [Qt](https://www.qt.io/)
- [PyInstaller](https://pyinstaller.org/)

## Roadmap

Possible future improvements:

- Multiple independent countdowns
- Custom fonts and colors
- Additional themes
- Custom widget dimensions
- Drag-and-drop positioning
- Startup with Windows
- Import and export of configurations
- Notifications when a countdown reaches zero
- Installer and automatic updates

## License

This project is currently provided without a defined license.

Before accepting external contributions or allowing redistribution, add a license such as MIT, Apache 2.0, or GPLv3.

---

Built as a learning project focused on Python, PySide6, desktop interfaces, application state, and Windows integration.
