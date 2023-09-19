from PyQt5.QtGui import QPixmap
from CONSTANTS import CURSOR, MEME_FOLDER, DATA
import sqlite3


def add(file_name, name, tags):
    try:
        if file_name == '':
            raise ValueError
        meme = QPixmap(file_name).copy()
        new_name = name + '.png'
        CURSOR.execute("insert into memes (title, file_name) "
                       "values (?, ?)",
                       (name, new_name))
        meme.save(str(MEME_FOLDER / new_name))
        meme_id = CURSOR.execute("select id from memes where title = ?",
                                 (name,)).fetchall()[0]
        ids_search = ', '.join([('\'' + i.text() + '\'') for i in
                                tags])
        execution = f"select id from memes where title in ({ids_search})"
        tags_ids = CURSOR.execute(execution).fetchall()
        for tag in tags_ids:
            CURSOR.execute("insert into tags_connection (meme, tag) "
                           "values (?, ?)", (meme_id[0], tag[0]))
        DATA.commit()
        return 0
    except sqlite3.IntegrityError:
        return -1
    except ValueError:
        return -1
