from flask import Flask, render_template, request, send_file
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
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

def texr_speech(text,lang):
    """Synthesizes speech from the input string of text or ssml.
    Make sure to be working in a virtual environment.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=lang, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    #The response's audio_content is binary.
    with open("static/output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    return render_template('audio.html', audio_path='static/output.mp3')

@app.route('/tr/<word>/static/output.mp3')
def send_audio(word):
    print(word)
    return send_file('static/output.mp3', mimetype='audio/mpeg')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tr/<text>/<lang>')
def perevod(text, lang):
    tr_text = translate_text(lang, text)
    return texr_speech(tr_text, lang)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
