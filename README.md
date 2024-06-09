# Sudoku Standard

## Table of Contents
- [Description](#description)
- [How to Run](#how-to-run)
- [Instructions for testing](#instructions-for-testing)
- [Installation](#installation)

## Description
The Sudoku Standard is an application where puzzles are solved and scores are saved. <br>

When completing a puzzle the metrics such as time spent and amount of mistakes are recorded and saved to the database. Anyone can view the scoretable <code>highscores</code> but only logged in users are able to submit their score when completing a puzzle. <br>
Anyone are able to customize predetermined elements such as <code>text-size</code>, <code>text-font</code> and <code>background-color</code> of the frontend to their liking.

The project is Flask based with Sqlite3 as database. The database consists of three tables: <code>users</code>, <code>puzzles</code> and <code>fastestTimes</code>. The latter table shares some elements in the form of <code>FOREIGN KEYS</code>.

All puzzles are stored inside <code>sudoku_bank.py</code> and extracted from when initializing the puzzle table for the database.

## Instructions for testing
Overview of existing <code>users</code> where the last element [2] determines admin rights. If None, set to 0.<br> <code> init = [<br>('Albert', 'password'),<br>('Bando', '12345678'),<br>('Camilla', 'hiddenpass')<br>('Admin007', 'Admin007', 1),<br>('Daniel', 'gangmannen1')<br>] </code> <br> The <code>Admin007</code> has administration rights which covers the deletion of any score in the <code>highscores</code> table when logged in and viewing the <code>'/highscores'</code>. The option for deleting those entries will not be displayed if the users session is not an admin.

## List of all functionalities
1. User Authentication: Users can sign up, log in, and log out. Passwords are securely hashed using Werkzeug.
2. Gameloop: Users can play randomly given Sudoku puzzles.
3. High Scores: completion times and mistakes are recorded and displayed on the high-scores page.
4. Admin Features: Admin user(s) can delete high-score entries.


## Packages used
1. Python 3.9.18 
2. Flask 3.0.2 
3. Werkzeug 3.0.1
4. sqlite3 3.31.1

## How to run
1. Set up the database:
   ```sh
   python3 setup_db.py
2. Run the application:
   ```sh
   python3 app.py
The application will run on port 7071