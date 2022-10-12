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

        # set dimensions
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAM_WIDTH)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAM_HEIGHT)

    def capture(self):
        
        self.ret, self.frame = self.cap.read()
        
        if self.ret == False:
            print("ret is False")
            exit()
        
        
        # if you want a photo to test, use this code.
        
        # print("write")
        # cv2.imwrite('../../target.jpg', self.frame)
        # print("finish")
        
        # cv2.imshow('frame', self.frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # exit()


        self.before = cv2.imread('../../target.jpg')
        self.after = self.frame
    
    def processing(self):
        
        coordinates = {}

        # total = 0
        
        # if self.after == None:
            # print("Didn't take a picture")
          
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

        # contour 좌표를  array로 추출
        contours_xy = np.array(contours)

        # contour 중심 좌표(평균) 계산 -> median으로 바꾸거나 min, max 계산해서 평균 구해도 됨
        contour_center = []
        for i in range(len(contours)):
            contours_mean = np.mean(contours[i], axis = 0)
            contour_center.append(contours_mean)

        # 모든 중심좌표를 list에 넣고, 이미지에 중심 좌표 표시하게 함
        for i in range(len(contour_center)):
            temp = contour_center[i][0]
            temp = temp.tolist()
            x = int(temp[0])
            y = int(temp[1])
            # print(temp)
            # print(temp[0])
            #contours_image[y, x] = [255,0,0]
            contours_image[y, x] = [128,128,5]
            
            coordinates[f"{i}"] = f"({x}, {y})"

        return coordinates



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




