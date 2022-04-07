import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, PlainTextResponse
import os
import shutil
from urllib.request import Request, urlopen
import uvicorn
from bs4 import BeautifulSoup


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Welcome to the main module!"


@app.post("/file")
async def file_input(file: UploadFile = File(...)):
    try:
        # Save a local copy of file
        with open(f'{file.filename}', 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = str(os.getcwd()) + "\\" + file.filename
        file_path = file_path.replace("\\", "/")

        # Send path of local copy to preprocessing module to get content
        text = requests.post(url="http://localhost:7000/path", json={"text": file_path}).text
        # Send text to model module for results
        summary = requests.post(url="http://localhost:5000/input", json={"text": text}).text
        # Save response to send as api response
        response = JSONResponse(status_code=202, content=dict(
            Summary=summary))
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

        # Send path of local file to get content
        text = requests.post(url="http://127.0.0.1:7000/path", json={"text": file_path}).text
        # Send text to model api to get result
        summary = requests.post(url="http://127.0.0.1:5000/input", json={"text": text}).text
        response = JSONResponse(status_code=202, content=dict(
            Summary=summary))
        os.remove(file_path)

    except RuntimeError as e:
        response = JSONResponse(status_code=400, content=dict(message=e))

    return response


if __name__ == "__main__":
    # Run uvicorn server from inside docker
    uvicorn.run(app, host="localhost", port=8000)
