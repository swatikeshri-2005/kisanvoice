import streamlit as st  # noqa: I001
from dotenv import load_dotenv
from backend.answer_engine import answer_question
from backend.speech_to_text import transcribe_audio
from backend.text_to_speech import synthesize_speech
from backend.config import settings

load_dotenv()
st.set_page_config(page_title="KisanVoice", page_icon="🌾", layout="centered")

LANGUAGES = {
    "हिन्दी (Hindi)": "hi",
    "বাংলা (Bengali)": "bn",
}
COPY = {
    "hi": {
        "title": "🌾 किसानवॉइस",
        "subtitle": "किसानों के लिए आवाज़-आधारित कृषि सहायता",
        "question": "अपना कृषि प्रश्न लिखें",
        "placeholder": "उदाहरण: धान की फसल में पत्तियाँ पीली क्यों हो रही हैं?",
        "ask": "उत्तर पाएँ",
        "audio": "या अपनी आवाज़ की रिकॉर्डिंग अपलोड करें",
        "answer": "उत्तर",
        "speak": "उत्तर को आवाज़ में सुनें",
        "no_answer": "इस प्रश्न के लिए हमारे उपलब्ध ज्ञान-संग्रह में सत्यापित उत्तर नहीं मिला। कृपया स्थानीय कृषि विशेषज्ञ या कृषि विज्ञान केंद्र से सलाह लें।",
        "demo": "डेमो मोड चालू है: अभी स्थानीय कृषि FAQ ज्ञान-संग्रह का उपयोग हो रहा है।",
    },
    "bn": {
        "title": "🌾 কৃষকভয়েস",
        "subtitle": "কৃষকদের জন্য কণ্ঠভিত্তিক কৃষি সহায়তা",
        "question": "আপনার কৃষি-সংক্রান্ত প্রশ্ন লিখুন",
        "placeholder": "উদাহরণ: ধানের পাতাগুলি হলুদ হয়ে যাচ্ছে কেন?",
        "ask": "উত্তর দেখুন",
        "audio": "অথবা আপনার কণ্ঠের রেকর্ডিং আপলোড করুন",
        "answer": "উত্তর",
        "speak": "উত্তরটি অডিওতে শুনুন",
        "no_answer": "আমাদের উপলব্ধ জ্ঞানভান্ডারে এই প্রশ্নের যাচাইকৃত উত্তর পাওয়া যায়নি। স্থানীয় কৃষি বিশেষজ্ঞ বা কৃষি বিজ্ঞান কেন্দ্রের পরামর্শ নিন।",
        "demo": "ডেমো মোড চালু আছে: বর্তমানে স্থানীয় কৃষি FAQ জ্ঞানভান্ডার ব্যবহার করা হচ্ছে।",
    },
}

st.title("🌾 KisanVoice")
st.caption("Hindi-first bilingual agricultural voice assistant | Gnani AI integration scaffold")

language_label = st.selectbox("भाषा / ভাষা", list(LANGUAGES.keys()))
lang = LANGUAGES[language_label]
copy = COPY[lang]

st.header(copy["title"])
st.write(copy["subtitle"])
if not settings.gnani_stt_url or not settings.gnani_tts_url:
    st.info(copy["demo"])

with st.form("question_form"):
    question = st.text_area(copy["question"], placeholder=copy["placeholder"], height=100)
    submitted = st.form_submit_button(copy["ask"], type="primary")

st.divider()
st.subheader(copy["audio"])
audio_file = st.file_uploader("Audio file (WAV/MP3/M4A/OGG)", type=["wav", "mp3", "m4a", "ogg", "webm"])
transcribe_clicked = st.button("🎙️ Transcribe uploaded audio")

if transcribe_clicked:
    if audio_file is None:
        st.warning("Please upload an audio file first.")
    else:
        with st.spinner("Transcribing audio..."):
            result = transcribe_audio(audio_file.getvalue(), audio_file.name, lang)
        if result.ok:
            question = result.text
            st.session_state["transcribed_question"] = question
            st.success(f"Transcription: {result.text}")
            st.caption(f"Provider: {result.provider}")
        else:
            st.error(result.error)

if "transcribed_question" in st.session_state and not submitted:
    question = st.session_state["transcribed_question"]

if submitted or (transcribe_clicked and st.session_state.get("transcribed_question")):
    if not question.strip():
        st.warning("Please enter or transcribe a question.")
    else:
        with st.spinner("Finding a grounded answer..."):
            result = answer_question(question.strip(), lang)
        st.subheader(copy["answer"])
        st.write(result.answer)
        st.caption(f"Source: {result.source} · Match score: {result.score:.2f} · Mode: {result.mode}")
        if result.is_fallback:
            st.warning("This is a fallback response. Do not use it as a substitute for local agricultural advice.")
        if st.button(copy["speak"]):
            with st.spinner("Generating audio..."):
                audio_result = synthesize_speech(result.answer, lang)
            if audio_result.ok:
                st.audio(audio_result.audio_bytes, format=audio_result.mime_type)
                st.caption(f"TTS provider: {audio_result.provider}")
            else:
                st.error(audio_result.error)

with st.expander("Project status / configuration"):
    st.write({
        "STT configured": bool(settings.gnani_stt_url),
        "TTS configured": bool(settings.gnani_tts_url),
        "STT language codes": {"Hindi": settings.hindi_stt_language, "Bengali": settings.bengali_stt_language},
        "TTS language codes": {"Hindi": settings.hindi_tts_language, "Bengali": settings.bengali_tts_language},
    })
    st.caption("Use the exact endpoint, headers, request fields, and response parsing specified in your Gnani AI account documentation.")
