import time, re, sys, csv
from game21_pkg import dealcards,menus,simulation

global wins
global loss
global games
global black_jack_player
global black_jack_dealer
global total_tokens
global int_total
player_total=dealer_total=wins=loss=games=black_jack_player=black_jack_dealer=total_tokens=0

def replay():
    global int_total
    global total_tokens
    print("Total tokens:",total_tokens)
    while True:
        menus.blackjack_outro(wins,loss)
        replay=input("Choose an option: ").lower()
        
        if replay=="p" or replay=="1":
            game_play()
        elif replay=="s" or replay=="2":
            print("---------------------------------------------")
            print("|                   Stats                   |")
            print("---------------------------------------------")
            print ("Wins:",wins,"    Losses:",loss,"    No Result:",games-(wins+loss) )
            print ("Games:",games)
            if total_tokens-int_total>=0:
                print ("Total Winnings:",total_tokens-int_total)
            elif total_tokens-int_total<0:
                print ("Total Losses:",abs(total_tokens-int_total))
            print ("Tokens:",total_tokens)
            print ("BlackJacks for Player:",black_jack_player)
            print ("BlackJacks for Dealer:",black_jack_dealer)
        elif replay=="q" or replay=="3":
            sys.exit()
        else:
            print("Invalid Input")   
    
def game_play():
    global wins
    global loss
    global games
    global black_jack_player
    global black_jack_dealer
    global total_tokens
    global int_total
    
    db= black_jack_dealer
    pb= black_jack_player
    dhl=17 # dealer hit limit set to be less than 17
    while True:
        try:
            bet=int(input("Enter your Bet: "))
        except ValueError:
            print("Please enter a valid bet")
            game_play()
        if bet>total_tokens:
            print("Please enter more tokens to play")
            enter_tokens()
        else:
            print("Dealer is shuffling and dealing cards .",".",".")
            #delay of 2 seconds is added for effect of dealing cards
            time.sleep(2)

            #Create a deck of 52 cards and shuffle the deck
            deck=dealcards.create_deck()
            deck=dealcards.shuffle_deck(deck)

            #Player and Dealer pick 2 cards each .Dealer shows one card
            player_hand=dealcards.pick_cards(2,deck)
            player_hand_value=dealcards.hand_val(player_hand)
            print("Player Hand: ",dealcards.show_hand(player_hand,2))
            dealer_hand=dealcards.pick_cards(2,deck)
            dealer_hand_value=dealcards.hand_val(dealer_hand)
            print("Dealer Hand: ",dealcards.show_hand(dealer_hand,1))

            #Calculate  totals for Player and Dealer 
            pt=dealcards.calculate_card_total(player_hand_value)
            dt=dealcards.calculate_card_total(dealer_hand_value)
            player_total=pt
            dealer_total=dt
            print("Player Total: ",player_total)

            #check for blackjack after first 2 cards
            pl=dealcards.check_blackjack(player_total)
            dl=dealcards.check_blackjack(dealer_total)
            
            if pl=="blackjack" and dl==False:
                print ("You hit BlackJack!")
                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack",dl,total_tokens,bet,wins,loss,games,db,pb,sim)
                replay()
            if pl=="blackjack" and dl=="blackjack":
                print("Both Dealer and Player hit BlackJack. No one wins")
                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(pl,dl,total_tokens,bet,wins,loss,games,db,pb,sim)
                replay()
            if dl=="blackjack" and pl==False:
                print("Dealer Hand: ",dealcards.show_hand(dealer_hand,2))
                print("Dealer Total:",dealer_total,"\n")
                print("Dealer hits BlackJack!")
                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(pl,"blackjack",total_tokens,bet,wins,loss,games,db,pb,sim)
                replay()
            if pl==False and dl==False:
                print ("The Next round begins!")

            # if no blackjack in the first round then play continues with menus depending on cards drawn for player
            while pl==False and dl==False:
                menus.blackjack_menu()
                pl_option=input("Choose an option to play: ").lower()
                if pl_option=="1" or pl_option=="h":
                    #draw a new card for player and show the new card and player hand
                    player_hand+=dealcards.pick_cards(1,deck)
                    player_hand_value=dealcards.hand_val(player_hand)
                    print("Your new card is",player_hand[-2],player_hand[-1])
                    print("Player Hand: ",dealcards.show_hand(player_hand,2))
                    #calculate new total for player
                    pt=dealcards.calculate_card_total(player_hand_value)
                    player_total=pt
                    print("Player Total:",player_total)
                    pl=dealcards.check_blackjack(player_total)
                    dl=dealcards.check_blackjack(dealer_total) 
                    #calculate for blackjack or bust after every new card is drawn       
                    if pl=="blackjack" and dl==False:
                        print("Player hits BlackJack!. Player wins")
                        wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack",dl,total_tokens,bet,wins,loss,games,db,pb,sim)
                        replay()
                    elif pl=="blackjack" and dl=="blackjack":
                        print("Both Player and Dealer hit BlackJack. No wins")
                        wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack","blackjack",total_tokens,bet,wins,loss,games,db,pb,sim)
                        replay()
                    elif dl=="blackjack" and pl==False:
                        print("Dealer hits BlackJack!. Dealer wins")
                        wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(pl,"blackjack",total_tokens,bet,wins,loss,games,db,pb,sim)
                        replay()
                    elif pl=="Bust":
                        print("Bust. You lose")
                        wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,True,total_tokens,bet,wins,loss,games,db,pb,sim)
                        replay() 
                #if player decides to stand then the players final total is displayed and dealer's play begins          
                elif pl_option=="2" or pl_option=="s":
                    print("Your total is",player_total,"\n")
                    print("Dealer's Turn")
                    print("Dealer Hand:",dealcards.show_hand(dealer_hand,2))
                    print("Dealer Total:",dealer_total,"\n") 
                    while True:
                        # hit limit of dealer is set to 16
                        if dealer_total<dhl:
                            # new card is drawn for dealer and dealer total is calculated with the new hand
                            # this loop repeats till dealer hit limit is reached
                            dealer_hand+=dealcards.pick_cards(1,deck)
                            dealer_hand_value=dealcards.hand_val(dealer_hand)
                            print("Dealer is picking a new card .",".",".")
                            time.sleep(2)
                            print("Dealer's new card is",dealer_hand[-2],dealer_hand[-1])
                            print("Dealer Hand:",dealcards.show_hand(dealer_hand,2))
                            pt=dealcards.calculate_card_total(player_hand_value)
                            dt=dealcards.calculate_card_total(dealer_hand_value)
                            dealer_total=dt
                            print("Dealer Total:",dealer_total,"\n")
                            dl=dealcards.check_blackjack(dealer_total)
                            # dealer total is checked after every card drawn for bust or blackjack
                            if dl=="Bust":
                                print("Bust. Dealer loses")
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(True,False,total_tokens,bet,wins,loss,games,db,pb,sim)
                                replay()
                            elif dl=="blackjack":
                                print("Dealer hits BlackJack!")
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,"blackjack",total_tokens,bet,wins,loss,games,db,pb,sim)
                                replay()
                        else:
                            # when dealer total reaches dealer hit limit, dealer total is compared to player total and winner is decided
                            if player_total> dealer_total:
                                print("Your total is higher than the dealer's total.You win!")
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(True,False,total_tokens,bet,wins,loss,games,db,pb,sim)
                                replay()
                            elif player_total < dealer_total:
                                print("Dealer's total is higher than your total.You lose!")
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,True,total_tokens,bet,wins,loss,games,db,pb,sim)
                                replay()
                            elif player_total==dealer_total:
                                print("Push. No one wins this round")
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,False,total_tokens,bet,wins,loss,games,db,pb,sim)
                                replay()
                            break
                    
                elif (len(player_hand)>4 and pl_option=="3") or (len(player_hand)==4 and pl_option=="5") or (len(player_hand)>4 and pl_option=="f"):
                    print("GoodBye!")
                    sys.exit()
                else:
                    print("Invalid option ")

def enter_tokens():
    global total_tokens
    global int_total
    try:
        total_tokens+=int(input("Enter Total tokens for this session: "))  
        int_total+=total_tokens  
    except ValueError:
        print("Please enter a valid number")
        enter_tokens()

    return total_tokens
    
""" options when running the program in either game mode or simulation mode
game mode usage python .\black_jack.py
simulation mode usage  .\black_jack.py simulation """

if __name__ == "__main__":
    sim = sys.argv[-1]
    print(sim)
    if sim=="simulation":
        sim='Yes'
        header= ['player_total', 'dealer_total','wins','loss','games','black_jack_player','black_jack_dealer','total_tokens','bet']
        simulation.append_list_as_row('simulation_results.csv', header)
        while True:
            simulation.blackjack_simulation(sim) 

    else:
               
        menus.blackjack_intro(wins,loss)
        int_total=0
        total_tokens=0
        enter_tokens()      
        game_play()










   







