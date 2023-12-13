from flask import Flask, render_template, request
from google.cloud import translate_v2 as translate
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bcnpy2key.json'
app = Flask(__name__)

def translate_text(target: str, text: str) -> dict:

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    # print("Text: {}".format(result["input"]))
    # print("Translation: {}".format(result["translatedText"]))
    # print("Detected source language: {}".format(result["detectedSourceLanguage"]))
    return result["translatedText"]
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tr/<text>/<lang>')
def perevod(text, lang):
    return  translate_text(lang, text)


if __name__ == '__main__':
    app.run(debug=True)