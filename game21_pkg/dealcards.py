import random

#define suite and cards to create a deck of cards
suite=['♣','♥','♦','♠']
cards=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]

#create deck of 52 cards
def create_deck():
    deck=[]
    for i in suite:
        for j in cards:
            deck.append([i,j])
    return deck

#shuffle the deck of cards
def shuffle_deck(dec):
    random.shuffle(dec)
    return dec

#pick one or more cards and remove the picked card(s) from the deck
def pick_cards(num,deck):
    pick=[]
    #global deck
    for i in range(num):
        new_pick=random.choice(deck)
        deck.remove(new_pick)
        pick=pick+new_pick    
    return (pick)

# show hand based on arguments ,example : 2 cards for player and 1 for dealer in the first round
def show_hand(h,who):
    hand_str=''
    if who==2:
        for i in h:
            hand_str=hand_str+i+ " "      
    elif who==1:
        for i in h[0:2]:
            hand_str=hand_str+i+ " "
    return hand_str

# calculate the total value of player or dealers hand value by only counting the face card value in the hand
def hand_val(h):
    new_list=[]
    for i in range(1,len(h),2):
        new_list.append(h[i])
    return new_list


# show 2 cards for player and 1 card for dealer.The other card is chosen but hidden 
def deal_cards():
    player_hand=pick_cards(2)
    player_hand_value=hand_val(player_hand)
    dealer_hand=pick_cards(2)
    dealer_hand_value=hand_val(dealer_hand)


# remove all occurences of an element from list
# this function was searched and derived from stackoverflow but I couldn't find the link later 
def remove_all(list_obj, value):
    while value in list_obj:
        list_obj.remove(value)

#check blackjack
def check_blackjack(total):
    blackjack=""   
    if total==21:
        blackjack="blackjack"

    elif total<21:
        blackjack=False  

    elif total>21:
        blackjack="Bust"
    
    return (blackjack)


# calculate card total
def calculate_card_total(hand_value):
    total=0
    rep_cards=["J","Q","K"]
    #replace J,Q,K with value 10
    for i in range(0,len(hand_value)):
        if hand_value[i] in rep_cards:
            hand_value[i]="10"
        else:
            continue  
    # calculate total of other cards by removing the Ace card(s) from the hand
    # I got this idea to create a temp list to remove all Aces to calculate the value of the remaining cards from stackoverflow but I didnt make a note of the source at that time.
    h_temp=hand_value.copy()
    remove_all(h_temp,"A")
    for i in h_temp:
        total+=int(i)
    # if total value of all cards after removing the Aces is 10 or less then assign Ace a value of 11
    # loop stops as soon as the first Ace is given a value of 11
    for i in range(len(hand_value)):
        while total<11:
            if hand_value[i]=="A":
                hand_value[i]=11
                total+=11
            break
    # if total value of all cards after removing the Aces is greater than  than 10 then assign Ace a value of 1
    # this loop will assign Ace with value 1 for each Ace after the score reaches 10
    if total>11:
        for i in range(len(hand_value)):
            if hand_value[i]=="A":
                hand_value[i]=1
                total+=1

    return(total)
# calculate wins and losses for player, black jacks for player and dealer, total tokens for player and games
def calculate_tokens_wins(pl,dl,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim):
    if pl=='blackjack' and dl==False:
        total_tokens+=(1.5* bet)
        wins+=1
        black_jack_player+=1
        black_jack_dealer+=0
        games+=1
    elif pl==True and dl==False:
        total_tokens+=bet
        black_jack_player+=0
        black_jack_dealer+=0
        wins+=1
        games+=1
    elif pl==False and dl==False:
        black_jack_player+=0
        black_jack_dealer+=0
        games+=1    
    elif dl=='blackjack' and pl==False:
        black_jack_dealer+=1
        black_jack_player+=0
        total_tokens=total_tokens-bet
        loss+=1
        games+=1
    elif dl==True and pl==False:
        total_tokens=total_tokens-bet
        black_jack_player+=0
        black_jack_dealer+=0
        loss+=1
        games+=1
    elif dl=='blackjack' and pl=='blackjack':
        black_jack_player+=1
        black_jack_dealer+=1
        games+=1
    return(wins,loss,games,total_tokens,black_jack_player,black_jack_dealer)
    