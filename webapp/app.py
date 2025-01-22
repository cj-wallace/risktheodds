from flask import Flask, render_template, request, redirect, session, session
import random
import json
import os


app = Flask(__name__)

app.secret_key='SECRET_KEY'

@app.route('/', methods=['GET', 'POST'])
def index():
    score = float(session['score'] if 'score' in session else 100.00)
    history = list(session['history'] if 'history' in session else [])

    print(score)
    print(history)

    if request.method == 'POST':
        post_data = dict(request.form)

        #Parse POST info and get random odds
        risk = int(post_data['risk'])
        wager = int(post_data['wager'])

        game_result,rand = run_game(risk, wager)
        score += game_result
        score_str = "{:,.2f}".format(score)
        if game_result > 0:
            result_str = "{:,.2f}".format(game_result)
            message = f"You won ${result_str}!"
            output = f"Score: {score_str} | Risk: {risk} | Rand: {rand} | Win: ${result_str}"
        else:
            result_str = "{:,.2f}".format(game_result * -1)
            message = f"You lost ${result_str}!"
            output = f"Score: {score_str} | Risk: {risk} | Rand: {rand} | Loss: ${result_str}"
        

        history.insert(0,output)
        history = history[:5]

        session['score'] = score
        session['history'] = history

        print(score)
        print(history)

        return render_template('risk.html',score=score_str, message=message, risk=int(risk), wager=int(wager), rand=int(rand), history=history)
    elif request.method == 'GET':
        score_str = "{:,.2f}".format(score)
        return render_template('risk.html', wager=10, risk=50, score=score_str, history=history)

def run_game(current_risk, current_wager):

    # Calculate the multiplier
    multiplier = 1 / ((100.00 - current_risk) / 100)

    # Calculate the win amount
    win_amount = round((current_wager * multiplier) - current_wager, 2)
    lose_amount = round(current_wager, 2) * -1

    # Get the odds from the database
    rand = int(get_rand())
    
    #TODO: Add one more try mode
    #if rand < current_risk and losses >= 3:
    #    rand = max(rand, get_rand())

    if rand == current_risk:
        return win_amount*10,rand
    elif rand > current_risk:
        return win_amount,rand
    else:
        return lose_amount,rand

@app.route('/scores', methods=['GET', 'POST'])
def scores():
    scores_file = os.path.join(os.path.dirname(__file__), 'data/scores.json')
    if request.method == 'POST':
        post_data = dict(request.form)
        score = float(post_data['score'])
        name = str(post_data['name'])
        if score <= 0:
            return "Invalid score"
        elif len(name) == 0:
            return "Invalid name"
        else:
            with open(scores_file, 'r') as f:
                scores = list(json.load(f))
                for i in scores:
                    if name in i:
                        return "Name already exists"
                    else:
                        new_score = {"name": name, "score": score, "score_string": "{:,.2f}".format(score)}
                        scores.append(new_score)
                        with open(scores_file, 'w') as f:
                            json.dump(scores, f)

                        session['score'] = 100.00
                        session['history'] = []

                        return redirect("/scores")

    elif request.method == 'GET':
        with open(scores_file, 'r') as f:
            scores = json.load(f)# Sort entries by score
            scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        return render_template('scores.html', scores=scores)

@app.route('/rand/', methods=['GET'])
def get_rand(min=1, max=100):
    try:
        min = int(request.args.get('min', min))
    except ValueError:
        min = min

    try:
        max = int(request.args.get('max', max))
    except ValueError:
        max = max

    # Get the random number
    rand = random.randint(min, max)
    return str(rand)

@app.route('/updateScore', methods=['POST'])
def update_score(current_score):
    # Get the high score
    high_score = 0

    # Update the high score
    high_score = max(high_score, current_score)

    # TODO Save the high score to the database

    return str(high_score)

if __name__ == '__main__':
    app.run(debug=True)