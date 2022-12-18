import cv2
import numpy as np
import time

class Cam:
    """properties
        cap, ret, frame, before, after
    """
    
    
    def __init__(self):
        self.CAM_WIDTH = 720
        self.CAM_HEIGHT = 1280
        
        self.cap = cv2.VideoCapture(0)#, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            print("cam is not opened")
            exit()

    # first initial image capture
    def firstCapture(self):
        
        self.ret, self.frame = self.cap.read()
        
        cv2.imwrite('/home/ksw-user/first.jpg', self.frame)
        
        # take a first capture
        self.before = self.frame
        
        self.frame = self.removeBackGround(self.frame)
        
        cv2.imwrite('/home/ksw-user/remove_first.jpg', self.frame)
        
        if self.ret == False:
            print("ret is False")
            exit()
        
        # turn the image into bytes
        imageBytes = cv2.imencode('.jpg', self.frame)[1].tobytes()

        
        self.cap.release()
                
        return imageBytes
    
    
    # get the coordinate
    def captureForCoordinate(self):
        
        self.cap = cv2.VideoCapture(0)
        
        self.ret, self.frame = self.cap.read()
        
        cv2.imwrite('/home/ksw-user/coordinate.jpg', self.frame)
        
        self.after = self.frame
        
        # self.frame = self.removeBackGround(self.frame)
        
        if self.ret == False:
            print("ret is False")
            exit()
                    
        coordinate = self.processing()
        
        self.before = self.after
            
        self.cap.release()
            
        return coordinate
    

    # calculation the shooting point
    def processing(self):
        
        coordinates = []
        
        cv2.imwrite("/home/ksw-user/before.jpg", self.before)
        cv2.imwrite("/home/ksw-user/after.jpg", self.after)
        
        # subtract the images
        subtracted = cv2.subtract(self.before, self.after)
    
        # image blur
        blur = cv2.GaussianBlur(subtracted, ksize=(3,3), sigmaX=0)

        # thresholding
        self.ret, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY)

        # edge detector(canny)
        edged = cv2.Canny(blur, 0, 255)

        # structure element and morphology function
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        # contour(closed curve)
        contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours_image = cv2.drawContours(subtracted, contours, -1, (0,255,0), 3)

        cv2.imwrite('/home/ksw-user/contour.jpg', contours_image)

        contours_xy = np.array(contours)

        contour_center = []
        for i in range(len(contours)):
            contours_mean = np.mean(contours[i], axis = 0)
            contour_center.append(contours_mean)


        for i in range(len(contour_center)):
            temp = contour_center[i][0]
            temp = temp.tolist()
            x = int(temp[0])
            y = int(temp[1])
            
            if (self.minX <= x) and (x <= self.maxX) and (self.minY <= y) and (y <= self.maxY):
                contours_image[y, x] = [128,128,5]
                coordinates.append(x)
                coordinates.append(y)
            
            
        
        if len(coordinates) != 0:
            perspect_x = round((self.mtrx[0][0]* coordinates[0]+self.mtrx[0][1]* coordinates[1]+self.mtrx[0][2])/(self.mtrx[2][0]* coordinates[0]+self.mtrx[2][1]* coordinates[1]+self.mtrx[2][2]))
            perspect_y = round((self.mtrx[1][0]* coordinates[0]+self.mtrx[1][1]* coordinates[1]+self.mtrx[1][2])/(self.mtrx[2][0]* coordinates[0]+self.mtrx[2][1]* coordinates[1]+self.mtrx[2][2]))

            coordinates = [perspect_x, perspect_y]
        
            print(coordinates)

            return coordinates
        else:
            return []

    # get only the target portion
    def removeBackGround(self, image):

        copy = image.copy()
        
        # turn image from RGB to YCBCR (brightness)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        
        cv2.imwrite("/home/ksw-user/gray.jpg", gray)
        
        # Denoise by Gaussian Blur
        gray = cv2.GaussianBlur(gray, (3,3), 0)
        
        cv2.imwrite("/home/ksw-user/gaussian.jpg", gray)
        
        # Canny Edge Detection
        edged = cv2.Canny(gray.copy(), 150, 255)
        
        cv2.imwrite("/home/ksw-user/canny.jpg", edged)
        
        # find a closed curve
        cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
        # draw a contours
        cv2.drawContours(copy, cnts, -1, (0, 255, 0))
                
        # After finding a contour, sort the square picture in order of large area
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
        
        for c in cnts:
            # simplify approximate contour from largest area    
            peri = cv2.arcLength(c, True)   # circumferential length
            
            # Approximate to 0.02 approximation of perimeter length
            vertices = cv2.approxPolyDP(c, 0.02 * peri, True)

            # Stop with 4 approximate vertices
            if len(vertices) == 4:
                break
            
        # change vertex to 4 by 2
        if vertices.shape[0] == 4:
            pts = vertices.reshape(4,2)
            
        # mark a green circle at a coordinate
        for x, y in pts:
            cv2.circle(copy, (x, y), 5, (0, 255, 0), -1)
            
        # find a center of coordinates
        alpha = 10
        center = (image.shape[0] // 2, image.shape[1] // 2)
        pts = pts[np.argsort([np.arctan2(p[0] - center[0] // alpha, p[1] + center[1]) for p in pts])]

        # coordinate of target's vertexes
        self.topLeft = pts[1]
        self.bottomRight = pts[2]
        self.topRight = pts[3]
        self.bottomLeft = pts[0]
        
        # find min x, y and max x, y
        self.minX = min(self.topLeft[0], self.bottomLeft[0])
        self.maxX = max(self.topRight[0], self.bottomRight[0])

        self.minY = min(self.topLeft[1], self.topRight[1])
        self.maxY = max(self.bottomLeft[1], self.bottomRight[1])        


        # 4 coordinates before conversion
        pts1 = np.float32([self.topLeft, self.topRight, self.bottomRight, self.bottomLeft])

        # calculate the width and height for the post-conversion image
        w1 = abs(self.bottomRight[0] - self.bottomLeft[0]) # top width
        w2 = abs(self.topRight[0] - self.topLeft[0]) # bottom width
        h1 = abs(self.topRight[1] - self.bottomRight[1]) # right height
        h2 = abs(self.topLeft[1] - self.bottomLeft[1]) # left height
        width = max([w1,w2]) # total width
        height = max([h1,h2]) # total height
        
        # 4 coordinates after conversion
        pts2 = np.float32([[0,0],[width-1,0],[width-1,height-1],[0,height-1]])

        # calculate the transformation Matrix
        self.mtrx = cv2.getPerspectiveTransform(pts1, pts2)

        # apply the Perspective transformation
        result = cv2.warpPerspective(image, self.mtrx, (width, height))
        
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
        return result
        
        

    def getImage(self):
        
        # self.ret, self.frame = self.cap.read()
        
        if self.ret == False:
            print("ret is False")
            exit()

        return self.after


