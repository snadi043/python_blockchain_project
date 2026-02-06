# creating a new class printable which returns the string version of the the class attributes itself.
class Printable:
    # __repr__() -> This is a python built-in method which returns the string value of the class attributes.
    def __repr__(self):
        return str(self.__dict__)