import docx
import PyPDF2
import pandas as pd

def get_txt_info(file):
    try:
        with open(file, "r", encoding="utf-8") as fl:
            text = fl.readlines()
            text = str(text)
            text.split()
            return text
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
    
import docx

def docx_to_text(path):
    try:
        doc = docx.Document(path)
        text = []
        
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  
                text.append(paragraph.text)
        
        return '\n'.join(text)
    
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None
    
def pdf_to_text(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
    
    except Exception as e:
        print(f"Ошибка при чтении PDF: {e}")
        return None

def excel_to_text(path):
    try:
        text_parts = []
        
        excel_file = pd.ExcelFile(path)
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet_name)
            
            if df.empty:
                continue
                
            text_parts.append(f"=== Лист: {sheet_name} ===")
            
            for index, row in df.iterrows():
                row_text = []
                for col_name, cell_value in row.items():
                    if pd.notna(cell_value) and str(cell_value).strip():
                        row_text.append(f"{col_name}: {cell_value}")
                
                if row_text:
                    text_parts.append(f"Строка {index + 1}: " + " | ".join(row_text))
            
            text_parts.append("")
        
        return '\n'.join(text_parts).strip()
    
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return None