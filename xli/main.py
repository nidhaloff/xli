from typing import Any

import inspect
import sys
import textwrap

import typer


class XLI:
    """XLI is a wrapper class that exposes methods used to convert python scripts to a cli"""

    def __init__(self, *objects, **cli_kwargs) -> None:
        # sub clis that will be added to the parent cli app
        sub_clis = objects
        if cli_kwargs.get("clis"):
            sub_clis = cli_kwargs.pop("clis")
        if cli_kwargs.get("apps"):
            sub_clis = cli_kwargs.pop("apps")

        self.app = typer.Typer(**cli_kwargs)
        self._add_clis_from_objects(*sub_clis)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.app(*args, **kwds)

    def _add_clis_from_objects(self, *objects):
        for cli in objects:
            if inspect.isclass(cli):
                self._add_cli_from_class(cli)
            elif inspect.isfunction(cli):
                self._add_cli_from_func(cli)
            elif inspect.ismodule(cli):
                self._add_cli_from_module(cli)

    def _add_cli_from_func(self, func):
        """create a typer cli app from a function"""
        self.app.command()(func)

    def _add_cli_from_class(self, class_):
        """create a typer cli app from a class"""
        sub_app = typer.Typer(help=class_.__doc__)  # init a sub typer app
        class_name = class_.__name__.lower()  # get class name that will be used as a sub command name
        # get all public class methods
        class_methods = [
            getattr(class_, func)
            for func in dir(class_)
            if callable(getattr(class_, func)) and not func.startswith("__")
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

            sub_app.command()(method)

        # add the sub cli app to the root app
        self.app.add_typer(sub_app, name=class_name)

    def _add_cli_from_module(self, module):
        """create a typer cli app from a python module"""
        sub_app = typer.Typer(help=module.__doc__)  # init a sub typer app
        function_list = [func for (_, func) in inspect.getmembers(module, inspect.isfunction)]
        sub_command_name = module.__name__.split(".")[-1]
        for func in function_list:
            sub_app.command()(func)
        self.app.add_typer(sub_app, name=sub_command_name)

    def _add_cli_from_modules(self, *modules, **kwargs):
        """create a typer cli app from multiple modules where module name is used as subcommand"""
        for module in modules:
            self._add_cli_from_module(module)
