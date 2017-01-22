from random import randint

class Deck():
  def __init__(self):
    self.Card_Count = 52
    self.Hearts = 13
    self.Spades = 13
    self.Clubs = 13
    self.Diamonds = 13
    self.CardList = []
  def getCard(self):
    GoodCard = False
    if self.Card_Count != 0:
      while not GoodCard:
        Suit = randint(1,4)
        if Suit == 1:
          Card = "H"
        elif Suit == 2:
          Card = "S"
        elif Suit == 3:
          Card = "C"
        elif Suit == 4:
          Card = "D"
        Number = randint(1,13)
        if Number == 11:
          Number = "J"
        elif Number == 12:
          Number = "Q"
        elif Number == 13:
          Number = "K"
        elif Number == 1:
          Number = "A"
        Card = Card + str(Number)
        if Card not in self.CardList:
          GoodCard = True
          self.CardList.append(Card)
          self.Card_Count = self.Card_Count - 1
    else:
      return "Deck is Empty!"
    return Card

class BlackJack:
  def __init__(self):
    self.playerHands = []
    self.dealerHand = []
    self.deck = Deck()
  def startGame(self):
    for _ in range(2): #gives the player 2 cards and puts the players hand in 1 postion in the list
      self.playerHands.append(self.deck.getCard())
      self.dealerHand.append(self.deck.getCard()) #keeps in list because only 1 dealer
  def getPlayerScore(self):
    Score = 0
    for i in range(len(self.playerHands)):
      if not self.playerHands[i].isalpha():
        Score = int(self.playerHands[i][1:]) + Score
      elif self.playerHands[i][1:] == "K" or self.playerHands[i][1:] == "J" or self.playerHands[i][1:] == "Q":
        Score = Score + 10
      elif self.playerHands[i][1] == "A" and Score <= 10:
        Score = Score + 11
      elif self.playerHands[i][1] == "A" and Score > 10:
        Score = Score + 1
    return Score
  def hit(self):
    self.playerHands.append(self.deck.getCard())
  def getDealerScore(self):
    Score = 0
    for i in range(len(self.dealerHand)):
      if not self.dealerHand[i].isalpha():
        Score = int(self.dealerHand[i][1:]) + Score
      elif self.dealerHand[i][1:] == "K" or self.dealerHand[i][1:] == "J" or self.dealerHand[i][1:] == "Q":
        Score = Score + 10
      elif self.dealerHand[i][1] == "A" and Score <= 10:
        Score = Score + 11
      elif self.dealerHand[i][1] == "A" and Score > 10:
        Score = Score + 1
    return Score
  def finishGame(self):
    while True:
      if int(self.getDealerScore()) >= 17 and int(self.getDealerScore()) >= int(self.getPlayerScore()) and int(self.getDealerScore() <= 21):
        return str(self.dealerFlip()) + "\n The Dealer Wins"
      elif int(self.getDealerScore()) < 17:
        self.dealerHand.append(self.deck.getCard())
      elif int(self.getDealerScore()) > 21:
        return str(self.dealerFlip()) + "\n The Player Wins!"
      elif int(self.getDealerScore() < self.getPlayerScore()):
        self.dealerHand.append((self.deck.getCard()))
  def getCards(self):
    display = "Your Hand is:"
    for i in range(len(self.playerHands)):
      if self.playerHands[i][0] == "H":
        display = display + "\n" + self.playerHands[i][1:] + " :heart: " + self.playerHands[i][1:]
      elif self.playerHands[i][0] == "S":
        display = display + "\n" + self.playerHands[i][1:] + " :spades: " + self.playerHands[i][1:]
      elif self.playerHands[i][0] == "C":
        display = display + "\n" + self.playerHands[i][1:] + " :clubs: " + self.playerHands[i][1:]
      elif self.playerHands[i][0] == "D":
        display = display + "\n" + self.playerHands[i][1:] + " :diamonds: " + self.playerHands[i][1:]
    return display
  def dealerFlip(self):
    display = "The dealer has:"
    for i in range(len(self.dealerHand)):
      if self.dealerHand[i][0] == "H":
        display = display + "\n" + self.dealerHand[i][1:] + " :heart: " + self.dealerHand[i][1:]
      elif self.dealerHand[i][0] == "S":
        display = display + "\n" + self.dealerHand[i][1:] + " :spades: " + self.dealerHand[i][1:]
      elif self.dealerHand[i][0] == "C":
        display = display + "\n" + self.dealerHand[i][1:] + " :clubs: " + self.dealerHand[i][1:]
      elif self.dealerHand[i][0] == "D":
        display = display + "\n" + self.dealerHand[i][1:] + " :diamonds: " + self.dealerHand[i][1:]
    return display
  def flipOneCard(self):
    display = "One of the dealers cards is..."
    if self.dealerHand[0][0] == "H":
      display = display + "\n" + self.dealerHand[0][1:] + " :heart: " + self.dealerHand[0][1:]
    elif self.dealerHand[0][0] == "S":
      display = display + "\n" + self.dealerHand[0][1:] + " :spades: " + self.dealerHand[0][1:]
    elif self.dealerHand[0][0] == "C":
      display = display + "\n" + self.dealerHand[0][1:] + " :clubs: " + self.dealerHand[0][1:]
    elif self.dealerHand[0][0] == "D":
      display = display + "\n" + self.dealerHand[0][1:] + " :diamonds: " + self.dealerHand[0][1:]
    return display
