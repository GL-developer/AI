import requests, time, queue, os, threading
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

# for reference
#sf_subtypes = ['ALAW', 'DOUBLE', 'FLOAT', 'G721_32', 'GSM610', 'IMA_ADPCM', 'MS_ADPCM', 'PCM_16', 'PCM_24', 'PCM_32', 'PCM_U8', 'ULAW']
#sd_dtypes = ['float32', 'int32', 'int16']  
#sd_rare_dtypes = ['int8', 'uint8', 'int24','float64']

soundfile_wav = '/home/pi/AI/voiceAI/temp.wav'
q = queue.Queue()
recorder = False
recording = False

samplerate=16000
subtype = 'PCM_16'
dtype = 'int16' 
channel = 1 #Mono

# recorder, based on arbitrary duration example
def complicated_record():
    with sf.SoundFile(soundfile_wav, mode='w', samplerate=samplerate, subtype=subtype, channels=channel) as file:
        with sd.InputStream(samplerate=samplerate, dtype=dtype, channels=channel, callback=complicated_save):
            while recording:
                file.write(q.get())

def complicated_save(indata, frames, time, status):
    q.put(indata.copy())


def start():
    global recorder
    global recording
    recording=True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()

def stop():
    global recorder
    global recording
    recording=False
    recorder.join()
    print('stop recording')

if __name__ == '__main__':
    start()
    time.sleep(5)
    stop()

#https://github.com/spatialaudio/python-sounddevice/issues/312
