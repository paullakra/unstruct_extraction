import os
import shutil
from urllib.request import Request, urlopen

import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, PlainTextResponse

from utils import preprocessing_manager, summarise_long_text, get_entities, get_email_address, get_phone_number

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Welcome to the main module!"


@app.post("/file")
async def file_input(file: UploadFile = File(...), summary_mode: str = "separative"):
    try:
        # Save a local copy of file
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = str(os.getcwd()) + "\\" + file.filename
        file_path = file_path.replace("\\", "/")

        # Send path of local copy to preprocessing module to get content
        text = preprocessing_manager(file_path)
        # Send text to model module for results
        summary = summarise_long_text(text, mode=summary_mode)
        phones = get_phone_number(text)
        emails = get_email_address(text)
        entities = get_entities(text)
        # Save response to send as api response
        response = JSONResponse(status_code=202, content=dict(
            Summary=summary, Phone=phones, Email=emails, Entites=entities))
        # Remove local copy of file
        os.remove(file_path)

    except RuntimeError as e:
        response = JSONResponse(status_code=400, content=dict(message=e))

    return response


@app.post("/url")
async def url_input(url: str):
    try:
        # Parse URL and save a local copy of it as text file
        req = Request(url)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "html.parser")
        html_text = soup.get_text()
        file_path = str(os.getcwd()) + "\\" + "html_text.txt"
        file_path = file_path.replace("\\", "/")
        f = open(file_path, "w", encoding='utf-8')  # Creating html_text.txt File
        for line in html_text:
            f.write(line)
        f.close()

        # Send path of local copy to preprocessing module to get content
        text = preprocessing_manager(file_path)
        # Send text to model module for results
        summary = summarise_long_text(text)
        phones = get_phone_number(text)
        emails = get_email_address(text)
        entities = get_entities(text)
        # Save response to send as api response
        response = JSONResponse(status_code=202, content=dict(
            Summary=summary, Phone=phones, Email=emails, Entites=entities))
        os.remove(file_path)

    except RuntimeError as e:
        response = JSONResponse(status_code=400, content=dict(message=e))

    return response


if __name__ == "__main__":
    # Run uvicorn server from inside docker
    uvicorn.run(app, host="localhost", port=8000)
