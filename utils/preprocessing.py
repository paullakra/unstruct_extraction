import re
import docx as python_docx
import fitz


def preprocess_string(text: str):
    text = text.lower()
    text = re.sub('\r', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub(r"[^a-zA-Z0-9. ]", "", text)
    text = re.sub(' +', ' ', text)
    text.strip()
    return text


def doc(path):
    text = python_docx.Document(path)
    data = ""
    full_text = []
    for para in text.paragraphs:
        full_text.append(para.text)
        data = '\n'.join(full_text)

    return data


def txt(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def pdf(path):
    fitz_doc = fitz.open(path)  # open document
    data = ""

    for page in fitz_doc:
        data = data + " " + page.get_text("text")

    return data


docx = doc
