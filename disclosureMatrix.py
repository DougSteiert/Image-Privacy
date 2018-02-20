import networkx as nx
import time
import ast

startTime = time.time()

socialNetwork = {}
allPeople = []

firstOrderShares = {}

with open("TestNetwork.txt") as f:
    for line in f:
        (key, value) = line.split('{')
        # (person, shares) = key.split(' ')
        newValue = '{' + value
        newValue = newValue.rstrip()
        newDict = ast.literal_eval(newValue)
        if key in socialNetwork:
            if key in newDict:
                del newDict[key]
            for newKey, (origin, sender, sentShares, origShares) in newDict.iteritems():
                newerDict = {}
                newerDict[newKey] = (origin, sender, sentShares, origShares)
                socialNetwork[key].append(newDict)
        else:
            socialNetwork[key] = []
            for newKey, (origin, sender, sentShares, origShares) in newDict.iteritems():
                newerDict = {}
                newerDict[newKey] = (origin, sender, sentShares, origShares)
                socialNetwork[key].append(newerDict)

shareNetwork = {}

# # Create a share network, similar to the social network, but for easier access to get shares to people
# for person, theList in socialNetwork.iteritems():
#     if person not in allPeople:
#         allPeople.append(person)
#     directConnections = {}
#     for theGoods in theList:
#         for friend, (origin, direct, sentShares, origShares) in theGoods.items():
#             if friend == person:
#                 firstOrderShares[person] = origShares
#             if friend not in allPeople:
#                 allPeople.append(friend)
#             directConnections[friend] = sentShares
#     shareNetwork[person] = directConnections

dgraph = nx.DiGraph()

# Create a directed graph between all people in the social network
for person, theList in socialNetwork.iteritems():
    if person not in allPeople:
        allPeople.append(person)
    for theGoods in theList:
        for friend in theGoods:
            if friend not in allPeople:
                allPeople.append(friend)
            dgraph.add_edge(person, friend)

# The total amount of people within the network, used later for looping
totalPeople = len(allPeople)

# nx.write_graphml(dgraph, "twitter.graphml")

# Compute the probability score between somePerson and aFriend based on existing parents array
def computeScore(somePerson, aFriend, parentsList):
    sharesToPerson = 0
    sharesToFriend = 0

    for theLists in socialNetwork[somePerson]:
        for friend, (originalSender, directSender, sentShares, origShares) in theLists.items():
            if friend == aFriend:
                sharesToFriend = sentShares
                sharesToPerson = origShares

    if somePerson in firstOrderShares and origin == somePerson:
        probability = float(sharesToFriend)/(float(firstOrderShares[somePerson]))
    else:
        probability = float(sharesToFriend)/float(sharesToPerson)

    return probability


# Check if the parents of mainFriend have already been computed, so that mainFriend may be computed
def checkParents(mainFriend, parentsMap, parentsList):
    allComputed = False
    for parent in parentsList[mainFriend]:
        if parent in parentsMap and parentsMap[parent] is True:
            allComputed = True
        elif parent in parentsMap and parentsMap[parent] is False:
            allComputed = False
            break

    return allComputed


def computeChild(mainPerson, newFriend, probMatrix, parentsList, parents):
    for aParent in parentsList[newFriend]:
        if aParent in parents:
            score = computeScore(aParent, newFriend, parentsList)

            if newFriend in probMatrix[mainPerson]:
                if aParent == mainPerson:
                    scoreToUse = 1
                else:
                    if aParent in probMatrix[mainPerson]:
                        scoreToUse = probMatrix[mainPerson][aParent]
                    else:
                        scoreToUse = 1
                probMatrix[mainPerson][newFriend] = (scoreToUse * (1 - score))
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
                miniProbability[newFriend] = (scoreToUse * (1 - score))
                probMatrix[mainPerson].update(miniProbability)

    parents[newFriend] = True

def checkParentsTwo(theProbMatrix, parentsList, mainFriend, theChild, priQ):
    numReady = 0
    for parent in parentsList[theChild]:
        priQ.append(parent)
        if parent in theProbMatrix[mainFriend]:
            numReady += 1
        elif parent == theChild:
            numReady += 1

    return numReady

def expansionRoutine(friend, firstFriends, friendsParents):
    friendsFriends = dgraph.successors(friend)

    for successor in friendsFriends:
        if not successor in firstFriends and (successor != friend):
            firstFriends.append(successor)
            friendsParents[successor] = dgraph.predecessors(successor)

# Calculates the probability of someone and all their friends
def calculateProb(someone, firstFriends, probMatrix, parents):
    parents[someone] = True
    friendsParents = {}

    while firstFriends:
        for friend in firstFriends:
            if friend not in friendsParents:
                temp = []
                for eachPred in dgraph.predecessors(friend):
                    if eachPred != friend:
                        temp.append(eachPred)
                friendsParents[friend] = temp
            # numberParentsCalc = checkParentsTwo(probMatrix, friendsParents, someone, friend, priorityQueue)
            #
            # if numberParentsCalc == len(friendsParents[friend]):
            #     computeChild(someone, friend, probMatrix, friendsParents)
            #     firstFriends.remove(friend)
            # expansionRoutine(friend, firstFriends, friendsParents)

            if friend in parents:
                if parents[friend] is True:
                        firstFriends.remove(friend)
                        break

            if friend in socialNetwork:
                for listsOfPeople in socialNetwork[friend]:
                    for newFriend, (origin, direct, sentShares, origShares) in listsOfPeople.items():
                        if newFriend == friend:
                            pass
                        elif newFriend in parents and parents[newFriend] is True:
                            pass
                        elif newFriend in firstFriends and newFriend in dgraph.predecessors(friend):
                            computeChild(someone, newFriend, probMatrix, friendsParents, parents)
                        elif newFriend not in firstFriends:
                            firstFriends.append(newFriend)
                            if dgraph.successors(newFriend):
                                parents[newFriend] = False
                                for eachSuccessor in dgraph.successors(newFriend):
                                    if eachSuccessor not in firstFriends:
                                        firstFriends.append(eachSuccessor)
                                    elif eachSuccessor in firstFriends:
                                        computeChild(someone, eachSuccessor, probMatrix, friendsParents, parents)


            # if friend in parents:
            #     if parents[friend] is True:
            #         firstFriends.remove(friend)
            #         break
            # if friend in socialNetwork:
            #     for otherFriend, junk in socialNetwork[friend].iteritems():
            #         if otherFriend in parents and parents[otherFriend] is True:
            #             pass
            #         elif otherFriend in firstFriends and otherFriend in dgraph.predecessors(friend):
            #             computeChild(someone, otherFriend, probMatrix, parents, firstFriends)
            #         elif otherFriend not in firstFriends:
            #             firstFriends.append(otherFriend)
            #             if dgraph.successors(otherFriend):
            #                 parents[otherFriend] = False
            #                 for eachSuccessor in dgraph.successors(otherFriend):
            #                     if eachSuccessor not in firstFriends:
            #                         firstFriends.append(eachSuccessor)
            #                     elif eachSuccessor in firstFriends:
            #                         computeChild(someone, eachSuccessor, probMatrix, parents, firstFriends)

            isReady = checkParents(friend, parents, friendsParents)
            if isReady:
                computeChild(someone, friend, probMatrix, friendsParents, parents)
                firstFriends.remove(friend)

loop = 1
finalProbMatrix = {}
for person in allPeople:
    print loop, person
    loop += 1
    priorityQueue = []
    finalProbMatrix[person] = {}
    parents = {}
    if person in socialNetwork:
        for listsOfInfo in socialNetwork[person]:
            for theFriend, (origin, direct, sent, orig) in listsOfInfo.items():
                if theFriend != person and (theFriend not in priorityQueue):
                    priorityQueue.append(theFriend)
                if dgraph.successors(theFriend):
                    parents[theFriend] = False

        finalProbMatrix[person][person] = 1
        calculateProb(person, priorityQueue, finalProbMatrix, parents)
    # else:
    #     finalProbMatrix[person] = {}

print (time.time() - startTime)

print finalProbMatrix