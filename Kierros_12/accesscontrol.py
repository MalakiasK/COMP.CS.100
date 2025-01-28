"""
COMP.CS.100 Ohjelmointi 1
Malakias Kosonen
Tehtävä 12.5: Kulunvalvonta
"""

DOORCODES = {'TC114': ['TIE'], 'TC203': ['TIE'], 'TC210': ['TIE', 'TST'],
             'TD201': ['TST'], 'TE111': [], 'TE113': [], 'TE115': [],
             'TE117': [], 'TE102': ['TIE'], 'TD203': ['TST'], 'TA666': ['X'],
             'TC103': ['TIE', 'OPET', 'SGN'], 'TC205': ['TIE', 'OPET', 'ELT'],
             'TB109': ['OPET', 'TST'], 'TB111': ['OPET', 'TST'],
             'TB103': ['OPET'], 'TB104': ['OPET'], 'TB205': ['G'],
             'SM111': [], 'SM112': [], 'SM113': [], 'SM114': [],
             'S1': ['OPET'], 'S2': ['OPET'], 'S3': ['OPET'], 'S4': ['OPET'],
             'K1705': ['OPET'], 'SB100': ['G'], 'SB202': ['G'],
             'SM220': ['ELT'], 'SM221': ['ELT'], 'SM222': ['ELT'],
             'secret_corridor_from_building_T_to_building_F': ['X', 'Y', 'Z'],
             'TA': ['G'], 'TB': ['G'], 'SA': ['G'], 'KA': ['G']}


class Accesscard:
    """
    This class models an access card which can be used to check
    whether a card should open a particular door or not.
    """

    def __init__(self, id, name):
        """
        Constructor, creates a new object that has no access rights.

        :param id: str, card holders personal id
        :param name: str, card holders name
        """

        self.__id = id
        self.__name = name
        self.__access = []

    def info(self):
        """
        The method has no return value. It prints the information related to
        the access card in the format:
        id, name, access: a1,a2,...,aN
        for example:
        777, Thelma Teacher, access: OPET, TE113, TIE
        Note that the space characters after the commas and semicolon need to
        be as specified in the task description or the test fails.
        """

        # Initialize a list for access rights.
        rights = []

        # This following part of code removes redundant access codes from the
        # card's info for clear printing purposes.

        # Cycle through saved codes in the card.
        for area in self.__access:
            # Split between doorcodes and areacodes.

            # This portion uses doorcodes.
            if area in DOORCODES:

                # Check if the code is for a particular unique door.
                # (As in there are no payloads for that key in {DOORCODES}.)
                # (Could be written as: "if DOORCODES[area] == []")
                if not DOORCODES[area]:

                    # Add to access rights list.
                    rights.append(area)

                else:

                    # Cycles through possible multiple keys.
                    for clearance in DOORCODES[area]:
                        # Check if the card has rights to that room
                        # and check for redundancies in the access rights list.

                        # If the card has an clearance
                        # that covers multiple rooms.
                        if clearance in self.__access \
                                and clearance not in rights:

                            # Add to access rights list.
                            rights.append(clearance)
                            # Remove unneccessary access code.
                            rights.remove(area)

                        # If the card has an access code for a door
                        # but doesn't have the clearance for it.
                        elif clearance not in self.__access \
                                and area in self.__access \
                                and area not in rights \
                                and len(DOORCODES[area]) == 1:
                            rights.append(area)

            # This portion uses areacodes.
            else:

                # Cycle through every value in {DOORCODES}.
                for load in DOORCODES.values():

                    # As there can be multiple different access rights to
                    # a single room, cycle through them.
                    for key in load:

                        # Check if the card ahs the same access right
                        # and check for redundancies in the access rights list.
                        if key in self.__access and key not in rights:

                            # Add to access rights list.
                            rights.append(key)

        # Convert the access rights list to a string with separation by commas.
        # Also sorts the list to alphabetical order.
        areas = ", ".join(sorted(rights))

        # Print the information.
        print(f"{self.__id}, {self.__name}, access: {areas}")

    def get_name(self):
        """
        :return: Returns the name of the accesscard holder.
        """

        return self.__name

    def add_access(self, new_access_code):
        """
        The method adds a new accesscode into the accesscard according to the
        rules defined in the task description.

        :param new_access_code: str, the accesscode to be added in the card.
        """

        rights = self.__access

        # Prevent duplicate codes in the card.
        if new_access_code in rights:
            return

        else:
            # Add access code to the card.
            rights.append(new_access_code)
            self.__access = rights

        # Remove unnecessary access codes if given a broad clearance.
        # (Ex. "TIE")
        for code in self.__access:
            if code in DOORCODES:
                if new_access_code in DOORCODES[code]:

                    # Remove unnecessary access code(s).
                    rights.remove(code)
                    self.__access = rights

    def check_access(self, door):
        """
        Checks if the accesscard allows access to a certain door.

        :param door: str, the doorcode of the door that is being accessed.
        :return: True: The door opens for this accesscard.
                 False: The door does not open for this accesscard.
        """

        # Check if door is in the card's access rights.
        if door in self.__access:

            return True

        else:

            # Check for a possible clearance code.
            for code in DOORCODES[door]:
                if code in self.__access:

                    return True

        # If all else fails => no access, return False.
        return False

    def merge(self, card):
        """
        Merges the accesscodes from another accesscard to this accesscard.

        :param card: Accesscard, the accesscard whose access rights
                                  are added to this card.
        """

        # Cycle through the codes that need to be added.
        for code in card.__access:

            # Use the "add" method to add the access code to the card.
            self.add_access(code)


def id_check(card_bank, card_id):
    """
    Error check for a given card ID.
    :param card_bank: dict, Holds the information of every card.
    :param card_id: str, Card ID to be checked.
    :return: True, if the card ID exists.
             False, if the card ID doesn't exist.
    """

    try:

        # "card_bank[card_id]" returns True, if it exists in the dictionary.
        if card_bank[card_id]:

            return True

    except KeyError:

        # Print error text and return False.
        print(f"Error: unknown id.")
        return False


def door_check(door_id):
    """
    Error check for an existing door in {DOORCODES}.

    :param door_id: str, Door to be checked.
    :return: True, if the door exists in {DOORCODES}.
             False, if the door doesn't exist in {DOORCODES}.
    """

    try:

        # "DOORCODES[door_id]" returns True,
        #                           if it exists in the dictionary.
        # "not DOORCODES[door_id]" returns True,
        #                           if it has a value of an empty list [].
        if DOORCODES[door_id] or not DOORCODES[door_id]:
            return True

    except KeyError:

        # Print error text and return False.
        print("Error: unknown doorcode.")
        return False


def access_code_check(access_code):
    """
    Error check for if an entered access code exists.

    :param access_code: str, Access code to be checked.
    :return: True, If the access code exists.
             False, If the access code doesn't exist.
    """

    # Initialize a list for general clearance codes.
    # (Ex. "TIE", "TST"...)
    general_codes = []

    # Cycle through rooms and their clearance codes.
    for codes in DOORCODES.values():

        # Cycle through individual clearance codes in rooms.
        for clearance in codes:

            # Prevent duplicates.
            if clearance not in general_codes:

                # Add to the list.
                general_codes.append(clearance)

    try:

        # Check if the access code exists as either a room
        # or a general clearance code.
        if access_code in general_codes:
            return True

        elif DOORCODES[access_code] or not DOORCODES[access_code]:
            return True

    except KeyError:

        # Print the error text and return False.
        print("Error: unknown accesscode.")
        return False


def info_command(card_info, card_id):
    """
    Path for Accesscard's method "info".

    Checks for errors in the user's input regarding the info command.
    Ex. If the entered the card id doesn't exist.

    :param card_info: dict, Information of every card given from a .txt file.
    :param card_id: str, ID of the card where the user wants information from.
    """

    # Check if the entered card ID exists,
    # through error check function id_check.
    if id_check(card_info, card_id):

        # Execute the method.
        card_info[card_id].info()


def list_command(card_info):
    """
    Prints the information of every card.
    Uses the info_command function to print information of a single card.
    (See info_command for more details.)

    :param card_info: dict, Holds the information of every card.
    """

    # Cycle through every card ID in alphabetical order.
    for card_id in sorted(card_info):

        # Use the info_command function
        # to print the information of a single card.
        info_command(card_info, card_id)


def access_command(card_bank, card_id, door_id):
    """
    Path to Accesscard's method check_access.
    Goes through two error checks:
        id_check and door_check (More info in their respective functions.)

    Main purpose is to check if a card has rights to access a given door.

    :param card_bank: dict, Holds the information of every card.
    :param card_id: str, Given ID of a card.
    :param door_id: str, Door to check access for.
    """

    # Check if the card id exists.
    if id_check(card_bank, card_id):

        # Check if the door id exists.
        if door_check(door_id):

            # Check if the card has access to the door.
            if card_bank[card_id].check_access(door_id):

                # Has access, print text.
                print(f"Card {card_id} ( {card_bank[card_id].get_name()} ) "
                      f"has access to door {door_id}")
            else:

                # Doesn't have access, print text.
                print(f"Card {card_id} ( {card_bank[card_id].get_name()} ) "
                      f"has no access to door {door_id}")


def add_command(card_bank, card_id, access_code):
    """
    Path for Accesscard's method "add".
    Performs two error checks:
            id_check and access_code_check
            (More info in their respective functions.)

    :param card_bank: dict, Holds the information of every card.
    :param card_id: str, ID of the card.
    :param access_code: str, The access code to be added.
    """

    # Check if the card id exists.
    if id_check(card_bank, card_id):

        # Check if the access code exists.
        if access_code_check(access_code):

            # Execute the method.
            card_bank[card_id].add_access(access_code)


def merge_command(card_bank, card_id_to, card_id_from):
    """
    Path for Accesscard's method "merge".
    Performs two card ID error checks:
                One for each of the cards.
                (More information in the function "id_check")

    :param card_bank: dict, Holds the information of every card.
    :param card_id_to: str, The recipient card, where codes will be added to.
    :param card_id_from: str, The donor card, where codes will be copied from.
    """

    # Check if both card id's exist.
    if id_check(card_bank, card_id_to):
        if id_check(card_bank, card_id_from):

            # Execute the method.
            card_bank[card_id_to].merge(card_bank[card_id_from])


def main():
    """
    This program acts as an access card system,
    that stores information from a ".txt" file. (CSV-format)

    This "main" function includes the user interface and file reading.
    File information is stored into a dictionary.

    Information is stored into an object called Accesscard,
    in the form of (ID, name).
    Access rights are added using a method of the belonging to the class.

    The main dictionary {card_bank} holds the information of those objects,
    in the form of {ID, object}.
    """

    # File that holds the information of every card. (Format: CSV)
    filename = "accessinfo.txt"

    # Initialize a dictionary where the information will be stored.
    card_bank = {}

    # Error check for if the file can't be opened.
    try:

        # Open file.
        file = open(filename, mode="r")

        # Cycle through every line of text in the text file.
        for line in file:

            # Split the line at every ";".
            info = line.split(";")

            # Remove any empty space at the end of text line,
            # and split the access codes at the commas.
            rights = info[2].rstrip().split(",")

            # Make an object of the card, with given information.
            card_bank[info[0]] = Accesscard(info[0], info[1])

            # Cycle through access rights.
            for area in rights:

                # Add access information to the card.
                card_bank[info[0]].add_access(area)

    except OSError:

        # Print error text if reading the file fails.
        print(f"Error: opening the file '{filename}' failed!")

        return

    # Close file.
    file.close()

    # User interface.
    while True:

        # User command input.
        line = input("command> ")

        # If the user presses enter, as in enters nothing, end the program.
        if line == "":
            break

        # Split input for possible commands.
        strings = line.split()
        command = strings[0]

        if command == "list" and len(strings) == 1:

            # Use the function to print information of every card.
            list_command(card_bank)

        elif command == "info" and len(strings) == 2:

            # Prints information of a single card entered by the user.
            card_id = strings[1]

            # Uses a function to operate cleanly.
            info_command(card_bank, card_id)

        elif command == "access" and len(strings) == 3:

            # Separate the user input for differentiation between information.
            card_id = strings[1]
            door_id = strings[2]

            # Uses a function to operate cleanly.
            access_command(card_bank, card_id, door_id)

        elif command == "add" and len(strings) == 3:

            # Separate the user input for differentiation between information.
            card_id = strings[1]
            access_code = strings[2]

            # Uses a function to operate cleanly.
            add_command(card_bank, card_id, access_code)

        elif command == "merge" and len(strings) == 3:

            # Separate the user input for differentiation between information.
            card_id_to = strings[1]
            card_id_from = strings[2]

            # Uses a function to operate cleanly.
            merge_command(card_bank, card_id_to, card_id_from)

        elif command == "quit":

            # The command to end the program.
            print("Bye!")
            return
        
        else:

            # Error message for errorneus command.
            print("Error: unknown command.")


if __name__ == "__main__":
    main()
