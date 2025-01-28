"""
COMP.CS.100 Ohjelmointi 1
Malakias Kosonen
Tehtävä 10.4: Tuote
"""


class Product:
    """
    This class defines a simplified product for sale in a store.
    """

    def __init__(self, product_name, product_price):
        """
        A product is initialized with the name and price and possible
        sale percentage
        :param product_name: str, product name
        :param product_price: float, price of the product
        :param sale_percentage: float, percentage of the sale
        """

        self.__product_name = product_name
        self.__product_price = product_price
        self.__sale_percentage = 0

    def printout(self):
        """
        Prints out the needed information. Good for debugging.
        """

        print(self.__product_name)
        print(f"  price: {self.__product_price}")
        print(f"  sale%: {self.__sale_percentage}")

    def get_price(self):
        """
        Calculates the new price with the possible sale percentage.
        :return: float, price after the sale
        """

        price = self.__product_price * (1 - self.__sale_percentage/100)
        return price

    def set_sale_percentage(self, sale_percentage):
        """
        Sets the sale percentage.
        :param sale_percentage: float, sale percentage
        :return: float, sale percentage
        """

        self.__sale_percentage = sale_percentage


def main():
    ################################################################
    #                                                              #
    #  You can use the main-function to test your Product class.   #
    #  The automatic tests will not use the main you submitted.    #
    #                                                              #
    #  Voit käyttää main-funktiota Product-luokkasi testaamiseen.  #
    #  Automaattiset testit eivät käytä palauttamaasi mainia.      #
    #                                                              #
    ################################################################

    test_products = {
        "milk":   1.00,
        "sushi": 12.95,
    }

    sale_percentage = 0

    for product_name in test_products:
        print("=" * 20)
        print(f"TESTING: {product_name}")
        print("=" * 20)

        prod = Product(product_name, test_products[product_name])

        prod.printout()
        print(f"Normal price: {prod.get_price():.2f}")

        print("-" * 20)

        prod.set_sale_percentage(10.0)
        prod.printout()
        print(f"Sale price: {prod.get_price():.2f}")

        print("-" * 20)

        prod.set_sale_percentage(25.0)
        prod.printout()
        print(f"Sale price: {prod.get_price():.2f}")

        print("-" * 20)


if __name__ == "__main__":
    main()
