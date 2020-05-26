from skimage.measure import compare_ssim as ssim
import numpy as np
import cv2



def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB):

    #m = mse(imageA, imageB)
    try:
        s = ssim(imageA, imageB)
    except Exception:
        return 0
    s = round(s, 3)
    return s




def compare_images_OpenCV(img1, img2):
    try:
        img1Read = cv2.imread(img1)
        img2Read = cv2.imread(img2)
    except Exception:
        return 0

    try:
        img1Read = cv2.resize(img1Read, (400,400))
        img2Read = cv2.resize(img2Read, (400,400))
    except Exception:
        print('resize error')

    try:
        # convert the images to grayscale
        img1Read = cv2.cvtColor(img1Read, cv2.COLOR_BGR2GRAY)
        img2Read = cv2.cvtColor(img2Read, cv2.COLOR_BGR2GRAY)
    except Exception:
        print('grayscale error')
        return 0


    result = compare_images(img2Read, img1Read)
    return result


# load the images -- the original, the original + contrast,
# and the original + photoshop
# original = cv2.imread("img/salvini2.jpg")
# contrast = cv2.imread("img/twitter/4uaibbs2ldkum9pTwit.jpg")
# shopped = cv2.imread("img/salvini2.jpg")
#
#
# original = cv2.resize(original, (400,400))
# contrast = cv2.resize(contrast, (400,400))
# shopped = cv2.resize(shopped, (400,400))
#
# # convert the images to grayscale
# original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
# contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
# shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)



# compare the images
# compare_images(original, original, "Original vs. Original")
# compare_images(original, contrast, "Original vs. Contrast")
# compare_images(original, shopped, "Original vs. Photoshopped")

#print(compare_images_OpenCV("img/salvini2.jpg","img/twitter/4uaibbs2ldkum9pTwit.jpg"))