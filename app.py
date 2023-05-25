from flask import Flask, render_template,session,request,jsonify
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f724'

@app.route('/')
def start():
    '''Show the game board'''
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore',0)
    num_plays = session.get('num_plays', 0)
    return render_template('boggle_game.html', board = board,highscore = highscore, num_plays = num_plays)

@app.route('/check-word')
def check_word():
    '''Check if the submitted word is in the dictionary'''
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board,word)

    return jsonify({'result' : res})

@app.route('/scoring', methods=['POST'])
def scoring():
    ''''''
    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)
    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score,highscore)

    return jsonify(newRecord = score > highscore)