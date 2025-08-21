import requests
import json
import re
import time
import unicodedata

qwen = "qwen/qwen3-4b-2507"
gemma = "google/gemma-3-12b"

def query_ollama(prompt: str, model: str = gemma) -> str:
    """ Отправляет запрос к локальной модели Ollama и возвращает ответ """

    url = f"http://localhost:1234/v1/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "temperature": 1.3,
        "max_tokens": 1600,  # Исправлено название параметра
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status() #Вывод ошибки если запрос не правильный
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Ошибка запроса {e}")
        return ""

def generate_words() -> str:
    prompt = """Сгенерируй список из 300 уникальных русских слов, подходящих для тренировки памяти. Слова должны быть:  
        1. Разнообразными (существительные, прилагательные, глаголы).  
        2. Относительно простыми, но не слишком примитивными (например, "яблоко", "радость", "изобретать").  
        3. Без повторений и редких/узкоспециальных терминов.  
        4. В разных тематических категориях: природа, эмоции, профессии, наука, искусство, спорт, быт и т. д.  
        
        Формат: строго одно слово в строке, без номеров и дополнительных символов.  
        
        Пример первых 10 слов:  
        яблоко  
        горизонт  
        благодарность  
        акварель  
        парашют  
        верность  
        эксперимент  
        журчание  
        корабль  
        вдохновение  
        
        Продолжи список до 300 слов."""
    return query_ollama(prompt=prompt)


def check_words(original_words: str, my_words: str) -> int:
    """
    Сравнение без учёта порядка.
    Возвращает количество совпадений (целое).
    Алгоритм: нормализация -> опц. лемматизация -> жадное fuzzy-совпадение.
    """
    import re, unicodedata
    from difflib import SequenceMatcher

    FUZZY_THRESHOLD = 0.80  # порог для fuzzy (0..1)

    def normalize(s: str) -> str:
        s = (s or "").strip()
        s = unicodedata.normalize("NFKC", s)
        s = s.lower()
        s = re.sub(r"[^0-9a-zA-Z\u0400-\u04FF\-\s]+", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    def split_input(s: str):
        if not s:
            return []
        if "\n" in s:
            items = [line.strip() for line in s.splitlines() if line.strip()]
            if items:
                return items
        return [tok for tok in re.split(r"\s+", s.strip()) if tok]

    # лемматизация, если есть
    try:
        import pymorphy2
        _morph = pymorphy2.MorphAnalyzer()
        def lemma(w: str) -> str:
            w = normalize(w)
            return _morph.parse(w)[0].normal_form if w else ""
    except Exception:
        def lemma(w: str) -> str:
            return normalize(w)

    # fuzzy функция (rapidfuzz если есть, иначе SequenceMatcher)
    try:
        from rapidfuzz.fuzz import ratio as rf_ratio
        def fuzzy(a, b):
            return rf_ratio(a, b) / 100.0
    except Exception:
        def fuzzy(a, b):
            return SequenceMatcher(None, a, b).ratio()

    orig_list = split_input(original_words)
    my_list = split_input(my_words)

    # подготовка списков лемм (с учётом пустых значений)
    orig_lem = [lemma(w) for w in orig_list]
    my_lem = [lemma(w) for w in my_list]

    matched = 0
    used = [False] * len(orig_lem)

    # для каждого пользовательского слова ищем лучший ещё не использованный оригинал
    for u in my_lem:
        if not u:
            continue
        best_idx = -1
        best_score = 0.0
        for i, o in enumerate(orig_lem):
            if used[i] or not o:
                continue
            score = 1.0 if o == u else fuzzy(o, u)
            if score > best_score:
                best_score = score
                best_idx = i
        if best_idx >= 0 and best_score >= FUZZY_THRESHOLD:
            used[best_idx] = True
            matched += 1

    # matched не может превышать количество оригинальных слов
    return int(min(matched, len(orig_lem)))
