import numpy as np
import cv2




# def drawMatches(img1, kp1, img2, kp2, matches):
#
#     rows1 = img1.shape[0]
#     cols1 = img1.shape[1]
#     rows2 = img2.shape[0]
#     cols2 = img2.shape[1]
#
#     out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
#     out[:rows1,:cols1] = np.dstack([img1])
#     out[:rows2,cols1:] = np.dstack([img2])
#     for mat in matches:
#         img1_idx = mat.queryIdx
#         img2_idx = mat.trainIdx
#         (x1,y1) = kp1[img1_idx].pt
#         (x2,y2) = kp2[img2_idx].pt
#
#         cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0, 1), 1)
#         cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0, 1), 1)
#         cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0, 1), 1)
#
#     return out





def compare_images_SIFT(img1, img2):
    try:
        img1Read = cv2.imread(img1)
        img2Read = cv2.imread(img2)
    except Exception:
        print('err img')
        return 0

    #img1Read = cv2.resize(img1Read, (400,400))
    #img2Read = cv2.resize(img2Read, (400,400))
    #print(img1,img2)
    # convert the images to grayscale
    try:
        img1Read = cv2.cvtColor(img1Read, cv2.COLOR_BGR2GRAY)
    except Exception:
        print('err gray scale img1')
        return 0
    try:
        img2Read = cv2.cvtColor(img2Read, cv2.COLOR_BGR2GRAY)
    except Exception:
        print('err gray scale img2')
        return 0

    #orb = cv2.ORB_create()
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1Read,None)
    kp2, des2 = sift.detectAndCompute(img2Read,None)

    # BFMatcher with default params
    try:
        bf = cv2.BFMatcher()
        matches = bf.match(des1,des2)
    #matches = bf.knnMatch(des1, des2, k=2)
    except Exception:
        print('err matcher')
        return 0

    matches = sorted(matches, key=lambda val: val.distance)

    #img3 = drawMatches(img1,kp1,img2,kp2,matches[:25])
    return len(matches)

#print(compare_images_SIFT("img/twitter/_vssrss_Twit.jpg","img/facebook/themillmancaveFace.jpg"))
