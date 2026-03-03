# 🐦 Twitter Sentiment Analyzer

An end-to-end AI-powered web application that performs real-time tweet sentiment analysis using Machine Learning.

🚀 **Live Demo:**
https://twitter-sentiment-ai-b2pr.onrender.com

---

## 📌 Project Overview

This project is a full-stack AI deployment pipeline built using:

* 🧠 Machine Learning (Scikit-learn)
* ⚡ FastAPI (Backend API)
* 🎨 Streamlit (Frontend UI)
* 🐳 Docker (Containerization)
* ☁ Render (Cloud Deployment)
* 🔗 GitHub (Version Control & CI)

The system classifies tweets as **Positive** or **Negative** with confidence scores.

---

## 🧠 Machine Learning Details

* **Model:** Logistic Regression
* **Vectorizer:** TF-IDF
* **Dataset:** Sentiment140
* **Task:** Binary Sentiment Classification
* **Accuracy:** ~80–85%

The trained model and vectorizer are saved using `joblib` and loaded inside the FastAPI service.

---

## 🏗 Architecture

```
User (Browser)
        ↓
Streamlit Frontend (UI)
        ↓
FastAPI Backend (Prediction API)
        ↓
Scikit-learn Model
```

Both FastAPI and Streamlit run inside the same Docker container and communicate internally.

---

## 🚀 Features

✅ Real-time tweet sentiment prediction
✅ Confidence score display
✅ Sentiment history tracking
✅ Download prediction history as CSV
✅ Responsive UI with custom CSS
✅ Dockerized production deployment
✅ Cloud-hosted on Render

---

## 📂 Project Structure

```
twitter-sentiment-ai/
│
├── app/
│   └── main.py              # FastAPI backend
│
├── frontend/
│   └── streamlit_app.py     # Streamlit frontend
│
├── model/
│   ├── sentiment_model.pkl
│   └── vectorizer.pkl
│
├── train_model.py           # Model training script
├── requirements.txt
├── Dockerfile
├── start.sh
└── README.md
```

---

## 🐳 Run Locally with Docker

```bash
docker build -t twitter-sentiment-ai .
docker run -p 8501:8501 -p 8000:8000 twitter-sentiment-ai
```

Then open:

```
http://localhost:8501
```

---

## ⚙ Run Without Docker (Local Dev)

### 1️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Start backend

```bash
uvicorn app.main:app --reload
```

### 4️⃣ Start frontend

```bash
streamlit run frontend/streamlit_app.py
```

---

## ☁ Deployment

This project is deployed using:

* Docker container
* GitHub integration
* Render Web Service

Every push to `main` branch triggers automatic redeployment.

---

## 🧑‍💻 Author

**Mayur Chauhan**
BE – Artificial Intelligence & Data Science
Aspiring AI/ML Engineer

---

## 📌 Future Improvements

* Multi-class sentiment (Positive / Neutral / Negative)
* Model upgrade (Transformer / BERT)
* Separate backend & frontend services
* Authentication system
* Database integration

---

⭐ If you like this project, give it a star on GitHub!
