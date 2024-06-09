import sqlite3
from sudoku_bank import sudoku_puzzles, replace_dots_with_hyphens
from werkzeug.security import generate_password_hash

database = r"./database.db"

def create_connection():
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(create_table_sql):
    """Create a table from the create_table_sql statement"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.close()
    except sqlite3.Error as e:
        print(e)

sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_name TEXT NOT NULL,
                                password_hash TEXT NOT NULL,
                                is_admin INTEGER DEFAULT 0
                            );"""

sql_create_puzzles_table = """CREATE TABLE IF NOT EXISTS puzzles (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    unsolved_board TEXT NOT NULL,
                                    solved_board TEXT NOT NULL
                                );"""

sql_create_fastest_times_table = """CREATE TABLE IF NOT EXISTS fastestTimes (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                        puzzle_id INTEGER NOT NULL,
                                        fastest_time REAL NOT NULL,
                                        mistakes INTEGER NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users(id),
                                        FOREIGN KEY (puzzle_id) REFERENCES puzzles(id)
                                    );"""

#### INSERT ####

def insert_user(user):
    """Insert a new user into the users table"""
    sql = '''INSERT INTO users(user_name, password_hash, is_admin) VALUES(?, ?,?)'''
    try:
        username = user[0]
        password = user[1]
        if len(user) == 3:
            is_admin = user[2]
        else:
            is_admin = 0
        password_hash = generate_password_hash(password)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (username, password_hash, is_admin,))
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except sqlite3.Error as e:
        return e
    
def insert_puzzle(puzzle):
    """Insert a new puzzle into the puzzles table"""
    sql = '''INSERT INTO puzzles(unsolved_board, solved_board) VALUES(?, ?)'''
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql, puzzle)
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except sqlite3.Error as e:
        return e

def insert_fastest_time(fastest_time):
    """Insert a new fastest time into the fastestTimes table"""
    sql = '''INSERT INTO fastestTimes(user_id, puzzle_id, fastest_time, mistakes) VALUES(?, ?, ?, ?)'''
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql, fastest_time)
        conn.commit()
        conn.close()
        return cursor.lastrowid
    except sqlite3.Error as e:
        return e


#### DELETE ####

def delete_user_by_id(id):
    sql = f"DELETE FROM users WHERE id = {id}"
    try:
        if select_user_by_id(id):        
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return f"user_id: {id} has been succsessfully deleted"
        else:
            return f"Could not find user_id: {id}"
    except sqlite3.Error as e:
        return e
    
def delete_fastest_time(fastestTimes_id):
    """Delete a fastest time entry by id"""
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fastestTimes WHERE id = ?", (fastestTimes_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)


#### INIT ####

def init_users():
    init = [('Albert', 'password'),
            ('Bando', '12345678'),
            ('Camilla', 'hiddenpass'),
            ('Admin007', 'Admin007', 1),
            ('Daniel', 'gangmannen1')]
    for element in init:
        insert_user(element)

def init_puzzles():
    for sudoku in sudoku_puzzles:
        unsolved = replace_dots_with_hyphens(sudoku['unsolved'])
        solved = sudoku['solved']
        insert_puzzle((unsolved, solved))

def init_fastest_times():
    init = [(1, 1, 372.393, 2),
            (1, 2, 515.556, 0),
            (2, 2, 495.928, 0),
            (3, 1, 205.125, 5),
            (2, 7, 302.821, 1),
            (4, 8, 242.149, 6),
            (3, 6, 522.871, 0),
            (5, 4, 721.921, 0)]
    # missing (102, 1) & (103, 2)
    for element in init:
        insert_fastest_time(element)
        

#### SELECT ####

def select_user_by_id(user_id):
    """Query user by id"""
    sql = f"SELECT * FROM users WHERE id = {user_id}"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    return row

def select_user_by_username(user_name):
    """Query user by name"""
    sql = "SELECT * FROM users WHERE user_name = ?"
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (user_name,))
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.Error as e:
        return e
    
def select_puzzle_by_id(puzzle_id):
    """Query puzzle by ID"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM puzzles WHERE id = ?", (puzzle_id,))
    row = cursor.fetchone()
    conn.close()
    return row


#### GET for app.py ####
def get_username_by_id(user_id):
    """Query username by id"""
    sql = f"SELECT user_name FROM users WHERE id = {user_id}"
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    # returns a string instead of a tuple
    return row[0]

def get_random_puzzle():
    """Fetch a random puzzle from the puzzles table"""
    sql = "SELECT * FROM puzzles ORDER BY RANDOM() LIMIT 1"
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.Error as e:
        return e
    
def get_users():
    """Fetch all id and usernames from users table"""
    sql = "SELECT id, user_name FROM users"
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        return e

def get_fastestTimes():
    """Fetch fastest_times from the fastestTimes table"""
    sql = "SELECT * FROM fastestTimes ORDER BY mistakes ASC, fastest_time ASC"
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchall()
        conn.close()
        return row
    except sqlite3.Error as e:
        return e

#### SETUP ####

def setup():
    create_table(sql_create_users_table)
    create_table(sql_create_fastest_times_table)
    create_table(sql_create_puzzles_table)

    init_users()
    init_fastest_times()
    init_puzzles()
    
    
#### MAIN ####

def main():

    conn = create_connection()
    
    if conn is not None:
        setup()
        #print(delete_user_by_id(102))
        
        # Close the connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")
    

if __name__ == '__main__':
    main()