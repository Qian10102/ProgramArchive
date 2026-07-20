class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.name = restaurant_name
        self.cuisine_type = cuisine_type

    def describe_restaurant(self):
        print(f"The restaurant is named as {self.name} and it's cuisine type is {self.cuisine_type}.")

    def open_restaurant(self):
        print(f"The restaurant is now open.")