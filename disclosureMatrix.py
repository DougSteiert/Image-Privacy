import networkx as nx
import time

startTime = time.time()

socialNetwork = {}
allPeople = []

firstOrderShares = {}

with open("RealSocialNetwork.txt") as f:
    for line in f:
        (key, value) = line.split('{')
        (person, shares) = key.split(' ')
        newValue = '{' + value
        firstOrderShares[person] = shares
        socialNetwork[person] = eval(newValue)

shareNetwork = {}

# Create a share network, similar to the social network, but for easier access to get shares to people
for person, connection in socialNetwork.iteritems():
    if person not in allPeople:
        allPeople.append(person)
    directConnections = {}
    for friend, (relation, shares) in connection.iteritems():
        if friend not in allPeople:
            allPeople.append(friend)
        directConnections[friend] = shares
    shareNetwork[person] = directConnections

# The total amount of people within the network, used later for looping
totalPeople = len(allPeople)

dgraph = nx.DiGraph()

# Create a directed graph between all people in the social network
for person, info in socialNetwork.iteritems():
    for friend, (relation, shares) in info.iteritems():
        dgraph.add_edge(person, friend)

# nx.write_graphml(dgraph, "twitter.graphml")

# Compute the probability score between somePerson and aFriend based on existing parents array
def computeScore(somePerson, aFriend, parentsList):
    sharesToPerson = 0
    sharesToFriend = 0

    for acq, info in shareNetwork.iteritems():
        if acq in parentsList:
            for person, shares in info.iteritems():
                if person == somePerson:
                    sharesToPerson += shares

    if aFriend in shareNetwork[somePerson]:
        sharesToFriend = shareNetwork[somePerson][aFriend]

    if sharesToPerson == 0 and somePerson in firstOrderShares:
        probability = float(sharesToFriend)/(float(firstOrderShares[somePerson]))
    else:
        probability = float(sharesToFriend)/float(sharesToPerson)

    return probability


# Check if the parents of mainFriend have already been computed, so that mainFriend may be computed
def checkParents(mainFriend, parentsMap):
    allComputed = False
    for parent in dgraph.predecessors(mainFriend):
        if parent in parentsMap and parentsMap[parent] is True:
            allComputed = True
        elif parent in parentsMap and parentsMap[parent] is False:
            allComputed = False
            break

    return allComputed


def computeChild(mainPerson, newFriend, probMatrix, parentsList, friendsList):
    for aParent in dgraph.predecessors(newFriend):
        if aParent in parentsList:
            score = computeScore(aParent, newFriend, parentsList)

            if newFriend in probMatrix[mainPerson]:
                if aParent == mainPerson:
                    scoreToUse = 1
                else:
                    if aParent in probMatrix[mainPerson]:
                        scoreToUse = probMatrix[mainPerson][aParent]
                    else:
                        scoreToUse = 1
                probMatrix[mainPerson][newFriend] += (scoreToUse * score)
                if probMatrix[mainPerson][newFriend] > 1:
                    probMatrix[mainPerson][newFriend] = 1
            else:
                miniProbability = {}
                if aParent == mainPerson:
                    scoreToUse = 1
                else:
                    if aParent in probMatrix[mainPerson]:
                        scoreToUse = probMatrix[mainPerson][aParent]
                    else:
                        scoreToUse = 1
                miniProbability[newFriend] = scoreToUse * score
                probMatrix[mainPerson].update(miniProbability)

    parentsList[newFriend] = True


# Calculates the probability of someone and all their friends
def calculateProb(someone, firstFriends, probMatrix, parents):
    parents[someone] = True

    while firstFriends:
        for friend in firstFriends:
            if friend in parents:
                if parents[friend] is True:
                    firstFriends.remove(friend)
                    break
            if friend in socialNetwork:
                for otherFriend, junk in socialNetwork[friend].iteritems():
                    if otherFriend in parents and parents[otherFriend] is True:
                        pass
                    elif otherFriend in firstFriends and otherFriend in dgraph.predecessors(friend):
                        computeChild(someone, otherFriend, probMatrix, parents, firstFriends)
                    elif otherFriend not in firstFriends:
                        firstFriends.append(otherFriend)
                        if dgraph.successors(otherFriend):
                            parents[otherFriend] = False
                            for eachSuccessor in dgraph.successors(otherFriend):
                                if eachSuccessor not in firstFriends:
                                    firstFriends.append(eachSuccessor)
                                elif eachSuccessor in firstFriends:
                                    computeChild(someone, eachSuccessor, probMatrix, parents, firstFriends)
                                
            isReady = checkParents(friend, parents)
            if isReady:
                computeChild(someone, friend, probMatrix, parents, firstFriends)
                firstFriends.remove(friend)

loop = 1
finalProbMatrix = {}
for person in allPeople:
    if person is "58":
        # print loop, person
        # loop += 1
        friends1 = []
        finalProbMatrix[person] = {}
        parents = {}
        if person in socialNetwork:
            for friend, info in socialNetwork[person].iteritems():
                friends1.append(friend)
                if dgraph.successors(friend):
                    parents[friend] = False

            calculateProb(person, friends1, finalProbMatrix, parents)
        else:
            finalProbMatrix[person] = {}
        break

print (time.time() - startTime)

print finalProbMatrix