import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein as lev

#Edit based
def similarityName(name1,name2):

    #Distance = lev.distance(name1.lower(),name2.lower()),
    try:
        Ratio = lev.ratio(name1.lower(),name2.lower())
    except Exception:
        Ratio = 0
    return Ratio

#Token based
def DistJaccard(str1, str2):
    try:
        str1 = set(str1.split())
        str2 = set(str2.split())
        distJAccard = float(len(str1 & str2)) / len(str1 | str2)
    except Exception:
        distJAccard = 0
    return distJAccard

#Sequence based longest common subsequence similarity
#Ratcliff-Obershelp similarity

def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
    L = [[None] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]



# print(lcs('dario rui','dario rui'))
# print(DistJaccard('dario rui','dario rui'))
# print(similarityName('dario rui','dario rui'))


def similarity(str1, str2):

    lenStr1 = len(str1)

    firstMetric = lcs(str1, str2)
    secondMetric = DistJaccard(str1, str2)
    thirdMetric = similarityName(str1, str2)

    # vectors
    a = np.array([lenStr1, 1.0, 1.0])
    b = np.array([firstMetric, secondMetric, thirdMetric])

    # use library, operates on sets of vectors
    aa = a.reshape(1, 3)
    ba = b.reshape(1, 3)
    cos_lib = cosine_similarity(aa, ba)

    result =  np.asscalar(cos_lib)
    result = round(result, 3)
    return result


#print(similarity('tario rui','dario rui'))

def similarity_Levenshtein(str1, str2):
    lev = similarityName(str1, str2)
    return lev



#print(similarity_Levenshtein(m1,m2))
