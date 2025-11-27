import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os
from core.get_txt_info import get_txt_info, docx_to_text, pdf_to_text, excel_to_text
from core.neero import chat
from core.askings import ask_from_txt
from core.settings_manager import save_settings, load_proxy_settings, load_openai_key, update_openai_key, update_proxy_url, delete_proxy, delete_openai_key, delete_all_settings
from core.logo import gradient_logo

class SocialEngineeringApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title("Проверка на социальную инженерию")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Загрузка настроек
        self.u_proxy = load_proxy_settings()
        self.u_key = load_openai_key()
        
        # Настройка темы
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        self.check_initial_settings()
        
    def setup_ui(self):
        # Создание основной структуры
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Левая панель навигации
        self.create_navigation_frame()
        
        # Основная область контента
        self.create_main_content_area()
        
    def create_navigation_frame(self):
        # Фрейм навигации
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(8, weight=1)
        
        # Логотип и заголовок
        self.logo_label = ctk.CTkLabel(
            self.navigation_frame, 
            text="Security AI", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Кнопки навигации
        nav_buttons = [
            ("📄 Текст файл", self.show_file_check_frame),
            ("📊 PDF файл", lambda: self.show_file_check_frame("pdf")),
            ("📝 DOCX файл", lambda: self.show_file_check_frame("docx")),
            ("📈 EXCEL файл", lambda: self.show_file_check_frame("excel")),
            ("🤖 Чат с AI", self.show_chat_frame),
            ("⚙️ Настройки", self.show_settings_frame),
            ("ℹ️ Статус", self.show_status_frame)
        ]
        
        for i, (text, command) in enumerate(nav_buttons, 1):
            btn = ctk.CTkButton(
                self.navigation_frame,
                corner_radius=0,
                height=40,
                border_spacing=10,
                text=text,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=command
            )
            btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
        
        # Кнопка выхода
        self.exit_button = ctk.CTkButton(
            self.navigation_frame,
            text="🚪 Выход",
            command=self.quit_app,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        )
        self.exit_button.grid(row=9, column=0, padx=20, pady=20, sticky="s")
    
    def create_main_content_area(self):
        # Основной фрейм контента
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Добро пожаловать",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Область контента
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Начальный экран
        self.show_welcome_screen()
    
    def show_welcome_screen(self):
        self.clear_content_frame()
        
        welcome_text = """
        🔒 Security AI - Анализ файлов на социальную инженерию
        
        Возможности приложения:
        • Проверка текстовых файлов на фишинг и манипуляции
        • Анализ PDF документов
        • Проверка DOCX файлов
        • Анализ Excel таблиц
        • Чат с AI-ассистентом
        • Гибкие настройки прокси и API
        
        Выберите раздел в левом меню для начала работы.
        """
        
        text_widget = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=ctk.CTkFont(size=14)
        )
        text_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        text_widget.insert("1.0", welcome_text)
        text_widget.configure(state="disabled")
    
    def show_file_check_frame(self, file_type="txt"):
        self.clear_content_frame()
        
        self.title_label.configure(text=f"Проверка {file_type.upper()} файла")
        
        # Выбор файла
        file_frame = ctk.CTkFrame(self.content_frame)
        file_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(file_frame, text="Выберите файл:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.file_path_var = ctk.StringVar()
        file_entry = ctk.CTkEntry(file_frame, textvariable=self.file_path_var, state="readonly")
        file_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        browse_btn = ctk.CTkButton(
            file_frame,
            text="Обзор",
            command=lambda: self.browse_file(file_type)
        )
        browse_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Кнопка проверки
        check_btn = ctk.CTkButton(
            self.content_frame,
            text="🔍 Начать проверку",
            command=lambda: self.check_file(file_type),
            font=ctk.CTkFont(weight="bold"),
            height=40
        )
        check_btn.grid(row=1, column=0, padx=20, pady=10)
        
        # Область результатов
        self.result_text = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=ctk.CTkFont(size=12)
        )
        self.result_text.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(2, weight=1)
        
        self.current_file_type = file_type
    
    def browse_file(self, file_type):
        file_types = {
            "txt": [("Text files", "*.txt")],
            "pdf": [("PDF files", "*.pdf")],
            "docx": [("Word documents", "*.docx")],
            "excel": [("Excel files", "*.xlsx *.xls")]
        }
        
        filename = filedialog.askopenfilename(filetypes=file_types.get(file_type, [("All files", "*.*")]))
        if filename:
            self.file_path_var.set(filename)
    
    def check_file(self, file_type):
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Ошибка", "Файл не выбран или не существует")
            return
        
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "⏳ Проверка файла...\n")
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self._check_file_thread, args=(file_type, file_path))
        thread.daemon = True
        thread.start()
    
    def _check_file_thread(self, file_type, file_path):
        try:
            # Чтение файла в зависимости от типа
            if file_type == "txt":
                content = get_txt_info(file_path)
            elif file_type == "pdf":
                content = pdf_to_text(file_path)
            elif file_type == "docx":
                content = docx_to_text(file_path)
            elif file_type == "excel":
                content = excel_to_text(file_path)
            else:
                content = ""
            
            # Проверка на социальную инженерию
            result = ask_from_txt(content, proxy_url=self.u_proxy, api_key=self.u_key)
            
            # Обновление UI в основном потоке
            self.after(0, self._update_result, result)
            
        except Exception as e:
            self.after(0, self._show_error, f"Ошибка при проверке файла: {str(e)}")
    
    def _update_result(self, result):
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)
    
    def _show_error(self, error_msg):
        messagebox.showerror("Ошибка", error_msg)
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"❌ {error_msg}")
    
    def show_chat_frame(self):
        self.clear_content_frame()
        self.title_label.configure(text="Чат с AI")
        
        # Область чата
        self.chat_text = scrolledtext.ScrolledText(
            self.content_frame,
            wrap="word",
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white"
        )
        self.chat_text.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 5))
        self.chat_text.configure(state="disabled")
        
        # Фрейм ввода
        input_frame = ctk.CTkFrame(self.content_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Введите ваше сообщение..."
        )
        self.chat_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.chat_entry.bind("<Return>", lambda e: self.send_chat_message())
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Отправить",
            command=self.send_chat_message
        )
        send_btn.grid(row=0, column=1, padx=10, pady=10)
        
        clear_btn = ctk.CTkButton(
            input_frame,
            text="Очистить чат",
            command=self.clear_chat,
            fg_color="transparent",
            border_width=2
        )
        clear_btn.grid(row=0, column=2, padx=10, pady=10)
        
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def send_chat_message(self):
        message = self.chat_entry.get().strip()
        if not message:
            return
        
        # Добавление сообщения пользователя
        self._add_chat_message("Вы", message)
        self.chat_entry.delete(0, "end")
        
        # Запуск AI в отдельном потоке
        thread = threading.Thread(target=self._chat_ai_thread, args=(message,))
        thread.daemon = True
        thread.start()
    
    def _chat_ai_thread(self, message):
        try:
            response = chat(prompt=message, proxy_url=self.u_proxy, api_key=self.u_key)
            self.after(0, self._add_chat_message, "AI", response)
        except Exception as e:
            self.after(0, self._add_chat_message, "Система", f"Ошибка: {str(e)}")
    
    def _add_chat_message(self, sender, message):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"\n{sender}: {message}\n")
        self.chat_text.configure(state="disabled")
        self.chat_text.see("end")
    
    def clear_chat(self):
        self.chat_text.configure(state="normal")
        self.chat_text.delete("1.0", "end")
        self.chat_text.configure(state="disabled")
    
    def show_settings_frame(self):
        self.clear_content_frame()
        self.title_label.configure(text="Настройки")
        
        # Настройки прокси
        proxy_frame = ctk.CTkFrame(self.content_frame)
        proxy_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        proxy_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(proxy_frame, text="HTTPS Прокси:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.proxy_entry = ctk.CTkEntry(
            proxy_frame,
            placeholder_text="http://123.313.12:4322"
        )
        self.proxy_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        if self.u_proxy:
            self.proxy_entry.insert(0, self.u_proxy)
        
        proxy_buttons_frame = ctk.CTkFrame(proxy_frame, fg_color="transparent")
        proxy_buttons_frame.grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(
            proxy_buttons_frame,
            text="Сохранить",
            command=self.save_proxy,
            width=80
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            proxy_buttons_frame,
            text="Очистить",
            command=self.clear_proxy,
            width=80,
            fg_color="transparent",
            border_width=2
        ).grid(row=0, column=1, padx=5)
        
        # Настройки API ключа
        api_frame = ctk.CTkFrame(self.content_frame)
        api_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        api_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(api_frame, text="OpenAI API Key:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        
        self.api_entry = ctk.CTkEntry(
            api_frame,
            placeholder_text="sk-...your-api-key...",
            show="*"
        )
        self.api_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        if self.u_key:
            self.api_entry.insert(0, self.u_key)
        
        api_buttons_frame = ctk.CTkFrame(api_frame, fg_color="transparent")
        api_buttons_frame.grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(
            api_buttons_frame,
            text="Сохранить",
            command=self.save_api_key,
            width=80
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            api_buttons_frame,
            text="Очистить",
            command=self.clear_api_key,
            width=80,
            fg_color="transparent",
            border_width=2
        ).grid(row=0, column=1, padx=5)
        
        # Кнопки управления
        control_frame = ctk.CTkFrame(self.content_frame)
        control_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        
        ctk.CTkButton(
            control_frame,
            text="Сбросить все настройки",
            command=self.reset_all_settings,
            fg_color="red",
            hover_color="darkred"
        ).grid(row=0, column=0, padx=20, pady=10)
        
        ctk.CTkButton(
            control_frame,
            text="Показать текущие настройки",
            command=self.show_current_settings
        ).grid(row=0, column=1, padx=20, pady=10)
    
    def save_proxy(self):
        proxy = self.proxy_entry.get().strip()
        if proxy and update_proxy_url(proxy):
            self.u_proxy = proxy
            messagebox.showinfo("Успех", "Прокси успешно сохранен")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить прокси")
    
    def clear_proxy(self):
        self.proxy_entry.delete(0, "end")
        delete_proxy()
        self.u_proxy = None
        messagebox.showinfo("Успех", "Прокси очищен")
    
    def save_api_key(self):
        api_key = self.api_entry.get().strip()
        if api_key and update_openai_key(api_key):
            self.u_key = api_key
            messagebox.showinfo("Успех", "API ключ успешно сохранен")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить API ключ")
    
    def clear_api_key(self):
        self.api_entry.delete(0, "end")
        delete_openai_key()
        self.u_key = None
        messagebox.showinfo("Успех", "API ключ очищен")
    
    def reset_all_settings(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите сбросить все настройки?"):
            delete_all_settings()
            self.u_proxy = None
            self.u_key = None
            self.proxy_entry.delete(0, "end")
            self.api_entry.delete(0, "end")
            messagebox.showinfo("Успех", "Все настройки сброшены")
    
    def show_current_settings(self):
        settings_info = f"""
Текущие настройки:

Прокси: {self.u_proxy or "Не установлен"}
API ключ: {'Установлен' if self.u_key else 'Не установлен'}

Статус: {'✅ Готов к работе' if self.u_key else '❌ Требуется настройка API ключа'}
        """
        messagebox.showinfo("Текущие настройки", settings_info.strip())
    
    def show_status_frame(self):
        self.clear_content_frame()
        self.title_label.configure(text="Статус системы")
        
        status_text = f"""
🔍 Статус проверки системы:

📡 Прокси: {self.u_proxy or "❌ Не установлен"}
🔑 API ключ: {'✅ Установлен' if self.u_key else '❌ Не установлен'}

💡 Рекомендации:
{'✅ Система готова к работе' if self.u_key else '❌ Установите API ключ для работы'}
{'✅ Прокси настроен' if self.u_proxy else '💡 Прокси не обязателен, но рекомендуется'}

🛡️ Безопасность:
• Все проверки выполняются локально
• API ключ хранится в защищенном хранилище
• Прокси обеспечивает дополнительную анонимность
        """
        
        text_widget = ctk.CTkTextbox(
            self.content_frame,
            wrap="word",
            font=ctk.CTkFont(size=14)
        )
        text_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        text_widget.insert("1.0", status_text.strip())
        text_widget.configure(state="disabled")
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def check_initial_settings(self):
        if not self.u_key:
            messagebox.showwarning(
                "Внимание", 
                "API ключ не установлен. Для работы приложения перейдите в настройки и укажите ваш OpenAI API ключ."
            )
    
    def quit_app(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.destroy()

def main():
    try:
        app = SocialEngineeringApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Ошибка запуска", f"Не удалось запустить приложение: {str(e)}")

if __name__ == "__main__":
    main()