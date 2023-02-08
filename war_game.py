import random
import playing_cards as pc

war_scores = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

deck = pc.create_deck()

random.shuffle(deck)

num_players = 2

hand_size = len(deck) // num_players

hand_one = deck[:hand_size]
hand_two = deck[hand_size:]

discard_one = []
discard_two = []

def play_hand(h1, h2):
    # play hand
    p1 = h1.pop()
    p2 = h2.pop()
    # Add to discard piles
    discard_one.append(p1)
    discard_two.append(p2)
    # Show cards
    print("Player one's card is:", p1)
    print("Player two's card is:", p2)
    return p1, p2
    

def ordinary_win(winner) -> None:
    """ Add stack cards to bottom of winner's pile -assumes 2 players """
    winner.insert(0, discard_one.pop())
    winner.insert(0, discard_two.pop())


def print_deck_sizes() -> None:
    """ Print deck sizes """
    print(f"Player 1 has {len(hand_one)} card(s) left.")
    print(f"Player 2 has {len(hand_two)} card(s) left.")


while hand_one and hand_two:
    # Check values
    p1, p2 = play_hand(hand_one, hand_two)
    if war_scores[p1.rank] > war_scores[p2.rank]:
        print("Player 1 wins the hand!")
        ordinary_win(hand_one)
        print_deck_sizes()
    elif war_scores[p1.rank] < war_scores[p2.rank]:
        print("Player 2 wins the hand!")
        ordinary_win(hand_two)
        print_deck_sizes()
    else:
        if len(hand_one) == 1:
            hand_one.pop()
            print("Player 1 is out of cards!")
            break
        if len(hand_two) == 1:
            hand_two.pop()
            print("Player 2 is out of cards!")
            break
        print("WAR!!!")
        undecided = True
        while undecided:
            discard_one.append(hand_one.pop())
            discard_two.append(hand_two.pop())
            next1, next2 = play_hand(hand_one, hand_two)
            if war_scores[next1.rank] > war_scores[next2.rank]:
                hand_one = discard_one + discard_two + hand_one 
                print("Player 1 gets the loot!")
                undecided = False
            elif war_scores[next1.rank] < war_scores[next2.rank]:
                hand_two = discard_one + discard_two + hand_two
                print("Player 2 gets the loot!")
                undecided = False
            print_deck_sizes()
        discard_one = []
        discard_two = []

if hand_one and not hand_two:
    print("Player 1 wins the game")
elif hand_two and not hand_one:
    print("Player 2 wins the game")
