from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 
import random

class Score(BaseModel):
    score: float
    name: str

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

def calculate_win_amount(risk: int, wager: int) -> float:
    """Calculate the win amount based on risk and wager."""
    multiplier = 1 / ((100.00 - risk) / 100)
    win_amount = round((wager * multiplier) - wager, 2)
    return win_amount

@app.post('/score/'):
async def post_score(score: Score):
    try:
        score_value = score.score
        name = score.name
    except ValueError as e:
        return {"error": str(e)}

    return {"message": f"Score {score_value} for {name} has been recorded."}

@app.get('/score/')
async def get_score():
    try:
        # Get the score from the database
        score = 100.00  # Placeholder for actual score retrieval logic
        return {"score": score}
    except Exception as e:
        return {"error": str(e)}

@app.get('/odds/')
async def get_odds(risk: int = 50, wager: int = 10):
    rand = (await get_rand(1, 100))['rand']  # Get a random number between 1 and 100
    print(f"Random number generated: {rand}")
    if rand >= risk:
        win_amount = calculate_win_amount(risk,wager)
    else:
        win_amount = round(wager * -1, 2)  # Lose the wager amount
    return {"win_amount": win_amount, "rand": rand}

@app.get('/rand/')
async def get_rand(min: int = 1, max: int = 100):
    if min > max: 
        return {"error": "min value cannot be greater than max value."}

    # Get the random number
    rand = random.randint(min, max)
    return {"rand": int(rand)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)