#Import relevant modules
import cv2
import numpy as np
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import winsound



def mail_sent(toaddr, filename, path, body):
    fromaddr = "testingautomation243@gmail.com"
    toaddr = toaddr
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "Object detected at child"
    body = body
    msg.attach(MIMEText(body, 'plain')) 
    ''''filename = filename
    attachment = open(path, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) '''
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "qfbhurcoigibaezh") 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text)
    print("sent mail")
    s.quit() 


# Fetch the service account key JSON file contents
cred = credentials.Certificate('childobjkey.json')

# Initialize the app with a service account, granting admin privileges

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://childobj-default-rtdb.firebaseio.com/"
})

#Read in the image file
thres = 0.45 #Threshold to detect object
nms_threshold = 0.5 #NMS
cap = cv2.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)
cap.set(10,150)


#Import the class names
classNames = []
classFile = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'config_files', 'coco.names'))


# Read object classes
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#Import the config and weights file
os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'config_files', 'coco.names'))
configPath =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'config_files', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'))
weightsPath = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'config_files', 'frozen_inference_graph.pb')) #Weights derived from training on large objects dataset

#Set relevant parameters
net = cv2.dnn_DetectionModel(weightsPath,configPath)

#These are some suggested settings from the tutorial, others are fine but this can be used as a baseline
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)

val1=""

while True:
    # Start Webcam
    success, image = cap.read()

    # Tuple unpacking net.detect provides ID of object, confidence and bounding box
    classIds, confs, bbox = net.detect(image,confThreshold = thres)

    # It's not in a nice format to print, so it needs to be cleaned up
    bbox = list(bbox) #NMS function required bbox as a list, not a tuple
    confs = list(np.array(confs).reshape(1,-1)[0]) #[0] removed extra bracket, and reshape used to get the values on the same row
    confs = list(map(float,confs))
    #print(classIds, confs,bbox)

    # Extract co-ordinates of bounding box (with NMS)
    indicies = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)

    # add boxes for each detection on each frame
    #print(indicies)
    for i in indicies:
        i = indicies[0] #Get the bounding box info
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(image,(x,y),(x+w,h+y),color = (0,255,0), thickness =2)
        #print(classNames[classIds[i]-1])
        res = classNames[classIds[i]-1]
        cv2.putText(image,classNames[classIds[i]-1],(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        ref = db.reference('CHILD_IOT')
        ref.set({'OBJ_STATUS': res})
        val = ref.get()
        val = dict(val)
        print(val.get('Dist'))
        if( val1 != res):
            val1 = res 
            mail_sent("ankithakatkar@gmail.com", "child.txt",  "childobjkey.json", "the object "+ res+ " has been detected at distance ")
    ref = db.reference('CHILD_IOT')
    ref.set({'OBJ_STATUS': ""})

    # Show output until CTRL+C
    cv2.imshow("Output", image)
    cv2.waitKey(1)
 
    #Without NMS
    #if len(classIds) != 0:
        #for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
            #cv2.rectangle(image,box,color=(0,255,0), thickness=2)
            #cv2.putText(image,classNames[classId-1],(box[0]+10,box[1]+30),
                        #cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)