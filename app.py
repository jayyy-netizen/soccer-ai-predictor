import streamlit as st
import numpy as np
from scipy.stats import poisson

st.title("AI Soccer Prediction Engine")

matches = [
("Team A", "Team B"),
("Team C", "Team D"),
("Team E", "Team F")
]

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

    return home,draw,away,over25,btts

for home_team,away_team in matches:

    h,d,a,o,b = predict()

    st.write("---")
    st.subheader(home_team + " vs " + away_team)

    st.write("Home:", round(h*100,1),"%")
    st.write("Draw:", round(d*100,1),"%")
    st.write("Away:", round(a*100,1),"%")

    st.write("Over 2.5:", round(o*100,1),"%")
    st.write("BTTS:", round(b*100,1),"%")
