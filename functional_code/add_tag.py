from CONSTANTS import CURSOR, DATA
import sqlite3


def addition(tag_name, memes):
    try:
        if tag_name == '':
            raise ValueError
        CURSOR.execute("insert into tags (tag) values (?)",
                       (tag_name,))
        tag_id = CURSOR.execute("select id from tags where tag = ?",
                                (tag_name,
                                 )).fetchall()[0]
        ids_search = ', '.join([('\'' + i.text() + '\'') for i in
                                memes])
        execution = f"select id from memes where title in ({ids_search})"
        memes_ids = CURSOR.execute(execution).fetchall()
        for meme in memes_ids:
            CURSOR.execute(
                "insert into tags_connection (meme, tag) values ("
                "?, ?)", (meme[0], tag_id[0]))
        DATA.commit()
        return 0
    except sqlite3.IntegrityError:
        return -1
    except ValueError:
        return -1
