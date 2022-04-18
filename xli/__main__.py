# type: ignore[attr-defined]

from xli.cli import example, example2
from xli.xli import XLI

app = XLI.from_modules(example, example2)


if __name__ == "__main__":
    app()
