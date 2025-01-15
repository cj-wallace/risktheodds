from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/rand', methods=['GET'])
def get_rand(min=1, max=100):
    # Get the random number
    rand = random.randint(min, max)
    return str(rand)

if __name__ == '__main__':
    app.run(debug=True)