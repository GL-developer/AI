import os, requests, json, wave, vlc
if __name__ == '__main__':
    from common import *
else:
    from .common import *

url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
headers = {
    "Content-Type": "application/xml",
    "Authorization": "KakaoAK " + getKey(),
}

def getTTS(text):
    data = "<speak>"+text+"</speak>"
    res = requests.post(url, headers=headers, data=data)
    f= open(getWavPath(), 'wb')
    f.write(res.content)
    f.close()
    
if __name__ == '__main__':
    getTTS(latin2utf8("Hello. I've never seen you before"))
    vlc.MediaPlayer("temp.wav").play()
    