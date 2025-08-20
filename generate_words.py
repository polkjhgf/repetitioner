import requests
import json
import re
import time

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
    prompt = f"""Сравни два списка и выведи только число — количество точных совпадений (с учётом порядка и формы слов). Ничего не добавляй.
            Оригинал: {original_words}
            Пользователь: {my_words}
            Число:"""
    return int(query_ollama(prompt=prompt))

