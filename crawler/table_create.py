import MySQLdb
import os
import sys


def create_news_list_table():
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS news_list")
    cur.execute("""CREATE TABLE IF NOT EXISTS news_list(
                id INT PRIMARY KEY AUTO_INCREMENT,
                source_token VARCHAR(50) NOT NULL UNIQUE,
                category VARCHAR(50) NOT NULL,
                category_tag VARCHAR(50) NOT NULL,
                title VARCHAR(300) NOT NULL,
                abstract VARCHAR(500) NOT NULL,
                date_str VARCHAR(50) NOT NULL,
                date DATETIME NOT NULL,
                image VARCHAR(500),
                url VARCHAR(500) NOT NULL,
                dt_created datetime DEFAULT CURRENT_TIMESTAMP,
                dt_modified datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )""")
    cur.close()
    print('Table created successfully')


def create_news_table():
    cur = conn.cursor()
    # cur.execute("DROP TABLE IF EXISTS news")
    cur.execute("""CREATE TABLE IF NOT EXISTS news(
                id INT PRIMARY KEY AUTO_INCREMENT,
                source_token VARCHAR(50) NOT NULL UNIQUE,
                category VARCHAR(50) NOT NULL,
                title VARCHAR(300) NOT NULL,
                author VARCHAR(200),
                date_str VARCHAR(50) NOT NULL,
                date DATETIME NOT NULL,
                image VARCHAR(500),
                content VARCHAR(15000) NOT NULL,
                dt_created datetime DEFAULT CURRENT_TIMESTAMP,
                dt_modified datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )""")
    cur.close()
    print('Table created successfully')


if __name__ == '__main__':
    # Check for environment variable
    if not os.getenv("PASSWORD"):
        raise RuntimeError("PASSWORD is not set: export PASSWORD='your password'")

    # Connect to database
    try:
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=os.getenv("PASSWORD"),
            db='news',
        )
    except MySQLdb.Error as e:
        print(e)
        sys.exit()

    create_news_list_table()
    create_news_table()

    conn.close()
