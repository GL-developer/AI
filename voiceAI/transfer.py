import requests, json, os
if __name__ == '__main__':
    from common import getKey, latin2utf8
else:
    from .common import getKey, latin2utf8
    
type_url = "https://dapi.kakao.com/v3/translation/language/detect"
trans_url = "https://dapi.kakao.com/v2/translation/translate"

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "KakaoAK " + getKey(),
}

def senseSpeech(text):
    res = requests.post(type_url, headers=headers, data="query="+text)
    res = json.loads(res.content.decode())
    return res['language_info'][0]['code']

def transLang(src, target, text):
    data = {"src_lang":src, "target_lang":target, "query":text}
    res = requests.post(trans_url, headers=headers, data=data)
    res = json.loads(res.content.decode())
    if 'translated_text' in res:
        return res['translated_text'][0][0]
    else:
        return "No Result"
    

if __name__ == '__main__':
    print(senseSpeech(latin2utf8("안녕하세요 처음 뵙겠습니다")))
    print(transLang("kr","en","안녕하세요 처음 뵙겠습니다"))