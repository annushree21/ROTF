###################################
##### Authors:                #####
##### Stephane Vujasinovic    #####
##### Frederic Uhrweiller     ##### 
#####                         #####
##### Creation: 2017          #####
###################################

import numpy as np
import cv2
import time

cv2.useOptimized()
print('Starting the Calibration just press the space bar to exit this part of the Programm\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')

# Contador de Imagenes guardadas
i=0

# termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all images
objpoints= []   # 3d points in real world space
imgpointsR= []  # 2d points in image plane   
imgpointsL= []   

# Call the two cameras
CamR= cv2.VideoCapture(2)  # Wenn 0 then Right Cam and wenn 2 Left Cam
CamL= cv2.VideoCapture(0)

while True:
    retR, frameR= CamR.read()
    retL, frameL= CamL.read()

    dim = (128, 128)
    resizedL = cv2.resize(frameL, dim)
    resizedR= cv2.resize(frameR, dim)

    grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
    grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)

    startTime = time.time()

    # Find the chess board corners
    retR, cornersR = cv2.findChessboardCorners(grayR, (9,6), None)  # Define the number of chess corners we are looking for (9,6)
    retL, cornersL = cv2.findChessboardCorners(grayL, (9,6), None)  # Left side
    cv2.imshow('imgR', frameR)
    cv2.imshow('imgL', frameL)

    endTime = time.time()  

    # If found, add object points, image points (after refining them)
    if (True == retR) & (True == retL) :
        print("ok")
        objpoints.append(objp)
        corners2R= cv2.cornerSubPix(grayR,cornersR,(11,11),(-1,-1),criteria)    # Refining the Position
        imgpointsR.append(cornersR)
        corners2L= cv2.cornerSubPix(grayL,cornersL,(11,11),(-1,-1),criteria)
        imgpointsL.append(cornersL)

        # Draw and display the corners
        cv2.drawChessboardCorners(grayR,(9,6),corners2R,retR)
        cv2.drawChessboardCorners(grayL,(9,6),corners2L,retL)
        cv2.imshow('VideoR',grayR)
        cv2.imshow('VideoL',grayL)

        if cv2.waitKey(0) & 0xFF == ord('s'):   # Push "s" to save the images and "c" if u want to not save the images
            t= str(i)
            print('Saved'+t)
            cv2.imwrite('images/chessboard-R'+t+'.png',frameR) # Save the image in the file where this Programm is located
            cv2.imwrite('images/chessboard-L'+t+'.png',frameL)
            i=i+1
        else:
            print('canceled')
    workTime =  endTime - startTime
        
        #print results
    print ("The job took " + str(workTime) + " sconds to complete")

    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord(' '):   # Push the space bar and maintan to exit this Programm
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()    
