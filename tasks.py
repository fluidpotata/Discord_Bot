import sqlite3


def connectDB():
    cnx = sqlite3.connect("db/bot.db")
    return cnx


def data(ctx):
    connection = connectDB()
    cursor = connection.cursor()
    query3 = f"""SELECT * from tasks where user='{ctx}'"""
    cursor.execute(query3)
    y = cursor.fetchall()
    x = ""
    for i in y:
        x+=f"- {i[1]}"
        x+="\n"
    return x


def commit(author, data):
    connection = connectDB()
    cursor = connection.cursor()
    query4 = f"""INSERT INTO tasks VALUES('{author}','{data}')"""
    cursor.execute(query4)
    connection.commit()
    return True


def rem(author, data):
    connection = connectDB()
    cursor = connection.cursor()
    query4 = f"""DELETE FROM tasks WHERE user='{author}' and task='{data}'"""
    cursor.execute(query4)
    connection.commit()
    return True