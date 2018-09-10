import numpy as np
from scipy.optimize import minimize

"""
    cascadeList: timestamp in minute, each cascade has at least 50 retweets
    windows: 50
    # of pattern: 9
"""

# evolving function
def evolving(alpha, beta, gamma, h1, h2, h3, cascade):
    """
    alpha, beta, gamma: parameters for each pattern: float
    h1(influence), h2(attractiveness), h3(potentiality): for each cascade: float
    pattern: timestamp list of each cascade
    formula: h1*(gamma+e^(-alpha*tj))+h2*sigma(evolving(tp)*e^(-beta(tj-tp)))
                + h3*(evolving(tj)-evolving(tj-1))
    """
    if len(cascade)==0:
        return 0
    elif len(cascade)==1:
        return 1
    else:
        temp = 0
        for i,timestamp in enumerate(cascade[:-1]):
            temp += evolving(alpha, beta, gamma, h1, h2, h3, cascade[:,-i])
                    *np.exp(-beta*(cascade[-1]-cascade[-i-1]))
        return float(h1*(gamma+np.exp(-alpha*cascade[-1]))+h2*temp
                -h3*evolving(alpha, beta, gamma, h1, h2, h3, cascade[:,-1]))/(1-h3)

# get pattern
def getPattern(cascade):
    """
        cascade is a list of timestamp
    """
    return [i for i in range(1,len(cascade)+1,1)]/float(len(cascade))

# k-means
def kMeans(cascadeList, windows=50, pNum=9):
    """
        windows: 50, can be tailored for specifical case
        return: index of cluster
    """
    # get pattern
    tempPattern = []
    for cascade in cascadeList:
        tempPattern.append(getPattern(cascade))

    # tailored to fixed windows
    tempPattern2 = []
    for pattern in tempPattern:
        selectList = [(len(pattern)-1)*i/windows for i in range(1,windows+1,1)]
        tempPattern2.append(pattern[selectList])

    # k-means
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=pNum, random_state=0).fit(np.array(tempPattern2))
    return kmeans.labels_


# square loss for each cascade
def squareLoss(alpha, beta, gamma, h1, h2, h3, cascade):
    """
        square loss:
            from 1 to ne: sigma((Ae(tj)-AeStar(tj))^2/AeStar(tj)^2)
    """
    loss = 0
    for num in range(len(pattern)):
        loss += (evolving(alpha, beta, gamma, h1, h2, h3, pattern[:-num])-(len(pattern)-num))^2/(len(pattern)-num)^2

# minimization
def minimization(cascadeList, pNum=9):
    """
        cascadeList: list of cascade pattern
        pNum: number of patterns
        alphaList: list of alpha for N patterns
        betaList: list of beta for N patterns
        gammaList: list of gamma for N patterns
        h1List: list of h1 for each cascade
        h2List: list of h2 for each cascade
        h3List: list of h3 for each cascade
    """
    # initialize, parameters
    alphaList = (np.arange(pNum)+1)/10.0
    betaList = (np.arange(pNum)+1)/10.0
    gammaList = (np.arange(pNum)+1)/10.0
    h1List = np.random.rand(len(cascadeList))
    h2List = np.random.rand(len(cascadeList))
    h3List = np.random.rand(len(cascadeList))

    # get cluster index
    clusterIndex = kMeans(cascadeList)
    result = optimize.minimize(func, [alphaList, betaList, gammaList, h1List,
            h2List, h3List, clusterIndex, cascadeList])
    return result

# optimization func
def func(x):
    """
        optimization func
    """
    alphaList, betaList, gammaList, h1List, h2List, h3List, clusterIndex, cascadeList = x

    Loss = 0
    for i,cascade in enumerate(cascadeList):
        Loss += squareLoss(alphaList[clusterIndex[i]], betaList[clusterIndex[i]], gammaList[clusterIndex[i]],
                    h1List[i], h2List[i], h3List[i], cascade)
    return Loss
