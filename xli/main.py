import inspect
import textwrap
from dataclasses import dataclass

import click


@dataclass
class XLI:
    """XLI is a wrapper class that exposes methods used to convert python scripts to a cli"""

    cli = click.command(lambda: None)

    @classmethod
    def from_func(cls, func):
        cls.cli.command()(func)
        return cls.cli

    @classmethod
    def from_class(cls, _class):
        cli_group = click.command(lambda: None)
        class_name = _class.__name__.lower()  # get class name that will be used as a sub command name
        # get all public class methods
        class_methods = [
            getattr(_class, func)
            for func in dir(_class)
            if callable(getattr(_class, func)) and not func.startswith("__")
        ]

        for method in class_methods:
            method_src_code = inspect.getsource(method)
            # remove self from method args (since args are parsed by typer to be used in the cli app)
            if "self" in method_src_code:
                method_name = method.__name__
                method_src_code = textwrap.dedent(method_src_code)
                method_src_code = method_src_code.replace("self,", "")
                exec(method_src_code)
                method = locals()[method_name]

            # add method as a command to the sub cli app
            cli_group.command()(method)

        # add the sub cli app to the root app
        cls.cli.add_command(cli_group, name=class_name)
        return cls.cli

    @classmethod
    def from_module(cls, module):

        cli_group = click.command(lambda: None)
        function_list = [func for (_, func) in inspect.getmembers(module, inspect.isfunction)]
        sub_command_name = module.__name__.split(".")[-1]
        for func in function_list:
            cli_group.command()(func)
        cls.cli.add_command(cli_group, name=sub_command_name)
        return cls.cli

    @classmethod
    def from_modules(cls, *modules, **kwargs):
        for module in modules:
            cls.from_module(module)
        return cls.cli
