import streamlit as st
import requests
import time
import pandas as pd

API_URL = "/predict"
HEALTH_URL = "/health"

# -------- Page Config --------
st.set_page_config(page_title="Twitter Sentiment Analyzer", page_icon="🐦", layout="wide")

# -------- Session State --------
if "history" not in st.session_state:
    st.session_state.history = []

if "tweet_text" not in st.session_state:
    st.session_state.tweet_text = ""

# -------- FINAL CSS (All fixes merged) --------
st.markdown("""
<style>

/* ================= Background ================= */
.stApp {
    background: linear-gradient(-45deg, #141E30, #243B55, #0f2027, #2c5364);
    background-size: 400% 400%;
    animation: gradient 12s ease infinite;
    color: white;
}

/* ================= Buttons ================= */
div.stButton > button {
    background: linear-gradient(90deg, #1DA1F2, #0d8ddb) !important;
    color: white !important;
    border-radius: 10px !important;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background: #0d8ddb !important;
}

/* Download button fix */
div.stDownloadButton > button {
    background: linear-gradient(90deg, #1DA1F2, #0d8ddb) !important;
    color: white !important;
    border-radius: 10px !important;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
}

div.stDownloadButton > button:hover {
    background: #0d8ddb !important;
}

/* ================= Text Area ================= */
textarea {
    background-color: rgba(0,0,0,0.6) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #1DA1F2 !important;
}

/* Label visibility */
label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}

/* ================= Metrics ================= */
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 28px !important;
}

[data-testid="stMetricLabel"] {
    color: #cccccc !important;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #1DA1F2 !important;
}

/* ================= Character Counter ================= */
.counter {
    text-align: right;
    font-size: 13px;
    color: #bbbbbb;
}

/* ================= Footer ================= */
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    background: rgba(0,0,0,0.4);
    padding: 8px;
    font-size: 12px;
    color: #cccccc;
}

</style>
""", unsafe_allow_html=True)

# -------- Header --------
st.markdown("## 🐦 Twitter Sentiment Analyzer")
st.caption("AI-powered real-time tweet sentiment analysis")

# -------- API Status --------
try:
    requests.get(HEALTH_URL, timeout=2)
    st.success("API Connected")
except:
    st.error("API Not Running")

# -------- Layout --------
col_main, col_history = st.columns([2,1])

# ================= MAIN PANEL =================
with col_main:

    # Example Tweets
    st.write("Try examples:")
    ex1, ex2 = st.columns(2)

    with ex1:
        if st.button("Positive Example"):
            st.session_state.tweet_text = "I absolutely love this product! Amazing experience."

    with ex2:
        if st.button("Negative Example"):
            st.session_state.tweet_text = "This service is terrible and disappointing."

    # Input
    tweet = st.text_area(
        "✍️ Compose Tweet",
        height=140,
        max_chars=280,
        value=st.session_state.tweet_text
    )

    st.session_state.tweet_text = tweet

    # Character Counter
    char_count = len(tweet)
    color = "#bbbbbb"
    if char_count > 240:
        color = "orange"
    if char_count > 270:
        color = "red"

    st.markdown(
        f'<div class="counter" style="color:{color}">{char_count}/280</div>',
        unsafe_allow_html=True
    )

    # Buttons
    col1, col2 = st.columns([3,1])
    with col1:
        analyze = st.button("Analyze Sentiment")
    with col2:
        if st.button("Clear"):
            st.session_state.tweet_text = ""
            st.rerun()

    # -------- Prediction --------
    if analyze:
        if tweet.strip() == "":
            st.warning("Please enter a tweet.")
        else:
            start_time = time.time()

            try:
                with st.spinner("Analyzing with AI..."):
                    response = requests.post(API_URL, json={"text": tweet}, timeout=10)

                end_time = time.time()

                if response.status_code == 200:
                    result = response.json()
                    sentiment = result["sentiment"]
                    confidence = float(result["confidence"])

                    emoji = "😊" if sentiment == "Positive" else "😞"

                    # Result
                    if sentiment == "Positive":
                        st.success(f"{emoji} Positive Sentiment")
                    else:
                        st.error(f"{emoji} Negative Sentiment")

                    # Confidence
                    st.markdown("### Model Confidence")
                    st.metric("Confidence", f"{round(confidence*100,2)}%")
                    st.progress(confidence)

                    # Confidence strength
                    if confidence > 0.7:
                        st.success("Strong prediction")
                    elif confidence > 0.4:
                        st.warning("Moderate confidence")
                    else:
                        st.error("Low confidence")

                    st.caption(f"Prediction time: {round(end_time-start_time,3)} sec")

                    # Save history
                    st.session_state.history.insert(0, {
                        "text": tweet,
                        "sentiment": sentiment,
                        "confidence": confidence
                    })

                else:
                    st.error(response.json().get("detail", "API Error"))

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to API.")

# ================= HISTORY PANEL =================
with col_history:
    st.subheader("🕘 Sentiment History")

    if len(st.session_state.history) == 0:
        st.write("No predictions yet.")
    else:
        for item in st.session_state.history[:5]:
            emoji = "😊" if item["sentiment"] == "Positive" else "😞"
            st.write(f"{emoji} {item['sentiment']} ({round(item['confidence']*100,1)}%)")
            st.caption(item["text"][:80])

    # Clear History
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

    # Download CSV (Styled)
    if len(st.session_state.history) > 0:
        df = pd.DataFrame(st.session_state.history)
        st.download_button(
            "⬇ Download History (CSV)",
            df.to_csv(index=False),
            file_name="sentiment_history.csv",
            mime="text/csv"
        )

# -------- Model Info --------
with st.expander("About the Model"):
    st.write("""
    **Model:** Logistic Regression  
    **Vectorizer:** TF-IDF  
    **Dataset:** Sentiment140  
    **Task:** Binary Sentiment Classification  
    **Accuracy:** ~80–85%
    """)

# -------- Footer --------
st.markdown(
    '<div class="footer">End-to-End AI Deployment | Built by Mayur Chauhan</div>',
    unsafe_allow_html=True
)