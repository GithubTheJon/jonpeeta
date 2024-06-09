from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash
import setup_db


app = Flask(__name__)
app.secret_key = '1101'


@app.route('/')
def home():
    username = session.get('username')
    return render_template('sudoku.html', username=username)

@app.route('/settings')
def settings():
    username = session.get('username')
    return render_template('settings.html', username=username)

@app.route('/highscores')
def highscores():
    entries = setup_db.get_fastestTimes()
    users = setup_db.get_users()
    username = session.get('username')
    return render_template('highscores.html', entries=entries, users=users, username=username)

@app.route('/delete_highscore', methods=['POST'])
def delete_highscore():
    if request.method == 'POST':
        fastestTimes_id = request.json.get('fastestTimes_id')
        if fastestTimes_id:
            setup_db.delete_fastest_time(fastestTimes_id)
            return jsonify({'status': 'success', 'message': 'High score deleted successfully.'})
        else:
            return jsonify({'status': 'error', 'message': 'Invalid ID provided.'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # if username is None or password is None:
        #     flash('Username and Password are Required', 'info')
        #     return redirect('/')
        # Check if the user exists
        user = setup_db.select_user_by_username(username)
        
        if user and check_password_hash(user[2], password):
            session['username'] = username
            session['user_id'] = user[0]
            session['is_admin'] = user[3]
            flash('Login successful!', 'info')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'info')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if password is at least 8 characters
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('signup'))
        
        # Check if username is already taken
        if setup_db.select_user_by_username(username):
            flash('Username already taken')
            return redirect(url_for('signup'))

        # Insert the new user where the password is hashed
        setup_db.insert_user((username, password))
        
        flash('User registered successfully')
        return redirect(url_for('login'))
    
    return render_template('signup.html')


# https://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/
@app.route('/get_random_puzzle', methods=['GET'])
def get_random_puzzle():
    puzzle = setup_db.get_random_puzzle()
    return jsonify({
        'puzzle_id': puzzle[0],
        'unsolved_board': puzzle[1],
        'solved_board': puzzle[2]
    })

    
@app.route('/save_fastest_time', methods=['POST'])
def save_fastest_time():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.get_json()
    user_id = session['user_id']
    puzzle_id = data['puzzle_id']
    elapsed = data['elapsed']
    mistakes = data['mistakes']

    fastest_time_data = (user_id, puzzle_id, elapsed, mistakes)
    result = setup_db.insert_fastest_time(fastest_time_data)

    if isinstance(result, setup_db.sqlite3.Error):
        return jsonify({'error': str(result)}), 500

    return jsonify({'message': 'Fastest time saved successfully'})
    

if __name__ == '__main__':
    app.run(debug=True, port=7071)