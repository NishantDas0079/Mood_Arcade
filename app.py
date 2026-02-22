import streamlit as st
from streamlit_drawable_canvas import st_canvas
from textblob import TextBlob
import nltk
import colorsys
import random

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Page config
st.set_page_config(page_title="Mood Discovery Games", page_icon="🎭", layout="centered")
st.title("🎭 Discover Your Mood Through Play")

# ---------- CUSTOM CSS (Soft gradient + cinematic buttons) ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #fdfcfb 0%, #e2d1c3 100%);
        font-family: 'Quicksand', sans-serif;
    }

    h1, h2, h3 {
        color: #5e4b3c;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
    }

    .stMarkdown, .stText, .stSelectbox, .stMultiselect, .stColorPicker {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    .stTextArea textarea, .stSelectbox, .stMultiselect {
        border-radius: 15px !important;
        border: 1px solid #d9c8b2 !important;
    }

    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        font-weight: 600;
    }

    .stAlert {
        border-radius: 15px;
        border-left: 5px solid #b8a9c9;
    }

    /* ===== CINEMATIC BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        background-size: 300% 300%;
        color: white;
        border: none;
        border-radius: 50px;
        padding: 12px 40px;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3), 0 0 20px rgba(255,107,107,0.5);
        transition: all 0.4s ease;
        animation: gradientShift 8s ease infinite;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(5px);
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(0,0,0,0.4), 0 0 30px rgba(255,107,107,0.8);
        cursor: pointer;
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.95);
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stButton.small > button {
        padding: 8px 20px;
        font-size: 0.9rem;
        background: linear-gradient(45deg, #a8edea, #fed6e3);
    }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE INITIALIZATION ----------
if 'game_data' not in st.session_state:
    st.session_state.game_data = {
        'words': None,
        'drawing_mood': None,
        'story_sentiment': None,
        'color_mood': None
    }

# ---------- PROGRESS INDICATOR ----------
def calculate_progress(data):
    """Returns number of completed games (0-4)"""
    completed = 0
    if data.get('words'):           # user selected words
        completed += 1
    if data.get('drawing_mood'):     # user selected drawing mood
        completed += 1
    if data.get('story_sentiment'):  # user wrote a story
        completed += 1
    if data.get('color_mood'):       # user submitted color
        completed += 1
    return completed

progress = calculate_progress(st.session_state.game_data)
st.progress(progress / 4.0, text=f"**Games completed: {progress}/4**")
if progress == 4:
    st.balloons()

# ---------- DAILY AFFIRMATION SIDEBAR ----------
affirmations = [
    "You are capable of amazing things.",
    "Today is full of possibilities.",
    "You are exactly where you need to be.",
    "Your feelings are valid and important.",
    "You have the power to create change.",
    "Breathe. You've got this.",
    "You are loved and you matter.",
    "Every step forward is progress.",
    "You are stronger than you think.",
    "This moment is a gift."
]

st.sidebar.markdown("---")
st.sidebar.header("✨ Daily Affirmation")
if 'affirmation' not in st.session_state:
    st.session_state.affirmation = random.choice(affirmations)

st.sidebar.info(f"💬 {st.session_state.affirmation}")
if st.sidebar.button("🔄 New Affirmation"):
    st.session_state.affirmation = random.choice(affirmations)
    st.rerun()

# ---------- GAME 1: WORD ASSOCIATION ----------
st.header("📝 Game 1: Word Association")
st.write("Select the words that best describe how you feel right now (you can choose multiple).")

word_list = [
    "😊 Happy", "😄 Cheerful", "🌟 Joyful", "☀️ Optimistic", "🎉 Excited",
    "😔 Sad", "💔 Heartbroken", "😢 Melancholic", "🌧️ Gloomy", "🕯️ Lonely",
    "😤 Stressed", "😰 Anxious", "⚡ Overwhelmed", "🌀 Restless", "🔥 Frustrated",
    "😌 Calm", "🍃 Relaxed", "🌊 Peaceful", "🧘 Centered", "🌸 Content",
    "⚡ Energetic", "🏃 Eager", "🚀 Motivated", "💪 Strong", "✨ Lively",
    "😴 Tired", "🛌 Exhausted", "🥱 Sleepy", "🐢 Sluggish", "☁️ Drained",
    "😨 Anxious", "😱 Fearful", "🤔 Worried", "😬 Nervous", "🌀 Uneasy",
    "🤔 Thoughtful", "📚 Reflective", "🧐 Curious", "💭 Introspective", "🎨 Creative",
    "😐 Neutral", "⚖️ Balanced", "🙂 Okay", "🕊️ Serene", "🌱 Grounded"
]

selected_words = st.multiselect("Pick any that apply", word_list, key="words_multi")

# Count mood scores
if selected_words:
    mood_scores = {'happy':0, 'sad':0, 'stressed':0, 'calm':0, 'energetic':0,
                   'tired':0, 'anxious':0, 'thoughtful':0, 'neutral':0}
    for word in selected_words:
        if any(x in word for x in ["Happy","Cheerful","Joyful","Optimistic","Excited"]):
            mood_scores['happy'] += 1
        elif any(x in word for x in ["Sad","Heartbroken","Melancholic","Gloomy","Lonely"]):
            mood_scores['sad'] += 1
        elif any(x in word for x in ["Stressed","Anxious","Overwhelmed","Restless","Frustrated"]):
            mood_scores['stressed'] += 1
        elif any(x in word for x in ["Calm","Relaxed","Peaceful","Centered","Content"]):
            mood_scores['calm'] += 1
        elif any(x in word for x in ["Energetic","Eager","Motivated","Strong","Lively"]):
            mood_scores['energetic'] += 1
        elif any(x in word for x in ["Tired","Exhausted","Sleepy","Sluggish","Drained"]):
            mood_scores['tired'] += 1
        elif any(x in word for x in ["Anxious","Fearful","Worried","Nervous","Uneasy"]):
            mood_scores['anxious'] += 1
        elif any(x in word for x in ["Thoughtful","Reflective","Curious","Introspective","Creative"]):
            mood_scores['thoughtful'] += 1
        else:
            mood_scores['neutral'] += 1
    st.session_state.game_data['words'] = mood_scores
else:
    st.session_state.game_data['words'] = None

# ---------- GAME 2: DRAWING ----------
st.header("🎨 Game 2: Draw Your Mood")
st.write("Use the canvas below to draw anything that represents how you feel.")

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=5,
    stroke_color="#000000",
    background_color="#FFFFFF",
    update_streamlit=True,
    height=300,
    drawing_mode="freedraw",
    key="canvas",
)

if canvas_result.image_data is not None:
    drawing_mood = st.selectbox("What mood does your drawing express?",
                                ["Happy", "Sad", "Stressed", "Calm", "Energetic",
                                 "Tired", "Anxious", "Thoughtful"],
                                key="drawing_mood_select")
    st.session_state.game_data['drawing_mood'] = drawing_mood.lower()
else:
    st.session_state.game_data['drawing_mood'] = None

# ---------- GAME 3: STORY COMPLETION ----------
st.header("📖 Game 3: Story Completion")
st.write("Complete the following story in a few sentences:")

story_prompt = "Once upon a time, on a day just like today, I woke up feeling..."
st.markdown(f"**{story_prompt}**")

user_story = st.text_area("Your story continuation:", height=150, key="story_input")

if user_story.strip():
    blob = TextBlob(user_story)
    polarity = blob.sentiment.polarity

    if polarity > 0.3:
        story_mood = 'happy'
        strength = 2
    elif polarity < -0.3:
        story_mood = 'sad'
        strength = 2
    elif polarity > 0.1:
        story_mood = 'calm'
        strength = 1
    elif polarity < -0.1:
        story_mood = 'anxious'
        strength = 1
    else:
        story_mood = 'neutral'
        strength = 0

    st.session_state.game_data['story_sentiment'] = {
        'mood': story_mood,
        'strength': strength,
        'polarity': polarity
    }
    st.write(f"*Story sentiment score: {polarity:.2f}*")
else:
    st.session_state.game_data['story_sentiment'] = None

# ---------- GAME 4: COLOR PREFERENCE ----------
st.header("🎨 Game 4: Color Preference")
st.write("Pick a color that feels right for you, then click Submit.")

color = st.color_picker("Choose a color", "#00f900")

if st.button("✅ Submit Color Choice"):
    def hex_to_hsv(hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = r/255.0, g/255.0, b/255.0
        return colorsys.rgb_to_hsv(r, g, b)

    h, s, v = hex_to_hsv(color)

    if h < 0.05 or h > 0.95:      # Red
        color_mood = 'energetic'
    elif 0.05 <= h < 0.15:         # Orange
        color_mood = 'happy'
    elif 0.15 <= h < 0.25:         # Yellow
        color_mood = 'happy'
    elif 0.25 <= h < 0.45:         # Green
        color_mood = 'calm'
    elif 0.45 <= h < 0.65:         # Blue
        color_mood = 'sad'
    elif 0.65 <= h < 0.85:         # Purple
        color_mood = 'thoughtful'
    else:                           # Pink/Magenta
        color_mood = 'energetic'

    st.session_state.game_data['color_mood'] = color_mood
    st.success(f"Color saved! Detected mood: **{color_mood.title()}**")
else:
    # Do not store anything until submit is pressed
    pass

# ---------- MOOD PREDICTION FUNCTION ----------
def predict_mood(data):
    totals = {'happy':0, 'sad':0, 'stressed':0, 'calm':0, 'energetic':0,
              'tired':0, 'anxious':0, 'thoughtful':0}

    # Word association (weight 3)
    words = data.get('words')
    if words:
        for mood, score in words.items():
            if mood in totals:
                totals[mood] += score * 3

    # Drawing (weight 2)
    drawing = data.get('drawing_mood')
    if drawing and drawing in totals:
        totals[drawing] += 2

    # Story (weight based on strength)
    story = data.get('story_sentiment')
    if story and story['mood'] in totals:
        totals[story['mood']] += story['strength']

    # Color (weight 1)
    color = data.get('color_mood')
    if color and color in totals:
        totals[color] += 1

    predicted = max(totals, key=totals.get)
    return predicted, totals

# ---------- SOLUTIONS ----------
solutions = {
    'happy': "😊 You seem happy! Channel that energy into something creative or share your positivity with someone. Maybe write a gratitude note or listen to upbeat music.",
    'sad': "😔 It's okay to feel sad. Consider talking to a friend, journaling your thoughts, or watching a comforting movie. Remember, this feeling will pass.",
    'stressed': "😤 You might be stressed. Try a 5‑minute breathing exercise: inhale for 4 seconds, hold for 4, exhale for 6. Repeat a few times. Also, stepping away from screens can help.",
    'calm': "😌 You're in a calm state – perfect for meditation or mindfulness. You could also read a book or enjoy a quiet walk.",
    'energetic': "⚡ You're full of energy! Great for exercise, dancing, or tackling a project you've been putting off.",
    'tired': "😴 You seem tired. Rest is important. Consider a short nap, drink some water, or just take a break. Maybe listen to soothing music.",
    'anxious': "😨 Feeling anxious? Try the 5‑4‑3‑2‑1 grounding technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste. You're safe.",
    'thoughtful': "🤔 You're in a reflective mood. Journaling or reading something philosophical might resonate with you right now."
}

# ---------- PREDICT BUTTON ----------
st.markdown("---")
if st.button("🔮 Reveal My Mood & Get Solutions"):
    if not st.session_state.game_data.get('words'):
        st.warning("Please complete at least the word association game.")
    else:
        predicted, scores = predict_mood(st.session_state.game_data)
        st.success(f"**Your predicted mood is: {predicted.title()}**")
        st.info(solutions.get(predicted, "Take care of yourself!"))
        with st.expander("See detailed scores"):
            st.write(scores)

# ---------- RESET BUTTON ----------
if st.button("Start Over"):
    st.session_state.game_data = {
        'words': None,
        'drawing_mood': None,
        'story_sentiment': None,
        'color_mood': None
    }
    st.rerun()