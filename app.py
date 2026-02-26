import streamlit as st
import requests
from scipy.stats import poisson
from datetime import date

st.title("AI Soccer Prediction Engine")

#########################################
# API SETTINGS
#########################################

API_KEY = "x-rapidapi-key: 7f6830d7bbmsh8e5aeb397ef584dp14c6dejsn66526c44d2b0"

today = date.today()

url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={today}"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

data = response.json()

matches = data["response"]

#########################################
# POISSON MODEL FUNCTION
#########################################

def predict():

    home_xg = 1.6
    away_xg = 1.2

    max_goals = 5
    probs = {}

    for h in range(max_goals):
        for a in range(max_goals):
            probs[(h,a)] = poisson.pmf(h, home_xg) * poisson.pmf(a, away_xg)

    home=draw=away=over25=btts=0

    for (h,a),p in probs.items():

        if h>a:
            home+=p
        elif h==a:
            draw+=p
        else:
            away+=p

        if h+a>2:
            over25+=p

        if h>0 and a>0:
            btts+=p

    confidence = max(home, draw, away)

    return home, draw, away, over25, btts, confidence

#########################################
# RUN PREDICTIONS
#########################################

results = []

for match in matches:

    home = match["teams"]["home"]["name"]
    away = match["teams"]["away"]["name"]

    h,d,a,o,b,c = predict()

    results.append({
        "home":home,
        "away":away,
        "home_prob":h,
        "draw_prob":d,
        "away_prob":a,
        "over25":o,
        "btts":b,
        "confidence":c
    })

#########################################
# TOP 10 DAILY PICKS
#########################################

sorted_games = sorted(results, key=lambda x: x["confidence"], reverse=True)
top10 = sorted_games[:10]

st.header("Daily Winners (Top 10 Highest Probability)")

for game in top10:

    st.write("---")
    st.subheader(game["home"] + " vs " + game["away"])

    st.write("Home:", round(game["home_prob"]*100,1), "%")
    st.write("Draw:", round(game["draw_prob"]*100,1), "%")
    st.write("Away:", round(game["away_prob"]*100,1), "%")

    st.write("Over 2.5:", round(game["over25"]*100,1), "%")
    st.write("BTTS:", round(game["btts"]*100,1), "%")

#########################################
# ALL MATCHES
#########################################

st.header("All Matches Today")

for game in results:
    st.write(game["home"], "vs", game["away"])
