from core.neero import gpt

def ask_from_txt(t, proxy_url, api_key):
    if not t or not t.strip():
        return "Ошибка: Передан пустой текст для анализа."
    
    prompt = f"""
    Проанализируй следующий текст файла и предоставь информацию:
    
    {t}
    
    Проанализируй:
    1. Тип содержимого
    2. Возможные угрозы безопасности
    3. Подозрительные паттерны
    4. Рекомендации по безопасности
    5. Дай итоговый вердикт пользователю, открывать файл или нет.
    
    Будь кратким и конкретным.
    """
    
    try:
        response = gpt(prompt=prompt, proxy_url=proxy_url, api_key=api_key)
        return response
    except Exception as e:
        return f"Ошибка: {e}"