from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)

score = 100.00
history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global score
    global history
    if request.method == 'POST':
        post_data = dict(request.form)

        #Parse POST info and get random odds
        risk = int(post_data['risk'])
        wager = int(post_data['wager'])
        winnings = round(((1 / ((100 - risk) / 100)) * wager) - wager, 2)
        print(f"Risk: {risk} | Wager: {wager} | Winnings: {winnings}")
        rand = int(get_rand())
        win = bool(rand >= risk)
        score_str = "{:.2f}".format(score)
        winnings_str = "{:.2f}".format(winnings)
        lose_str = "{:.2f}".format(wager)
        if(win):
            score += winnings
            output = f"Score: {score_str} | Risk: {risk} | Rand: {rand} | Win: {winnings_str}"
            message = f"You won ${winnings_str}!"
        else:
            score -= wager
            output = f"Score: {score_str} | Risk: {risk} | Rand: {rand} | Loss: {lose_str}"
            message = f"You lost ${lose_str}!"
        
        history.insert(0,output)
        history = history[:5]

        return render_template('risk.html',score=score_str, message=message, risk=int(risk), wager=int(wager), rand=int(rand), history=history)
    elif request.method == 'GET':
        return render_template('risk.html', wager=10, risk=50, score=score_str, history=history)

@app.route('/scores', methods=['GET', 'POST'])
def scores():
    if request.method == 'POST':
        post_data = dict(request.form)
        score = float(post_data['score'])
        return f"Score: {score}"
    elif request.method == 'GET':
        return "unfinished"



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