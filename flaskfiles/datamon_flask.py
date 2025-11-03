"""
Datamon - Flask Version

A math problem helper that helps students, teachers and parents
make math fun.

Haylee Kaheel Teresa Aryan Justin
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from AnswerChecker_flask import check_answer
import secrets

# Create Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Needed for sessions

# Configure session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    """Main menu page"""
    # Initialize player_points in session if it doesn't exist
    if 'player_points' not in session:
        session['player_points'] = 0
    
    return render_template('index.html', points=session['player_points'])


@app.route('/answer-checker')
def answer_checker():
    """Answer Checker game page"""
    # Initialize game state if starting fresh
    if 'ac_problem_count' not in session:
        session['ac_problem_count'] = 0
        session['ac_score'] = 0
        session['ac_game_active'] = False
    
    return render_template('answer_checker.html', 
                         problem_count=session.get('ac_problem_count', 0),
                         score=session.get('ac_score', 0),
                         game_active=session.get('ac_game_active', False),
                         total_points=session.get('player_points', 0))


@app.route('/answer-checker/start', methods=['POST'])
def start_quiz():
    """Start a new quiz"""
    session['ac_problem_count'] = 0
    session['ac_score'] = 0
    session['ac_game_active'] = True
    return redirect(url_for('answer_checker'))


@app.route('/answer-checker/submit', methods=['POST'])
def submit_answer():
    """Check the submitted answer"""
    problem = request.form.get('problem', '').strip()
    
    if not problem:
        flash('Please enter a problem!', 'warning')
        return redirect(url_for('answer_checker'))
    
    # Check the answer
    is_correct, correct_answer, error_msg = check_answer(problem)
    
    if error_msg:
        flash(error_msg, 'error')
    elif is_correct:
        flash('✅ Correct! Great job!', 'success')
        session['ac_score'] = session.get('ac_score', 0) + 1
        session['ac_problem_count'] = session.get('ac_problem_count', 0) + 1
    else:
        flash(f'❌ Wrong! The correct answer is {correct_answer}', 'error')
        session['ac_problem_count'] = session.get('ac_problem_count', 0) + 1
    
    # Check if quiz is complete
    if session.get('ac_problem_count', 0) >= 10:
        session['ac_game_active'] = False
        # Add score to total points
        session['player_points'] = session.get('player_points', 0) + session.get('ac_score', 0)
    
    return redirect(url_for('answer_checker'))


@app.route('/answer-checker/reset', methods=['POST'])
def reset_quiz():
    """Reset the quiz"""
    session['ac_problem_count'] = 0
    session['ac_score'] = 0
    session['ac_game_active'] = False
    return redirect(url_for('answer_checker'))


@app.route('/memory-bank')
def memory_bank():
    """Memory Bank game page (placeholder)"""
    return render_template('coming_soon.html', 
                         game_name='Memory Bank',
                         game_icon='🧠',
                         total_points=session.get('player_points', 0))


@app.route('/electro-flash')
def electro_flash():
    """Electro Flash game page (placeholder)"""
    return render_template('coming_soon.html', 
                         game_name='Electro Flash',
                         game_icon='⚡',
                         total_points=session.get('player_points', 0))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
