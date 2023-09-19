import sqlite3
from pathlib import Path


MEME_FOLDER = Path("memes")
UIC_FOLDER = Path("uic")
DATA = sqlite3.connect("project.db")
CURSOR = DATA.cursor()
RESULT_FOLDER = Path("your memes")