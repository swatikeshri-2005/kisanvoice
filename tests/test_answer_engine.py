from backend.answer_engine import answer_question  # noqa: I001

def test_hindi_known_question_returns_answer():
    result = answer_question("धान की पत्तियाँ पीली क्यों हो रही हैं?", "hi")
    assert result.answer
    assert not result.is_fallback

def test_bengali_known_question_returns_answer():
    result = answer_question("ধানের পাতা হলুদ হয়ে যাচ্ছে কেন?", "bn")
    assert result.answer
    assert not result.is_fallback

def test_unknown_question_uses_safe_fallback():
    result = answer_question("मंगल ग्रह पर खेती कैसे करें?", "hi")
    assert result.is_fallback
    assert "कृषि" in result.answer
