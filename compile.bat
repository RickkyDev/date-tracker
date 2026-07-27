@echo off

del "Date Tracker.spec"

call venv\Scripts\activate.bat

pip install pyinstaller

pyinstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name "Date Tracker" ^
    --icon "src\icon.ico" ^
    --add-data "src:src" ^
    main.py

pause