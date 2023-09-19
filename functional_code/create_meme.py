from CONSTANTS import CURSOR


def search_results(search):
    result = []
    execution1 = f"select title from memes where title like \'%{search}%\'"
    name_search = CURSOR.execute(execution1).fetchall()
    for name in name_search:
        result.append(name[0])
    execution2 = f"select id from tags where tag like \'%{search}%\'"
    try:
        tag_id = CURSOR.execute(execution2).fetchall()[0]
        tag_search_id = CURSOR.execute("select meme from tags_connection "
                                       "where tag = ?",
                                       (*tag_id,)).fetchall()
        ids = ', '.join([str(i[0]) for i in tag_search_id])
        execution3 = f"select title from memes where id in ({ids})"
        tag_search = CURSOR.execute(execution3).fetchall()

        for tag_name in range(len(tag_search)):
            current = tag_search[tag_name][0]
            if current not in result:
                result.append(current)
        return result
    except IndexError:
        return []


def change_results(tag):
    result = []
    tag_id = CURSOR.execute("select id from tags where tag = ?",
                            (tag,)).fetchall()[0]
    tag_search_id = CURSOR.execute("select meme from tags_connection "
                                   "where tag = ?",
                                   (*tag_id,)).fetchall()
    ids = ', '.join([str(i[0]) for i in tag_search_id])
    execution3 = f"select title from memes where id in ({ids})"
    tag_search = CURSOR.execute(execution3).fetchall()
    for title in tag_search:
        result.append(title[0])
    return result
