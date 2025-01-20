from flask import Flask
import random
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

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