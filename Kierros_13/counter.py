"""
COMP.CS.100 Ohjelmointi 1
Malakias Kosonen
Tehtävä 13.5: Kappaletavaralaskuri
"""

from tkinter import *


class Counter:
    def __init__(self):
        """
        Initialize the user interface window, with the value of zero.
        """

        self.__value = 0

        self.__mainwindow = Tk()

        self.__current_value = Label(self.__mainwindow, text=self.__value)
        self.__current_value.pack(side=TOP)

        self.__reset_button = Button(self.__mainwindow, text="Reset",
                                     command=self.reset)
        self.__reset_button.pack(side=LEFT)

        self.__increase_button = Button(self.__mainwindow, text="Increase",
                                        command=self.increase)
        self.__increase_button.pack(side=LEFT)

        self.__decrease_button = Button(self.__mainwindow, text="Decrease",
                                        command=self.decrease)
        self.__decrease_button.pack(side=LEFT)

        self.__quit_button = Button(self.__mainwindow, text="Quit",
                                    command=self.quit)
        self.__quit_button.pack(side=LEFT)

        self.__mainwindow.mainloop()

    def reset(self):
        """
        Reset the counter to zero.
        """

        self.__value = 0
        self.__current_value.configure(text=self.__value)

    def increase(self):
        """
        Increase the counter by one.
        """

        self.__value += 1
        self.__current_value.configure(text=self.__value)

    def decrease(self):
        """
        Decrease the counter by one.
        """

        self.__value -= 1
        self.__current_value.configure(text=self.__value)

    def quit(self):
        """
        Closes the window and quits.
        """

        self.__mainwindow.destroy()


def main():
    # There is no need to modify the main function.
    # As a matter of fact, automated tests ignore main
    # once again.

    Counter()


if __name__ == "__main__":
    main()
