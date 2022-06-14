from xli.cli import example, example2
from xli.main import XLI

if __name__ == "__main__":
    cli = XLI.from_modules(example, example2)
    cli()
