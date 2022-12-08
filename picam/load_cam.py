import cv2
import numpy as np
import time

class Cam:
    """properties
        cap, ret, frame, before, after
    """
    
    # sel.befer, self.after 에는 grayscale이고, background가 제거된 이미지만 넣도록 한다.
    
    def __init__(self):
        self.CAM_WIDTH = 720
        self.CAM_HEIGHT = 1280
        
        self.cap = cv2.VideoCapture(0)#, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            print("cam is not opened")
            exit()

        # set dimensions
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAM_WIDTH)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAM_HEIGHT)

    # def capture(self):
        
    #     self.ret, self.frame = self.cap.read()
        
    #     if self.ret == False:
    #         print("ret is False")
    #         exit()
        
    #     # take an after picture
    #     cv2.imwrite('../../after.jpg', self.frame)
        
    #     # if you want a photo to test, use this code.
        
    #     # print("write")
    #     # cv2.imwrite('../../before.jpg', self.frame)
    #     # print("finish")
        
    #     # cv2.imshow('frame', self.frame)
    #     # cv2.waitKey(0)
    #     # cv2.destroyAllWindows()
    #     # exit()


    #     self.before = cv2.imread('../../before.jpg')
    #     self.after = self.frame

    #     # RGB to YCbCr
    #     self.before = cv2.cvtColor(self.before, cv2.COLOR_BGR2GRAY)
    #     self.after = cv2.cvtColor(self.after, cv2.COLOR_BGR2GRAY)
    #     cv2.imwrite('../../afterGray.jpg', self.after)

    def firstCapture(self):
        
        self.ret, self.frame = self.cap.read()
        
        cv2.imwrite('/home/ksw-user/first.jpg', self.frame)
        
        # take a first capture
        self.before = self.frame
        # self.img = self.homomorphic_filtering(self.frame, 0.5, 15.0, 25)#, True)

        #self.img = self.homomorphic_filtering(self.frame, .9, 3.5,3)#, True)
        # cv2.imwrite('/home/ksw-user/morphic.jpg', self.img)
        # self.edged = self.edge_detection(self.img)
        # self.frame = self.preprocess(self.frame, self.edged)
        # cv2.imwrite('/home/ksw-user/edged.jpg', self.edged)
        
        self.frame = self.removeBackGround(self.frame)
        
        height, width = self.frame.shape
        
        cv2.imwrite('/home/ksw-user/remove_first.jpg', self.frame)
        
        if self.ret == False:
            print("ret is False")
            exit()
        
        # turn the image into bytes
        imageBytes = cv2.imencode('.jpg', self.frame)[1].tobytes()

        cv2.imwrite('/home/ksw-user/send_image.jpg', self.frame)
        
        print("firstCapture")
        self.cap.release()
                
        return [imageBytes, width, height]
    
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
    

    def processing(self):
        
        coordinates = []
        
        # total = 0
        
        # self.before = cv2.cvtColor(self.before, cv2.COLOR_BGR2GRAY)
        # self.after = cv2.cvtColor(self.after, cv2.COLOR_BGR2GRAY)
        
        # if self.after == None:
            # print("Didn't take a picture")
        cv2.imwrite("/home/ksw-user/before.jpg", self.before)
        cv2.imwrite("/home/ksw-user/after.jpg", self.after)
        
        # subtract the images
        subtracted = cv2.subtract(self.before, self.after)
    
        # image blur 처리 커널
        blur = cv2.GaussianBlur(subtracted, ksize=(3,3), sigmaX=0)

        # 2진 thresholding 흑백
        self.ret, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY)

        # edge detector(canny) - 가장자리 검출
        edged = cv2.Canny(blur, 0, 255)

        # 수직적인 요소 검출(?), 형태학적인 물체 검출
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        # contour : 형태 높낮이가 같은 거 경계 그려줌
        contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # image에 컨투어 그려줌
        contours_image = cv2.drawContours(subtracted, contours, -1, (0,255,0), 3)

        # test 예제 사진
        cv2.imwrite('/home/ksw-user/contour.jpg', contours_image)

        # contour 좌표를  array로 추출
        contours_xy = np.array(contours)

        # contour 중심 좌표(평균) 계산 -> median으로 바꾸거나 min, max 계산해서 평균 구해도 됨
        contour_center = []
        for i in range(len(contours)):
            contours_mean = np.mean(contours[i], axis = 0)
            contour_center.append(contours_mean)

        # print("minX : " + str(self.minX))
        # print("maxX : " + str(self.maxX))
        # print("minY : " + str(self.minY))
        # print("maxY : " + str(self.maxY))

        # 모든 중심좌표를 list에 넣고, 이미지에 중심 좌표 표시하게 함
        for i in range(len(contour_center)):
            temp = contour_center[i][0]
            temp = temp.tolist()
            x = int(temp[0])
            y = int(temp[1])
            
            if (self.minX <= x) and (x <= self.maxX) and (self.minY <= y) and (y <= self.maxY):
                contours_image[y, x] = [128,128,5]
                coordinates.append(x)
                coordinates.append(y)
                # print(str(x) + ", " + str(y))
            
            
            # coordinates[f"{i}"] = [x, y]
        
        # print(coordinates)
        if len(coordinates) != 0:
            perspect_x = round((self.mtrx[0][0]* coordinates[0]+self.mtrx[0][1]* coordinates[1]+self.mtrx[0][2])/(self.mtrx[2][0]* coordinates[0]+self.mtrx[2][1]* coordinates[1]+self.mtrx[2][2]))
            perspect_y = round((self.mtrx[1][0]* coordinates[0]+self.mtrx[1][1]* coordinates[1]+self.mtrx[1][2])/(self.mtrx[2][0]* coordinates[0]+self.mtrx[2][1]* coordinates[1]+self.mtrx[2][2]))

            coordinates = [perspect_x, perspect_y]
        
            print(coordinates)

            return coordinates
        else:
            return []

    def removeBackGround(self, image):

        copy = image.copy()
        
        # turn image from RGB to YCBCR (brightness)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # modified
        
        cv2.imwrite("/home/ksw-user/gray.jpg", gray)
        
        # Denoise by Gaussian Blur
        gray = cv2.GaussianBlur(gray, (3,3), 0)
        
        cv2.imwrite("/home/ksw-user/gaussian.jpg", gray)
        
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        
        # Canny Edge Detection
        # edged = cv2.Canny(gray.copy(), 150, 255)
        edged = cv2.Canny(gray.copy(), 0, ret)
                        
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
        sm = pts.sum(axis = 1)
        diff = np.diff(pts, axis = 1)
        
        self.topLeft = pts[np.argmin(sm)]
        self.bottomRight = pts[np.argmax(sm)]
        self.topRight = pts[np.argmin(diff)]
        self.bottomLeft = pts[np.argmax(diff)]
        
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
    
    

# # open camera
# cap = cv2.VideoCapture(0)#, cv2.CAP_V4L2)


# if not cap.isOpened():
#     print("cam is not opened")
#     exit()

# print(cap)
# print("-----------cap---------")

# # set dimensions
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)

# # take frame
# ret, frame = cap.read()

# if ret == False:
#     print("ret = False")
#     print("frame: " + str(frame))
#     exit()

# #if  cv2.waitKey(0) & 0xFF==ord('q'):
# #    cv2.destroyAllWindows()

# # test code

# before = cv2.imread('../../target1.jpg')
# after = frame

# print(before)
# print("------------------")
# print(after)
# print(ret)

# # image size
# # print(before.shape)


# # In[33]:

# # 밝기 조절
# def adjust_gamma(image, gamma=1.0):
#     invGamma = 1.0 / gamma
#     table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    
#     return cv2.LUT(image, table)

# #x = 'test3.jpg'  #location of the image
# # original = cv2.imread('test3.jpg', 1)
# # cv2.imshow('original',original)

# # gamma = 2.5                                   # change the value here to get different result
# # before = adjust_gamma(original, gamma=gamma)
# # cv2.putText(before, "g={}".format(gamma), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
# # cv2.imshow("gammam image 1", before)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[34]:


# # original = cv2.imread('test4.jpg', 1)
# # cv2.imshow('original',original)

# # gamma = 2.5                                   # change the value here to get different result
# # after = adjust_gamma(original, gamma=gamma)
# # cv2.putText(after, "g={}".format(gamma), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
# # cv2.imshow("gammam image 1", after)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[35]:


# # 해상 조절
# # before = cv2.resize(before, (720, 480))
# # after = cv2.resize(after, (720, 480))


# # In[36]:


# # print(before.shape)


# # In[37]:


# # cv2.imshow('before', before)

# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[38]:


# # cv2.imshow('after', before)

# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[39]:



# # subtract the images
# subtracted = cv2.subtract(before, after)
 
# # TO show the output
# # cv2.imshow('image', subtracted)

# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[40]:

# # image blur 처리 커널
# blur = cv2.GaussianBlur(subtracted, ksize=(3,3), sigmaX=0)


# # In[41]:

# # 2진 thresholding 흑백
# ret, thresh1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY)


# # In[ ]:





# # In[42]:

# # edge detector(canny) - 가장자리 검출
# edged = cv2.Canny(blur, 0, 255)
# # cv2.imshow('Edged', edged)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[43]:

# # 수직적인 요소 검출(?), 형태학적인 물체 검출
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
# closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
# # cv2.imshow('closed', closed)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[44]:

# # contour : 형태 높낮이가 같은 거 경계 그려줌
# #contours, contourlist, hierarchy = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# #im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# total = 0


# # In[45]:

# # image에 컨투어 그려줌
# contours_image = cv2.drawContours(subtracted, contours, -1, (0,255,0), 3)
# # cv2.imshow('contours_image', contours_image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[46]:

# # contour 좌표를  array로 추출
# contours_xy = np.array(contours)
# # contours_xy.shape


# # In[47]:


# # contours


# # In[48]:

# # contour 중심 좌표(평균) 계산 -> median으로 바꾸거나 min, max 계산해서 평균 구해도 됨
# contour_center = []
# for i in range(len(contours)):
#     contours_mean = np.mean(contours[i], axis = 0)
#     contour_center.append(contours_mean)


# # In[49]:


# # contour_center


# # In[50]:
# coordinates = {}

# # 모든 중심좌표를 list에 넣고, 이미지에 중심 좌표 표시하게 함
# for i in range(len(contour_center)):
#     temp = contour_center[i][0]
#     temp = temp.tolist()
#     x = int(temp[0])
#     y = int(temp[1])
#     # print(temp)
#     # print(temp[0])
#     #contours_image[y, x] = [255,0,0]
#     contours_image[y, x] = [128,128,5]
    
#     coordinates[f"{i}"] = f"({x}, {y})"
    
# # print(coordinates)





# # In[51]:

# # 이미지에 중심 좌표 표시한 것을 보여줌
# # cv2.imshow('contours_image', contours_image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[140]:

# # gray -> bgr로 변환
# # closed = cv2.cvtColor(closed, cv2.COLOR_GRAY2BGR)


# # In[141]:

# # contour를 딴 이미지에 중심 좌표 표시
# # for i in range(len(contour_center)):
# #     temp = contour_center[i][0]
# #     #temp = temp.tolist()
# #     temp = temp.tolist()
# #     x = int(temp[0])
# #     y = int(temp[1])
# #     print(temp)
# #     print(temp[0])
# #     closed[y, x] = [128, 128,5]


# # In[142]:


# # contours_image.shape


# # In[143]:


# # TO show the output
# # cv2.imshow('image', closed)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # In[ ]:

    def homomorphic_filtering(self, image, gamma1, gamma2, power, white = False):
        img = image.copy()
        
        # RGB이미지를 YUV로 변환
        # RGB to YUV conversion
        img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)    
        y = img_YUV[:,:,0]    

        rows, cols = y.shape[0], y.shape[1]

        ### illumination, reflectance elements(조명, 반사 요소)를 분리하기 위해 log를 취함
        ### log operation to seperate illumination and reflection elements

        imgLog = np.log1p(np.array(y, dtype='float') / 255) # y값을 0~1사이로 조정

        ### frequency를 이미지로 나타내면 4분면에 대칭적으로 나타나므로 
        ### 4분면 중 하나에 이미지를 대응시키기 위해 row와 column을 2배씩 늘려줌
        ### 이미지 복원 시 aliasing 발생을 막도록 하는 것임(이미지 깨지는 것 방지)
        ### to prevent aliasing, row and columns multipies 2
        M = 2*rows + 1
        N = 2*cols + 1

        ### gaussian mask with sigma = 10
        sigma = 10
        (X, Y) = np.meshgrid(np.linspace(0, N-1, N), np.linspace(0, M-1, M)) # 0~N-1(과 M-1) 까지 1 단위로 space 생성
        Xc = np.ceil(N/2) # 올림
        Yc = np.ceil(M/2)
        gaussianNumerator = (X - Xc)**2 + (Y - Yc)**2 # gaussian 분자

        ### low pass filter, high pass filter 
        LPF = np.exp(-gaussianNumerator / (2* (sigma**2)))
        HPF = 1 - LPF

        ### LPF와 HPF 모두 0이 가운데로 오도록 IFFT 
        ### frequency를 각 귀퉁이로 모아 줌
        LPF_shift = np.fft.ifftshift(LPF.copy())
        HPF_shift = np.fft.ifftshift(HPF.copy())

        ### Log를 취한 이미지에 FFT를 적용해서 LPF와 HPF를 곱하여 Low Frequency성분과 High Frequency 성분 분리
        img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
        img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))
        img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))
        
        ### 각 LF, HF 성분에 scaling factor(gamma)를 곱하여 조명값과 반사값을 조절
        img_adjust = gamma1*img_LF[0:rows, 0:cols] + gamma2*img_HF[0:rows, 0:cols]

        ### 조정된 데이터를 이제 exp 연산을 통해 원래 형태의 이미지로 생성
        img_exp = np.expm1(img_adjust) # exp(x) + 1
        img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp)) # 0 ~ 1사이 정규화
        img_out = np.array(255 * img_exp, dtype = 'uint8') # 255를 곱해서 intensity값을 만들어줌

        ## pixel 값 50 미만은 white로 변환
        img_out2 = (img_out < 50)
        img_out = 255*img_out2.astype("uint8")        


        ## YUV의 Y space를 filtering된 이미지로 교체해주고 RGB로 변환
        img_YUV[:,:,0] = img_out
        rgb_img = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
        
        if white == True:
            _, rgb_img = cv2.pencilSketch(rgb_img, sigma_s=60, sigma_r=0.05, shade_factor=0.02)
            
        ## image intensity normalization
        gray = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2GRAY)   
        result = np.array(255 * (gray / 255) ** power, dtype = 'uint8')
        
        return result
    
    def edge_detection(self, image):
        # gaussian bluring
        blur = cv2.GaussianBlur(image, (5,5), 0)
        
        # canny
        canny = cv2.Canny(blur, 0, 255)
        
        ## closed 연산 = 팽창(dilate) 후 침식(erode)
        ## closed 연산하는 이유 : contour(closed curve)를 찾기 위해 edge를 더욱 선명하게 하기 위함
        # 침식(erode) : object의 테두리를 깎는 효과
        # 팽창(dilate) : 이미지의 모든 픽셀을 스캔하면서 구조적인 요소와 하나의 픽셀이라도 일치할 때 픽셀에 마킹
        # 구조적 요소 : 원본 이미지에 적용되는 커널(Kernel)로, 커널이 image 내의 sub pixel에 하나라도 canny edge를 딴 것이 있으면 커널 내 모든 픽셀을 색칠해버림
        dilate_img = cv2.dilate(canny, (3,3), iterations=2)
        edged = cv2.erode(dilate_img, (3,3), iterations=2)
        
        return edged
    
    def preprocess(self, image, edged):
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

        for i in cnts:
            peri = cv2.arcLength(i, True)  # contour가 그리는 길이 반환
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)  # 길이에 2% 정도 오차를 둔다
            print('arclength', peri)
            print(len(approx))
            if len(approx) == 4:  # 도형을 근사해서 외곽의 꼭짓점이 4개라면 명암의 외곽으로 설정
                screenCnt = approx
                size = len(screenCnt)
                
            if len(approx) == 4: # 근사한 꼭짓점이 4개면 중지
                break
            
        pts = []    
            
        if approx.shape[0] == 4 :
            pts = approx.reshape(4,2) # N * 1 * 2 -> 4 * 2

        for x,y in pts:
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
        diff = np.diff(pts, axis = 1)       # 4쌍의 좌표 각각 x-y 계산

        topLeft = pts[np.argmin(sm)]         # x+y가 가장 값이 좌상단
        bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단
        topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단
        bottomLeft = pts[np.argmax(diff)] 

        pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

        # 변환 후 영상에 사용할 폭과 높이 계산
        w1 = abs(bottomRight[0] - bottomLeft[0]) # 상단 폭
        w2 = abs(topRight[0] - topLeft[0]) # 하단 폭
        h1 = abs(topRight[1] - bottomRight[1]) # 우측 높이
        h2 = abs(topLeft[1] - bottomLeft[1]) # 좌측 높이
        width = max([w1,w2]) # 폭
        height = max([h1,h2]) # 높이

        # 변환 후 4개의 좌표
        pts2 = np.float32([[0,0],[width-1,0],[width-1,height-1],[0,height-1]])

        # 변환 행렬 계산
        mtrx = cv2.getPerspectiveTransform(pts1, pts2)

        # Perspective transformation 적용
        result = cv2.warpPerspective(image, mtrx, (width, height))

        return result
        
        