from core.get_txt_info import get_txt_info, docx_to_text, pdf_to_text, excel_to_text
from core.neero import chat
from core.askings import ask_from_txt
from core.settings_manager import save_settings, load_proxy_settings, load_openai_key, update_openai_key, update_proxy_url, delete_proxy, delete_openai_key, delete_all_settings
from core.logo import gradient_logo
import os

cls_cmm = "clear"

print("Загрузка программы...")

global u_proxy 
global u_key

u_proxy = load_proxy_settings()
u_key = load_openai_key()

    

def menu():
    gradient_logo()
    print("\n(Так как это бета-версия, при запуске программы из других папок\nмогут возникать ошибки)")
    print("")
    print("Выберите пункт из меню ниже: ")
    print("(1) Проверить текстовый файл на соц. инжинерию.")
    print("(2) Проверить PDF файл на соц. инжинерию.")
    print("(3) Проверить DOCX файл на соц. инжинерию.")
    print("(4) Проверить EXCEL файл на соц. инжинерию.")
    print("(5) Поболтать с нееронкой.")
    print("(6) Настройки.")
    print("(7) Выйти.")

    try:
        user_ans = int(input("Выберите пункт: "))
        return user_ans
    except ValueError:
        print("Неверный пункт меню.")


def menu_proxy():
    global u_proxy
    global u_key
    os.system(cls_cmm)
    print("Меню настройки прокси:")
    print("(1) HTTPS прокси.")
    print("(2) Очистить прокси.")
    print("(3) Выход.")

    try:
        u_ans = int(input("Выберите вариант: "))

        if u_ans == 1:
            print("Введите прокси (пример: http://123.313.12:4322)")
            u_proxy = input("Ввод: ")
            if update_proxy_url(u_proxy):
                print("✔ Прокси сохранен")
            
        elif u_ans == 2:
            u_proxy = None
            delete_proxy()
            print("✔ Прокси очищен")


        elif u_ans == 3:
            os.system(cls_cmm)
            exit
            
        else:
            print("✖ Неверный вариант")
            
    except ValueError:
        menu_proxy()

def menu_openai():
    global u_proxy
    global u_key
    os.system(cls_cmm)
    print("Меню настройки OpenAI:")
    print("(1) Изменить API KEY.")
    print("(2) Удалить API KEY.")
    print("(3) Выход.")

    try:
        u_ans = int(input("Выберите вариант: "))

        if u_ans == 1:
            print("Введите API KEY (пример: sk-...your-api-key...")
            u_key = input("Ввод: ")
            if update_openai_key(u_key):
                print("✓ API KEY сохранен")
            
        elif u_ans == 2:
            u_key = None
            delete_openai_key()
            print("✓ API KEY очищен")

        elif u_ans == 3:
            os.system(cls_cmm)
            exit
            
        else:
            print("✖ Неверный вариант")
            
    except ValueError:
        menu_openai()


def check_settings():
    global u_proxy
    global u_key
    if u_proxy is None or u_proxy == "":
        print("✖ Запуск без прокси (вы не указали)")
    else:
        print(f"✓ Запуск с прокси: {u_proxy}")

    if u_key is None or u_key == "":
        print("📛 Запуск без API KEY (вы не указали) БУДУТ ОШИБКИ 📛")
    else:
        print(f"✓ API KEY установлен.")


def main():
    global u_proxy
    global u_key

    u_proxy = load_proxy_settings()
    
    os.system(cls_cmm)

    while True:
        ans = menu()
        try:
            if ans == 1:
                os.system(cls_cmm)
                check_settings()
                
                print("Начата проверка файла...")
                print(ask_from_txt(get_txt_info('basic.txt'), proxy_url=u_proxy, api_key=u_key))
                print("Файл успешно проверен на Соц. Инженирию!\n")

            elif ans == 2:
                try:
                    os.system(cls_cmm)
                    check_settings()
                    
                    print("Начинаем проверку файла...")
                    print(ask_from_txt(pdf_to_text('Document 1.pdf'), proxy_url=u_proxy, api_key=u_key))
                    print("\n")
                except NotADirectoryError:
                    print("[ERROR] Файла нету в папке.")

            elif ans == 3:
                os.system(cls_cmm)
                check_settings()
                
                print("Начинаем проверку файла на социальную инженирию...")
                print(f"\n{ask_from_txt(docx_to_text("123.docx"), proxy_url=u_proxy, api_key=u_key)}\n")
                print("✓ Проверка файла завершена.")

            elif ans == 4:
                os.system(cls_cmm)

                check_settings()

                print("Начинаем проверку файла на социальную инженирию...")
                print(f"\n{ask_from_txt(excel_to_text('123.xlsx'), proxy_url=u_proxy, api_key=u_key)}\n")
                print("✓ Проверка файла завершена.")

            elif ans == 5:
                os.system(cls_cmm)
                
                check_settings()                    
                
                print("Что бы выйти, напишите (exit)")
                while True:
                    prompt = input("💬 Введите запрос: ")
                    if prompt == "exit":
                        break
                    chat(prompt=prompt, proxy_url=u_proxy, api_key=u_key)
                os.system(cls_cmm)

            elif ans == 6:
                os.system(cls_cmm)
                print("Меню настроек:")
                print("(1) Настроить прокси.")
                print("(2) Настроить OpenAI.")
                print("(3) Сброс настроек.")
                print("(4) [DEBUG] выод json.")

                try:
                    menu_ans = int(input("Выберите вариант: "))

                    if menu_ans == 1:
                        menu_proxy()
                    if menu_ans == 2:
                        menu_openai()
                    if menu_ans == 3:
                        yh = input("Вы уверены? Да - y Нет - n: ")
                        if yh == "y":
                            delete_all_settings()
                            u_proxy = None
                            u_key = None
                            print("Все настройки успешно удалены.")
                        elif yh == "n":
                            print("aborted.")
                    if menu_ans == 4:
                        os.system(cls_cmm)
                        print(f"proxy: {u_proxy}\nkey: {u_key}\n")

                except ValueError:
                    print("Введите число.")

            elif ans == 7:
                break

        except Exception as e:
            print(f"Возникла ошибка: {e}")

    print("Досвидания.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена!")