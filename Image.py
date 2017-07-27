# use open cv to show new images from AirSim 
#coding=utf-8
from PythonClient import *
import cv2
import time
import sys

def printUsage():
   print("Usage: python camera.py [depth|segmentation|scene]")

cameraType = "depth"

for arg in sys.argv[1:]:
  cameraType = arg.lower()
print (">>>>>>>>>>")
print (cameraType)
cameraTypeMap = { 
 "depth": AirSimImageType.Depth,
 "segmentation": AirSimImageType.Segmentation,
 "seg": AirSimImageType.Segmentation,
 "scene": AirSimImageType.Scene,
}

if (not cameraType in cameraTypeMap):
  printUsage()
  sys.exit(0)

print cameraTypeMap[cameraType]

client = AirSimClient('127.0.0.1')

help = False

fontFace = cv2.FONT_HERSHEY_SIMPLEX #使用默认字体类型
fontScale = 0.5 # 字体大小
thickness = 2 #字体粗细
textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness) 
textOrg = (10, 10 + textSize[1])
frameCount = 0

startTime=time.clock() #在第一次调用的时候，返回的是程序运行的实际时间；以第二次之后的调用，返回的是自第一次调用后,到这次调用的时间间隔

print (startTime)
fps = 0

while True:
    # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
    rawImage = client.simGetImage(0, cameraTypeMap[cameraType])
    if (len(rawImage) == 0):
        print("Camera is not returning image, please check airsim for error messages")
        sys.exit(0)
    else:
        png = cv2.imdecode(rawImage, cv2.IMREAD_UNCHANGED)
        #cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
        #cv2.imshow("Depth", png)
        cv2.imwrite("/opt/AirSim/PythonClient/depth/"+str(frameCount)+".png", png )
    frameCount  = frameCount  + 1
    endTime=time.clock()
    diff = endTime - startTime\
    '''
    if (diff > 1):
        fps = frameCount
        frameCount = 0
        startTime = endTime
    '''    
    key = cv2.waitKey(1) & 0xFF;
    if (key == 27 or key == ord('q') or key == ord('x')):
        break;
