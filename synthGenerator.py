import random

numUsers = 200
maxShare = 500

# lines = open('names.txt').read().splitlines()

people = []

relationships = {"None": 0, "Co-worker": 1, "Friend": 2, "Family": 3, "Close Friend": 4, "Close Family": 5}

# oneMillLines = open("onemill.txt").read().splitlines()
#
# for x in range(1, numUsers + 1):
#     myline = random.choice(oneMillLines)
#     people.append(myline)
#
# socialNetwork = {}
#
# for person in people:
#     socialNetwork[person] = {}

def share(mainPerson, level, socNetwork, previousFriend, friendsList, origShares, origSender, sharedPpl):
    numberFriends = 0
    if mainPerson in friendsList:
        for someFriend in friendsList[mainPerson]:
            numberFriends += 1
    if level >= 2 or numberFriends < 1 or (mainPerson is origSender and mainPerson in sharedPpl):
        pass
    else:
        if mainPerson not in origShares:
            pass
        else:
            for friend in friendsList[mainPerson]:
                if friend is not previousFriend and friend is not origSender:
                    randShare = random.randint(0, origShares[mainPerson])
                    # relationToUse = "Close Friend"
                    socNetwork[mainPerson][friend] = (origSender, mainPerson, randShare, origShares[mainPerson])
                    origShares[friend] = randShare
            textFile.write(mainPerson)
            # if mainPerson in origShares:
            #     textFile.write(" " + str(origShares[mainPerson]))
            textFile.write(str(socNetwork[mainPerson]))
            textFile.write('\n')
            sharedPpl.append(mainPerson)
            for friend in friendsList[mainPerson]:
                if friend is not previousFriend and friend is not origSender:
                    (origin, direct, receivedShares, directShares) = socNetwork[mainPerson][friend]
                    share(friend, level+1, socNetwork, mainPerson, friendsList, origShares, origSender, sharedPpl)

# friends = {}
#
# for person in people:
#     numFriends = 10
#     tempFriends = []
#     lines = open('onemill.txt').read().splitlines()
#     for _ in range(0, numFriends):
#         friend = random.choice(lines)
#         while friend in tempFriends or friend is person:
#             friend = random.choice(lines)
#         tempFriends.append(friend)
#     friends[person] = tempFriends
#     socialNetwork[person] = {}
#
# textFile = open("SynthSocialNetwork.txt", "w")
# sharedFakePeople = []
# for person in people:
#     level = 0
#     previousPerson = ""
#     share(person, maxShare, level, previousPerson, friends, sharedFakePeople)

# textFile.close()

textFile = open("TestNetwork.txt", "w")
socialNetwork = {}

# uncomment if using real set
numShared = 0
realPeople = []
realFriends = {}
realSet = open("test.txt", "r")
originalShares = {}
randCoin = 0
for line in realSet:
    first = True
    firstPerson = ""
    tempRealFriends = []
    for word in line.split():
        if first:
            if not isinstance(word, str):
                if word in socialNetwork:
                    if numShared < 1:
                        originalShares[word] = random.randint(0, maxShare)
                        firstPerson = word
                        socialNetwork[word][word] = (word, '#', originalShares[word], originalShares[word])
                        first = False
                        numShared += 1
                    else:
                        firstPerson = word
                        first = False
                else:
                    if numShared < 1:
                        originalShares[word] = random.randint(0, maxShare)
                        firstPerson = word
                        socialNetwork[word] = {}
                        socialNetwork[word][word] = (word, '#', originalShares[word], originalShares[word])
                        first = False
                        numShared += 1
                    else:
                        firstPerson = word
                        first = False
                        socialNetwork[word] = {}
                # else:
                #     if word in socialNetwork:
                #         firstPerson = word
                #         first = False
                #     else:
                #         firstPerson = word
                #         socialNetwork[word] = {}
                #         first = False
                if word not in realPeople:
                    realPeople.append(str(word))
            else:
                if word in socialNetwork:
                    if numShared < 1:
                        originalShares[word] = random.randint(0, maxShare)
                        firstPerson = word
                        socialNetwork[word][word] = (word, '#', originalShares[word], originalShares[word])
                        first = False
                        numShared += 1
                    else:
                        firstPerson = word
                        first = False
                else:
                    if numShared < 1:
                        originalShares[word] = random.randint(0, maxShare)
                        firstPerson = word
                        socialNetwork[word] = {}
                        socialNetwork[word][word] = (word, '#', originalShares[word], originalShares[word])
                        first = False
                        numShared += 1
                    else:
                        firstPerson = word
                        first = False
                        socialNetwork[word] = {}
            if word not in realPeople:
                realPeople.append(str(word))
        else:
            randCoin = random.randint(1,10)
            if randCoin <= 10:
                tempRealFriends.append(word)

    if firstPerson not in realFriends:
        realFriends[firstPerson] = tempRealFriends
    else:
        for eachFriend in tempRealFriends:
            realFriends[firstPerson].append(eachFriend)


loop = 1
sharedPeople = []
for person in realPeople:
    level = 0
    # print loop
    # loop += 1
    previousPerson = ""
    originalSender = person
    share(person, level, socialNetwork, previousPerson, realFriends, originalShares, originalSender, sharedPeople)

textFile.close()