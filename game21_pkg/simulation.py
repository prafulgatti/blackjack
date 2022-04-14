import sys,csv
from game21_pkg import dealcards,menus

# this function to append csv data was taken from https://thispointer.com/python-how-to-append-a-new-row-to-an-existing-csv-file/
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def blackjack_simulation(sim):
    if sim=="Yes":
        player_total=0
        dealer_total=0
        global wins
        global loss
        global games
        global black_jack_player
        global black_jack_dealer
        global total_tokens
        total_tokens=0
        wins=0
        loss=0
        games=0
        black_jack_player=0
        black_jack_dealer=0
        menus.blackjack_simulation()
        simulation=input("Choose an option: ").lower()
        if simulation=='s' or simulation=="1":
            try:
                # get the input parameters for the simulation
                gm=int(input("Total games: "))
                phl=int(input("Player hit limit:"))
                dhl=int(input("Dealer hit limit:"))
                total_tokens=int(input("Total tokens:"))
                bet=int(input("Bet:"))
            except ValueError:
                print("Please enter valid input")
            
            dhl=dhl-1 # limit is 1 less than what it cannot exceed
            int_tokens=total_tokens
            while games<gm:
                deck=[]
                deck=dealcards.create_deck()
                deck=dealcards.shuffle_deck(deck)
                player_hand=dealcards.pick_cards(2,deck)
                player_hand_value=dealcards.hand_val(player_hand)
                dealer_hand=dealcards.pick_cards(2,deck)
                dealer_hand_value=dealcards.hand_val(dealer_hand)
                pt=dealcards.calculate_card_total(player_hand_value)
                dt=dealcards.calculate_card_total(dealer_hand_value)
                player_total=pt
                dealer_total=dt
                pl=dealcards.check_blackjack(player_total)
                dl=dealcards.check_blackjack(dealer_total)
                #check for blackjack after first round
                if pl=="blackjack" and dl==False:
                    
                    wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack",False,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                elif pl=="blackjack" and dl=="blackjack":
                    
                    wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack","blackjack",total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                elif dl=="blackjack" and pl==False:
                    
                    wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,"blackjack",total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                elif pl==False and dl==False:
                    while player_total<phl:
                        player_hand+=dealcards.pick_cards(1,deck)
                        player_hand_value=dealcards.hand_val(player_hand)
                        pt=dealcards.calculate_card_total(player_hand_value)
                        player_total=pt
                        pl=dealcards.check_blackjack(player_total)
                        dl=dealcards.check_blackjack(dealer_total)
                        #check for black jack and bust each time a new card is drawn for player
                        if pl=="blackjack" and dl==False:
                            wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack",dl,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)    
                        elif pl=="blackjack" and dl=="blackjack":
                            wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins("blackjack","blackjack",total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                        elif dl=="blackjack" and pl==False:
                            wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,"blackjack",total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                        elif pl=="Bust":
                            wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,True,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                    
                    if player_total>=phl and player_total<21:
                        while dealer_total<dhl:
                            dealer_hand+=dealcards.pick_cards(1,deck)
                            dealer_hand_value=dealcards.hand_val(dealer_hand)
                            pt=dealcards.calculate_card_total(player_hand_value)
                            dt=dealcards.calculate_card_total(dealer_hand_value)
                            dealer_total=dt
                            dl=dealcards.check_blackjack(dealer_total)
                            #check for blackjack or bust after every new card is dealt to dealer
                            if dl=="Bust":
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(True,False,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                            elif dl=="blackjack":
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,"blackjack",total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                        #compare player and dealer total for the winner
                        if dealer_total>=dhl and dealer_total<21:
                            if player_total> dealer_total:
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(True,False,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                            elif player_total < dealer_total:   
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,True,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                            elif player_total==dealer_total:
                                wins,loss,games,total_tokens,black_jack_player,black_jack_dealer=dealcards.calculate_tokens_wins(False,False,total_tokens,bet,wins,loss,games,black_jack_dealer,black_jack_player,sim)
                print("Game:",games)                
                print("Player Hand:",player_hand,"Total:",player_total)
                print("Dealer Hand:",dealer_hand,"Total:",dealer_total,"\n")
                #print out to csv file the simulation data after each game
                row_contents = [player_total, dealer_total,wins,loss,games,black_jack_player,black_jack_dealer,total_tokens,bet]
                append_list_as_row('simulation_results.csv', row_contents)
            #display simulation results on terminal at the end of the simulation                              
            print("---------------------------------------------")                       
            print("      Simulation Result of",games,"games     ")
            print("---------------------------------------------")
            print ("Wins:",wins,"    Losses:",loss,"    No Result:",games-(wins+loss) )
            print ("Win %:","{:.2f}".format(wins*100/(games)))
            print ("Total Tokens (start):",int_tokens)
            print ("Total Tokens (end):",total_tokens)
            print ("Player Bet:",bet)
            if total_tokens-int_tokens>=0:
                print ("Total winnings:",total_tokens-int_tokens)
            else:
                print ("Total losses:",abs(total_tokens-int_tokens))
            print ("BlackJacks for Player:",black_jack_player)
            print ("BlackJacks for Dealer:",black_jack_dealer)

        elif simulation=='q' or simulation=="2":
            sys.exit()
        else:
            print("Invalid option")
