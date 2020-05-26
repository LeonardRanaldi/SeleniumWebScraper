import compareImageName
import writeAndReadFile
import statisticheFile
import nameSimilarityMetrics
import imageClassificatorLR
import textSimilarity
import countryAndGender
import collections
import imageClassificatorDT
import time
import types
import random
import image_similarity.SIFT as sift



#taking two complete dataset we want create third dataset where there are features values of of the first two datasets. We use defaultdict for save values.
def buildDatasetTwoSocial_TW_FB(tw, fb):


    dictTw = writeAndReadFile.readFileNOprint(tw)
    dictFb = writeAndReadFile.readFileNOprint(fb)
    d = collections.defaultdict(dict)

    listKeyFb = []
    listKeyTw = []

    numImg = 0

#half set for maching profiles
    for key, value in dictTw.items():

        listKeyTw.append(key)

        if key in dictFb:
            el1 = value[0]
            el2 = dictFb[key][0]
				#we use twitter screen name for index of dict
            if ('url' in el1) and (len(el1['url']) > 1) and ('twitter.com' in el1['url'] ):

                print(el1['url'])

                nameRow = el1['url'].split("twitter.com/")[1]
                nameRow = nameRow.split("?")[0]
                nameRow = nameRow.replace("/", "")
            else:
                nameRow = key


            #sim names
            compareName = 0
            if ('name' in el1) and ('name' in el2):
                compareName = nameSimilarityMetrics.similarity(el1['name'], el2['name'])
                compareName1 = nameSimilarityMetrics.similarity_Levenshtein(el1['name'],el2['name']) 
                compareName2 = nameSimilarityMetrics.DistJaccard(el1['name'],el2['name'])
                compareName3 = nameSimilarityMetrics.lcs(el1['name'],el2['name'])
                #print(el1['name'],'..', el2['name'],'..',compare)
            d.setdefault(nameRow, []).append(compareName1)
            d.setdefault(nameRow, []).append(compareName2)
            d.setdefault(nameRow, []).append(compareName3)

            #sim img
            predictedProbs1  = 0
            if ('posImg' in el1) and ('posImg' in el2):
                numImg = numImg +1
                img1 = el1['posImg']
                img2 = el2['posImg']
                sim1, sim2, sim3, sim4 = compareImageName.similarityImage(img1, img2)
                faceReco = compareImageName.similarityFace(img1, img2)
                siftSim = sift.compare_images_SIFT(img1, img2)
                #predictedProbs1, predictedProbs0 = imageClassificatorDT.predictProbClass(sim1, sim2, sim3, sim4)
            d.setdefault(nameRow, []).append(predictedProbs1)
            d.setdefault(nameRow, []).append(sim1)
            d.setdefault(nameRow, []).append(sim2)
            d.setdefault(nameRow, []).append(sim3)
            d.setdefault(nameRow, []).append(sim4)
            d.setdefault(nameRow, []).append(siftSim)

            #print(predictedProbs1)
            #print(sim1, sim2)

            # sim country
            compareCountry = 0
            if ('country' in el1) and ('country' in el2):
                country1 = el1['country']
                country2 = el2['country']
                countryList1 = statisticheFile.findCountry(country1)
                countryList2 = statisticheFile.findCountry(country2)
                compareCountry = statisticheFile.compareCountry(countryList1, countryList2)
                #print(key,' ...',countryList1,'...',countryList2,'...',compareCountry)

            d.setdefault(nameRow, []).append(compareCountry)

            #sim gender
            compareGender = 0
            if ('gender' in el1) and ('gender' in el2):
                if el1['gender'] == el2['gender']:
                    compareGender = 1
                else:
                    compareGender = 0
                #print(key,' ...', el1['gender'], '...', el2['gender'], '...',compareGender )

            d.setdefault(nameRow, []).append(compareGender)

        #######################################################
            lable = 1
            d.setdefault(nameRow, []).append(lable)

#profiles that non match
    for key, value in dictFb.items():
        listKeyFb.append(key)

    listKeyFb = list(set(listKeyFb))
    listKeyTw = list(set(listKeyTw))
    lenListKeyFb = len(listKeyFb)

    for i in range(0,lenListKeyFb-1):

        keyFb = listKeyFb[i]
        keyTw = listKeyTw[i]

        if keyFb == keyTw:
            keyTw = listKeyTw[i+1]

        nameRow = keyFb+'_'+keyTw


        if (keyFb in dictFb) and (keyTw in dictTw):
            el1 = dictTw[keyTw][0]
            el2 = dictFb[keyFb][0]

           # sim names
            compareName = 0
            if ('name' in el1) and ('name' in el2):
                compareName = nameSimilarityMetrics.similarity(el1['name'], el2['name'])
                compareName1 = nameSimilarityMetrics.similarity_Levenshtein(el1['name'], el2['name'])
                compareName2 = nameSimilarityMetrics.DistJaccard(el1['name'], el2['name'])
                compareName3 = nameSimilarityMetrics.lcs(el1['name'], el2['name'])
                # print(el1['name'],'..', el2['name'],'..',compare)
            d.setdefault(nameRow, []).append(compareName1)
            d.setdefault(nameRow, []).append(compareName2)
            d.setdefault(nameRow, []).append(compareName3)

            # sim img
            predictedProbs1 = 0
            if ('posImg' in el1) and ('posImg' in el2):
                numImg = numImg + 1
                img1 = el1['posImg']
                img2 = el2['posImg']
                sim1, sim2, sim3, sim4 = compareImageName.similarityImage(img1, img2)
                siftSim = sift.compare_images_SIFT(img1, img2)
                faceReco = compareImageName.similarityFace(img1, img2)
                predictedProbs1, predictedProbs0 = imageClassificatorDT.predictProbClass(sim1, sim2, sim3, sim4)
            d.setdefault(nameRow, []).append(sim1)
            d.setdefault(nameRow, []).append(sim2)
            d.setdefault(nameRow, []).append(sim3)
            d.setdefault(nameRow, []).append(sim4)
            d.setdefault(nameRow, []).append(siftSim)

            # sim country
            compareCountry = 0
            if ('country' in el1) and ('country' in el2):
                country1 = el1['country']
                country2 = el2['country']
                countryList1 = statisticheFile.findCountry(country1)
                countryList2 = statisticheFile.findCountry(country2)
                compareCountry = statisticheFile.compareCountry(countryList1, countryList2)
                # print(key,' ...',countryList1,'...',countryList2,'...',compareCountry)

            d.setdefault(nameRow, []).append(compareCountry)

            # metrica similarità gender
            compareGender = 0
            if ('gender' in el1) and ('gender' in el2):
                if el1['gender'] == el2['gender']:
                    compareGender = 1
                else:
                    compareGender = 0
                # print(key,' ...', el1['gender'], '...', el2['gender'], '...',compareGender )

            d.setdefault(nameRow, []).append(compareGender)


            # #########################################################

            lable = 0
            d.setdefault(nameRow, []).append(lable)


    #write file in default dict
    #writeAndReadFile.writeFile(d, 'dataset_Twitter_Facebook')

    return d

#example
#buildDatasetTwoSocial_TW_FB('twitter.json','facebook.json')



