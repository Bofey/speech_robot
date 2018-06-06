# -*-utf-8-*-
#author:Bowen
#dev version: V1.0
import requests,json
from bs4 import BeautifulSoup as bs
import re,keyboard,os  
import wave,pyaudio 
import pylab as pl 
from pyaudio import PyAudio,paInt16
from aip import AipSpeech

framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2

def save_wave_file(filename,data):

    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():

    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    while not (keyboard.is_pressed('s')):
        None
    print('Recording:...')
    while keyboard.is_pressed('s'): #count<TIME*10:    #控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        #count+=1
        #print('.')
    save_wave_file('01.wav',my_buf)
    stream.close()
    #print('recording is over!')

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def speech_recognition(): #baidu cloud speech recognition
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    audio_res = client.asr(get_file_content('01.wav'),'wav', 16000, {'dev_pid': '1536',})

    if audio_res['err_msg'] == 'success.':
        _text = (audio_res['result'][0])
        print('S: '+_text)
    else:
        _text = '0'
        print(audio_res)

    url = 'http://openapi.tuling123.com/openapi/api/v2' #tuling api
    user={"apiKey": " ","userId": " "}
    param = {"inputText":{"text": _text},}
    x_header = {"reqType": 0,
                "perception": param,
                "userInfo": user}

    r = requests.post(url,json= x_header) #post请求

    try:
        codeloc = r.text.find('code')
        if r.text[codeloc+6] == '1':
            res = re.findall(r'[^\x00-\xff]',r.text)
            w=''
            for i in res:
                w+=i
        else:
            print(r.text[codeloc+6:codeloc+6+4])
            w='0'
    except:
        w='0'
        return 0

    print('R: '+w)
    speech_res = client.synthesis(w, 'zh', 1, {'vol': 5,'spd':5,'pit':5,'vol':10,'per':3,})
    if not isinstance(speech_res, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(speech_res)
    os.system('auido.mp3')

if __name__ == '__main__':
    print('press "s" to speak!')
    while True:
        my_record()
        speech_recognition()
