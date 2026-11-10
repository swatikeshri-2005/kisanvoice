
import os

import streamlit as st  # noqa: I001, RUF100
from dotenv import load_dotenv

# Load environment variables BEFORE importing backend settings/modules.
load_dotenv(override=True)

GNANI_TTS_URL = os.getenv("GNANI_TTS_URL")
GNANI_API_KEY = os.getenv("GNANI_API_KEY")

# The TTS request itself is implemented in backend/text_to_speech.py.
# That module must use this authentication header in its requests.post() call.
GNANI_TTS_HEADERS = {
    "X-API-Key-ID": GNANI_API_KEY or "",
    "Content-Type": "application/json",
}

from backend.answer_engine import answer_question  # noqa: I001
from backend.speech_to_text import transcribe_audio
from backend.text_to_speech import synthesize_speech
from backend.config import settings

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="KisanVoice | AI Farming Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Hind+Siliguri:wght@400;500;600;700&display=swap');

.stApp {
    background: #f5f8f3;
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.hero {
    background: linear-gradient(120deg, #104b32, #258653);
    padding: 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 8px 25px rgba(18,75,50,0.12);
}

.hero h1 {
    color: white !important;
    font-size: 36px;
    font-weight: 800;
}

.hero p {
    color: #e0f4e5;
    font-size: 16px;
}

.section-title {
    color: #174d32;
    font-size: 23px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.feature-card {
    background: white;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #e2ece1;
    min-height: 150px;
    box-shadow: 0 4px 14px rgba(30,80,50,0.04);
}

.feature-card h3 {
    color: #174d32;
    font-size: 18px;
}

.feature-card p {
    color: #69796c;
    font-size: 14px;
}

.assistant-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e0ebe0;
    box-shadow: 0 4px 15px rgba(30,80,50,0.05);
}

div.stButton > button {
    background: #18794e;
    color: white;
    border: none;
    border-radius: 11px;
    font-weight: 600;
    min-height: 42px;
}

div.stButton > button:hover {
    background: #105d3a;
    color: white;
}

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #e4eee5;
    border-radius: 15px;
    padding: 12px;
}

section[data-testid="stSidebar"] {
    background: #eaf3e8;
}

div[data-testid="stForm"] {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #e0ebe0;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #738176;
    font-size: 13px;
}

.status {
    background: #e6f4e8;
    color: #17643e;
    padding: 12px;
    border-radius: 10px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LANGUAGE CONFIGURATION
# --------------------------------------------------

LANGUAGES = {
    "🇮🇳 हिन्दी (Hindi)": "hi",
    "🇮🇳 বাংলা (Bengali)": "bn"
}

COPY = {
    "hi": {
        "title": "🌾 किसानवॉइस",
        "subtitle": "आपका स्मार्ट डिजिटल कृषि सहायक",
        "question": "अपना कृषि प्रश्न लिखें",
        "placeholder": "उदाहरण: धान की पत्तियाँ पीली क्यों हो रही हैं?",
        "ask": "उत्तर पाएँ",
        "audio": "अपनी आवाज़ की रिकॉर्डिंग अपलोड करें",
        "answer": "कृषि विशेषज्ञ AI का उत्तर",
        "speak": "🔊 उत्तर सुनें",
        "demo": "डेमो मोड: स्थानीय कृषि FAQ ज्ञान-संग्रह सक्रिय है।",
        "welcome": "नमस्ते किसान मित्र! आज मैं आपकी कैसे मदद कर सकता हूँ?",
    },
    "bn": {
        "title": "🌾 কৃষকভয়েস",
        "subtitle": "আপনার স্মার্ট ডিজিটাল কৃষি সহায়ক",
        "question": "আপনার কৃষি-সংক্রান্ত প্রশ্ন লিখুন",
        "placeholder": "উদাহরণ: ধানের পাতাগুলি হলুদ হয়ে যাচ্ছে কেন?",
        "ask": "উত্তর দেখুন",
        "audio": "আপনার কণ্ঠের রেকর্ডিং আপলোড করুন",
        "answer": "AI কৃষি সহায়কের উত্তর",
        "speak": "🔊 উত্তর শুনুন",
        "demo": "ডেমো মোড: স্থানীয় কৃষি FAQ জ্ঞানভান্ডার সক্রিয়।",
        "welcome": "নমস্কার কৃষক বন্ধু! আজ আমি কীভাবে সাহায্য করতে পারি?",
    }
}


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "latest_answer" not in st.session_state:
    st.session_state.latest_answer = None

if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 🌾 KisanVoice")

    st.caption("AI Powered Agricultural Assistant")

    st.divider()

    st.markdown("### 🌐 Language / भाषा")

    language_label = st.selectbox(
        "Choose your language",
        list(LANGUAGES.keys())
    )

    lang = LANGUAGES[language_label]
    copy = COPY[lang]

    st.divider()

    st.markdown("### 🌱 Features")

    st.markdown("""
    - 🌿 Crop Health Guidance
    - 💧 Irrigation Advice
    - 🧪 Fertilizer Guidance
    - 🎙️ Voice-based Questions
    - 🗣️ Multilingual Support
    """)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latest_answer = None
        st.session_state.question_input = ""
        st.rerun()

    st.markdown("---")

    st.caption("Developed for farmers 🌾")


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(f"""
<div class="hero">
    <h1>🌾 Welcome to KisanVoice</h1>
    <p>{copy["subtitle"]}</p>
    <p>
        Ask farming questions. Speak naturally.
        Get helpful agricultural guidance in your language.
    </p>
    <p>🌱 Smart Farming · 🎙️ Voice AI · 🌍 Multilingual</p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🌱 Your Farming Assistant</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🌿 Crop Health</h3>
        <p>Get guidance about crop diseases,
        plant health and crop care.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>💧 Smart Irrigation</h3>
        <p>Learn about water management
        and irrigation practices.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🧪 Fertilizer Guide</h3>
        <p>Explore soil health and
        fertilizer management advice.</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🎙️ Talk to KisanVoice</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="status">{copy["welcome"]}</div>',
    unsafe_allow_html=True
)

st.write("")


# --------------------------------------------------
# TEXT QUESTION INPUT
# --------------------------------------------------

st.markdown("#### 💬 Ask your farming question")

with st.form("question_form"):

    question = st.text_area(
        copy["question"],
        placeholder=copy["placeholder"],
        height=110,
        key="question_input"
    )

    submitted = st.form_submit_button(
        copy["ask"] + " 🌱",
        use_container_width=True,
        type="primary"
    )


# --------------------------------------------------
# AUDIO UPLOAD AND SPEECH RECOGNITION
# --------------------------------------------------

st.markdown("#### 🎧 Ask using your voice")

audio_file = st.file_uploader(
    copy["audio"],
    type=["wav", "mp3", "m4a", "ogg", "webm"],
    help="Upload a recording of your farming question."
)

if st.button("🎙️ Transcribe Audio", use_container_width=True):

    if audio_file is None:
        st.warning("Please upload an audio file first.")

    else:
        with st.spinner("Listening and converting speech to text..."):

            stt_result = transcribe_audio(
                audio_file.getvalue(),
                audio_file.name,
                lang
            )

        if stt_result.ok:

            st.session_state.question_input = stt_result.text

            st.success("Audio successfully transcribed!")

            st.markdown("**Recognized Question:**")
            st.info(stt_result.text)

            st.caption(f"Provider: {stt_result.provider}")

            st.info("Click 'उत्तर पाएँ' above to submit this question.")

        else:
            st.error(stt_result.error)


# --------------------------------------------------
# GENERATE AGRICULTURAL ANSWER
# --------------------------------------------------

if submitted:

    user_question = question.strip()

    if not user_question:
        st.warning("Please enter a farming question.")

    else:

        with st.spinner("🌱 Finding the best available answer..."):

            try:

                result = answer_question(
                    user_question,
                    lang
                )

                st.session_state.messages.append({
                    "role": "user",
                    "content": user_question
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.answer,
                    "source": result.source,
                    "score": result.score,
                    "mode": result.mode,
                    "fallback": result.is_fallback
                })

                st.session_state.latest_answer = result.answer

            except Exception as error:  # noqa: BLE001

                st.error(f"Unable to generate answer: {error}")


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

st.markdown("---")

st.markdown(
    '<div class="section-title">💬 Conversation</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.info("Your conversation will appear here. Ask your first farming question!")

else:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

            if message["role"] == "assistant":

                st.caption(
                    f"Source: {message['source']} | "
                    f"Match score: {message['score']:.2f} | "
                    f"Mode: {message['mode']}"
                )

                if message["fallback"]:
                    st.warning(
                        "This is a fallback response. "
                        "Please consult a local agricultural expert."
                    )


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

if st.session_state.latest_answer:

    st.markdown("---")

    st.markdown("### 🔊 Listen to AI Response")

    if st.button(
        copy["speak"],
        use_container_width=True
    ):

        with st.spinner("Generating speech..."):

            tts_result = synthesize_speech(
                st.session_state.latest_answer,
                lang
            )

        if tts_result.ok:

            st.success("Audio generated successfully!")

            st.audio(
                tts_result.audio_bytes,
                format=tts_result.mime_type
            )

            st.caption(f"TTS Provider: {tts_result.provider}")

        else:
            st.error(tts_result.error)


# --------------------------------------------------
# PROJECT STATUS
# --------------------------------------------------

with st.expander("⚙️ Project Status & Configuration"):

    st.markdown("### Gnani AI Integration")

    col1, col2 = st.columns(2)

    with col1:

        if settings.gnani_stt_url and settings.gnani_api_key:
            st.success("STT Configuration Available")
        else:
            st.warning("STT Configuration Incomplete")

    with col2:

        if GNANI_TTS_URL and GNANI_API_KEY:
            st.success("TTS Configuration Available")
        else:
            st.warning("TTS Configuration Incomplete")

    st.markdown("### Language Configuration")

    st.write({
        "Hindi STT": settings.hindi_stt_language,
        "Bengali STT": settings.bengali_stt_language,
        "Hindi TTS": settings.hindi_tts_language,
        "Bengali TTS": settings.bengali_tts_language,
    })

    st.caption(
        "Verify API endpoints, authentication, language codes "
        "and response formats using your official Gnani AI documentation."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    <h3>🌾 KisanVoice</h3>
    <p>Empowering Farmers Through Artificial Intelligence</p>
    <p>Built with Python · Streamlit · Gnani AI</p>
    <p>Made with ❤️ for Indian Farmers</p>
</div>
""", unsafe_allow_html=True)
