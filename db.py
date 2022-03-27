import csv
import sqlite3

conn = sqlite3.connect('statistic.db')
cursor = conn.cursor()

def make_db():
    global cursor
    text = '''CREATE TABLE users (
        user_id INTEGER,
        "username" TEXT,
        results TEXT,
        US_result TEXT,
        S_result TEXT
    );'''
    cursor.execute(text)
    make_users()
    text = '''CREATE TABLE results (
        teacher TEXT,
        number INTEGER
    );'''
    conn.execute(text)
    make_results()
    conn.commit()

def make_users():
    global cursor
    with open('users.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        data.pop(0)
        for i in data:
            text = f'''INSERT INTO users (user_id, username, results, US_result, S_result)
                    VALUES ({i[0]}, {i[1]}, {i[2]}, {i[3]}, {i[4]});'''
            cursor.execute(text)


def make_results():
    global cursor
    with open('results.csv') as file:
        data = [r for r in csv.reader(file, delimiter=" ")]
        data.pop(0)
        for i in data:
            text = f'''INSERT INTO results (teacher, number)
                    VALUES ({i[0]}, {i[1]});'''
            cursor.execute(text)


def update_results(fio):
    global cursor
    cursor.execute("SELECT * FROM results WHERE teacher=?;", (fio,))
    data = cursor.fetchall()
    if len(data) == 0:
        text = f'''INSERT INTO results (teacher, number)
                            VALUES ({fio}, 0);'''
        cursor.execute(text)
    else:
        cursor.execute("UPDATE results SET number = ? WHERE teacher=?;", (int(data[0][1])+1, fio,))
    conn.commit()


def update_users(user_id, username, result):
    global cursor
    cursor.execute("SELECT * FROM users WHERE user_id=", (user_id,))
    data = cursor.fetchall()
    if len(data) == 0:
        if result != -1:
            cursor.execute(f'''INSERT INTO users (user_id, username, results, US_result, S_result) VALUES 
                            ({user_id}, {username}, 1, 0, 1);''')
        else:
            cursor.execute(f'''INSERT INTO users (user_id, username, results, US_result, S_result) VALUES 
                            ({user_id}, {username}, 1, 1, 0);''')
    else:
        if result != -1:
            cursor.execute("UPDATE users SET results = ?, S_result = ? WHERE user_id=?;", (int(data[0][2])+1, int(data[0][4])+1, data[0][0]))
        else:
            cursor.execute("UPDATE users SET results = ?, US_result = ? WHERE user_id=?;", (int(data[0][2])+1, int(data[0][3])+1, data[0][0]))
    conn.commit()


def top():
    global cursor
    cursor.execute("SELECT * FROM results ORDER BY number DESC")
    data = cursor.fetchall()
    return data[0:5]

if __name__ == '__main__':
    make_db()

