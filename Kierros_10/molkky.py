"""
COMP.CS.100 Ohjelmointi 1 / Programming 1

Code template for Mölkky.
"""


class Player:
    """
    Class for the players by the players.
    """

    def __init__(self, name):
        """
        Initialize the class.
        :param name: str, name of the player.
        """

        self.__name = name
        self.__points = 0
        self.__total_points = 0
        self.__throw_counter = 0
        self.__hit_percentage = 0
        self.__hit_counter = 0

    def get_name(self):
        """
        Method to get the name.
        :return: str, player name
        """

        return self.__name

    def add_points(self, points):
        """
        Method for adding points.
        :param points: int, points to be added
        """

        self.__points += points
        self.__total_points += points

        if 40 <= self.__points <= 49:
            print(f"{self.__name} needs only {50 - self.__points} points. "
                  f"It's better to avoid knocking down the "
                  f"pins with higher points.")

        if self.__points > 50:
            print(f"{self.__name} gets penalty points!")
            self.__points = 25

    def has_won(self):
        """
        Method for if the thor results in a win.
        :return: bool, true or false for the if-structure.
        """

        if self.__points == 50:
            return True
        else:
            return False

    def get_points(self):
        """
        Method to get points.
        :return: int, points
        """

        return self.__points

    def cheers(self, points):
        """
        Method for the special annotation if a throw was better
        than the average of throws.
        :param points: int, points
        """

        self.__throw_counter += 1

        average = self.__total_points / self.__throw_counter

        if points > average:
            print(f"Cheers {self.__name}!")

    def hit_percentage(self, points):
        """
        Calculates hit percentage.
        :param points: int, points
        """

        if self.__throw_counter == 0:
            self.__hit_percentage = 0
        elif points > 0:
            self.__hit_counter += 1
            self.__hit_percentage = (self.__hit_counter
                                     / self.__throw_counter) * 100
        else:
            self.__hit_percentage = (self.__hit_counter
                                     / self.__throw_counter) * 100

    def get_hit_percentage(self):
        """
        Method for getting the hit percentage.
        :return: float, hit percentage
        """

        return self.__hit_percentage


def main():
    # Here we define two variables which are the objects initiated from the
    # class Player. This is how the constructor of the class Player
    # (the method that is named __init__) is called!

    player1 = Player("Matti")
    player2 = Player("Teppo")

    throw = 1
    while True:

        # if throw is an even number
        if throw % 2 == 0:
            in_turn = player1

        # else throw is an odd number
        else:
            in_turn = player2

        pts = int(input("Enter the score of player " + in_turn.get_name() +
                        " of throw " + str(throw) + ": "))

        in_turn.add_points(pts)

        in_turn.cheers(pts)

        in_turn.hit_percentage(pts)

        if in_turn.has_won():
            print("Game over! The winner is " + in_turn.get_name() + "!")
            return

        print("")
        print("Scoreboard after throw " + str(throw) + ":")
        print(f"{player1.get_name()}: {player1.get_points()} p, "
              f"hit percentage {player1.get_hit_percentage():.1f}")
        print(f"{player2.get_name()}: {player2.get_points()} p, "
              f"hit percentage {player2.get_hit_percentage():.1f}")
        print("")

        throw += 1


if __name__ == "__main__":
    main()
