import docx2txt
from PyPDF2 import PdfReader

def extract_text_from_resume(resume_file):
    if resume_file.name.endswith('.pdf'):
        reader = PdfReader(resume_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    elif resume_file.name.endswith('.docx'):
        return docx2txt.process(resume_file)
    else:
        return ""
