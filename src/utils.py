import sys
from pathlib import Path


def getResourcePath(relativePath: str) -> str:
    if getattr(sys, "frozen", False):
        basePath = Path(sys._MEIPASS)
    else:
        basePath = Path(__file__).resolve().parent.parent

    return str(basePath / relativePath)