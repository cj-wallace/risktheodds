
def get_odds(request):
    if request.method == 'GET':
        try:
            # Get the odds from the database
            odds = Odds.objects.all()
            serializer = OddsSerializer(odds, many=True)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def updateScore(currentScore):
    self.highScore = max(self.highScore, currentScore)

    # TODO Save the high score to the database 

def run_game(current_risk, current_wager):
    # Get the odds from the database
    odds = Odds.objects.all()

    # Calculate the multiplier
    multiplier = 1 / ((100.00 - current_risk) / 100)

    # Calculate the win amount
    win_amount = (current_wager * multiplier) - current_wager

    if(currentWager <= 0):
        eventView.text = "Not enough wagered"
    elif(winAmt <= 0):
        eventView.text = "Not enough risk for a win"
    else:
        rand = random.randint(1, 100)

        #One more try...
        if rand < currentRisk and losses >= 3:
            rand = max(rand, random.randint(1, 100))

        if rand >= currentRisk:
            win_amount = (current_wager * multiplier) - current_wager
            self.losses = 0
        else:
            # Lose!
            self.losses += 1
            self.currentScore -= current_wager
            self.eventView.text = "Lose! " + current_wager

            if self.currentScore <= 0:
                self.currentScore = 0
                self.eventView.text = "You have lost everything!"


    return win_amount