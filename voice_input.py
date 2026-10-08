import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr


def listen():

    duration = 4
    samplerate = 30500

    print("Listening...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1
    )

    sd.wait()

    print("Voice captured")


    # Convert float audio to int16 PCM
    recording = np.int16(
        recording * 32767
    )


    filename = "voice.wav"


    wav.write(
        filename,
        samplerate,
        recording
    )


    recognizer = sr.Recognizer()


    with sr.AudioFile(filename) as source:

        audio = recognizer.record(source)


    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)

        return text


    except Exception as e:

        print("Error:", e)

        return None

