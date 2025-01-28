"""
COMP.CS.100 Ohjelmointi 1
Malakias Kosonen
Tehtävä 13.7: Painoindeksilaskuri
"""

from tkinter import *


class Userinterface:

    def __init__(self):
        """
        Iinitialize the window.
        """

        self.__mainwindow = Tk()

        self.__weight_value = Entry(self.__mainwindow, text="Weight:")

        self.__height_value = Entry(self.__mainwindow, text="Height:")

        self.__calculate_button = Button(self.__mainwindow, text="Calculate", bg="red", command=self.calculate_BMI)

        self.__result_text = Label(self.__mainwindow, text="", relief="raised", width=20)

        self.__explanation_text = Label(self.__mainwindow, text="", relief="sunken")

        self.__stop_button = Button(self.__mainwindow, text="STOP", command=self.stop)

        self.__weight_value.pack(expand=True, pady=5)
        self.__height_value.pack(expand=True, pady=5)
        self.__calculate_button.pack(expand=True, pady=5)
        self.__stop_button.pack(expand=True, pady=5)
        self.__result_text.pack(expand=True, padx=20, pady=10)
        self.__explanation_text.pack(expand=True, padx=60, pady=10)

    def calculate_BMI(self):
        """
        Part b) This method calculates the BMI of the user and
        displays it. First the method will get the values of
        height and weight from the GUI components
        self.__height_value and self.__weight_value.  Then the
        method will calculate the value of the BMI and show it in
        the element self.__result_text.

        Part e) Last, the method will display a verbal
        description of the BMI in the element
        self.__explanation_text.
        """

        try:

            weight_kg = float(self.__weight_value.get())
            height_cm = float(self.__height_value.get()) / 100

            if weight_kg <= 0 or height_cm <= 0:
                self.__explanation_text.configure(
                    text="Error: height and weight must be positive.")
                self.reset_fields()
                return

            bmi = weight_kg / (height_cm ** 2)

            self.__result_text.configure(text=f"{bmi:.2f}")

            if 18.5 < bmi < 25:
                self.__explanation_text.configure(text="Your weight is normal.")

            elif bmi < 18.5:
                self.__explanation_text.configure(text="You are underweight.")

            elif bmi > 25:
                self.__explanation_text.configure(text="You are overweight.")

        except ValueError:

            self.__explanation_text.configure(
                text="Error: height and weight must be numbers.")
            self.reset_fields()

    def reset_fields(self):
        """
        In error situations this method will zeroize the elements
        self.__result_text, self.__height_value, and self.__weight_value.
        """

        self.__weight_value.delete(0, "end")
        self.__height_value.delete(0, "end")
        self.__result_text.configure(text="")

    def stop(self):
        """
        Ends the execution of the program.
        """

        self.__mainwindow.destroy()

    def start(self):
        """
        Starts the mainloop.
        """
        self.__mainwindow.mainloop()


def main():
    # Notice how the user interface can be created and
    # started separately.  Don't change this arrangement,
    # or automatic tests will fail.
    ui = Userinterface()
    ui.start()


if __name__ == "__main__":
    main()
