""" docs for example.py """

CONST = 5


def static(user: str):
    """static command user greeting"""
    print(f"greeting user: {user} with const: {CONST}")


def hello(name: str) -> str:
    """hello cli function"""
    print(f"Hello {name}!")
