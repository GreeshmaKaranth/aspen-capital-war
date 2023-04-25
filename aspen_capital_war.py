import os
import random
from flask import Flask

import mysql.connector
import argparse

app = Flask(__name__)

suits = ['Hearts', 'Clubs', 'Spades', 'Diamonds']

ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

MYSQL_USER = os.environ.get("sql_user")
MYSQL_PWD = os.environ.get("sql_pwd")

class Card():

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    # String method for printing
    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck():

    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        return self.cards.pop()  # To get the last card from the deck


class Player():

    def __init__(self, name):
        self.name = name
        self.cards = []

    def remove_one(self):
        return self.cards.pop(0)  # To return a card from the beginning of the list

    def add_cards(self, new_cards):
        if type(new_cards) == type([]):
            self.cards.extend(new_cards)
        else:
            self.cards.append(new_cards)

    def __str__(self):
        return f'Player {self.name} has {len(self.all_cards)} cards.'


MAX_ROUNDS = 10000


def war():
    player1 = Player("Player 1")
    player2 = Player("Player 2")

    newdeck = Deck()
    newdeck.shuffle()

    for i in range(0, len(newdeck.cards) - 1, 2):
        player1.add_cards(newdeck.cards[i])
        player2.add_cards(newdeck.cards[i + 1])

    play_game = True
    round_num = 0

    while play_game and round_num < MAX_ROUNDS:

        round_num += 1
        print("\nRound ", round_num)

        # Uncomment if required
        # print("Player 1 cards:", len(player1.cards))
        # print("Player 2 cards: ", len(player2.cards))

        if len(player1.cards) == 0:
            print("Player 1 out of cards. " + player2.name + " wins!")
            winner = 1
            break

        if len(player2.cards) == 0:
            print("Player 2 out of cards. " + player1.name + " wins!")
            winner = 2
            break

        else:
            player1_card = player1.remove_one()
            player2_card = player2.remove_one()
            player_cards = [player1_card, player2_card]

            if player1_card.value == player2_card.value:

                at_war = True
                while at_war:

                    player1_list = []
                    player2_list = []

                    card_list = []

                    for _ in range(2):

                        if len(player1.cards) == 0:
                            print("Player 1 out of cards. " + player2.name + " wins!")
                            play_game = False
                            at_war = False
                            winner = 1
                            break

                        elif len(player2.cards) == 0:
                            print("Player 2 out of cards. " + player1.name + " wins!")
                            play_game = False
                            at_war = False
                            winner = 2
                            break

                        player1_list.append(player1.remove_one())
                        player2_list.append(player2.remove_one())

                    if not at_war:
                        break

                    card_list.extend(player1_list)
                    card_list.extend(player2_list)

                    if player1_list[0].value > player2_list[0].value:
                        player1.add_cards(card_list)
                        player1.add_cards(player_cards)
                        break

                    elif player1_list[0].value < player2_list[0].value:
                        player2.add_cards(card_list)
                        player2.add_cards(player_cards)
                        break

                    player_cards.extend(card_list)

            elif player1_card.value > player2_card.value:
                player1.add_cards(player_cards)

            elif player2_card.value > player1_card.value:
                player2.add_cards(player_cards)

    if round_num == MAX_ROUNDS:
        print("Reached " + str(MAX_ROUNDS) + " rounds. Game will be restarted.")

        # Game has not ended; must be restarted
        return 0, round_num

    if len(player1.cards) == 0:
        print("Player 2 won")

    elif len(player2.cards) == 0:
        print("Player 1 won")

    # Game has ended
    print("Game has ended in " + str(round_num) + " turns!")
    return winner, round_num


def add_to_db(winner):
    db = mysql.connector.connect(host='localhost', user=MYSQL_USER, password=MYSQL_PWD, port=3306, database="war")
    cursor = db.cursor()

    query = "SELECT number_of_wins FROM games WHERE player = " + str(winner) + ";"
    cursor.execute(query)
    curr_number_of_wins = str(cursor.fetchone()[0] + 1)

    query = "UPDATE games SET number_of_wins = " + curr_number_of_wins + " WHERE player = " + str(winner) + ";"
    cursor.execute(query)

    db.commit()


def read_db():
    db = mysql.connector.connect(host='localhost', user=MYSQL_USER, password=MYSQL_PWD, port=3306, database="war")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM games")
    all_data = cursor.fetchall()

    results = {all_data[0][0]: all_data[0][1], all_data[1][0]: all_data[1][1]}

    return results


def clear_db():
    db = mysql.connector.connect(host='localhost', user=MYSQL_USER, password=MYSQL_PWD, port=3306, database="war")
    cursor = db.cursor()

    cursor.execute("UPDATE games SET number_of_wins = 0")
    db.commit()

@app.route("/")
def main():
    output = '''Welcome to the Greeshma Karanth's implementation of the WAR game! 
    Use /game endpoint to start a game. Two simulated players will play out the game.  
    Use /history endpoint to get lifetime wins for each player stored in a database.
    Use /test to run some basic test cases for the application.
    
    Enjoy!'''
    return output

@app.route("/test")
def test():
    # Let us run the game 10 times and get winners

    trial_count = 0
    results = {1: 0, 2: 0}

    clear_db()
    while trial_count < 10:
        winner, _ = war()
        while winner == 0:
            winner, _ = war()

        trial_count += 1

        results[winner] += 1
        add_to_db(winner)

    db_results = read_db()

    assert (db_results == results)
    return "Completed test on 10 trial War games successfully."

@app.route("/game")
def play_game():

    winner, round_num = war()

    while winner == 0:
        winner, round_num = war()

    add_to_db(winner)

    return "Played a game of War. The winner was Player " + str(winner) + " after " + str(round_num) + " rounds!"


@app.route("/history")
def history():
    results = read_db()

    output = "Player 1 has " + str(results[1]) + " wins. Player 2 has " + str(results[2]) + " wins."

    return output

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('user', type=str, help='Enter MySQL username')
    # parser.add_argument('password', type=str, help='Enter MySQL password')
    # args = parser.parse_args()
    #
    # MYSQL_USER = args.user
    # MYSQL_PWD = args.password
    #
    # test()

    app.run()
