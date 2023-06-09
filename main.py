import random
import pandas as pd
import streamlit as st

def sortScoreList1(scores):
    minIndex = 0
    for rr in range(len(scores)):
        least = scores[rr]
        minIndex = rr
        for q in range(rr + 1, len(scores)):
            if scores[q][0] < least[0] or \
            (scores[q][0] == least[0] and scores[q][1] < least[1]) or \
            (scores[q][0] == least[0] and scores[q][1] == least[1] and scores[q][2] < least[2]) or \
            (scores[q][0] == least[0] and scores[q][1] == least[1] and scores[q][2] == least[3] and scores[q][2] < least[3]) or \
            (scores[q][0] == least[0] and scores[q][1] == least[1] and scores[q][2] == least[3] and scores[q][2] == least[3] and scores[q][4] < least[4]) or \
            (scores[q][0] == least[0] and scores[q][1] == least[1] and scores[q][2] == least[3] and scores[q][2] == least[3] and scores[q][4]  == least[4] and scores[q][5] < least[5]):
                least = scores[q]
                minIndex = q
        replacement = scores[rr]
        scores[rr] = least
        scores[minIndex] = replacement

    return scores

def placement(scoresList, score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore):
    numWon = 0
    numTied = 0
    indexWon = 0
    for l in range(len(scoresList)):
            if scoresList[l][0] > score or (scoresList[l][0] == score and scoresList[l][1] > subscore) or \
                (scoresList[l][0] == score and scoresList[l][1] == subscore and scoresList[l][2] > superSubScore) or \
                (scoresList[l][0] == score and scoresList[l][1] == subscore and scoresList[l][2] ==  superSubScore and scoresList[l][3] > tripleSubScore) or \
                (scoresList[l][0] == score and scoresList[l][1] == subscore and scoresList[l][2] ==  superSubScore and scoresList[l][3] == tripleSubScore and scoresList[l][4] > quadrupleSubScore) or \
                (scoresList[l][0] == score and scoresList[l][1] == subscore and scoresList[l][2] ==  superSubScore and scoresList[l][3] == tripleSubScore and scoresList[l][4] == quadrupleSubScore and scoresList[l][5] > quadrupleSubScore):
                indexWon = l
                break
            elif scoresList[l][0] == score and scoresList[l][1] == subscore and scoresList[l][2] == superSubScore and scoresList[l][3] == tripleSubScore and scoresList[l][4] == quadrupleSubScore and scoresList[l][5] == quintupleSubScore:
                numTied += 1
            else:
                numWon += 1
        
    numLost = len(scoresList) - indexWon
    totalGames = len(scoresList)
    return(totalGames, numWon, numTied, numLost)

def sortScoreList(scores):
    scores.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4], x[5]))
    return scores

def probWinningLosingTying(numPlayers, numWon, numTied, numLost, totalNum):
    #prob winning, pro losing, prob tying (1 person)
    probWin = (numWon/totalNum)**(numPlayers-1)
    probLoss = 1 - (((totalNum - numLost)/totalNum)**(numPlayers-1))
    probTie = 1 - probWin - probLoss
    return probWin, probLoss, probTie

    
def findNones(list):
    count = 0
    for entry in list:
        if entry is not None:
            count += 1
    return count


def compareHands(list):
    maxes = []
    max = list[0]
    
    tie = False
    for i in range(1, len(list)):
         if max[0] < list[i][0] or \
         (max[0] == list[i][0] and max[1] < list[i][1]) or \
         (max[0] == list[i][0] and max[1] == list[i][1] and max[2] < list[i][2]) or \
         (max[0] == list[i][0] and max[1] == list[i][1] and max[2] == list[i][3] and max[2] < list[i][3]) or \
         (max[0] == list[i][0] and max[1] == list[i][1] and max[2] == list[i][3] and max[2] == list[i][3] and max[4] < list[i][4]) or \
         (max[0] == list[i][0] and max[1] == list[i][1] and max[2] == list[i][3] and max[2] == list[i][3] and max[4]  == list[i][4] and max[5] < list[i][5]):
             max = list[i]
    
    maxes.append(max)
    
    for i in range(0, len(list)):  
         if (max[0] == list[i][0] and max[1] == list[i][1] and max[2] == list[i][3] and max[2] == list[i][3] and max[4]  == list[i][4] and max[5] < list[i][5]):
             maxes.append(list[i])
             tie = True
    
    return tie, maxes

def checkForTies(scores, winner):
    tied = [winner[6]]
    tie = False
    TheseScores = sortScoreList(scores)
    for i in range(len(scores)):
        if winner[0] == scores[i][0] and winner[1] == scores[i][1] and winner[2] == scores[i][2] and winner[3] == scores[i][3] and winner[4]  == scores[i][4] and winner[5] == scores[i][5] and winner[6] != scores[i][6]:
            tie = True 
            tied.append(scores[i][6])
    return tie, tied

class Card:
    
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        
        NumExists = False
        SuitExists = False
        for num in range(2,15):
            if num == self.number:
                NumExists = True
                
        suits = {'Hearts', 'Spades', 'Clubs', 'Diamonds'}
        for ww in suits:
            if self.suit == ww:
                SuitExists = True
                
        if (not NumExists or not SuitExists):
            print(str(self) + " is invalid. Please make a new card with a number 1 - 14 (numbers 10-14 represent Jack, Queen, King, Ace respectively) and a valid suit (Hearts, Spades, Clubs, Diamonds, capitalized first letter)")
            
        
    def __str__(self):
        return "{} of {}".format(self.getNumAsString(), self.getSuit())

    
    def getNumAsInt(self):
        return self.number
    
    def faceCard(self):
        if self.number > 10:
            if self.number == 11:
                return 'Jack'
            elif self.number == 12:
                return 'Queen'
            elif self.number == 13:
                return 'King'
            elif self.number == 14:
                return 'Ace'
            
    def getNumAsString(self):
        if (self.number > 10 and self.number < 15):
            return self.faceCard()
        else:
            return str(self.number)
    
    def getSuit(self):
        return self.suit
    
    def getCard(self):
        return(self.getNumAsString() + ' of ' + self.getSuit())
    

class Deck:
    
    def __init__(self):
        self.collection = []
        self._suits = {'Hearts', 'Clubs', 'Spades', 'Diamonds'}
        
    def suits(self):
        return self._suits
    
    def setDeck(self, deck):
        self.collection = deck
        
    def fillDeck(self):
        for num in range(2,15):
            for suit in self._suits:
                self.collection.append(Card(num, suit))
                
    def shuffleDeck(self):
        temporary = self.collection[:]
        nums = list(range(len(self.collection)))
        for card in self.collection:
            val = random.randint(0, len(nums)-1)
            x = nums.pop(val)
            temporary[x] = card
        
        self.collection = temporary
    
    def getCardinDeck(self, index):
        card = self.collection[index]
        return card
    
    def removeCard(self, index):
        self.collection.pop(index)
    
    def getDeck1(self):
        for num in range(0,52):
            print(self.getCardinDeck(num))
    
    def getDeck2(self):
        return self.collection
        
    def printPossibleHands(self):
        pairs = set()
        pair = []
        for num in range(0, 52):
            for number in range (0, 52):
                if (num != number):
                    pair = (self.collection[num], self.collection[number])
                    contains = False
                    for card in pairs:
                        if self.collection[num] in card and self.collection[number] in card:
                            contains = True
                            break
                    if not contains:
                        pairs.add(pair)
        
        for card_pair in pairs:
            card1 = card_pair[0]
            card2 = card_pair[1]
            print(card1.getCard() + ', ' + card2.getCard())
        print(len(pairs))
    
    
class HandDealt:
        
    def __init__(self, card1, card2, card3, card4, card5, card6, card7):
        self.card1 = card1
        self.card2 = card2
        self.card3 = None
        self.card4 = None
        self.card5 = None
        self.card6 = None
        self.card7 = None
        if card3 is not None:
            self.card3 = card3
            self.card4 = card4
            self.card5 = card5
        if card6 is not None:
            self.card6 = card6 
        if card7 is not None:
            self.card7 = card7
        self.hand = (self.card1, self.card2, self.card3, self.card4, self.card5, self.card6, self.card7)
    
    def getHand(self):
        return self.hand
    
    def getCardsInHand(self):
        card1 = self.hand[0]
        card2 = self.hand[1]
        card3 = self.hand[2]
        card4 = self.hand[3]
        card5 = self.hand[4]
        card6 = self.hand[5]
        card7 = self.hand[6]
        return card1, card2, card3, card4, card5, card6, card7
        
class GamePlay:
    
    def __init__(self, hand):
        self.hand = hand
        self.Deck1 = Deck()
        card1, card2, card3, card4, card5, card6, card7 = hand.getCardsInHand()
        self.Deck1.fillDeck()
        self.Deck1.shuffleDeck()
        self.Deck = self.Deck1.getDeck2()
        cards_to_remove = []
        for card in self.Deck:
                if card1 is not None and card1.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card2 is not None and card2.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card3 is not None and card3.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card4 is not None and card4.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card5 is not None and card5.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card6 is not None and card6.getCard() == card.getCard():
                    cards_to_remove.append(card)
                if card7 is not None and card7.getCard() == card.getCard():
                    cards_to_remove.append(card)

        for card in cards_to_remove:
            self.Deck.remove(card)
        
    def getDeck(self):
        return self.Deck1
    
#used to check what hands a player has - initialize with None for any card that has not come out yet
class FindHands:
       
        def __init__(self, card1, card2, card3, card4, card5, card6, card7):
            self.numPairsOfTwo = 0
            self.pairsOfTwo = []
            self.numPairsOfThree = 0
            self.pairsOfThree = []
            self.numPairsOfFour = 0
            self.pairsOfFour = []
            
            
            
            cards = []
           
            if card1 is not None and card2 is not None:
                # Constructor with both parameters
                self.card1 = card1
                self.card2 = card2
                
                cards.append(self.card1)
                cards.append(self.card2)
                
                if card3 is not None and card4 is not None and card5 is not None:
                    self.card3 = card3
                    self.card4 = card4
                    self.card5 = card5
                    
                    cards.append(self.card3)
                    cards.append(self.card4)
                    cards.append(self.card5)
                    
                    if card6 is not None:
                        self.card6 = card6
                        
                        cards.append(self.card6)
                        
                        if card7 is not None:
                            self.card7 = card7
                            cards.append(self.card7)
            self.cards = cards
                    
        def flop(self, card3, card4, card5):
            self.card3 = card3
            self.card4 = card4
            self.card5 = card5
            
            self.cards.append(self.card3)
            self.cards.append(self.card4)
            self.cards.append(self.card5)
            
        def turn(self, card6):
            self.card6 = card6
        
            self.cards.append(self.card6)
            
        def river(self, card7):
            self.card7 = card7
            
            self.cards.append(self.card7)
            
        def findPairsOfTwo(self):
            self.numPairsOfTwo = 0
            self.pairsOfTwo = []
            for cardX in self.cards:
                for cardY in self.cards:
                    if cardX.getCard() != cardY.getCard():
                        pair = (cardY, cardX)
                        if cardX.getNumAsInt() == cardY.getNumAsInt() and not pair in self.pairsOfTwo:
                            pair = (cardX, cardY)
                            self.numPairsOfTwo += 1
                            self.pairsOfTwo.append(pair)
            return self.numPairsOfTwo, self.pairsOfTwo        
                
        def findPairsOfThree(self):
            self.numPairsOfThree = 0
            self.pairsOfThree = []
            for i1 in range(0,len(self.cards)):
                for i2 in range(i1 + 1, len(self.cards)):
                    for i3 in range(i2 + 1, len(self.cards)):
                        if self.cards[i1].getNumAsInt() == self.cards[i2].getNumAsInt() and self.cards[i2].getNumAsInt() == self.cards[i3].getNumAsInt():
                            self.numPairsOfThree += 1
                            triple = (self.cards[i1], self.cards[i2], self.cards[i3])
                            self.pairsOfThree.append(triple)
            return self.numPairsOfThree, self.pairsOfThree
        
        def findPairsOfFour(self):
            self.numPairsOfFour = 0
            self.pairsOfFour = []
            for i1 in range(0,len(self.cards)):
                for i2 in range(i1 + 1, len(self.cards)):
                    for i3 in range(i2 + 1, len(self.cards)):
                        for i4 in range(i3 + 1, len(self.cards)):
                            if self.cards[i1].getNumAsInt() == self.cards[i2].getNumAsInt() and self.cards[i2].getNumAsInt() == self.cards[i3].getNumAsInt() and self.cards[i3].getNumAsInt() == self.cards[i4].getNumAsInt():
                                self.numPairsOfFour += 1
                                quad = (self.cards[i1], self.cards[i2], self.cards[i3], self.cards[i4])
                                self.pairsOfFour.append(quad)
            return self.numPairsOfFour, self.pairsOfFour
        
        
        def printPairsOfTwo(self):
            xx, yy = self.findPairsOfTwo()
            print('There are ' + str(xx) + ' pairs of two')
            for card in yy:
                card1, card2 = card
                print(card1)
                print(card2)
        
        def printPairsOfThree(self):
            xx, yy = self.findPairsOfThree()
            print('There are ' + str(xx) + ' pairs of three')
            for card in yy:
                card1, card2, card3 = card
                print(card1)
                print(card2)
                print(card3)
                
        def printPairsOfFour(self):
            xx, yy = self.findPairsOfFour()
            print('There are ' + str(xx) + ' pairs of four')
            for card in yy:
                card1, card2, card3, card4 = card
                print(card1)
                print(card2)
                print(card3)
                print(card4)
        
        
        def eliminateDuplicatePairs(self):
            self.findPairsOfTwo()
            self.findPairsOfThree()
            self.findPairsOfFour()
            pairsOfTwoCopy = self.pairsOfTwo.copy()
            numPairsOfTwoCopy = self.numPairsOfTwo
            
            if self.numPairsOfThree > 0:
                for x1 in self.pairsOfThree:
                    for x2 in x1:
                        for x3 in pairsOfTwoCopy:
                            if x2 in x3:
                                pairsOfTwoCopy.remove(x3)
                                numPairsOfTwoCopy -= 1
                                break
                                
            self.numPairsOfTwo = numPairsOfTwoCopy
            self.pairsOfTwo = pairsOfTwoCopy               

            pairsOfThreeCopy = self.pairsOfThree.copy()
            numPairsOfThreeCopy = self.numPairsOfThree
            
            if self.numPairsOfFour > 0:
                for i1 in self.pairsOfFour:
                    for i2 in i1:
                        for i3 in pairsOfThreeCopy:
                            if i2 in i3:
                                pairsOfThreeCopy.remove(i3)
                                numPairsOfThreeCopy -= 1
                                break
                                                     
            self.pairsOfThree = pairsOfThreeCopy 
            self.numPairsOfThree = numPairsOfThreeCopy
                                  
            return self.numPairsOfTwo, self.pairsOfTwo, self.numPairsOfThree, self.pairsOfThree, self.numPairsOfFour, self.pairsOfFour

        def printEliminateDuplicatePairs(self):
            x1, x2, x3, x4, x5, x6 = self.eliminateDuplicatePairs()
            print('there are ' + str(x1) + ' pairs of two')
            for card in x2:
                card1, card2 = card
                print(card1)
                print(card2)   
            print('There are ' + str(x3) + ' pairs of three')
            for card in x4:
                card1, card2, card3 = card
                print(card1)
                print(card2)
                print(card3)  
            print('There are ' + str(x5) + ' pairs of four')
            for card in x6:
                card1, card2, card3, card4 = card
                print(card1)
                print(card2)
                print(card3)
                print(card4)

        def fullHouse(self):
            house = []
            x1, x2, x3, x4, x5, x6 = self.eliminateDuplicatePairs()
            if (x1 > 0 and x3 > 0) or x3 > 1:
              for card in x2:
                house.append(card)
              for card in x4:
                house.append(card)
              return True, house
            else:
              return False, house

        def flush(self):
          numHearts = 0
          numDiamonds = 0
          numSpades = 0
          numClubs = 0
          hearts = []
          diamonds = []
          spades = []
          clubs = []
          null = []
          for card in self.cards:
            if card.getSuit() == 'Hearts':
              numHearts += 1
              hearts.append(card)
            if card.getSuit() == 'Diamonds':
              numDiamonds += 1
              diamonds.append(card)
            if card.getSuit() == 'Clubs':
              numClubs += 1
              clubs.append(card)
            if card.getSuit() == 'Spades':
              numSpades += 1
              spades.append(card)
          if numHearts >= 5:
            return True, 'Hearts', hearts
          if numDiamonds >= 5:
            return True, 'Diamonds', diamonds
          if numClubs >= 5:
            return True, 'Clubs', clubs
          if numSpades >= 5:
            return True, 'Spades', spades 
          return False, 'null', null

        def straight(self):
            numsInRow = 1
            collectionNums = []
            straightCards = []
            for card in self.cards:
                collectionNums.append(card.getNumAsInt())
                if card.getNumAsInt() == 14:
                    collectionNums.append(1)
            collectionNums.sort()
            numbers = []
            
            i = len(collectionNums) - 1
            while i > 0:
                if numsInRow > 4:
                    break
                if collectionNums[i] == collectionNums[i - 1] + 1:
                    numsInRow += 1
                    numbers.append(collectionNums[i])
                elif collectionNums[i] == collectionNums[i - 1]:
                    numsInRow += 0
                else:
                    if numsInRow < 5:
                        numsInRow = 1
                        numbers = []
                i -= 1
            
            if numsInRow > 4:
                # Handle special case for Ace-low straight (A, 2, 3, 4, 5)
                if collectionNums[-1] == 14 and collectionNums[0] == 2 and numsInRow == 5:
                    straightCards.append(self.cards[-1])  # Append the Ace card
                    for card in self.cards:
                        if card.getNumAsInt() in numbers:
                            straightCards.append(card)
                else:
                    for card in self.cards:
                        if card.getNumAsInt() in numbers:
                            straightCards.append(card)
                return True, straightCards
            else:
                return False, straightCards
                    
        def straightFlush(self):
            isFlush, flushSuit, flushCards = self.flush()
            if isFlush:
                numsInRow = 1
                collectionNums = []
                straightFlushCards = []
                
                for card in flushCards:
                    collectionNums.append(card.getNumAsInt())
                    if card.getNumAsInt() == 14:
                        collectionNums.append(1)
                collectionNums.sort()
                
                i = 1
                while i < len(collectionNums):
                    if numsInRow > 4:
                        break
                    if collectionNums[i] == collectionNums[i - 1] + 1:
                        numsInRow += 1
                    elif collectionNums[i] == collectionNums[i - 1]:
                        numsInRow += 0
                    else:
                        if numsInRow < 5:
                            numsInRow = 1
                    i += 1
                
                if numsInRow > 4:
                    for card in flushCards:
                        if card.getNumAsInt() in collectionNums[i - numsInRow:i]:
                            straightFlushCards.append(card)
                    return True, flushSuit, straightFlushCards
                else:
                    return False, 'null', []
            else:
                return False, 'null', []
            
        def scoreHand(self):
          mainScore = 0
          subScore = 0
          doubleSubScore = 0
          tripleSubScore = 0
          quadrupleSubScore = 0
          quintupleSubScore = 0
          bestHand = 'null'
          numTwoPair, twoPair, numThreePair, threePair, numFourPair, fourPair = self.eliminateDuplicatePairs()
          straightBool, straight = self.straight()
          flushBool, flushSuit, flush = self.flush()
          fullHouseBool, fullHouse = self.fullHouse()
          straightFlushBool, straightFlushSuit, straightFlush = self.straightFlush()
          
          if straightFlushBool:
              mainScore = 10
              bestHand = 'Straight Flush'
              max = 0
              for card in straightFlush:
                  if card.getNumAsInt() > max:
                      max = card.getNumAsInt()
              subScore = max
          
          elif numFourPair > 0:
              mainScore = 9
              bestHand = 'Four of a Kind'
              max = 0
              cardx = []
              for card in fourPair:
                for card2 in card:
                  cardx.append(card2)
                  if card2.getNumAsInt() > max:
                      max = card2.getNumAsInt()
              subMax = 0
              for card19 in self.cards:
                if not card19 in cardx:
                    if card19.getNumAsInt() > subMax:
                      subMax = card19.getNumAsInt()
              doubleSubScore = subMax
          
          elif fullHouseBool:
              mainScore = 8
              bestHand = 'Full House'
              max = 0
              tripmax = 0
              
              for card1 in threePair:
                for card2 in card1:
                  if card2.getNumAsInt() > max:
                      max = card2.getNumAsInt()
              subScore = max
              
              for card1 in twoPair:
                for card2 in card1:
                  if card2.getNumAsInt() > tripmax:
                      tripmax = card2.getNumAsInt()
              doubleSubScore = tripmax
              
            
          elif flushBool:
            mainScore = 7
            bestHand = 'Flush'
            max = 0
            doublemax = 0
            triplemax = 0
            quadruplemax = 0
            quintuplemax = 0
            
            for card in flush:
                  if card.getNumAsInt() > max:
                      max = card.getNumAsInt()
            subScore = max
            
            for card in flush:
                  if card.getNumAsInt() > doublemax and card.getNumAsInt() != subScore:
                      doublemax = card.getNumAsInt()
            doubleSubScore = doublemax
            
            for card in flush:
                  if card.getNumAsInt() > triplemax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore:
                      triplemax = card.getNumAsInt()
            tripleSubScore = triplemax
            
            for card in flush:
                  if card.getNumAsInt() > quadruplemax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore and card.getNumAsInt() != tripleSubScore:
                      quadruplemax = card.getNumAsInt()
            quadrupleSubScore = quadruplemax
            
            for card in flush:
                  if card.getNumAsInt() > quintuplemax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore and card.getNumAsInt() != tripleSubScore and card.getNumAsInt() != quadrupleSubScore:
                      quintuplemax = card.getNumAsInt()
            quintupleSubScore = quintuplemax
            
          elif straightBool: 
            mainScore = 6
            bestHand = 'Straight'
            max = 0
            for card in straight:
                  if card.getNumAsInt() > max:
                      max = card.getNumAsInt()
            subScore = max
            
          elif numThreePair > 0:
            mainScore = 5
            bestHand = 'Three of a Kind'
            max = 0
            tripmax = 0
            subMax = 0
            cardx = []
            for card1 in threePair:
              for card2 in card1:
                  cardx.append(card2)
                  if card2.getNumAsInt() > max:
                      max = card2.getNumAsInt()
            subScore = max

            for card19 in self.cards:
                if not card19 in cardx:
                    if card19.getNumAsInt() > subMax:
                      subMax = card19.getNumAsInt()
            doubleSubScore = subMax
            
            for card19 in self.cards:
                if not card19 in cardx and card19.getNumAsInt() != doubleSubScore:
                    if card19.getNumAsInt() > tripmax:
                      tripmax = card19.getNumAsInt()
            tripleSubScore = tripmax
            
          elif numTwoPair > 1:
            if numTwoPair > 2:
                min = 15
                for card1 in twoPair:
                    for card2 in card1:
                        if card2.getNumAsInt() < min:
                            min = card2.getNumAsInt()
                cardY = None
                for card1 in twoPair:
                    for card2 in card1:
                        if card2.getNumAsInt() == min:
                            cardY = card1
                            break
                if cardY is not None:
                    twoPair.remove(cardY)  
            mainScore = 4
            bestHand = 'Two Pair'
            max = 0
            subMax = 0
            cardx = []
            for card1 in twoPair:
              for card2 in card1:
                  cardx.append(card2)
                  if card2.getNumAsInt() > max:
                      max = card2.getNumAsInt()
            subScore = max

            for card1 in twoPair:
                for card2 in card1:
                    if card2.getNumAsInt() != subScore:
                        doubleSubScore = card2.getNumAsInt()
                        break 
            for card19 in self.cards:
                if not card19 in cardx:
                    if card19.getNumAsInt() > subMax:
                      subMax = card19.getNumAsInt()
            tripleSubScore = subMax
            
          elif numTwoPair > 0:
            mainScore = 3
            bestHand = 'Pair'
            max = 0
            cardx = []
            for card1 in twoPair:
              for card2 in card1:
                cardx.append(card2)
                if card2.getNumAsInt() > max:
                    max = card2.getNumAsInt()
            subScore = max
            
            subMax = 0
            for card19 in self.cards:
                if not card19 in cardx:
                    if card19.getNumAsInt() > subMax:
                      subMax = card19.getNumAsInt()
            doubleSubScore = subMax
            
            tupmax = 0
            for card19 in self.cards:
                if not card19 in cardx and card19.getNumAsInt() != doubleSubScore:
                    if card19.getNumAsInt() > tupmax:
                      tupmax = card19.getNumAsInt()
            tripleSubScore = tupmax
            
            tripmax = 0
            for card19 in self.cards:
                if not card19 in cardx and card19.getNumAsInt() != doubleSubScore and card19.getNumAsInt() != tripleSubScore:
                    if card19.getNumAsInt() > tripmax:
                      tripmax = card19.getNumAsInt()
            quadrupleSubScore = tripmax
            
            
          else:
            mainScore = 2
            bestHand = 'High Card'
            
            max = 0
            for card in self.cards:
                if card.getNumAsInt() > max:
                    max = card.getNumAsInt()
            subScore = max
            
            singlemax = 0
            for card in self.cards:
                if card.getNumAsInt() > singlemax and card.getNumAsInt() != subScore:
                    singlemax = card.getNumAsInt()
            doubleSubScore = singlemax
            
            doublemax = 0
            for card in self.cards:
                if card.getNumAsInt() > doublemax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore:
                    doublemax = card.getNumAsInt()
            tripleSubScore = doublemax
            
            triplemax = 0
            for card in self.cards:
                if card.getNumAsInt() > triplemax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore and card.getNumAsInt() != tripleSubScore:
                    triplemax = card.getNumAsInt()
            quadrupleSubScore = triplemax
            
            quadmax = 0
            for card in self.cards:
                if card.getNumAsInt() > quadmax and card.getNumAsInt() != subScore and card.getNumAsInt() != doubleSubScore and card.getNumAsInt() != tripleSubScore and card.getNumAsInt() != quadrupleSubScore:
                    quadmax = card.getNumAsInt()
            quintupleSubScore = quadmax
            
          return mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand
              
            
class DeckRemoval:
    
    def __init__(self):
        self.Deck1 = Deck()
        self.Deck1.fillDeck()
        self.Deck1.shuffleDeck()
        self.Deck = self.Deck1.getDeck2()
    
    def removeCard(self, card):
        
        if card is None:
            print('Error: NONE not in deck')
            return
        
        for card1 in self.Deck:
            if card.getCard() == card1.getCard():
                self.Deck.remove(card1)
                return
        
        print('Error: ' + card.getCard() + ' not in deck')
    
    def getDeck(self):
        return self.Deck
    
    def getDeckLength(self):
        return len(self.Deck)
    
class Game:
      def __init__(self, card1, card2, card3, card4, card5, card6, card7):
        self.deck = Deck()
        
        self.hand = [card1, card2]
        self.cardsOnTable = [None, None, None, None, None]
        self.total = [card1, card2, None, None, None, None, None]
        if card3 is not None:
          self.cardsOnTable[0] = card3
          self.cardsOnTable[1] = card4
          self.cardsOnTable[2] = card5
          self.total[2] = card3
          self.total[3] = card4
          self.total[4] = card5
        if card6 is not None:
          self.cardsOnTable[3] = card6
          self.total[5] = card6
        if card7 is not None:
          self.cardsOnTable[4] = card7
          self.total[6] = card7
        
        yy = HandDealt(self.total[0], self.total[1], self.total[2], self.total[3], self.total[4], self.total[5], self.total[6])
        x = GamePlay(yy)
        self.deck = x.getDeck()
            
      def flop(self, card3, card4, card5):
        self.cardsOnTable[0] = card3
        self.cardsOnTable[1] = card4
        self.cardsOnTable[2] = card5
        self.total[2] = card3
        self.total[3] = card4
        self.total[4] = card5
        yy = HandDealt(self.total[0], self.total[1], self.total[2], self.total[3], self.total[4], self.total[5], self.total[6])
        x = GamePlay(yy)
        self.deck = x.getDeck()

      def turn(self, card6):
        self.cardsOnTable[3] = card6
        self.total[5] = card6
        yy = HandDealt(self.total[0], self.total[1], self.total[2], self.total[3], self.total[4], self.total[5], self.total[6])
        x = GamePlay(yy)
        self.deck = x.getDeck()

      def river(self, card7):
        self.cardsOnTable[4] = card7
        self.total[6] = card7
        yy = HandDealt(self.total[0], self.total[1], self.total[2], self.total[3], self.total[4], self.total[5], self.total[6])
        x = GamePlay(yy)
        self.deck = x.getDeck()
        
      def flopTurnRiver(self, card3, card4, card5, card6, card7):
        self.flop(card3, card4, card5)
        self.turn(card6)
        self.river(card7)
        yy = HandDealt(self.total[0], self.total[1], self.total[2], self.total[3], self.total[4], self.total[5], self.total[6])
        x = GamePlay(yy)
        self.deck = x.getDeck()
    
      def scoreThisHandRiver(self):
        card1 = self.total[0]
        card2 = self.total[1]
        card3 = self.total[2]
        card4 = self.total[3]
        card5 = self.total[4]
        card6 = self.total[5]
        card7 = self.total[6]
        hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
        score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
        return score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand

      def scoreOtherHandsRiver(self):
          scores  = []
          deckList = self.deck.getDeck2()
          if len(self.cardsOnTable) == 5:
              card3 = self.cardsOnTable[0]
              card4 = self.cardsOnTable[1]
              card5 = self.cardsOnTable[2]
              card6 = self.cardsOnTable[3]
              card7 = self.cardsOnTable[4]
              for i in range(len(deckList)):
                  for z in range(i+1,len(deckList)):
                      card1 = deckList[i]
                      card2 = deckList[z]
                      hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                      score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
                      tup = (score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore)
                      scores.append(tup)
          
          #selection sort to sort scores 
          scores = sortScoreList(scores)
          return scores
        
      def findProbabilityRiver(self):
          scores = self.scoreOtherHandsRiver()
          x, y, w, xx, yy, ww, bestHand = self.scoreThisHandRiver()
          totalGames, numWon, numTied, numLost = placement(scores, x, y, w, xx, yy, ww)
          return totalGames, numWon, numTied, numLost, bestHand, y, w
      
      def scoreThisHandTurn(self):
        card1 = self.total[0]
        card2 = self.total[1]
        card3 = self.total[2]
        card4 = self.total[3]
        card5 = self.total[4]
        card6 = self.total[5]
        scores = []
        deckList = self.deck.getDeck2()
        for card7 in deckList:
          hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
          score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
          tup = (score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore)
          scores.append(tup)
          scores = sortScoreList(scores)
        
        return scores
       
      def scoreOtherHandsTurn(self):
        scores  = []
        deckList = self.deck.getDeck2()
        count=1
       # if len(self.cardsOnTable) == 4:
        card4 = self.cardsOnTable[0]
        card5 = self.cardsOnTable[1]
        card6 = self.cardsOnTable[2]
        card7 = self.cardsOnTable[3]
        for i in range(len(deckList)-2):
          for z in range(i+1,len(deckList)-1):
            for w in range(z+1, len(deckList)):
              count += 1
              card1 = deckList[i]
              card2 = deckList[z]
              card3 = deckList[w]
              hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
              score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
              tup = (score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore)
              scores.append(tup)
              
        scores = sortScoreList(scores)
        return scores, set(scores)
  
      def probabilityTurn(self):
        tot = []
        deckList = self.deck.getDeck2()
        card11 = self.total[0]
        card22 = self.total[1]
        card4 = self.cardsOnTable[0]
        card5 = self.cardsOnTable[1]
        card6 = self.cardsOnTable[2]
        card7 = self.cardsOnTable[3]
        for i in range(len(deckList)):
            scores = []
            thisHand = FindHands(card11, card22, deckList[i], card4, card5, card6, card7)
            x, y, uu, trip, quad, quint, zz = thisHand.scoreHand()
            for z in range(len(deckList)):
                for w in range(z + 1, len(deckList)):
                  if z != i and w != i:
                    card1 = deckList[i]
                    card2 = deckList[z]
                    card3 = deckList[w]
                    hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                    score, subscore, superSubScore, triplesub, quadsub, quintsub, bestHand = hand.scoreHand()
                    tup = (score, subscore, superSubScore, triplesub, quadsub, quintsub)
                    scores.append(tup)
            scores1 = sortScoreList(scores)
            total, numWon, numTied, numLost = placement(scores1, x, y, uu, trip, quad, quint)
            sack = (total, numWon, numTied, numLost, deckList[i])
            tot.append(sack)
        sum = 0
        count = 0
        max = 0
        maxCard = tot[0][4]
        min = 0
        minCard = tot[0][4]
        for entry in tot:
          sum += entry[1]
          count += 1
          if entry[1] > max:
            maxCard = entry[4]
            max = entry[1]
          if entry[3] > min:
            minCard = entry[4]
            min = entry[3]
      
        average = sum/count
        return tot, average, average/960, minCard, maxCard
      
      def scoreThisHandFlop(self):
        card1 = self.total[0]
        card2 = self.total[1]
        card3 = self.total[2]
        card4 = self.total[3]
        card5 = self.total[4]
        scores = []
        deckList = self.deck.getDeck2()
        for i in range(len(deckList)):
          for z in range(i + 1, len(deckList)):
            hand = FindHands(card1, card2, card3, card4, card5, deckList[i], deckList[z])
            score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
            tup = (score, subscore, superSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, deckList[i], deckList[z])
            scores.append(tup)
            scores = sortScoreList(scores)
      
        return scores
      
      def probabilityFlop(self):
        tot = []
        deckList = self.deck.getDeck2()
        card11 = self.total[0]
        card22 = self.total[1]
        card5 = self.cardsOnTable[0]
        card6 = self.cardsOnTable[1]
        card7 = self.cardsOnTable[2]
        for i in range(len(deckList)):
          for q in range(i+1, len(deckList)):
            scores = []
            thisHand = FindHands(card11, card22, deckList[i], deckList[q], card5, card6, card7)
            x, y, uu, trip, quad, quint, zz = thisHand.scoreHand()
            for z in range(len(deckList)):
                for w in range(z, len(deckList)):
                  if z != i and z != w and w != i:
                    card1 = deckList[i]
                    card2 = deckList[z]
                    card3 = deckList[w]
                    card4 = deckList[q]
                    hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                    score, subscore, superSubScore, triplesub, quadsub, quintsub, bestHand = hand.scoreHand()
                    tup = (score, subscore, superSubScore, triplesub, quadsub, quintsub)
                    scores.append(tup)
            scores1 = sortScoreList(scores)
            total, numWon, numTied, numLost = placement(scores1, x, y, uu, trip, quad, quint)
            sack = (total, numWon, numTied, numLost, deckList[i], deckList[q])
            tot.append(sack)
        sum = 0
        count = 0
        max = 0
        maxDuo = (tot[0][4], tot[0][5])
        min = 0
        minDuo = (tot[0][4], tot[0][5])
        for entry in tot:
          sum += entry[1]
          count += 1
          if entry[1] > max:
            maxDuo = (entry[4], entry[5])
            max = entry[1]
          if entry[3] > min:
            minDuo = (entry[4], entry[5])
            min = entry[3]
      
        average = sum/count
        return tot, average, average/960, minDuo, maxDuo
      
      def setNumPlayers(self, numPlayers):
        self.numPlayers = numPlayers
      
      def probabilityDealt(self):
        prob = 0
        FirstCard = self.hand[0]
        SecondCard = self.hand[1]
        
        FirstNum = FirstCard.getNumAsInt()
        SecondNum = SecondCard.getNumAsInt()
        
        paired = False
        if FirstNum > SecondNum:
          max = FirstNum
          min = SecondNum
        elif SecondNum > FirstNum:
          max = SecondNum
          min = FirstNum
        elif FirstNum == SecondNum:
          max = FirstNum
          min = SecondNum
          paired = True
        
        suited = False
        if FirstCard.getSuit() == SecondCard.getSuit():
          suited = True
          
        df = pd.read_csv('OffripProbabilities - Ace High-2.csv')
        for i in range(len(df)):
          if df.iloc[i, 0] == max and df.iloc[i, 1] == min:
            prob = df.iloc[i, self.numPlayers]
        
        if suited:
          prob += 2
        elif not paired:
          prob -= 1
        
        return prob

class multipleHands:
    
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.table = [None, None, None, None, None]
        self.list = []
        for i in range(self.numPlayers):
             tup = [None, None]
             self.list.append(tup)
        self.deck = DeckRemoval()
             
    def setCards(self, numPlayer, card1, card2):
        self.list[numPlayer - 1][0] = card1
        self.list[numPlayer - 1][1] = card2
        self.deck.removeCard(card1)
        self.deck.removeCard(card2)
        
    def cardsOnTable(self, card1, card2, card3, card4, card5):
        self.table[0] = card1
        self.table[1] = card2
        self.table[2] = card3
        self.table[3] = card4
        self.table[4] = card5
        self.deck.removeCard(card1)
        self.deck.removeCard(card2)
        self.deck.removeCard(card3)
        self.deck.removeCard(card4)
        self.deck.removeCard(card5)
        
    
    def flop(self, card1, card2, card3):
        self.table[0] = card1
        self.table[1] = card2
        self.table[2] = card3
        self.deck.removeCard(card1)
        self.deck.removeCard(card2)
        self.deck.removeCard(card3)
    
    def turn(self, card4):
        self.table[3] = card4
        self.deck.removeCard(card4)
    
    def river(self, card5):
        self.table[4] = card5
        self.deck.removeCard(card5)
    
    def getNumCards(self):
        numCards = findNones(self.table)
        return numCards
    
    def getPlayerCards(self):
        num = 0
        for entry in self.list:
            if entry[0] != None:
                num += 1
            if entry[1] != None:
                num += 1
        return num

    def getNumPlayers(self):
        return self.numPlayers
    
    def FindProbs(self):
        numCards = findNones(self.table)
        deck = self.deck.getDeck()
        
        if numCards == 0:
            probabilities = []
            df = pd.read_csv('OffripProbabilities - Ace High-2.csv')
            for them in self.list:
                card1 = them[0]
                card2 = them[1]
                FirstNum = card1.getNumAsInt()
                SecondNum = card2.getNumAsInt()
                
                paired = False
                if FirstNum > SecondNum:
                    maximum = FirstNum
                    minimum = SecondNum
                elif SecondNum > FirstNum:
                    maximum = SecondNum
                    minimum = FirstNum
                elif FirstNum == SecondNum:
                    maximum = FirstNum
                    minimum = SecondNum
                    paired = True
                
                suited = False
                if card1.getSuit() == card2.getSuit():
                    suited = True
                
                for i in range(len(df)):
                    if df.iloc[i, 0] == maximum and df.iloc[i, 1] == minimum:
                        prob = df.iloc[i, self.numPlayers]
                    
                if suited:
                    prob += 2
                elif not paired:
                    prob -= 1

                probabilities.append(prob)
            
            total = 0
            for num in probabilities:
                total += num
            
            for i in range(len(probabilities)):
                probabilities[i] = round(probabilities[i]/total, 4)
            
            maxPlayers = []
            minPlayers = []
           
            maximum_value = max(probabilities)
            maximumPlayer = probabilities.index(maximum_value)
            maxPlayers.append(maximumPlayer)
            
            min_value = min(probabilities)
            minPlayer = probabilities.index(min_value)
            minPlayers.append(minPlayer)
            
            tiedWinner = False
            tiedLoser = False
            for i in range(len(probabilities)):
                if probabilities[i] == maximum_value and i != maximumPlayer:
                    tiedWinner = True
                    maxPlayers.append(i)
                elif probabilities[i] == min_value and i != minPlayer:
                    tiedLoser = False
                    minPlayers.append(i)
                    
            
            return probabilities, maxPlayers, minPlayers, tiedWinner, tiedLoser
 
        elif numCards == 3:
            winnersCards = []
            for i in range(len(self.list)):
                list = []
                winnersCards.append(list)
            winners = []
            for i in range(len(self.list)):
                winners.append(0)
            card1 = self.table[0]
            card2 = self.table[1]
            card3 = self.table[2]
            for i in range(len(deck)):
                for j in range(i+1, len(deck)):
                    card4 = deck[i]
                    card5 = deck[j]
                    scores = []
                    for player in range(len(self.list)):
                        card6 = self.list[player][0]
                        card7 = self.list[player][1]
                        hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                        mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
                        tup = (mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, player, bestHand)
                        scores.append(tup)
                    TheseScores = sortScoreList(scores)
                    winner = TheseScores[self.numPlayers-1][6]
                    winners[winner] += 1
                    winnerTuple = [card4, card5]
                    winnersCards[winner].append(winnerTuple)
                    total = 0
                    winners1 = winners[:]
            for stuff in winners:
                total += stuff
            for i in range(len(winners)):
                winners[i] = round(winners[i]/total, 4)
            maximumVal = max(winners)
            victor = winners.index(maximumVal)
            return winners, victor, winnersCards, winners1
            
        elif numCards == 4:
            winnersCards = []
            for i in range(len(self.list)):
                list = []
                winnersCards.append(list)
            winners = []
            for i in range(len(self.list)):
                winners.append(0)
            card1 = self.table[0]
            card2 = self.table[1]
            card3 = self.table[2]
            card4 = self.table[3]
            for i in range(len(deck)):
                    card5 = deck[i]
                    scores = []
                    for player in range(len(self.list)):
                        card6 = self.list[player][0]
                        card7 = self.list[player][1]
                        hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                        mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
                        tup = (mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, player, bestHand)
                        scores.append(tup)
                    TheseScores = sortScoreList(scores)
                    winner = TheseScores[self.numPlayers-1][6]
                    winners[winner] += 1
                    winnersCards[winner].append(card5)
            total = 0
            winners1 = winners
            for stuff in winners:
                total += stuff
            for i in range(len(winners)):
                winners[i] = round(winners[i]/total, 4)
            maximumVal = max(winners)
            victor = winners.index(maximumVal)
            return winners, victor, winnersCards, winners1
            
        elif numCards == 5:
            card1 = self.table[0]
            card2 = self.table[1]
            card3 = self.table[2]
            card4 = self.table[3]
            card5 = self.table[4]
            scores = []
            
            for player in range(len(self.list)):
                card6 = self.list[player][0]
                card7 = self.list[player][1]
                hand = FindHands(card1, card2, card3, card4, card5, card6, card7)
                mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, bestHand = hand.scoreHand()
                tup = (mainScore, subScore, doubleSubScore, tripleSubScore, quadrupleSubScore, quintupleSubScore, player, bestHand)
                scores.append(tup)
            TheseScores = sortScoreList(scores)
            winner = TheseScores[self.numPlayers-1]
            
            tie, tiePlayers = checkForTies(scores, winner)
            
            return tiePlayers, scores, tie, TheseScores
    
        else:
            print('ERROR: MUST BE 0, 3, 4, or 5 CARDS ON TABLE')
            return None, None, None
                   
                   
class Player:
    def __init__(self, num, card1, card2):
        self.num = num
        self.card1 = card1
        self.card2 = card2
    
    def getCard1(self):
        return self.card1
    
    def getCard2(self):
        return self.card2
    
    def getPlayerNum(self):
        return self.num
options = {
    "Ace of Clubs": "Screenshot 2023-06-07 at 7.37.23 AM.png",
    "2 of Clubs": "Screenshot 2023-06-07 at 7.37.29 AM.png",
    "3 of Clubs": "Screenshot 2023-06-07 at 7.37.35 AM.png", 
    "4 of Clubs": "Screenshot 2023-06-07 at 7.37.42 AM.png",
    "5 of Clubs": "Screenshot 2023-06-07 at 7.37.54 AM.png",
    "6 of Clubs": "Screenshot 2023-06-07 at 7.38.00 AM.png",
    "7 of Clubs": "Screenshot 2023-06-07 at 7.38.06 AM.png",
    "8 of Clubs": "Screenshot 2023-06-07 at 7.38.12 AM.png",
    "9 of Clubs": "Screenshot 2023-06-07 at 7.38.17 AM.png",
    "10 of Clubs": "Screenshot 2023-06-07 at 7.38.23 AM.png",
    "Jack of Clubs": "Screenshot 2023-06-07 at 7.38.29 AM.png",
    "Queen of Clubs": "Screenshot 2023-06-07 at 7.38.35 AM.png",
    "King of Clubs":  "Screenshot 2023-06-07 at 7.38.43 AM.png",
    
    "Ace of Diamonds": "Screenshot 2023-06-07 at 7.38.51 AM.png",
    "2 of Diamonds": "Screenshot 2023-06-07 at 7.38.58 AM.png",
    "3 of Diamonds": "Screenshot 2023-06-07 at 7.39.05 AM.png", 
    "4 of Diamonds": "Screenshot 2023-06-07 at 7.39.15 AM.png",
    "5 of Diamonds": "Screenshot 2023-06-07 at 7.39.24 AM.png",
    "6 of Diamonds": "Screenshot 2023-06-07 at 7.39.29 AM.png",
    "7 of Diamonds": "Screenshot 2023-06-07 at 7.39.34 AM.png",
    "8 of Diamonds": "Screenshot 2023-06-07 at 7.39.39 AM.png",
    "9 of Diamonds": "Screenshot 2023-06-07 at 7.39.44 AM.png",
    "10 of Diamonds": "Screenshot 2023-06-07 at 7.39.50 AM.png",
    "Jack of Diamonds": "Screenshot 2023-06-07 at 7.39.56 AM.png",
    "Queen of Diamonds": "Screenshot 2023-06-07 at 7.40.01 AM.png",
    "King of Diamonds":  "Screenshot 2023-06-07 at 7.40.07 AM.png",
    
    "Ace of Hearts": "Screenshot 2023-06-07 at 7.40.22 AM.png",
    "2 of Hearts": "Screenshot 2023-06-07 at 7.40.29 AM.png",
    "3 of Hearts": "Screenshot 2023-06-07 at 7.40.35 AM.png", 
    "4 of Hearts": "Screenshot 2023-06-07 at 7.40.41 AM.png",
    "5 of Hearts": "Screenshot 2023-06-07 at 7.40.47 AM.png",
    "6 of Hearts": "Screenshot 2023-06-07 at 7.40.53 AM.png",
    "7 of Hearts": "Screenshot 2023-06-07 at 7.40.58 AM.png",
    "8 of Hearts": "Screenshot 2023-06-07 at 7.41.07 AM.png",
    "9 of Hearts": "Screenshot 2023-06-07 at 7.41.14 AM.png",
    "10 of Hearts": "Screenshot 2023-06-07 at 7.41.20 AM.png",
    "Jack of Hearts": "Screenshot 2023-06-07 at 7.41.27 AM.png",
    "Queen of Hearts": "Screenshot 2023-06-07 at 7.42.21 AM.png",
    "King of Hearts":  "Screenshot 2023-06-07 at 7.42.27 AM.png",
    
    "Ace of Spades": "Screenshot 2023-06-07 at 7.42.33 AM.png",
    "2 of Spades": "Screenshot 2023-06-07 at 7.42.39 AM.png",
    "3 of Spades": "Screenshot 2023-06-07 at 7.43.08 AM.png", 
    "4 of Spades": "Screenshot 2023-06-07 at 7.43.13 AM.png",
    "5 of Spades": "Screenshot 2023-06-07 at 7.43.19 AM.png",
    "6 of Spades": "Screenshot 2023-06-07 at 7.43.25 AM.png",
    "7 of Spades": "Screenshot 2023-06-07 at 7.43.30 AM.png",
    "8 of Spades": "Screenshot 2023-06-07 at 7.43.35 AM.png",
    "9 of Spades": "Screenshot 2023-06-07 at 7.43.40 AM.png",
    "10 of Spades": "Screenshot 2023-06-07 at 7.43.50 AM.png",
    "Jack of Spades": "Screenshot 2023-06-07 at 7.43.57 AM.png",
    "Queen of Spades": "Screenshot 2023-06-07 at 7.44.05 AM.png",
    "King of Spades":  "Screenshot 2023-06-07 at 7.44.59 AM.png",
    
}

st.title('Poker Probabilities Calculator')
choice = st.selectbox('Choose Your Mode', ['Probabilities Calculator (just your hand known)','Probabilities Calculator (everyones hand known)']) 
if choice == 'Probabilities Calculator (just your hand known)':
    st.header('Select your hand at the left. Hand must have 2, 5, 6, or 7 cards. If card has not yet been dealt, select None')
    st.subheader('Note that this mode is still very slow when there are 3 or 4 cards out on the table due to the many iterations required.')

    card1 = st.sidebar.selectbox('First Card', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card2 = st.sidebar.selectbox('Second Card',[
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card3 = st.sidebar.selectbox('3rd Card (1st of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card4 = st.sidebar.selectbox('4th Card (2nd of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs'] 
    )

    card5 = st.sidebar.selectbox('5th Card (3rd of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card6 = st.sidebar.selectbox('6th Card (Turn)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs'] 
    )

    card7 = st.sidebar.selectbox('7th Card (River)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )
    
    numPeople = st.selectbox('How many people (including yourself) are still in?',[ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])

    cardx = [card1, card2, card3, card4, card5, card6, card7]
    repeats = False
    for index in range(len(cardx)):
        for index1 in range(len(cardx)):
            if index != index1 and cardx[index] == cardx[index1] and cardx[index] != 'None':
                repeats = True
    
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col3:
        st.write('<-- your cards')
        st.write('cards on table -->')
    if not repeats:
        #initialize first card
        if not 'None' in card1:
            with col1:
                st.image(options[card1], caption=card1, use_column_width=True)
            if 'Clubs' in card1:
                card1_Suit = 'Clubs'
            elif 'Hearts' in card1:
                card1_Suit = 'Hearts'
            elif 'Spades' in card1:
                card1_Suit = 'Spades'
            else:
                card1_Suit = 'Diamonds'
            if '2' in card1:
                card1_Digit = 2
            elif '3' in card1:
                card1_Digit = 3
            elif '4' in card1:
                card1_Digit = 4
            elif '5' in card1:
                card1_Digit = 5
            elif '6' in card1:
                card1_Digit = 6
            elif '7' in card1:
                card1_Digit = 7
            elif '8' in card1:
                card1_Digit = 8
            elif '9' in card1:
                card1_Digit = 9
            elif '10' in card1:
                card1_Digit = 10
            elif 'Jack' in card1:
                card1_Digit = 11
            elif 'Queen' in card1:
                card1_Digit = 12
            elif 'King' in card1:
                card1_Digit = 13
            elif 'Ace' in card1:
                card1_Digit = 14
            FirstCard = Card(card1_Digit, card1_Suit)
        else:
            FirstCard = None

        #initialize second card
        if not 'None' in card2:
            with col2:
                st.image(options[card2], caption=card2, use_column_width=True)
            if 'Clubs' in card2:
                card2_Suit = 'Clubs'
            elif 'Hearts' in card2:
                card2_Suit = 'Hearts'
            elif 'Spades' in card2:
                card2_Suit = 'Spades'
            else:
                card2_Suit = 'Diamonds'
            if '2' in card2:
                card2_Digit = 2
            elif '3' in card2:
                card2_Digit = 3
            elif '4' in card2:
                card2_Digit = 4
            elif '5' in card2:
                card2_Digit = 5
            elif '6' in card2:
                card2_Digit = 6
            elif '7' in card2:
                card2_Digit = 7
            elif '8' in card2:
                card2_Digit = 8
            elif '9' in card2:
                card2_Digit = 9
            elif '10' in card2:
                card2_Digit = 10
            elif 'Jack' in card2:
                card2_Digit = 11
            elif 'Queen' in card2:
                card2_Digit = 12
            elif 'King' in card2:
                card2_Digit = 13
            elif 'Ace' in card2:
                card2_Digit = 14
            SecondCard = Card(card2_Digit, card2_Suit)
        else:
            SecondCard = None

        #initialize third card
        if not 'None' in card3:
            with col4:
                st.image(options[card3], caption=card3, use_column_width=True)
            if 'Clubs' in card3:
                card3_Suit = 'Clubs'
            elif 'Hearts' in card3:
                card3_Suit = 'Hearts'
            elif 'Spades' in card3:
                card3_Suit = 'Spades'
            else:
                card3_Suit = 'Diamonds'
            if '2' in card3:
                card3_Digit = 2
            elif '3' in card3:
                card3_Digit = 3
            elif '4' in card3:
                card3_Digit = 4
            elif '5' in card3:
                card3_Digit = 5
            elif '6' in card3:
                card3_Digit = 6
            elif '7' in card3:
                card3_Digit = 7
            elif '8' in card3:
                card3_Digit = 8
            elif '9' in card3:
                card3_Digit = 9
            elif '10' in card3:
                card3_Digit = 10
            elif 'Jack' in card3:
                card3_Digit = 11
            elif 'Queen' in card3:
                card3_Digit = 12
            elif 'King' in card3:
                card3_Digit = 13
            elif 'Ace' in card3:
                card3_Digit = 14
            ThirdCard = Card(card3_Digit, card3_Suit)
        else:
            ThirdCard = None

        #initialize fourth card
        if not 'None' in card4:
            with col5:
                st.image(options[card4], caption=card4, use_column_width=True)
            if 'Clubs' in card4:
                card4_Suit = 'Clubs'
            elif 'Hearts' in card4:
                card4_Suit = 'Hearts'
            elif 'Spades' in card4:
                card4_Suit = 'Spades'
            else:
                card4_Suit = 'Diamonds'
            if '2' in card4:
                card4_Digit = 2
            elif '3' in card4:
                card4_Digit = 3
            elif '4' in card4:
                card4_Digit = 4
            elif '5' in card4:
                card4_Digit = 5
            elif '6' in card4:
                card4_Digit = 6
            elif '7' in card4:
                card4_Digit = 7
            elif '8' in card4:
                card4_Digit = 8
            elif '9' in card4:
                card4_Digit = 9
            elif '10' in card4:
                card4_Digit = 10
            elif 'Jack' in card4:
                card4_Digit = 11
            elif 'Queen' in card4:
                card4_Digit = 12
            elif 'King' in card4:
                card4_Digit = 13
            elif 'Ace' in card4:
                card4_Digit = 14
            FourthCard = Card(card4_Digit, card4_Suit)
        else:
            FourthCard = None

        #initialize fifth card
        if not 'None' in card5:
            with col6:
                st.image(options[card5], caption=card5, use_column_width=True)
            if 'Clubs' in card5:
                card5_Suit = 'Clubs'
            elif 'Hearts' in card5:
                card5_Suit = 'Hearts'
            elif 'Spades' in card5:
                card5_Suit = 'Spades'
            else:
                card5_Suit = 'Diamonds'
            if '2' in card5:
                card5_Digit = 2
            elif '3' in card5:
                card5_Digit = 3
            elif '4' in card5:
                card5_Digit = 4
            elif '5' in card5:
                card5_Digit = 5
            elif '6' in card5:
                card5_Digit = 6
            elif '7' in card5:
                card5_Digit = 7
            elif '8' in card5:
                card5_Digit = 8
            elif '9' in card5:
                card5_Digit = 9
            elif '10' in card5:
                card5_Digit = 10
            elif 'Jack' in card5:
                card5_Digit = 11
            elif 'Queen' in card5:
                card5_Digit = 12
            elif 'King' in card5:
                card5_Digit = 13
            elif 'Ace' in card5:
                card5_Digit = 14
            FifthCard = Card(card5_Digit, card5_Suit)
        else:
            FifthCard = None

        #initialize sixth card
        if not 'None' in card6:
            with col7:
                st.image(options[card6], caption=card6, use_column_width=True)
            if 'Clubs' in card6:
                card6_Suit = 'Clubs'
            elif 'Hearts' in card6:
                card6_Suit = 'Hearts'
            elif 'Spades' in card6:
                card6_Suit = 'Spades'
            else:
                card6_Suit = 'Diamonds'
            if '2' in card6:
                card6_Digit = 2
            elif '3' in card6:
                card6_Digit = 3
            elif '4' in card6:
                card6_Digit = 4
            elif '5' in card6:
                card6_Digit = 5
            elif '6' in card6:
                card6_Digit = 6
            elif '7' in card6:
                card6_Digit = 7
            elif '8' in card6:
                card6_Digit = 8
            elif '9' in card6:
                card6_Digit = 9
            elif '10' in card6:
                card6_Digit = 10
            elif 'Jack' in card6:
                card6_Digit = 11
            elif 'Queen' in card6:
                card6_Digit = 12
            elif 'King' in card6:
                card6_Digit = 13
            elif 'Ace' in card6:
                card6_Digit = 14
            SixthCard = Card(card6_Digit, card6_Suit)
        else:
            SixthCard = None


        #initialize seventh card
        if not 'None' in card7:
            with col8:
                st.image(options[card7], caption=card7, use_column_width=True)
            if 'Clubs' in card7:
                card7_Suit = 'Clubs'
            elif 'Hearts' in card7:
                card7_Suit = 'Hearts'
            elif 'Spades' in card7:
                card7_Suit = 'Spades'
            else:
                card7_Suit = 'Diamonds'
            if '2' in card7:
                card7_Digit = 2
            elif '3' in card7:
                card7_Digit = 3
            elif '4' in card7:
                card7_Digit = 4
            elif '5' in card7:
                card7_Digit = 5
            elif '6' in card7:
                card7_Digit = 6
            elif '7' in card7:
                card7_Digit = 7
            elif '8' in card7:
                card7_Digit = 8
            elif '9' in card7:
                card7_Digit = 9
            elif '10' in card7:
                card7_Digit = 10
            elif 'Jack' in card7:
                card7_Digit = 11
            elif 'Queen' in card7:
                card7_Digit = 12
            elif 'King' in card7:
                card7_Digit = 13
            elif 'Ace' in card7:
                card7_Digit = 14
            SeventhCard = Card(card7_Digit, card7_Suit)
        else:
            SeventhCard = None
        
        hand = Game(FirstCard, SecondCard, ThirdCard, FourthCard, FifthCard, SixthCard, SeventhCard)
        
        cardsOut = 0
        if FirstCard != None:
            cardsOut += 1
            if SecondCard != None:
                cardsOut += 1
                if ThirdCard != None:
                    cardsOut += 1
                    if FourthCard != None:
                        cardsOut += 1
                        if FifthCard != None:
                            cardsOut += 1
                            if SixthCard != None:
                                cardsOut += 1
                                if SeventhCard != None:
                                    cardsOut += 1
        
        if cardsOut not in (2, 5, 6, 7):
            st.write('Choose 2, 5, 6, or 7 cards please')
        else:
            if cardsOut == 2:
                #st.write('Cards Dealt: ' + FirstCard.getCard() + ', ' + SecondCard.getCard())
                hand.setNumPlayers(numPeople)
                prob = hand.probabilityDealt()
                st.write('Your probability of winning a game of ' + str(numPeople) + ' players after being dealt ' + FirstCard.getCard() + ' and ' + SecondCard.getCard() + ' is ' + str(prob) + '%')
            elif cardsOut == 5:
               # st.write('Cards Dealt: ' + FirstCard.getCard() + ', ' + SecondCard.getCard())
               # st.write('Cards that came out on the flop: ' + ThirdCard.getCard() + ', ' + FourthCard.getCard() + ', ' + FifthCard.getCard())
                
                tot, average, prop, minDuo, maxDuo = hand.probabilityFlop()
                st.write('Probability of winning: ' + str(100*(prop**(numPeople-1))) + '%')
                st.write('Best combo of cards to come out: ' + maxDuo[0].getCard() + ', ' + maxDuo[0].getCard())
                st.write('Worst combo of cards to come out ' + minDuo[0].getCard() + ', ' + minDuo[1].getCard())
                
                if st.button('See breakdown by possible two-card combinations'):
                    for entry in tot:
                        propWin, propLoss, propTie = probWinningLosingTying(numPeople, entry[1], entry[2], entry[3], entry[0])
                        st.write('Duo: ' + entry[4].getCard() + ', ' + entry[5].getCard() + ', win probability: ' + str(100*propWin) + '%, tie probability: ' + str(100*propTie) + '%, loss probability: ' + str(100*propLoss) + '%')
            elif cardsOut == 6:
               # st.write('Cards Dealt: ' + FirstCard.getCard() + ', ' + SecondCard.getCard())
               # st.write('Cards that came out on the flop: ' + ThirdCard.getCard() + ', ' + FourthCard.getCard() + ', ' + FifthCard.getCard())
               # st.write('Card that came out on the turn: ' + SixthCard.getCard())
                
                
                
                tot, average, prop, minCard, maxCard = hand.probabilityTurn()
                st.write('For each of the ' + str(len(tot)) + ' possible cards to come out on the river, you would win an average of ' + str(average) + ' out of 990 possible hands')
                st.write('your probability of winning with ' + str(numPeople) + ' left in the game is : ' + str(100*(prop**(numPeople-1))) + '%')
                st.write('Best card to come out on the river: ' + maxCard.getCard())
                st.write('Worst card to come out on the river: ' + minCard.getCard())
                
                if st.button('See breakdown by possible cards to come out on the river'):
                    for entry in tot:
                        propWin, propLoss, propTie = probWinningLosingTying(numPeople, entry[1], entry[2], entry[3], entry[0])
                        st.write('Card: ' + entry[4].getCard() + ', win probability: ' + str(round(100*propWin, 3)) + '%, tie probability: ' + str(round(100*propTie, 3)) + '%, loss probability: ' + str(round(100*propLoss, 3)) + '%')

            elif cardsOut == 7:
                #st.write('Cards Dealt: ' + FirstCard.getCard() + ', ' + SecondCard.getCard())
               # st.write('Cards that came out on the flop: ' + ThirdCard.getCard() + ', ' + FourthCard.getCard() + ', ' + FifthCard.getCard())
               # st.write('Card that came out on the turn: ' + SixthCard.getCard())
               # st.write('Card that came out on the river: ' + SeventhCard.getCard())
                
                totalGames, numWon, numTied, numLost, bestHand, subscore, superSubScore = hand.findProbabilityRiver()
                if subscore == 14:
                    subscore = 'Ace'
                elif subscore == 13:
                    subscore = 'King'
                elif subscore == 12:
                    subscore = 'Queen'
                elif subscore == 11:
                    subscore = 'Jack'
                if superSubScore == 14:
                    superSubScore = 'Ace'
                elif superSubScore == 13:
                    superSubScore = 'King'
                elif superSubScore == 12:
                    superSubScore = 'Queen'
                elif superSubScore == 11:
                    superSubScore = 'Jack'
                st.write('You have a ' + bestHand + ' with a top card of ' + str(subscore) + ' and a second top card of ' + str(superSubScore))
                st.write('total number of other possible hands that people could have: ' + str(totalGames))
                st.write('Out of ' + str(totalGames) + ' other possible hands, you would beat ' + str(numWon))
                st.write('Out of ' + str(totalGames) + ' other possible hands, you would tie ' + str(numTied))
                st.write('Out of ' + str(totalGames) + ' other possible hands, you would lose to ' + str(numLost))
                probWin, probLose, probTie = probWinningLosingTying(numPeople, numWon, numTied, numLost, totalGames)
                st.write('Given that there are ' + str(numPeople - 1) + ' other people remaining, you have a ' 
                         + str(round(100*probWin, 3)) + "% probability of winning, a " + str(round(100*probTie, 3)) + "% probability of tying, and a "
                         + str(round(100*probLose, 3)) + "% probability of losing")
        
    else:
        st.write('No repeat cards allowed. Please change your selected cards')

elif choice == 'Probabilities Calculator (everyones hand known)':
    st.header('Select your hand at the left. Each hand must be full and table must have 0, 3, 4, or 5 cards. If card has not yet been dealt, select None')
    numPlayers = st.selectbox('Select the number of players in the game (including yourself)', [2,3,4,5,6,7,8,9,10])
    
    st.sidebar.write('Select Cards on the Table - If a card has not come out yet select None')
    card3 = st.sidebar.selectbox('1st Card on Table (1st of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card4 = st.sidebar.selectbox('2nd Card on Table (2nd of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs'] 
    )

    card5 = st.sidebar.selectbox('3rd Card on Table (3rd of flop)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )

    card6 = st.sidebar.selectbox('4th Card on Table (Turn)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs'] 
    )

    card7 = st.sidebar.selectbox('5th Card on Table (River)', [
    'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
    , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
    '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
    'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
    , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
    '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
    'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
    , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
    '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
    'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
    , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
    '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
    'King of Clubs', 'Ace of Clubs']
    )
    
    totalCardz = [card3, card4, card5, card6, card7]
    repeats = False
    num = 0
    for item in totalCardz:
        if item != 'None':
            num += 1
    for index in range(len(totalCardz)):
        for index1 in range(index + 1, len(totalCardz)):
            if totalCardz[index] == totalCardz[index1] and totalCardz[index] != 'None':
                repeats = True
                
    
    if repeats:
        st.write('Error: duplicate cards selected')
    elif num != 0 and num != 3 and num != 4 and num != 5:
        st.write('Error: must be 0, 3, 4, or 5 cards on the table')
    else:
        players = []
        theseColumns = st.columns(3*numPlayers)
        for i in range(1, numPlayers + 1):
            st.sidebar.write('Select Cards for player ' + str(i))
            PersonCard1 = st.sidebar.selectbox('First Card for Player ' + str(i), [
        'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
        , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
        '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
        'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
        , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
        '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
        'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
        , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
        '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
        'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
        , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
        '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
        'King of Clubs', 'Ace of Clubs']
        )

            PersonCard2 = st.sidebar.selectbox('2nd Card for Player ' + str(i), [
        'None', '2 of Hearts', '3 of Hearts', '4 of Hearts'
        , '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', 
        '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts',
        'King of Hearts', 'Ace of Hearts', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds'
        , '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', 
        '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds',
        'King of Diamonds', 'Ace of Diamonds', '2 of Spades', '3 of Spades', '4 of Spades'
        , '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', 
        '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades',
        'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs'
        , '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', 
        '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs',
        'King of Clubs', 'Ace of Clubs'] 
        )
        
            if PersonCard2 == 'None' or PersonCard1 == 'None':
                st.write('Error: Cards for Player ' + str(i) + ' cannot be None')
            elif PersonCard1 in totalCardz or PersonCard2 in totalCardz:
                st.write('Error: Cards selected for Player ' + str(i) + ' are already used')
            elif PersonCard1 == PersonCard2:
                st.write('Error: Duplicate Cards Selected for Player ' + str(i))
            else:
                totalCardz.append(PersonCard1)
                totalCardz.append(PersonCard2)
                with theseColumns[3*(i-1)]:
                    st.write('Cards for Player ' + str(i) + ' -->')
                with theseColumns[3*(i-1) + 1]:
                    st.image(options[PersonCard1], caption=PersonCard1, use_column_width=True)
                with theseColumns[3*(i-1) + 2]:
                    st.image(options[PersonCard2], caption=PersonCard2, use_column_width=True)
                    
                if 'Clubs' in PersonCard1:
                    PersonCard1_Suit = 'Clubs'
                elif 'Hearts' in PersonCard1:
                    PersonCard1_Suit = 'Hearts'
                elif 'Spades' in PersonCard1:
                    PersonCard1_Suit = 'Spades'
                else:
                    PersonCard1_Suit = 'Diamonds'
                if '2' in PersonCard1:
                    PersonCard1_Digit = 2
                elif '3' in PersonCard1:
                    PersonCard1_Digit = 3
                elif '4' in PersonCard1:
                    PersonCard1_Digit = 4
                elif '5' in PersonCard1:
                    PersonCard1_Digit = 5
                elif '6' in PersonCard1:
                    PersonCard1_Digit = 6
                elif '7' in PersonCard1:
                    PersonCard1_Digit = 7
                elif '8' in PersonCard1:
                    PersonCard1_Digit = 8
                elif '9' in PersonCard1:
                    PersonCard1_Digit = 9
                elif '10' in PersonCard1:
                    PersonCard1_Digit = 10
                elif 'Jack' in PersonCard1:
                    PersonCard1_Digit = 11
                elif 'Queen' in PersonCard1:
                    PersonCard1_Digit = 12
                elif 'King' in PersonCard1:
                    PersonCard1_Digit = 13
                elif 'Ace' in PersonCard1:
                    PersonCard1_Digit = 14
                FirstCard = Card(PersonCard1_Digit, PersonCard1_Suit)
                
                if 'Clubs' in PersonCard2:
                    PersonCard2_Suit = 'Clubs'
                elif 'Hearts' in PersonCard2:
                    PersonCard2_Suit = 'Hearts'
                elif 'Spades' in PersonCard2:
                    PersonCard2_Suit = 'Spades'
                else:
                    PersonCard2_Suit = 'Diamonds'
                if '2' in PersonCard2:
                    PersonCard2_Digit = 2
                elif '3' in PersonCard2:
                    PersonCard2_Digit = 3
                elif '4' in PersonCard2:
                    PersonCard2_Digit = 4
                elif '5' in PersonCard2:
                    PersonCard2_Digit = 5
                elif '6' in PersonCard2:
                    PersonCard2_Digit = 6
                elif '7' in PersonCard2:
                    PersonCard2_Digit = 7
                elif '8' in PersonCard2:
                    PersonCard2_Digit = 8
                elif '9' in PersonCard2:
                    PersonCard2_Digit = 9
                elif '10' in PersonCard2:
                    PersonCard2_Digit = 10
                elif 'Jack' in PersonCard2:
                    PersonCard2_Digit = 11
                elif 'Queen' in PersonCard2:
                    PersonCard2_Digit = 12
                elif 'King' in PersonCard2:
                    PersonCard2_Digit = 13
                elif 'Ace' in PersonCard2:
                    PersonCard2_Digit = 14
                SecondCard = Card(PersonCard2_Digit, PersonCard2_Suit)

                thisPlayer = Player(i, FirstCard, SecondCard)
                players.append(thisPlayer)

            #initialize third card
        st.write('\n')
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.write('Cards on table -->')
       
        if not 'None' in card3:
            with col2:
                st.image(options[card3], caption=card3, use_column_width=True)
            if 'Clubs' in card3:
                card3_Suit = 'Clubs'
            elif 'Hearts' in card3:
                card3_Suit = 'Hearts'
            elif 'Spades' in card3:
                card3_Suit = 'Spades'
            else:
                card3_Suit = 'Diamonds'
            if '2' in card3:
                card3_Digit = 2
            elif '3' in card3:
                card3_Digit = 3
            elif '4' in card3:
                card3_Digit = 4
            elif '5' in card3:
                card3_Digit = 5
            elif '6' in card3:
                card3_Digit = 6
            elif '7' in card3:
                card3_Digit = 7
            elif '8' in card3:
                card3_Digit = 8
            elif '9' in card3:
                card3_Digit = 9
            elif '10' in card3:
                card3_Digit = 10
            elif 'Jack' in card3:
                card3_Digit = 11
            elif 'Queen' in card3:
                card3_Digit = 12
            elif 'King' in card3:
                card3_Digit = 13
            elif 'Ace' in card3:
                card3_Digit = 14
            ThirdCard = Card(card3_Digit, card3_Suit)
        else:
            ThirdCard = None

        #initialize fourth card
        if not 'None' in card4:
            with col3:
               st.image(options[card4], caption=card4, use_column_width=True)
            if 'Clubs' in card4:
                card4_Suit = 'Clubs'
            elif 'Hearts' in card4:
                card4_Suit = 'Hearts'
            elif 'Spades' in card4:
                card4_Suit = 'Spades'
            else:
                card4_Suit = 'Diamonds'
            if '2' in card4:
                card4_Digit = 2
            elif '3' in card4:
                card4_Digit = 3
            elif '4' in card4:
                card4_Digit = 4
            elif '5' in card4:
                card4_Digit = 5
            elif '6' in card4:
                card4_Digit = 6
            elif '7' in card4:
                card4_Digit = 7
            elif '8' in card4:
                card4_Digit = 8
            elif '9' in card4:
                card4_Digit = 9
            elif '10' in card4:
                card4_Digit = 10
            elif 'Jack' in card4:
                card4_Digit = 11
            elif 'Queen' in card4:
                card4_Digit = 12
            elif 'King' in card4:
                card4_Digit = 13
            elif 'Ace' in card4:
                card4_Digit = 14
            FourthCard = Card(card4_Digit, card4_Suit)
        else:
            FourthCard = None

        #initialize fifth card
        if not 'None' in card5:
            with col4:
                st.image(options[card5], caption=card5, use_column_width=True)
            if 'Clubs' in card5:
                card5_Suit = 'Clubs'
            elif 'Hearts' in card5:
                card5_Suit = 'Hearts'
            elif 'Spades' in card5:
                card5_Suit = 'Spades'
            else:
                card5_Suit = 'Diamonds'
            if '2' in card5:
                card5_Digit = 2
            elif '3' in card5:
                card5_Digit = 3
            elif '4' in card5:
                card5_Digit = 4
            elif '5' in card5:
                card5_Digit = 5
            elif '6' in card5:
                card5_Digit = 6
            elif '7' in card5:
                card5_Digit = 7
            elif '8' in card5:
                card5_Digit = 8
            elif '9' in card5:
                card5_Digit = 9
            elif '10' in card5:
                card5_Digit = 10
            elif 'Jack' in card5:
                card5_Digit = 11
            elif 'Queen' in card5:
                card5_Digit = 12
            elif 'King' in card5:
                card5_Digit = 13
            elif 'Ace' in card5:
                card5_Digit = 14
            FifthCard = Card(card5_Digit, card5_Suit)
        else:
            FifthCard = None

        #initialize sixth card
        if not 'None' in card6:
            with col5:
                st.image(options[card6], caption=card6, use_column_width=True)
            if 'Clubs' in card6:
                card6_Suit = 'Clubs'
            elif 'Hearts' in card6:
                card6_Suit = 'Hearts'
            elif 'Spades' in card6:
                card6_Suit = 'Spades'
            else:
                card6_Suit = 'Diamonds'
            if '2' in card6:
                card6_Digit = 2
            elif '3' in card6:
                card6_Digit = 3
            elif '4' in card6:
                card6_Digit = 4
            elif '5' in card6:
                card6_Digit = 5
            elif '6' in card6:
                card6_Digit = 6
            elif '7' in card6:
                card6_Digit = 7
            elif '8' in card6:
                card6_Digit = 8
            elif '9' in card6:
                card6_Digit = 9
            elif '10' in card6:
                card6_Digit = 10
            elif 'Jack' in card6:
                card6_Digit = 11
            elif 'Queen' in card6:
                card6_Digit = 12
            elif 'King' in card6:
                card6_Digit = 13
            elif 'Ace' in card6:
                card6_Digit = 14
            SixthCard = Card(card6_Digit, card6_Suit)
        else:
            SixthCard = None


        #initialize seventh card
        if not 'None' in card7:
            with col6:
                st.image(options[card7], caption=card7, use_column_width=True)
            if 'Clubs' in card7:
                card7_Suit = 'Clubs'
            elif 'Hearts' in card7:
                card7_Suit = 'Hearts'
            elif 'Spades' in card7:
                card7_Suit = 'Spades'
            else:
                card7_Suit = 'Diamonds'
            if '2' in card7:
                card7_Digit = 2
            elif '3' in card7:
                card7_Digit = 3
            elif '4' in card7:
                card7_Digit = 4
            elif '5' in card7:
                card7_Digit = 5
            elif '6' in card7:
                card7_Digit = 6
            elif '7' in card7:
                card7_Digit = 7
            elif '8' in card7:
                card7_Digit = 8
            elif '9' in card7:
                card7_Digit = 9
            elif '10' in card7:
                card7_Digit = 10
            elif 'Jack' in card7:
                card7_Digit = 11
            elif 'Queen' in card7:
                card7_Digit = 12
            elif 'King' in card7:
                card7_Digit = 13
            elif 'Ace' in card7:
                card7_Digit = 14
            SeventhCard = Card(card7_Digit, card7_Suit)
        else:
            SeventhCard = None
        
        numPlayers = int(numPlayers)
        game = multipleHands(numPlayers)
        game.cardsOnTable(ThirdCard, FourthCard, FifthCard, SixthCard, SeventhCard)
        for him in players:
            num = him.getPlayerNum()
            card1 = him.getCard1()
            card2 = him.getCard2()
            game.setCards(num, card1, card2)
        
        numCards = game.getNumCards()
        nums = (0, 3, 4, 5)
        
        complete = False
        for i in range(5, len(totalCardz) - 1):
            if totalCardz[i] == 'None':
                complete = True
                break
        if complete:
            st.write('Error: please fill out all players cards')
        elif numCards not in nums:
            st.write('Error: Number of Cards on table is not 0, 3, 4, or 5')
        elif numCards == 0 and game.getPlayerCards() == 2*numPlayers:
            probabilities, maxPlayers, minPlayers, tiedWinner, tiedLoser = game.FindProbs()
            for i in range(len(probabilities)):
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Cards: ' + players[i].getCard1().getCard() + ', ' + players[i].getCard2().getCard())
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Probability of Winning: ' + str(probabilities[i]))
        elif numCards == 3 and game.getPlayerCards() == 2*numPlayers:
            winners, victor, winnersCards, winners1 = game.FindProbs()
            for i in range(len(winners)):
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Cards: ' + players[i].getCard1().getCard() + ', ' + players[i].getCard2().getCard())
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Probability of Winning: ' + str(winners[i]))
            
            numbers = ['None']
            for i in range(1, numPlayers+1):
                numbers.append('Player ' + str(i))
            
            chosenNum = st.radio(
                 "Click to see the 10 best cards that could come out for each player from best to worst", numbers)
            total = []
            for i in range(numPlayers):
                theseCards = {}
                for card in winnersCards[i]:
                    card1 = card[0].getCard()
                    card2 = card[1].getCard()
                    if card1 in theseCards:
                        theseCards[card1] += 1
                    else:
                        theseCards[card1] = 1
                    if card2 in theseCards:
                        theseCards[card2] += 1
                    else:
                        theseCards[card2] = 1
                theseCards = sorted(theseCards.items(), key=lambda x: x[1], reverse=True)
                total.append(theseCards)

            if 'Player' in chosenNum:
                num = int(chosenNum.split()[-1])
                theseCards = total[num-1]
                st.write(len(winnersCards[num-1]))

                max = 0
                if len(theseCards) >= 10:
                    most_common_cards = theseCards
                    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
                    cardx1 = most_common_cards[0][0]
                    cardx2 = most_common_cards[1][0]
                    cardx3 = most_common_cards[2][0]
                    cardx4 = most_common_cards[3][0]
                    cardx5 = most_common_cards[4][0]
                    cardx6 = most_common_cards[5][0]
                    cardx7 = most_common_cards[6][0]
                    cardx8 = most_common_cards[7][0]
                    cardx9 = most_common_cards[8][0]
                    cardx10 = most_common_cards[9][0]
                    
                    with col1:
                        st.image(options[cardx1], caption = cardx1, use_column_width = True)
                        st.write(most_common_cards[0][1])
                    with col2: 
                        st.image(options[cardx2], caption = cardx2, use_column_width = True)
                        st.write(most_common_cards[1][1])
                    with col3:
                        st.image(options[cardx3], caption = cardx3, use_column_width = True)
                        st.write(most_common_cards[2][1])
                    with col4:
                        st.image(options[cardx4], caption = cardx4, use_column_width = True)
                        st.write(most_common_cards[3][1])
                    with col5:
                        st.image(options[cardx5], caption = cardx5, use_column_width = True)
                        st.write(most_common_cards[4][1])
                    with col6:
                        st.image(options[cardx6], caption = cardx6, use_column_width = True)
                        st.write(most_common_cards[5][1])
                    with col7: 
                        st.image(options[cardx7], caption = cardx7, use_column_width = True)
                        st.write(most_common_cards[6][1])
                    with col8:
                        st.image(options[cardx8], caption = cardx8, use_column_width = True)
                        st.write(most_common_cards[7][1])
                    with col9:
                        st.image(options[cardx9], caption = cardx9, use_column_width = True)
                        st.write(most_common_cards[8][1])
                    with col10:
                        st.image(options[cardx10], caption = cardx10, use_column_width = True)
                        st.write(most_common_cards[9][1])
                else:
                    most_common_cards = sorted(theseCards.items(), key=lambda x: x[1], reverse=True)
                    columns = st.columns(len(theseCards))
                    for i in range(len(columns)):
                        column = columns[i]
                        with column:
                            card = most_common_cards[i][0]
                            st.image(options[card], caption=card, use_column_width = True)
                      
        elif numCards == 4 and game.getPlayerCards() == 2*numPlayers:
            winners, victor, winnersCards, winners1 = game.FindProbs()
            for i in range(len(winners)):
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Cards: ' + players[i].getCard1().getCard() + ', ' + players[i].getCard2().getCard())
                st.write('Player ' + str(players[i].getPlayerNum()) + ' Probability of Winning: ' + str(winners[i]))
            numbers = ['None']
            for i in range(1, numPlayers+1):
                numbers.append('Player ' + str(i))
            
            
            chosenNum = st.radio(
                 "Click to see which cards would have to come out for each player to win",
                 numbers)
            if 'Player' in chosenNum:
                columns = st.columns(5)
                num = int(chosenNum.split()[-1])
                thisNumber = 0
                for card in winnersCards[num - 1]:
                    with columns[thisNumber%5]:
                        card = card.getCard()
                        st.write(card)
                        st.image(options[card], caption=card, use_column_width = True)
                        thisNumber += 1
                
        elif numCards == 5 and game.getPlayerCards() == 2*numPlayers:
            for player in players:
                st.write('Cards for Player ' + str(player.getPlayerNum()) + ': ' + player.getCard1().getCard() + ', ' + player.getCard2().getCard())
            
            victor, winners, tie, TheseScores = game.FindProbs() 
            for entry in TheseScores:
                st.write('Player ' + str(entry[6] + 1) + ' has ' + entry[7])
            
            if not tie:
                st.write('The winner is player ' + str(victor[0] + 1) + ' with a hand of ' + TheseScores[len(TheseScores) - 1][7])
            else:
                st.write('Tie with a hand of ' + TheseScores[numPlayers-1][7] + ' between:')
                for stuff in victor:
                    st.write('Player ' + str(stuff + 1))
