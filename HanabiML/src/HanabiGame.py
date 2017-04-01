'''
Created on Mar 11, 2017
@author: dennis
'''

import random
from random import randint

class HanabiGame:
    'Common base class for all games of Hanabi.'
    'At this point we could have defined some class variables...'
    
    def __init__(self, numPlayers):
        print("Let's play a new game of Hanabi!")
        print("Creating a game with", numPlayers, "players...")
        self.numPlayers = numPlayers
        'This variable shows whether we are in the last round, or not. The last round begins when the final card of the stack is drawn.'
        self.isLastRound = False
        'The information tokens can be spent by the players in order to give info to their teamates.'
        self.numInfoTokens = 8
        'The fuse tokens are spent whenever the players make an error, and they represent their lives.'
        self.numFuseTokens = 3 
        'The complete list of cards which are used in a game of Hanabi.'
        self.cardList = []
        for i in range(0, len(Card.cardColors)):
            currentColor = Card.cardColors[i]
            for j in range(0, 3):
                'There are 3 cards with number 1 (for each color).'
                self.cardList.append(Card(currentColor, 1))
            for j in range(0, 2):
                'There are 2 cards with number 2 (for each color).'
                self.cardList.append(Card(currentColor, 2))
            for j in range(0, 2):
                'There are 2 cards with number 3 (for each color).'
                self.cardList.append(Card(currentColor, 3))
            for j in range(0, 2):
                'There are 2 cards with number 4 (for each color).'
                self.cardList.append(Card(currentColor, 4))
            for j in range(0, 1):
                'There is 1 card with number 5 (for each color).'
                self.cardList.append(Card(currentColor, 5))
        print()
        #print("cardList size is", len(cardList))
        #print(cardList[8].color)
        'Create (and shuffle) the game\'s stack pile (check that the cloning is properly done).'
        self.stackPile = self.cardList[:]
        random.shuffle(self.stackPile)
        #print(self.stackPile[40].color)
        'Create the game\'s discard pile, which is initially empty.'
        self.discardPile = []
        'Create the game\'s played firework-series. There are five lists of numbers (each one for a different color). They are all initially empty.'
        self.playedSeriesWhite = []
        self.playedSeriesYellow = []
        self.playedSeriesRed = []
        self.playedSeriesGreen = []
        self.playedSeriesBlue = []
        'Create the game\'s list of players.'
        self.playersList = []
        for i in range(0, numPlayers):
            self.playersList.append(Player(i, self))
        '****************'
        'Launch the game!'
        self.launchGame()
        '****************'
    
    def launchGame(self):
        print("Let the game begin!")
        playerToPlay = 0
        lastRoundCountdown = self.numPlayers
        'This is the game\'s protocol: the players play, one after the other, until some stopping condition is satisfied.'
        while ( (self.numFuseTokens > 0) & ( (not self.isLastRound) | lastRoundCountdown > 0)):
            self.playersList[playerToPlay].play()
            if (playerToPlay < len(self.playersList)-1):
                playerToPlay += 1
            else:
                playerToPlay = 0
            if (self.isLastRound):
                lastRoundCountdown -= lastRoundCountdown
        'When the game finishes, print the score!'
        print("$$$$$ Score =", self.computeScore(), "/ 25 $$$$$")
        
    def computeScore(self):
        'We add the highest numbers of all the played firework-series.'
        score = 0
        if (len(self.playedSeriesWhite) > 0):
            score += self.playedSeriesWhite[-1].number  
        if (len(self.playedSeriesYellow) > 0):
            score += self.playedSeriesYellow[-1].number  
        if (len(self.playedSeriesRed) > 0):
            score += self.playedSeriesRed[-1].number
        if (len(self.playedSeriesGreen) > 0):
            score += self.playedSeriesGreen[-1].number
        if (len(self.playedSeriesBlue) > 0):
            score += self.playedSeriesBlue[-1].number    
        return score        
    
    def getCardList(self):
        return self.cardList
    
    def getStackPile(self):
        return self.stackPile
    
    def getDiscardPile(self):
        return self.discardPile
#######################################################################################################################    
class Card:
    'Card colors are White (W), Yellow (Y), Red (R), Green (G), and Blue (B).'
    cardColors = ["W", "Y", "R", "G", "B"]
    
    def __init__(self, color, number):
        self.color = color
        self.number = number 
        #print("Creating a Hanabi card:")    
        #self.printCard()
   
    def getCardColor(self):
        return self.color
    
    def getCardNumber(self):
        return self.number

    def printCard(self):
        print(self.color, "/", self.number)
###############################################################################################################################
class Player:
    
    def __init__(self, pID, game):
        self.pID = 'X'
        if (pID == 0): self.pID = 'A'
        if (pID == 1): self.pID = 'B'
        if (pID == 2): self.pID = 'C'
        if (pID == 3): self.pID = 'D'   
        if (pID == 4): self.pID = 'E'
        print("Creating a new player with pID:", self.pID)
        
        self.game = game
        'Decide how many cards the player draws at the beginning of the game.'
        self.cardsInHand = []
        if (self.game.numPlayers == 2 | self.game.numPlayers == 3):
            self.drawCards(5)
        else:
            self.drawCards(4) 
        for i in range(0, len(self.cardsInHand)):
            self.cardsInHand[i].printCard()
        print()
        'The initial beliefs of the player concerning the colors of his cards.'
        self.cardsInHandColorBeliefs = []
        for i in range(0, len(self.cardsInHand)):
            self.cardsInHandColorBeliefs.append("?")
        'The initial beliefs of the player concerning the numbers of his cards.'
        self.cardsInHandNumberBeliefs = []
        for i in range(0, len(self.cardsInHand)):
            self.cardsInHandNumberBeliefs.append("?")
                            
    def drawCards(self, number):
        for i in range(0, number):
            if (len(self.game.stackPile) != 0):
                self.cardsInHand.append(self.game.stackPile[0])   
                self.game.stackPile.pop(0)
                'As soon as the last card is drawn from the stack, the final round starts (all players will play, at most, one more time).'
                if (len(self.game.stackPile) == 0):
                    self.game.isLastRound = True
    
    def play(self):
        if (self.game.numInfoTokens == 0):
            'Possibilities: discard, play.' 
            moveType = randint(1,2)
        if (self.game.numInfoTokens > 0):
            'Possibilities: discard, play, give info.'
            moveType = randint(1,3)
        
        if (moveType == 1):
            print("*** Player", self.pID, "discards a card. ***")
            'The player chooses a (random) card from his hand, and discards it.'
            'Then, he adds a new info token (if there are currently less than 8).'
            'Finally, he draws a new card.'            
            toDiscard = randint(0, len(self.cardsInHand)-1)
            'Put the chosen card in the discard pile.'
            self.game.getDiscardPile().append(self.cardsInHand[toDiscard])
            'The card is no longer in the player\'s hand.'
            del(self.cardsInHand[toDiscard])
            del(self.cardsInHandColorBeliefs[toDiscard])
            del(self.cardsInHandNumberBeliefs[toDiscard])
            'If there are less than 8 info tokens, then add one info token.'
            if (self.game.numInfoTokens < 8):
                self.game.numInfoTokens += 1
            'Draw a new card.'
            self.drawCards(1)
            self.cardsInHandColorBeliefs.append("?")
            self.cardsInHandNumberBeliefs.append("?")
        
        if (moveType == 2):
            print("*** Player", self.pID, "plays a firework. ***")
            'CASE 1: It\'s a valid move, thus the series of the corresponding color is updated.'
            'Also, if a 5 was played, and there are less than 8 info tokens, then add one info token.'
            'CASE 2: It\'s not a valid move, thus the series are not updated.'
            'Also, the number of fuse tokens decreases by 1.'
            'In either case, the player draws a card.'
            toPlay = randint(0, len(self.cardsInHand)-1)
            cardToPlay = self.cardsInHand[toPlay]
            validMove = False
            if ( (cardToPlay.color == "W") & (cardToPlay.number == len(self.game.playedSeriesWhite) + 1) ):
                validMove = True
                self.game.playedSeriesWhite.append(cardToPlay)
            if ( (cardToPlay.color == "Y") & (cardToPlay.number == len(self.game.playedSeriesYellow) + 1) ):
                validMove = True
                self.game.playedSeriesYellow.append(cardToPlay)
            if ( (cardToPlay.color == "R") & (cardToPlay.number == len(self.game.playedSeriesRed) + 1) ):
                validMove = True
                self.game.playedSeriesRed.append(cardToPlay)
            if ( (cardToPlay.color == "G") & (cardToPlay.number == len(self.game.playedSeriesGreen) + 1) ):
                validMove = True
                self.game.playedSeriesGreen.append(cardToPlay)
            if ( (cardToPlay.color == "B") & (cardToPlay.number == len(self.game.playedSeriesBlue) + 1) ):
                validMove = True 
                self.game.playedSeriesBlue.append(cardToPlay)
            'The card is no longer in the player\'s hand.'
            del(self.cardsInHand[toPlay])
            del(self.cardsInHandColorBeliefs[toPlay])
            del(self.cardsInHandNumberBeliefs[toPlay])
            'Check if the number of info tokens must be increased.'
            if (validMove & (cardToPlay.number == 5) & (self.game.numInfoTokens < 8)):
                self.game.numInfoTokens += 1
            'If it was not a valid move, then we spend a fuse counter.'
            if (not validMove):
                self.game.numFuseTokens -= 1
            'Draw a new card.'
            self.drawCards(1)
            self.cardsInHandColorBeliefs.append("?")
            self.cardsInHandNumberBeliefs.append("?")
            
        if (moveType == 3):
            print("*** Player", self.pID, "uses an info token. ***")
            'The player gives information to a (random) co-player, about some of his cards\' colors or numbers.'
            'We assume that each player knows the beliefs of each other player concerning his own cards.'
            'We assume that the player who gets this information, updates his beliefs about his cards (in a correct and complete way).'
            'First, choose (at random) another player to inform.'
            playerToInform = self
            while (playerToInform == self):
                toInform = randint(0, len(self.game.playersList)-1)
                playerToInform = self.game.playersList[toInform]
            print("Player", self.pID, "chose to inform player", playerToInform.pID)
            'Choose to inform that player on the basis of a (random) card which he holds.'
            cardInfoBasis = playerToInform.cardsInHand[randint(0, len(playerToInform.cardsInHand)-1)]
            print("He will inform him on the basis of the following card:")
            cardInfoBasis.printCard()
            'The player will send a list, whose first element is either a number, or a color, that the other player has, and'
            'all the other elements of the list are the positions in that player\'s hand where such color, or such number, is found.'
            infoToSend = []
            'Decide (randomly) if you will inform him on colors, or on numbers.'
            if (randint(0, 1) == 0):
                'Inform the player on his colors.'
                infoToSend.append(cardInfoBasis.getCardColor())
                'Tell him which are all his cards which have the same color as the cardInfoBasis card.'
                for i in range (0, len(playerToInform.cardsInHand)):
                    if (playerToInform.cardsInHand[i].getCardColor() == infoToSend[0]):
                        infoToSend.append(i) 
            else:
                'Inform the player on his numbers.'
                infoToSend.append(cardInfoBasis.getCardNumber())
                'Tell him which are all his cards which have the same number as the cardInfoBasis card.'
                for i in range (0, len(playerToInform.cardsInHand)):
                    if (playerToInform.cardsInHand[i].getCardNumber() == infoToSend[0]):
                        infoToSend.append(i)
            'Now pass the information to the other player (and update, for him, his beliefs about his cards).'
            for i in range(0, len(infoToSend)):
                print(infoToSend[i])
            if (type(infoToSend[0]) is int):
                print("Info is about a number.")
                for i in range(1, len(infoToSend)):
                    playerToInform.cardsInHandNumberBeliefs[infoToSend[i]] = infoToSend[0]
            else:
                print("Info is about a color.")
                for i in range(1, len(infoToSend)):
                    playerToInform.cardsInHandColorBeliefs[infoToSend[i]] = infoToSend[0]
            'Finally, decrease by 1 the number of info tokens.'
            self.game.numInfoTokens -= 1
            
######################################################################################################################################            

'Create (and launch) a Hanabi game with 3 players.'
game = HanabiGame(3);

'''
print("StackPile size =", len(game.stackPile))
print("Game score is = ", game.computeScore())
firstPlayer = game.playersList[0]
secondPlayer = game.playersList[1]
print("These are the cards of Player", firstPlayer.pID, ":")
for i in range(0, len(firstPlayer.cardsInHand)):
    firstPlayer.cardsInHand[i].printCard()
print("These are the beliefs of Player", firstPlayer.pID, "about his cards:")
for i in range(0, len(firstPlayer.cardsInHandColorBeliefs)):
    print("Color:", firstPlayer.cardsInHandColorBeliefs[i], "Number:", firstPlayer.cardsInHandNumberBeliefs[i])

print("Num of fuse tokens =", game.numFuseTokens)
firstPlayer.play()
print("Game score is = ", game.computeScore())
print("Num of fuse tokens =", game.numFuseTokens)
print("StackPile size =", len(game.stackPile))
print("DiscardPile size =", len(game.discardPile))

print("These are the cards of Player", secondPlayer.pID, ":")
for i in range(0, len(secondPlayer.cardsInHand)):
    secondPlayer.cardsInHand[i].printCard()
print("These are the beliefs of Player", secondPlayer.pID, "about his cards:")
for i in range(0, len(secondPlayer.cardsInHandColorBeliefs)):
    print("Color:", secondPlayer.cardsInHandColorBeliefs[i], "Number:", secondPlayer.cardsInHandNumberBeliefs[i])
'''