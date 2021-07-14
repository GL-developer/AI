key = "85ec632b61ae5c4346c9b8435d36a70b"

def getKey():
    return key

def latin2utf8(text):
    return text.encode('utf-8').decode('latin1')

def getWavPath():
    return '/home/pi/AI/voiceAI/temp.wav'