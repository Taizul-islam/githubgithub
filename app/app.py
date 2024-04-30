from fastapi import FastAPI, File, UploadFile
import easyocr
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def root(uploaded_file: UploadFile = File(...)):
    file_location = f"file/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    h = []
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_location)

    for (bbox, text, prob) in result:
        h.append(text)
        print(f'Text: {text}, Probability: {prob} {bbox}')

    os.remove(file_location)

    return {"result": h}


def get_app():
    return app
