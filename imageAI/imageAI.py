from tensorflow.keras.models import load_model
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

def loadModel(path):
    return load_model(path,compile=False)

def getImageResource(width, height): 
    ret, frame =cap.read()
    image = cv2.resize(frame,(width,height))
    return image
    
def getAnalyzedData(image, model):
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0)-1
    data = np.ndarray(shape=(1,224,224,3), dtype=np.float32)
    data[0] = normalized_image_array
    prediction = model.predict(data)[0]
    return prediction
    
def getTextLabel(path):
    with open(path,"r") as label:
        text = label.read()
        lines = text.split("\n")
        labels = {}
        for line in lines[0:-1]:
            hold = line.split(" ",1)
            labels[int(hold[0])] = hold[1]
    return labels
        
def showVideo(model):
    image = getImageResource(224, 224)
    prediction = getAnalyzedData(image,model)
    labels = getTextLabel("./labels.txt")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 0.5
    for index, value in enumerate(prediction):
        text = labels[index]+": "+str(np.around(value*100,2))+"%"
        width = 0
        height = 10+(index*20)
        font_color = (255 if index==3 else 0, 255 if index==2 else 0, 255 if index==1 else 0)
        cv2.putText(image,text,(width,height), font,font_size,font_color,2)
    
    cv2.imshow('video',image)
    
if __name__ == '__main__':
    model = loadModel('./keras_model.h5')
    while True:
        showVideo(model)
        if cv2.waitKey(1) & 0xff ==ord('q'):
            break;
        
    cap.release()
    cv2.destroyAllwindows()
