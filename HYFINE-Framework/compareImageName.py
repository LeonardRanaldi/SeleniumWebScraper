from PIL import Image
import imagehash
import Levenshtein as lev
import imageFace
import os
import glob


def resizeImage(img):
    print(img)
    basewidth = 150
    nameIMG = img

    img = Image.open(img)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    os.remove(nameIMG)
    img.save(nameIMG)



def similarityImage(img1, img2):

    try:
        enco1, enco2 = imageFace.findFace(img1,img2)
    except Exception:
        return None,None,None,None
    if (enco1 != []) and (enco2 != []):
        similarity = imageFace.similarityImageTakeEncoding(enco1,enco2)
    else:
        similarity = 0

    similarity = round(similarity, 5)

    hash0 = imagehash.average_hash(Image.open(img1))
    hash1 = imagehash.average_hash(Image.open(img2))

    similarityAverageHash = 0
    similarityAverageHash = (hash0-hash1)
    if similarityAverageHash != 0:
        similarityAverageHash = similarityAverageHash/100

    if similarityAverageHash == 0:
        print(img1, ' ', img2)

    hash0 = imagehash.dhash(Image.open(img1))
    hash1 = imagehash.dhash(Image.open(img2))
    similarityDHash = 0
    similarityDHash = (hash0-hash1)
    if similarityDHash != 0:
        similarityDHash = similarityDHash/100

    if similarityDHash == 0:
        print(img1, ' ', img2)

    hash0 = imagehash.phash(Image.open(img1))
    hash1 = imagehash.phash(Image.open(img2))
    similarityPHash = 0
    similarityPHash = (hash0 - hash1)
    if similarityPHash != 0:
        similarityPHash = similarityPHash / 100

    if similarityPHash == 0:
        print(img1, ' ', img2)


    return similarityAverageHash, similarityDHash, similarityPHash, similarity


def similarityName(name1,name2):
    Ratio = lev.ratio(name1.lower(),name2.lower())
    return Ratio

def similarityFace(img1, img2):

    try:
        enco1, enco2 = imageFace.findFace(img1,img2)
    except Exception:
        return 0
    if (enco1 != []) and (enco2 != []):
        similarity = imageFace.similarityImageTakeEncoding(enco1,enco2)
    else:
        similarity = 0

    similarity = round(similarity, 5)

    return similarity



