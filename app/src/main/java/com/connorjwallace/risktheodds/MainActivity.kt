package com.connorjwallace.risktheodds

import android.animation.ObjectAnimator
import android.content.Context
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.SeekBar
import android.widget.TextView
import androidx.activity.ComponentActivity
import kotlin.math.roundToInt
import kotlin.random.Random

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val sharedPref = getPreferences(Context.MODE_PRIVATE)

        val textView : TextView = findViewById(R.id.textView)
        val scoreView : TextView = findViewById(R.id.scoreTextView)

        val multiplierView : TextView = findViewById(R.id.multiplierTextView)
        val possibleWinView : TextView = findViewById(R.id.possibleWinTextView)
        val riskView : TextView = findViewById(R.id.riskTextView)
        val wagerView : TextView = findViewById(R.id.wagerTextView)
        val eventView : TextView = findViewById(R.id.eventTextView)
        val highScoreView : TextView = findViewById(R.id.highScoreTextView)

        val button : Button = findViewById(R.id.button)
        val restockButton : Button = findViewById(R.id.restockButton)
        val riskSeekBar : SeekBar = findViewById(R.id.seekBar)
        val wagerSeekBar : SeekBar = findViewById(R.id.wagerSeekBar)
        val progressBar : ProgressBar = findViewById(R.id.progressBar)

        var currentScore : Int = 100
        var currentRisk : Int = 50
        var multiplier : Float = minOf(1 / ((100.00f - currentRisk.toFloat()) / 100),50f)
        var currentWager : Int = 25
        var winAmt: Int = (currentWager * multiplier).roundToInt() - currentWager
        var losses : Int = 0
        var highScore : Int = 0

        restockButton.visibility = View.GONE

        var pref_score : Int = sharedPref.getInt("HighScore",0)
        if (pref_score > highScore){
            highScore = pref_score
        }

        riskSeekBar.progress = currentRisk
        wagerSeekBar.max = currentScore
        wagerSeekBar.progress = currentWager

        scoreView.text = "Score: " + currentScore.toString()
        riskView.text = "Select Risk: " + currentRisk.toString()
        wagerView.text = "Wager: " + currentWager.toString()
        multiplierView.text = "Multiplier: " + String.format("%.2f", multiplier)
        possibleWinView.text = "Possible Win: " + winAmt.toString()
        scoreView.text = "Score: " + currentScore.toString()
        highScoreView.text = "HighScore: " + highScore.toString()

        eventView.text = ""

        riskSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // Update UI or perform actions based on the seek bar progress

                var riskVal : Int = seekBar?.progress ?: 0

                multiplier  = minOf(1 / ((100.00f - riskVal.toFloat()) / 100),50f)

                currentRisk = riskVal

                winAmt = (currentWager * multiplier).roundToInt() - currentWager


                scoreView.text = "Score: " + currentScore.toString()
                riskView.text = "Select Risk: " + currentRisk.toString()
                wagerView.text = "Wager: " + currentWager.toString()
                highScoreView.text = "HighScore: " + highScore.toString()
                multiplierView.text = "Multiplier: " + String.format("%.2f", multiplier)
                possibleWinView.text = "Possible Win: " + winAmt.toString()
                scoreView.text = "Score: " + currentScore.toString()
                highScoreView.text = "HighScore: " + highScore.toString()
            }
            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        wagerSeekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // Update UI or perform actions based on the seek bar progress

                var wagerVal : Int = seekBar?.progress ?: 0

                currentWager = wagerVal
                winAmt = (currentWager * multiplier).roundToInt() - currentWager

                scoreView.text = "Score: " + currentScore.toString()
                riskView.text = "Select Risk: " + currentRisk.toString()
                wagerView.text = "Wager: " + currentWager.toString()
                highScoreView.text = "HighScore: " + highScore.toString()
                multiplierView.text = "Multiplier: " + String.format("%.2f", multiplier)
                possibleWinView.text = "Possible Win: " + winAmt.toString()

            }
            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })

        button.setOnClickListener(object : View.OnClickListener {
            override fun onClick(view: View?) {

                if(currentWager <= 0){
                    eventView.text = "Not enough wagered"
                }
                else if(winAmt <= 0){
                    eventView.text = "Not enough risk for a win"
                }
                else{
                    var rand : Int = Random.nextInt(100) + 1

                    // One more try..
                    if ( rand < currentRisk && losses >= 3 ){
                        rand = maxOf(rand, Random.nextInt(100) + 1)

                    }

                    //scoreView.text = rand.toString()
                    //progressBar.progress = rand.toInt()
                    progressBar.progress = 0
                    ObjectAnimator.ofInt(progressBar,"progress", rand.toInt())
                        .setDuration(1000)
                        .start()


                    winAmt = (currentWager * multiplier).roundToInt() - currentWager
                    if ( rand >= currentRisk){
                        //Win!
                        losses = 0
                        currentScore += winAmt
                        if (currentScore > highScore) {
                            highScore = currentScore
                            pref_score = sharedPref.getInt("HighScore",0)
                            if (highScore > pref_score){
                                sharedPref.edit().putInt("HighScore",highScore).apply()
                            }
                        }
                        eventView.text = "Win! " + winAmt.toString()

                        wagerSeekBar.max = currentScore
                    }
                    else {
                        //Lose!
                        losses++
                        currentScore -= currentWager
                        eventView.text = "Lose! " + currentWager.toString()

                        wagerSeekBar.max = currentScore

                        if(currentScore <= 0){
                            currentScore = 0
                            eventView.text = "You have lost everything!"
                            button.visibility = View.GONE
                            restockButton.visibility = View.VISIBLE
                        }
                    }
                }

                scoreView.text = "Score: " + currentScore.toString()
                riskView.text = "Select Risk: " + currentRisk.toString()
                wagerView.text = "Wager: " + currentWager.toString()
                highScoreView.text = "HighScore: " + highScore.toString()
                multiplierView.text = "Multiplier: " + String.format("%.2f", multiplier)
                possibleWinView.text = "Possible Win: " + winAmt.toString()
            }

        })

        restockButton.setOnClickListener(object : View.OnClickListener {
            override fun onClick(view: View?) {
                currentScore = 100

                wagerSeekBar.max = currentScore
                scoreView.text = "Score: " + currentScore.toString()
                riskView.text = "Select Risk: " + currentRisk.toString()
                wagerView.text = "Wager: " + currentWager.toString()
                highScoreView.text = "HighScore: " + highScore.toString()
                multiplierView.text = "Multiplier: " + String.format("%.2f", multiplier)
                possibleWinView.text = "Possible Win: " + winAmt.toString()

                button.visibility = View.VISIBLE
                restockButton.visibility = View.GONE
            }
        })
    }
}