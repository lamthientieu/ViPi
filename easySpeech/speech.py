# import required libraries
import sounddevice as sd
from .recognize import *
from .record import *
from .ml import *
import requests, time, random
session = requests.Session()
session.get('https://zalo.ai/experiments/automation-speech-recognition')
session_cookies = session.cookies
cookies_dictionary = session_cookies.get_dict()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62', 'origin': 'https://zalo.ai', 'referer': 'https://zalo.ai/experiments/automation-speech-recognition', 'apikey':'gpGSJHG7qNRnGpL6nnkI6N3RFbr9ikrB'}
from knowledge_base import proxies


def speech(using,freq = 44100,duration = 3,key=None, language="vi-VN", show_all=False):
    # Start recorder with the given values of 
    # duration and sample frequency
    recording = sd.rec(int(duration * freq), 
                    samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    sd.wait()
    write("recording.wav", recording, freq, sampwidth=2)
    if using.lower()=='google':
        tic = time.perf_counter()
        r = Recognizer()
        recording = AudioFile('recording.wav')
        with recording as source:
            audio = r.record(source)
        text=r.recognize_google(audio,key, language, show_all)
        toc = time.perf_counter()
        print("Google: " + text)
        print(f"Google free take {toc - tic:0.4f} seconds")      

    elif using.lower()=='ml':
        text=ml('recording.wav')
    elif using.lower() == 'zstt':
        tic = time.perf_counter()
        url = 'https://zalo.ai/api/demo/v1/asr'
        files = {'file': open('recording.wav','rb')}
        proxy = random.choice(proxies)
        print (proxy)
        phttp = "http://" + proxy        
#        resp = requests.post(url, files = files, headers=headers,cookies=cookies_dictionary).json()
#        text = resp['result']['text']
        try:
            resp = requests.post(url, files = files, headers=headers,cookies=cookies_dictionary, proxies={'http': phttp}).json()
            text = resp['result']['text']
        except:
            text = ''
        toc = time.perf_counter()
        print("Zalo: " + text)
        print(f"Zalo take {toc - tic:0.4f} seconds")                
    else:
        text='engine not found'
    return text

def google_audio(file,key=None, language="en-US", show_all=False):
    r = Recognizer()
    recording = AudioFile(file)
    with recording as source:
        audio = r.record(source)
    text=r.recognize_google(audio,key, language, show_all)
    return text

def recorder(name,duration = 5,freq = 44100):  
    recording = sd.rec(int(duration * freq),samplerate=freq, channels=2)
    sd.wait()
    write(name, recording, freq, sampwidth=2)