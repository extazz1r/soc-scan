import json
import os

SETTINGS_FILE = "settings.json"

def save_settings(proxy_url=None, openai_key=None):
    """
    Сохраняет настройки в файл
    Args:
        proxy_url: URL прокси сервера
        openai_key: API ключ OpenAI
    """
    try:
        # Загружаем существующие настройки если файл есть
        existing_settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                existing_settings = json.load(f)
        
        # Обновляем только переданные значения
        if proxy_url is not None:
            existing_settings['proxy_url'] = proxy_url
        if openai_key is not None:
            existing_settings['openai_key'] = openai_key
        
        # Добавляем время сохранения
        existing_settings['saved_at'] = str(os.path.getctime(__file__))
        
        # Сохраняем обратно
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(existing_settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения настроек: {e}")
        return False

def load_proxy_settings():
    """Загружает прокси из файла"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get('proxy_url', None)
        return None
    except Exception as e:
        print(f"Ошибка загрузки прокси: {e}")
        return None

def load_openai_key():
    """Загружает API ключ OpenAI из файла"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get('openai_key', None)
        return None
    except Exception as e:
        print(f"Ошибка загрузки API ключа: {e}")
        return None

def load_all_settings():
    """Загружает все настройки из файла"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Ошибка загрузки настроек: {e}")
        return {}

def delete_proxy():
    """Удаляет только прокси из настроек"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Удаляем только прокси
            if 'proxy_url' in settings:
                del settings['proxy_url']
            
            # Сохраняем обновленные настройки
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        return False
    except Exception as e:
        print(f"Ошибка удаления прокси: {e}")
        return False

def delete_openai_key():
    """Удаляет только API ключ из настроек"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Удаляем только API ключ
            if 'openai_key' in settings:
                del settings['openai_key']
            
            # Сохраняем обновленные настройки
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        return False
    except Exception as e:
        print(f"Ошибка удаления API ключа: {e}")
        return False

def delete_all_settings():
    """Удаляет файл с настройками полностью"""
    try:
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
            return True
        return False
    except Exception as e:
        print(f"Ошибка удаления настроек: {e}")
        return False

def update_openai_key(new_key):
    """Обновляет только API ключ OpenAI"""
    return save_settings(openai_key=new_key)

def update_proxy_url(proxy_url):
    """Обновляет только прокси"""
    return save_settings(proxy_url=proxy_url)