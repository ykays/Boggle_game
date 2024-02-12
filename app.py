from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"


boggle_game = Boggle()

@app.route('/')
def display_boggle():
    """To display the board (all the letters) when the game starts"""
    session['board'] = boggle_game.make_board()
    session['count'] = session.get('count', 0) + 1
    session['highscore'] = session.get('highscore', 0) 
    return render_template('home.html')

@app.route('/check-word/<word>')
def check_word(word):
    """ Function that checks if the word is valid and sends results back to be processed on the page"""
    result = boggle_game.check_valid_word(session['board'], word)
    return jsonify({"result": result})



@app.route('/update-score', methods=['POST'])
def update_score():
    """To get the current score from js and check whether is the highest score to store it in the session"""
    score = request.json['score']
    highscore = session.get("highscore", 0)
    session['highscore'] = max(score, highscore)
    return jsonify(session['highscore'])


