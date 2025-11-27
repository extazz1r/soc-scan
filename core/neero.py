from openai import OpenAI
import httpx
import os

os.system("clear")

def gpt(prompt, proxy_url, api_key):
    client = OpenAI(api_key=api_key) if proxy_url is None or proxy_url == "" else OpenAI(http_client=httpx.Client(proxy=proxy_url), api_key=api_key)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=f"Ты выводишь ответы в консоль, выводи не .md. Запрос пользователя: {prompt}"
    )

    return response.output_text

def chat(prompt, proxy_url, api_key):
    try:
        response = gpt(prompt=prompt, proxy_url=proxy_url, api_key=api_key)
        print("\n" + "=" * 25)
        print(response)
        print("=" * 25 + "\n")
    except KeyboardInterrupt:
        print("\n\n👋 До свидания!")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}\n")