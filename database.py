import sqlite3

def init_chatindex_db():
    con = sqlite3.connect('instance/chatdata.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS chat_index")
    cur.execute("CREATE TABLE chat_index (\
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        subject TEXT NOT NULL)")
    cur.close()
    con.close()
    print('データベースを初期化しました')

def init_chatconver_db():
    con = sqlite3.connect('instance/chatdata.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS chat_conver")
    cur.execute("CREATE TABLE chat_conver (\
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        subject TEXT NOT NULL,\
        poster TEXT NOT NULL,\
        content TEXT NOT NULL,\
        img TEXT NOT NULL)")
    cur.close()
    con.close()
    print('データベースを初期化しました')

if __name__ == '__main__':
    init_chatindex_db()
    init_chatconver_db()
