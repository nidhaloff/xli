from xli.cli import example, example2
from xli.main import XLI


class Test:
    """Command for tests."""

    def test_func(name: str):
        """Just a test."""
        print(f"testing: {name}")


if __name__ == "__main__":
    # cli = XLI.from_modules(example2, example)
    cli = XLI(Test, example, add_completion=False)
    cli()
