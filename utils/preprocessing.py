import re
import docx as python_docx
import fitz

from bs4 import BeautifulSoup


def preprocess_string(text: str):
    text = BeautifulSoup(text, "html.parser").text
    # text = text.lower()
    text = re.sub('\r', ' ', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('-', '', text)
    text = re.sub(r"[^a-zA-Z0-9.,()+@$ ]", " ", text)
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


if __name__ == "__main__":
    Source = ("boyuv yuov 9940-546-789</p>"
              "        <p><strong>Mutiara Damansara:</strong> 98-546-86-984</p>"
              "        <p><strong>Penang:</strong> + 60 (0)4 255 9000</p>"
              "        <h2>Where we are </h2>"
              "        <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8686"
              "        </p></div><div class=\"sys_two\">"
              "    <h3 class=\"parentSchool\">General enquiries</h3><p style=\"FONT-SIZE: 11px\">"
              "     <strong>&nbsp;Call us on:</strong>&nbsp;+6 (03) 8924 8000"
              "+ 60 (7) 268-6200 <br /> 99-556-88-987"
              " Fax:<br /> "
              " +60 (7) 228-6202<br /> "
              "Phone:</strong><strong style=\"color: #f00\">+601-4228-8055</strong> 99-556-88-987. "
              "Hi my name is John and email address is john.doe@somecompany.co.uk.fml and my friend's email is "
              "jane_doe124@gmail.com"
              "The legal status of stevia as a food additive or dietary supplement varies from country to country. In "
              "the United States, high-purity stevia glycoside extracts have been generally recognized as safe "
              "since 2008, and are allowed in food products, but stevia leaf and crude extracts do not have "
              "Food and Drug Administration (FDA) $$$ approval for use in food. The European Union approved Stevia "
              "additives in 2011, while in Japan, stevia has been widely used as a sweetener for decades.")
    Source = Source.encode().decode()
    print(preprocess_string(Source))
