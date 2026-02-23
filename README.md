# 🎭 Mood Arcade

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://moodarcadegit-24erpsqgxscs6rehrbachg.streamlit.app)

**Mood Arcade** is an interactive web app that helps you discover your current emotional state through a series of fun and relaxing games. Play with words, colors, drawings, and stories to get a personalized mood insight and gentle recommendations.

![App Screenshot](screenshot.png) <!-- Optional: Add a screenshot of your app -->

## ✨ Features

- **📝 Word Association** – Select words that resonate with your feelings from a rich vocabulary list.
- **🎨 Drawing Board** – Express yourself freely with a simple canvas and label the mood of your drawing.
- **📖 Story Completion** – Continue a story prompt; your narrative is analyzed for emotional sentiment.
- **🎨 Color Preference** – Pick a color that feels right, and let the app interpret its mood.
- **🔮 Mood Prediction** – Combines inputs from all games to predict your dominant mood.
- **💡 Personalized Suggestions** – Receive gentle, actionable recommendations based on your predicted mood.
- **📊 Progress Tracker** – A visual progress bar shows how many games you've completed.
- **✨ Daily Affirmation** – A random uplifting quote in the sidebar to brighten your day.
- **🎈 Celebratory Balloons** – Enjoy a fun animation when you complete all four games.
- **🎨 Relaxed Cosmic UI** – Soft gradients, blurred cards, and cinematic buttons for a calming experience.

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit** – For the web application framework.
- **Streamlit Drawable Canvas** – For the drawing game.
- **TextBlob** – For sentiment analysis on stories.
- **Pillow** – Image processing (dependency for the canvas).
- **NLTK** – Natural language toolkit (used by TextBlob).

## 🚀 Live Demo

Experience the app live: [Mood Arcade](https://moodarcadegit-24erpsqgxscs6rehrbachg.streamlit.app)

## 📦 Local Installation

Follow these steps to run the app on your own machine.

### Prerequisites

- Python 3.8 or higher
- Git

### Steps

# 1. Clone the repository
```bash
git clone https://github.com/NishantDas0079/Mood_Arcade.git
cd Mood_Arcade
```

# 2. Create and activate virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 4. Run the app
```bash
streamlit run app.py
```

Open your browser and go to `http://localhost:8501`

# ☁️ Deploy to Streamlit Cloud
Push your code to a GitHub repository.

Go to `share.streamlit.io` and sign in with GitHub.

Click `"New app"`, select your repository, branch, and set the main file to `app.py`.

No secrets are required for this app (it doesn't use external APIs).

Click `"Deploy"`. Your app will be live in a few minutes.

# 🎮 How to Play
Word Association: Choose any number of words that describe your current feelings.

Draw Your Mood: Use the canvas to draw freely, then select the mood your drawing expresses.

Story Completion: Continue the provided story prompt in a few sentences.

Color Preference: Pick a color and click "Submit" to register your choice.

Reveal Your Mood: Click the big button to see your predicted mood and get personalized suggestions.

