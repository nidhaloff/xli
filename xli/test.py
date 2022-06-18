from xli.cli import example, example2
from xli.main import XLI


class Test:
    """Command for tests."""

    def __init__(self) -> None:
        self.offset = 1
        print("hello init")

    def test_func(self, name: str):
        """Just a test."""
        print(f"testing: {name} using offset {self.offset}")


if __name__ == "__main__":
    # cli = XLI.from_modules(example2, example)
    cli = XLI(Test, example, example2, add_completion=False, context_settings=dict(help_option_names=["-h", "--help"]))
    cli()
