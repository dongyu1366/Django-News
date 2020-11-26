import sqlite3


def create_news_list_table():
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS news_list")
    cur.execute("""CREATE TABLE IF NOT EXISTS news_list(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                token VARCHAR(50) NOT NULL UNIQUE,
                category VARCHAR(50) NOT NULL,
                title VARCHAR(300) NOT NULL,
                abstract VARCHAR(1000) NOT NULL,
                date VARCHAR(50) NOT NULL,
                image VARCHAR(500),
                url VARCHAR(500) NOT NULL,
                dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
    cur.close()
    print('Table created successfully')


def create_news_table():
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS news")
    cur.execute("""CREATE TABLE IF NOT EXISTS news(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                token VARCHAR(50) NOT NULL UNIQUE,
                category VARCHAR(50) NOT NULL,
                title VARCHAR(300) NOT NULL,
                author VARCHAR(200),
                date VARCHAR(50) NOT NULL,
                image VARCHAR(500),
                content VARCHAR(15000) NOT NULL,
                dt_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")
    cur.close()
    print('Table created successfully')


if __name__ == '__main__':
    # Connect to database
    conn = sqlite3.connect('../news.sqlite3')

    create_news_list_table()
    create_news_table()

    conn.close()
