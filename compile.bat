@echo off

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
    --distpath build\exec ^
    --workpath build ^
    main.py

del *.spec

pause