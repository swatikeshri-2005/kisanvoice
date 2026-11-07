from backend.knowledge_base import retrieve
from backend.models import AnswerResult

FALLBACKS = {
    "hi": "मुझे उपलब्ध ज्ञान-संग्रह में इस प्रश्न का सत्यापित उत्तर नहीं मिला। कृपया अपने क्षेत्र के कृषि विज्ञान केंद्र (KVK) या कृषि विभाग से सलाह लें।",
    "bn": "আমাদের উপলব্ধ জ্ঞানভান্ডারে এই প্রশ্নের যাচাইকৃত উত্তর পাওয়া যায়নি। আপনার এলাকার কৃষি বিজ্ঞান কেন্দ্র (KVK) বা কৃষি দপ্তরের পরামর্শ নিন।",
}

def answer_question(question: str, language: str) -> AnswerResult:
    item, score = retrieve(question, language)
    # A deliberately conservative threshold: the FAQ match must share useful terms.
    if item and score >= 0.30:
        return AnswerResult(
            answer=item["answer"],
            source=item.get("source", "Local agriculture FAQ"),
            score=score,
            mode="local_faq_retrieval",
            is_fallback=False,
        )
    return AnswerResult(
        answer=FALLBACKS.get(language, FALLBACKS["hi"]),
        source="Fallback: no sufficiently strong FAQ match",
        score=score,
        mode="safe_fallback",
        is_fallback=True,
    )
