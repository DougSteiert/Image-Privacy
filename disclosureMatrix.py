import networkx as nx
import time, math
import ast

startTime = time.time()

socialNetwork = {}
allPeople = []

firstOrderShares = {}

totalLines = 0
with open("rem_friends/facebook_70_rem.txt") as f:
    firstPerson = True
    for line in f:
        totalLines += 1
        (key, value) = line.split('{')
        if key == str(-1):
            pass
        else:
            if firstPerson:
                allPeople.append(key)
                firstPerson = False
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
    # if person not in allPeople:
    #     allPeople.append(person)
    for theGoods in theList:
        for friend in theGoods:
            # if friend not in allPeople:
            #     allPeople.append(friend)
            dgraph.add_edge(str(person), str(friend))

# The total amount of people within the network, used later for looping
totalPeople = len(allPeople)


# nx.write_graphml(dgraph, "twitter.graphml")

# Compute the probability score between somePerson and aFriend based on existing parents array
def computeScore(somePerson, aFriend, parentsList, propaChain):
    sharesToPerson = 0
    sharesToFriend = 0

    for theLists in socialNetwork[somePerson]:
        for friend, (originalSender, directSender, sentShares, origShares) in theLists.items():
            friend = str(friend)
            originalSender = str(originalSender)
            directSender = str(directSender)
            if friend == aFriend and (originalSender in propaChain) and (directSender == somePerson):
                sharesToFriend = sentShares
                sharesToPerson = origShares

    if sharesToPerson != 0:
        probability = float(sharesToFriend) / float(sharesToPerson)
    else:
        probability = 0

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


def computeChild(mainPerson, newFriend, probMatrix, parentsList, parents, propagationChain):
    holdList = []
    for someParent in parentsList[newFriend]:
        if someParent in parents:
            holdList.append(someParent)

    mainCalc = False

    if mainPerson in holdList:
        while holdList:
            aParent = holdList.pop(0)
            if aParent != mainPerson and mainCalc == False:
                holdList.append(aParent)
                pass
            else:
                score = computeScore(aParent, newFriend, parentsList, propagationChain)
                mainCalc = True

                if newFriend in probMatrix[mainPerson]:
                    if aParent == mainPerson:
                        scoreToUse = 1
                    else:
                        if aParent in probMatrix[mainPerson]:
                            scoreToUse = probMatrix[mainPerson][aParent]
                        else:
                            scoreToUse = 1
                    probMatrix[mainPerson][newFriend] = (probMatrix[mainPerson][newFriend] * (1 - scoreToUse * score))
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
                    miniProbability[newFriend] = (1 * (1 - score * scoreToUse))
                    probMatrix[mainPerson].update(miniProbability)
    else:
        while holdList:
            aParent = holdList.pop(0)
            score = computeScore(aParent, newFriend, parentsList, propagationChain)

            if newFriend in probMatrix[mainPerson]:
                if aParent == mainPerson:
                    scoreToUse = 1
                else:
                    if aParent in probMatrix[mainPerson]:
                        scoreToUse = probMatrix[mainPerson][aParent]
                    else:
                        scoreToUse = 1
                probMatrix[mainPerson][newFriend] = (probMatrix[mainPerson][newFriend] * (1 - score * scoreToUse))
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
                miniProbability[newFriend] = (1 * (1 - score * scoreToUse))
                probMatrix[mainPerson].update(miniProbability)

    if newFriend in socialNetwork[mainPerson]:
        probMatrix[mainPerson][newFriend] = 1
    else:
        probMatrix[mainPerson][newFriend] = 1 - probMatrix[mainPerson][newFriend]
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
def calculateProb(someone, firstFriends, probMatrix, parents, averageTime):
    parents[someone] = True
    friendsParents = {}
    propChain = []
    propChain.append(someone)
    numUsersToShare = len(firstFriends)

    # for aFriend in firstFriends:
    #     if numUsersToShare > 0:
    #         probMatrix[someone][aFriend] = 1
    #         numUsersToShare -= 1
    #         parents[aFriend] = True
    #
    #         if aFriend in socialNetwork:
    #             for listsOfStuff in socialNetwork[aFriend]:
    #                 for aNewFriend, (ori, dire, sentSh, oriSh) in listsOfStuff.items():
    #                     if aNewFriend == aFriend:
    #                         pass
    #                     else:
    #                         firstFriends.append(aNewFriend)
    #     else:
    #         break

    while firstFriends:
        loopBegin = time.time()
        friend = str(firstFriends.pop(0))
        propChain.append(friend)
        skipReady = False
        if friend not in friendsParents:
            temp = []
            for eachPred in dgraph.predecessors(friend):
                if eachPred != friend:
                    temp.append(eachPred)
            friendsParents[friend] = temp

        # if friend in socialNetwork:
        #     for listsOfStuff in socialNetwork[friend]:
        #         for aNewFriend, (ori, dire, sentSh, oriSh) in listsOfStuff.items():
        #             if aNewFriend == friend:
        #                 pass
        #             elif aNewFriend in parents and parents[aNewFriend] == True:
        #                 pass
        #             elif aNewFriend not in firstFriends:
        #                 firstFriends.append(aNewFriend)

        skipParent = False

        if friend in parents:
            if parents[friend] is True:
                skipParent = True

        isReady = checkParents(friend, parents, friendsParents)
        alreadyComputed = False
        if isReady:
            computeChild(someone, friend, probMatrix, friendsParents, parents, propChain)
            alreadyComputed = True

        if not skipParent:
            if friend in socialNetwork:
                for listsOfPeople in socialNetwork[friend]:
                    for newFriend, (origin, direct, sentShares, origShares) in listsOfPeople.items():
                        newFriend = str(newFriend)
                        if newFriend == friend:
                            pass
                        elif newFriend in parents and parents[newFriend] == True:
                            pass
                        elif newFriend in firstFriends and newFriend in dgraph.predecessors(friend):
                            temp2 = []
                            for eachPred in dgraph.predecessors(newFriend):
                                if eachPred != newFriend:
                                    temp2.append(eachPred)
                            friendsParents[newFriend] = temp2
                            computeChild(someone, newFriend, probMatrix, friendsParents, parents, propChain)
                            if dgraph.successors(newFriend):
                                for eachSuccessor in dgraph.successors(newFriend):
                                    if eachSuccessor == newFriend:
                                        pass
                                    elif eachSuccessor not in firstFriends:
                                        if eachSuccessor in parents:
                                            if parents[eachSuccessor] == True:
                                                pass
                                        else:
                                            firstFriends.append(eachSuccessor)
                                            propChain.append(eachSuccessor)
                            skipReady = True
                        elif newFriend not in firstFriends:
                            firstFriends.append(newFriend)
                            propChain.append(newFriend)
                            if dgraph.successors(newFriend):
                                parents[newFriend] = False
                                for eachSuccessor in dgraph.successors(newFriend):
                                    if eachSuccessor == newFriend:
                                        pass
                                    elif eachSuccessor not in firstFriends:
                                        if eachSuccessor in parents:
                                            if parents[eachSuccessor] == True:
                                                pass
                                        else:
                                            firstFriends.append(eachSuccessor)
                                            propChain.append(eachSuccessor)
            if skipReady:
                isReady = False
                averageTime.append(time.time() - loopBegin)
                pass
            else:
                isReady = checkParents(friend, parents, friendsParents)
                averageTime.append(time.time() - loopBegin)
        if isReady and not alreadyComputed:
            computeChild(someone, friend, probMatrix, friendsParents, parents, propChain)
            isReady = False
            averageTime.append(time.time() - loopBegin)
        elif skipParent:
            averageTime.append(time.time() - loopBegin)
            pass
        elif alreadyComputed:
            pass
        else:
            firstFriends.append(friend)
            averageTime.append(time.time() - loopBegin)


preprocessTime = (time.time() - startTime)
afterTime = time.time()

loop = 1
finalProbMatrix = {}
averageTime = []
for person in allPeople:
    print loop, person
    loop += 1
    priorityQueue = []
    finalProbMatrix[person] = {}
    parents = {}
    if person in socialNetwork:
        for listsOfInfo in socialNetwork[person]:
            for theFriend, (origin, direct, sent, orig) in listsOfInfo.items():
                theFriend = str(theFriend)
                if theFriend != person and (theFriend not in priorityQueue):
                    priorityQueue.append(theFriend)
                if dgraph.successors(theFriend):
                    parents[theFriend] = False

        finalProbMatrix[person][person] = 1
        calculateProb(person, priorityQueue, finalProbMatrix, parents, averageTime)

calcTime = (time.time() - afterTime)

avgTime = 0
totalAvg = 0
for eachItem in averageTime:
    totalAvg += eachItem
avgTime = (totalAvg / len(averageTime))

print "Preprocess: ", preprocessTime
print "Calculate Prob: ", calcTime
print "Avg Person: ", avgTime

removedPeople = ["483", "896", "941", "969", "1014", "1020", "1099", "1108", "1170", "1215", "1245", "1261", "1303", "1324",
                 "1396", "1427", "1454", "1495", "1503", "1582", "1591", "1638", "1661", "1706", "1732", "1742", "1751",
                 "1812", "1848", "1893", "1907", "596", "919", "954", "1018", "1067", "1086", "1104", "1192", "1235", "1273",
                 "1281", "1309", "1373", "1406", "1473", "1502", "1595", "1649", "1729", "1783", "1824", "1871", "917",
                 "971", "1066", "1102", "1204", "1247", "1316", "1429", "1489", "1704", "1786", "1828", "1894", "942",
                 "1081", "1227", "1277"]
probs = []

for person in removedPeople:
    if person in finalProbMatrix["1032"]:
        probs.append(finalProbMatrix["1032"][person])
    else:
        probs.append(0)

sum = 0
for num in probs:
    sum += num

print "Average Prob: " + str(float(sum/len(probs)))
dgraph2 = nx.DiGraph()

thePerson = allPeople.pop(0)
# Create a directed graph between all people in the social network
for person, theList in socialNetwork.iteritems():
    for theGoods in theList:
        for friend in theGoods:
            if str(friend) in finalProbMatrix[thePerson]:
                dgraph2.add_edge(str(person), str(friend), weight=finalProbMatrix[thePerson][str(friend)])

nx.write_graphml(dgraph2, "rem70.graphml")