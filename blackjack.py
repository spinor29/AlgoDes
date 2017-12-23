# Blackjack with Reinforcement learning
# Author: Jong-Chin Lin <jongchin.lin2@aexp.com>

import random

class Hand:
    def __init__(self,role):
        self.role = role
        self.score = 0
        self.cards = []
        self.stick = False
        self.states = []
        self.usableAce = False

    def hit(self,card):
        self.score = self.handScore(self.score,card)
        self.cards.append(card)

    def cardState(self,card):
        temp = card
        if card in ['J','Q','K']:
           temp = '10'
        return temp

    def handScore(self,score,card):
        #temp = self.cardScore(card)
        temp = 0
        if card in ['J','Q','K']:
           temp = 10
        elif card == 'A':
            if score < 11:
                temp = 11
                self.usableAce = True
            else:
                temp = 1
        else:
            temp = int(card)
        score += temp
        if score > 21 and self.usableAce:
            score -= 10
            self.usableAce = False
        return score


class Player(Hand):
    def __init__(self):
        Hand.__init__(self, 'Player')

    def policyA(self,card):
    #while self.score <= 21:
        if self.score < 20:
            self.hit(card)
            self.states.append(self.score)
        else:
            self.stick = True

    def policyES(self,card):
        state = (s, self.dealer.cardState(self.dealer.cards[1]), self.player.usableAce)
        actions = self.qvalues[state]
        action = max(actions, key=lambda k: (actions[k], random.random()))
        if action == 'h':
            self.hit(card)
            self.states.append(self.score)
        else:
            self.stick = True



        
class Dealer(Hand):
    def __init__(self):
        Hand.__init__(self, 'Dealer')

    def policy(self,card):
        if self.score < 17:
            self.hit(card)
        else:
            self.stick = True


class Blackjack:
    def __init__(self):
        self.cards = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.dealer = Dealer()
        self.player = Player()
        self.hidden = True # Whether first card of dealer's hand is hidden
        self.opening = True
        self.records = {}
        self.finalReward = 0
        self.winLoss = {1:0,0:0,-1:0}
        self.qvalues = {}

    def dealCard(self,hand):
        card = random.choice(self.cards)
        if hand == 'P':
            self.player.hit(card)
        elif hand == 'D':
            self.dealer.hit(card)

    def status(self):
        print "\nDealer's hand:"
        if self.hidden:
            print 'X,', self.dealer.cards[1]
        else:
            print ','.join(self.dealer.cards)
            print 'score:',self.dealer.score
        print "Player's hand:"
        print ','.join(self.player.cards)
        print 'score:',self.player.score

        if not self.opening:
            if self.player.score > 21 and self.hidden:
                print 'Go bust!!'
                print 'Player lose!'
                self.finalReward = -1
            else:
                if self.dealer.score > 21 or self.dealer.score < self.player.score:
                    print 'Player win!'
                    self.finalReward = 1
                elif self.dealer.score == self.player.score:
                    print 'Draw!'
                    self.finalReward = 0
                else:
                    print 'Player lose!'
                    self.finalReward = -1
                #state = (self.player.score, self.dealer.cardState(self.dealer.cards[1]))
                #self.updateRecords(state, self.finalReward)
        print 'States:',self.player.states

    def getRecords(self):
        print 'Records:',self.records

    def reset(self):
        self.hidden = True
        self.opening = True
        self.player.cards = []
        self.dealer.cards = []
        self.player.score = 0
        self.dealer.score = 0
        self.finalReward = 0
        self.player.states = []
        self.player.stick = False

    def updateRecords(self,state,reward):
        if state not in self.records:
            self.records[state] = (1,reward)
        else:
            self.records[state] = (self.records[state][0]+1, self.records[state][1]+reward)

    def averageReturn(self):
        print '\nAverage return:'
        print 'State, frequency, AverageReturn'
        for state in self.records:
            avg = self.records[state][1]*1.0 / self.records[state][0]
            print state,',',self.records[state][0],',',avg

    def playGame(self):
        # Opening
        self.dealCard('P')
        self.dealCard('P')
        self.dealCard('D')
        self.dealCard('D')
        self.player.states = [self.player.score]
        self.status()
        # Player's turn
        self.opening = False
        while self.player.score <= 21 and not self.player.stick:
            previousScore = self.player.score
            card = random.choice(self.cards)
            self.player.policyA(card)
            '''
            if (not self.player.stick) and self.player.score <= 21:
                state = (previousScore, self.dealer.cardState(self.dealer.cards[1]))
                self.updateRecords(state, 0)
            elif self.player.score > 21:
                state = (previousScore, self.dealer.cardState(self.dealer.cards[1]))
                self.updateRecords(state, -1)
            '''
        # Dealer's turn
        if self.player.score <= 21:
            self.hidden = False
            while self.dealer.score <= 21 and not self.dealer.stick:
                card = random.choice(self.cards)
                self.dealer.policy(card)
        self.status()    
        for s in self.player.states:
            if s <= 21:
                state = (s, self.dealer.cardState(self.dealer.cards[1]), self.player.usableAce)
                self.updateRecords(state, self.finalReward)
        self.winLoss[self.finalReward] += 1


if __name__ == '__main__':
    bj = Blackjack()
    ngames = 100
    winLoss = {1:0,0:0,-1:0}
    for i in range(ngames):
        print '\nGame ',i+1,':'
        bj.playGame()
        bj.getRecords()
        winLoss
        bj.reset()
    bj.averageReturn()
    print bj.winLoss
