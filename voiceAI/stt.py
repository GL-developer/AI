import requests, json
if __name__ == '__main__':
    from common import *
else:
    from .common import *

url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"
key = getKey()
headers = {
    "Content-Type": "application/octet-stream",
    "Authorization": "KakaoAK " + key,
}

def getSTT():
    with open(getWavPath(), 'rb') as fp:
        audio = fp.read()
    res = requests.post(url, headers=headers, data=audio)
    index = res.text.find('{"type":"finalResult"')
    if index <0:
        return "No Result"
    else:
        res = res.text[index:res.text.rindex('}')+1]
    res = json.loads(res)
    return res['value']

def exSTT():
    with open('heykakao.wav', 'rb') as fp:
        audio = fp.read()
    res = requests.post(url, headers=headers, data=audio)
    print(res.text)

if __name__ == '__main__':
    print(exSTT())
    print(getSTT())