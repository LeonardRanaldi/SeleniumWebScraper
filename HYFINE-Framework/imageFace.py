import face_recognition
from PIL import Image, ImageDraw


#input file1, file2 return encodings face if there are
def findFace(file1, file2):

    try:
        image1 = face_recognition.load_image_file(file1)
        image_face_encoding1 = face_recognition.face_encodings(image1)

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        return 0
        #quit()

    try:
        image2 = face_recognition.load_image_file(file2)
        image_face_encoding2 = face_recognition.face_encodings(image2)

    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        return 0
        #quit()

    return image_face_encoding1, image_face_encoding2

#print(findFace('/path/img.jpg', ''))

def compareFace(image_face_encoding1, image_face_encoding2):

    know = image_face_encoding1

    print(' Num. faces in first img: ',len(know))
    print(' Num. faces in second img: ', len(image_face_encoding2))

    if len(image_face_encoding2) > 1:
        i = 0
        for face in image_face_encoding2:
            i=i+1
            result = face_recognition.compare_faces(know, face)

            print("comparation is? {}".format(result[0]), ' ---> with face num. ', i)


    if len(image_face_encoding2) == 1:
        result = face_recognition.compare_faces(know, face)

        print("comparation is? {}".format(result[0]), ' ---> with face on second img', )

    return len(know), len(image_face_encoding2)


def similarityImageTakeEncoding(image_face_encoding1, image_face_encoding2):


    listImgDist = []

    face_encoding = image_face_encoding1
    known_encodings = face_encoding
    image_to_test_encoding = image_face_encoding2

    # See how far apart the test image is from the known faces
    for image in image_to_test_encoding:

        face_distances = face_recognition.face_distance(known_encodings, image)

        for i, face_distance in enumerate(face_distances):
            listImgDist.append(face_distance)
    return min(listImgDist)


def similarityImageTakeImg(image1, image2):

    # Load some images to compare against
    known_image = face_recognition.load_image_file(image1)

    # Get the face encodings for the known images
    face_encoding = face_recognition.face_encodings(known_image)


    known_encodings = face_encoding


    # Load a test image and get encondings for it
    image_to_test = face_recognition.load_image_file(image2)
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)

    # See how far apart the test image is from the known faces
    for image in image_to_test_encoding:

        face_distances = face_recognition.face_distance(known_encodings, image)


        for i, face_distance in enumerate(face_distances):
            print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
            print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
            print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
            print()




def printFace(fileLocation):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(fileLocation)

    # Find all facial features in all the faces in the image
    face_list = face_recognition.face_locations(image)
    i = 0
    for face_location in face_list:
        i = i+1
        top, right, bottom, left = face_location

        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        pil_image.save('img/prova2'+str(i)+'.jpg')


