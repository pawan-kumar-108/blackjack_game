import random
suits= ('Heart', 'Diamond', 'Spade', 'Club')
ranks= ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values= {'Two': 2 , 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card():
    def __init__ (self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f'{self.rank} of {self.suit}'
        
 
class Deck():
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
                
    def __str__(self):
        #return self.all_cards  #It is not effective bcz it return list but print should always return str statements, that's why we use alternative technique by appending __str__ method of Card class into it!!
        
        deck_compo = ''
        for card in self.all_cards:
            deck_compo = deck_compo + '\n' + card.__str__()#can be weittern as str(Card)
        return 'The Deck Composition is:' + deck_compo
    
    def deck_shuffle(self):
        random.shuffle(self.all_cards)
    
    def gamble_one(self):
        popped_card = self.all_cards.pop()
        return popped_card
 
 
 
class Hand():
    def __init__(self):
        self.cards= []
        self.value = 0  # Initially cards & decks have nothing (in player's hand)
        self.aces = 0  #To check on the no. of aces
    
    def add_cards(self, card):
        #here 'card' in the parameter would be the pulled card (will come through Deck's function 'gamble_one')
        self.cards.append(card)
        self.value += values[card.rank]
        if card == 'Ace':
            self.aces += 1
        
    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            # when self.aces i.e. no. of aces is more than zero (atleast 1 ace) then only this condition
            # is True, else false. And loop will not work then. Numbers other than 0 are treated as True,
            # we have set 'Ace': 11, then bcz have hve to make sure to use Ace = 1 or 11 (whichever
            # helps in winning (i.e. do not cross 21 mark)
            
            self.value -= 10 
            self.aces -= 1 #decreasing the value of ace by 1    
        
        
class Chips():
    
    def __init__(self, total=100):
        self.total = total # Setting it as default value for the personalized gameplay
        self.bet = 0  # upOn initialization, no bet would be there
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
        
        
def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input("How many chips you would like to bet?: "))
            
        except ValueError:
            print("OOPS, that's not an integer!!")
        else:
            if chips.bet > chips.total:
                print(f"Hhh, You do not have enough chips. You only have {chips} chips!")
            else:
                break
#main motive of this function is just to take the no. of chips       
 
 
def hit(deck,hand):
    hand.add_cards(deck.gamble_one())
    hand.adjust_for_aces()
    
 
def hit_or_stand(deck,hand):
    
    global playing  # to control an upcoming while loop in the actual functioning
    while playing:
        i = input("Type your choice. h for Hit and s for Stay")
        if i[0].lower() == 'h':
            hit(deck, hand)
        elif i[0].lower() == 's':
            print("Player Stands. Now, Dealer's turn")
            playing = False
        else:
            print("Please enter the valid alphabet. Either h or s")
            
        break
    
 
 
def show_some(player,dealer):
    # Showing only second card of dealer (out of 2) bcz 1st one was flipped down!
    print("Dealer's First Card is hidden!" )
    print("Dealer's second card is:\n")
    print(dealer.cards[1]) # technically second card
    
    #Show 2 cards of the player
    print("Player's Cards are:")
    for cards in player.cards:
        print(cards)    
    
def show_all(player, dealer):
    #showing all cards of Dealer
    print("Dealer's cards are: \n")
    for cards in dealer.cards:
        print(cards)
    #calculate and display value of dealer
    print("Value of dealer's hand is: ", dealer.value)
    
    #showing all player's cards
    print("Player's Cards are:\n")
    for cards in player.cards:
        print(cards)
    #calculate and display value of player
    print("Player's total card value is: ", player.value)
    
    
 
def player_busts(player, dealer, chips):
    print("Dealer Wins!! Player Busted!")
    chips.lose_bet()
 
def player_wins(player, dealer, chips):
    print("Player Wins! Dealer busted.")
    chips.win_bet()
 
def dealer_busts(player, dealer, chips):
    print("Dealer Wins!! Player Busted!")
    chips.lose_bet()
    
def dealer_wins(player, dealer, chips):
    print("Dealer Wins!! Player busted")
    chips.win_bet()
    
def push(player, dealer):
    # i.e both player and dealer exceeds the 21 limit
    print("Both the Player and Dealer loses. PUSH!")
    
    
    
while True:
    # Printing an opening statement
    print("Hey, Welcome to the Blackjack Game :)\n")
    
    # Creating & shuffling the deck, dealing two cards to each (player and dealer)
    deck= Deck()
    deck.deck_shuffle()
    player_hand = Hand()
    player_hand.add_cards(deck.gamble_one())
    player_hand.add_cards(deck.gamble_one())
    dealer_hand = Hand()
    dealer_hand.add_cards(deck.gamble_one())
    dealer_hand.add_cards(deck.gamble_one())
    
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_all(player_hand, dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
              
 
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 (a standard way to make sure that it would not bust)
    # Alternative way is to check if player value is less than dealer's
    if player_hand.value <= 21:
        
        while player_hand.value < dealer_hand.value:
            hit(deck,dealer_hand)
        
        # Show all cards
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)   
        elif dealer_hand.value < player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
    
    # Inform Player of their chips total 
    print(f"\nThe Player has {player_chips.total} left!")
    # Ask to play again
    new_game = input("Do you want to play? Type 'y' for yes and 'n' for no.")
    if new_game[0].lower() == 'y':
        continue
    else:
        print("Thank you for playing. Have a good day!!")
        break