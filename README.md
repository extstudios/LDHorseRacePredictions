**Race Betting Predictor**

A Python-based desktop application with a graphical interface that predicts the most likely winner for the next race using historical data, pattern detection, and statistical analysis.

**Features**
1. Race Tracking & Data Storage

Input race results for multiple games and rounds.

Saves all results to race_data.csv.

Automatically increments game numbers for seamless tracking.


2. Smart Prediction Engine

Uses all historical data to predict the most likely 1st place finisher.

Detects recurring race order patterns to improve accuracy.

If no matching patterns exist, uses the statistically most successful racer overall.

No hardcoded defaults — predictions are data-driven.


3. Visual Analytics

Generates a heatmap showing how frequently each racer places 1st across all games.

Displays a pattern detection table highlighting recurring race sequences.

5. Always-On-Top Overlay

The app window stays on top of all other windows — perfect for tracking predictions while gaming.

**Installation**

Requirements

Python 3.9+

Install dependencies:

pip install pandas matplotlib seaborn


Usage

Run the application:

python race_predictor.py


Start a new game and input race results.

View recommended bets based on pattern analysis.

Open the heatmap and pattern table from the GUI for deeper insights.

**Data File
**
The app uses race_data.csv for storing results.

Each entry records:

Game number

Round number

1st, 2nd, 3rd, and 4th placements.


Example:
Game	Round	1st	2nd	3rd	4th
1	1	1	3	4	2
1	2	1	2	3	4
🧠 How Predictions Work

Pattern Detection
Looks at the most recent race order and finds all past occurrences of the same order.
Uses the next result after those sequences to predict the next likely winner.

Statistical Fallback
If no pattern is found, the app recommends the racer with the highest historical win rate.
