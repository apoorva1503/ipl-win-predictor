import streamlit as st
import pickle
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide"
)


# =========================================================
# LOAD MODEL
# =========================================================

pipe = pickle.load(open("pipe.pkl", "rb"))


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b0f19;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
    margin-top: 10px;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 17px;
    margin-bottom: 35px;
}

/* Section heading */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Prediction cards */
.win-card {
    background: linear-gradient(135deg, #123d2a, #0d241b);
    border: 1px solid #1f6f4a;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.lose-card {
    background: linear-gradient(135deg, #3d1717, #241010);
    border: 1px solid #713030;
    border-radius: 18px;
    padding: 25px;
    text-align: center;
}

.team-name {
    font-size: 19px;
    font-weight: 600;
    margin-bottom: 8px;
}

.probability {
    font-size: 38px;
    font-weight: 800;
}

.probability-label {
    color: #9ca3af;
    font-size: 14px;
}

/* Match summary */
.summary-box {
    background-color: #111827;
    border: 1px solid #293241;
    border-radius: 15px;
    padding: 20px;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title"> IPL Win Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Predict the winning probability during an IPL run chase'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DATA
# =========================================================

teams = [
    "Sunrisers Hyderabad",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Kings XI Punjab",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Delhi Daredevils"
]

cities = [
    "Hyderabad",
    "Mumbai",
    "Bangalore",
    "Kolkata",
    "Chandigarh",
    "Chennai",
    "Jaipur",
    "Delhi"
]


# =========================================================
# MATCH INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title"> Match Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox(
        "Batting Team",
        teams
    )

with col2:
    bowling_team = st.selectbox(
        "Bowling Team",
        teams,
        index=1
    )

with col3:
    city = st.selectbox(
        "City",
        cities
    )


# =========================================================
# CURRENT MATCH SITUATION
# =========================================================

st.markdown(
    '<div class="section-title"> Current Match Situation</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    target = st.number_input(
        " Target Score",
        min_value=1,
        max_value=300,
        value=180
    )

with col2:
    current_score = st.number_input(
        " Current Score",
        min_value=0,
        max_value=300,
        value=50
    )

with col3:
    wickets_left = st.number_input(
        " Wickets Left",
        min_value=0,
        max_value=10,
        value=8
    )


col1, col2 = st.columns(2)

with col1:
    overs_completed = st.number_input(
        " Overs Completed",
        min_value=0,
        max_value=20,
        value=5,
        step=1
    )

with col2:
    balls_in_over = st.number_input(
        " Balls in Current Over",
        min_value=0,
        max_value=5,
        value=0,
        step=1
    )

# Total balls completed
total_balls_completed = (overs_completed * 6) + balls_in_over

# Balls remaining
balls_left = 120 - total_balls_completed

# Display overs in cricket format
overs_display = f"{overs_completed}.{balls_in_over}"

st.caption(f"Current overs: **{overs_display}**")
# =========================================================
# CALCULATED FEATURES
# =========================================================
# Runs remaining
runs_left = target - current_score

# Total balls completed
total_balls_completed = (overs_completed * 6) + balls_in_over

# Balls remaining
balls_left = 120 - total_balls_completed

# Current Run Rate
if total_balls_completed > 0:
    crr = (current_score / total_balls_completed) * 6
else:
    crr = 0

# Required Run Rate
if balls_left > 0:
    rrr = (runs_left / balls_left) * 6
else:
    rrr = 0

# =========================================================
# MATCH STATISTICS
# =========================================================

st.markdown(
    '<div class="section-title"> Match Statistics</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Runs Left",
        max(runs_left, 0)
    )

with col2:
    st.metric(
        "Balls Left",
        balls_left
    )

with col3:
    st.metric(
        "Current Run Rate",
        f"{crr:.2f}"
    )

with col4:
    st.metric(
        "Required Run Rate",
        f"{rrr:.2f}"
    )

# =========================================================
# PREDICTION BUTTON
# =========================================================

st.markdown("")

predict = st.button(
    " PREDICT WINNING PROBABILITY",
    use_container_width=True
)


# =========================================================
# PREDICTION
# =========================================================

if predict:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if batting_team == bowling_team:

        st.error(
            "Batting Team and Bowling Team cannot be the same."
        )

    elif current_score >= target:

        st.success(
            f" {batting_team} has already reached the target!"
        )

    elif balls_left <= 0:

        st.error("The innings has ended.")

    elif wickets_left <= 0:

        st.error("All wickets have fallen.")

    else:

        # -------------------------------------------------
        # MODEL INPUT
        # -------------------------------------------------

        input_data = pd.DataFrame({
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [city],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets_left": [wickets_left],
            "total_runs_x": [target],
            "target": [target],
            "crr": [crr],
            "rrr": [rrr]
        })


        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        prediction = pipe.predict_proba(input_data)

        lose_probability = prediction[0][0] * 100
        win_probability = prediction[0][1] * 100


        # =================================================
        # MATCH PREDICTION
        # =================================================

        st.divider()

        st.header(" Match Prediction")

        st.caption(
            "Winning probability based on the current match situation."
        )

        st.write("")


        # =================================================
        # WINNING PROBABILITY
        # =================================================

        col1, col2 = st.columns(2)


        # Batting team
        with col1:

            st.subheader(" " + batting_team)

            st.metric(
                "Winning Probability",
                f"{win_probability:.1f}%"
            )

            st.progress(
                int(win_probability)
            )


        # Bowling team
        with col2:

            st.subheader(" " + bowling_team)

            st.metric(
                "Winning Probability",
                f"{lose_probability:.1f}%"
            )

            st.progress(
                int(lose_probability)
            )


        # =================================================
        # PREDICTED WINNER
        # =================================================

        st.write("")
        st.subheader(" Model Prediction")


        if win_probability > lose_probability:

            st.success(
                f" {batting_team} has a "
                f"{win_probability:.1f}% winning probability."
            )

        else:

            st.error(
                f" {bowling_team} has a "
                f"{lose_probability:.1f}% winning probability."
            )


        # =================================================
        # CURRENT MATCH STATUS
        # =================================================

        st.write("")
        st.subheader(" Current Match Status")

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Current Score",
                f"{current_score}/{10 - wickets_left}"
            )


        with col2:

            st.metric(
                "Target",
                target
            )


        with col3:

            st.metric(
                "Runs Required",
                max(runs_left, 0)
            )


        with col4:

            st.metric(
                "Wickets Left",
                wickets_left
            )


        # =================================================
        # RUN RATE INFORMATION
        # =================================================

        st.write("")
        st.subheader(" Run Rate")

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Current Run Rate",
                f"{crr:.2f}"
            )


        with col2:

            st.metric(
                "Required Run Rate",
                f"{rrr:.2f}"
            )


        with col3:

            st.metric(
                "Balls Left",
                balls_left
            )


        # =================================================
        # MATCH SUMMARY
        # =================================================

        st.write("")
        st.subheader(" Match Summary")

        st.info(
            f" {batting_team} need "
            f"{max(runs_left, 0)} runs from "
            f"{balls_left} balls to reach the target of "
            f"{target}."
                )