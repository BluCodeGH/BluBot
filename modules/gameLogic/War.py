import modules.gameLogic.BlackJack as BlackJack

class War:
  def __init__(self):
    self.playerCard = []
    self.dealerCard = []
    self.deck = BlackJack.Deck()

  def startGame(self):
    self.playerCard.append(self.deck.getCard())
    self.dealerCard.append(self.deck.getCard())

  def getPlayerScore(self):
    Score = 0
    for i in range(1, len(self.playerCard[0]), 2):
      if self.playerCard[0][i].isdigit():
        Score = Score + int(self.playerCard[0][i])
      elif self.playerCard[0][i] == "K":
        Score = Score + 13
      elif self.playerCard[0][i] == "J":
        Score = Score + 11
      elif self.playerCard[0][i] == "Q":
        Score = Score + 12
      elif self.playerCard[0][i] == "A":
        Score = Score + 14
    return Score

  def getDealerScore(self):
    Score = 0
    for i in range(1, len(self.dealerCard[0]), 2):
      if self.dealerCard[0][i].isdigit():
        Score = Score + int(self.dealerCard[0][i])
      elif self.dealerCard[0][i] == "K":
        Score = Score + 13
      elif self.dealerCard[0][i] == "J":
        Score = Score + 11
      elif self.dealerCard[0][i] == "Q":
        Score = Score + 12
      elif self.dealerCard[0][i] == "A":
        Score = Score + 14
    return Score

  def getPlayerCards(self):
    display = ""
    if self.playerCard[0][0] == "H":
      display = display + "\n" + self.playerCard[0][1:] + " :heart: " + self.playerCard[0][1:]
    if self.playerCard[0][0] == "S":
      display = display + "\n" + self.playerCard[0][1:] + " :spades: " + self.playerCard[0][1:]
    if self.playerCard[0][0] == "C":
      display = display + "\n" + self.playerCard[0][1:] + " :clubs: " + self.playerCard[0][1:]
    if self.playerCard[0][0] == "D":
      display = display + "\n" + self.playerCard[0][1:] + " :diamonds: " + self.playerCard[0][1:]
    return display

  def getDealerCards(self):
    display = ""
    if self.dealerCard[0][0] == "H":
      display = display + "\n" + self.dealerCard[0][1:] + " :heart: " + self.dealerCard[0][1:]
    if self.dealerCard[0][0] == "S":
      display = display + "\n" + self.dealerCard[0][1:] + " :spades: " + self.dealerCard[0][1:]
    if self.dealerCard[0][0] == "C":
      display = display + "\n" + self.dealerCard[0][1:] + " :clubs: " + self.dealerCard[0][1:]
    if self.dealerCard[0][0] == "D":
      display = display + "\n" + self.dealerCard[0][1:] + " :diamonds: " + self.dealerCard[0][1:]
    return display

  def finishGame(self):
    if int(self.getDealerScore()) >= int(self.getPlayerScore()):
      return ":cry: The Dealer Wins :cry:"
    else:
      return ":100: The Player Wins! :100:"
