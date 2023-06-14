Important information:
End of year AP CSA Project --> created a streamlit that allows you to input poker cards and it calculates your probability of winning the hand

Explanation of Basic Class functionality
This program works by simulating poker hands, scoring them, and then ranking them based on how they score against other poker hands. A quick explanation of each major class is below:

Card() → creates a card object with both a number and a suit 
Deck() → creates a deck of 52 cards and shuffles them using the random library
HandDealt() → creates your personal 7-card hand
Gameplay() → creates an instance of a poker game with a deck and cards dealt, removing cards dealt from the deck
FindHands() → looks for pairs, straights, flushes, and other poker hands within a hand of 7 cards, then uses the scoreHand() method to score the hand based on what it contains 
DeckRemoval() → helps with removing cards from a deck that have come out on the table
Game() → used to calculate the probability that you will win a certain poker game if you only know your cards and the cards on the table. Iterates through all possible hands that other people in the game could possibly have and sees how your hand would perform against theirs
MultipleHands() → similarly to Game, this class calculates the probability of winning a poker hand. However, with this class all the other players’ hands are known and this mode works by iterating through possible cards that could come down on the table and seeing how players’ hands would perform against each other. 
Player() → creates a player object with a number and 2 cards that they were dealt 

Streamlit Explanation
Streamlit is a software that allows you to easily create data apps from python and display them on the web. In streamlit, I created two modes → one uses the Game() class and assumes that no other players cards are known, whereas the other uses the MultipleHands() class and calculates probabilities assuming that the hands of other players are known. 
