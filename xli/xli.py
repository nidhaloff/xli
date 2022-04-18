import inspect
import textwrap

import typer


class XLI:
    """XLI is a wrapper class that exposes methods used to convert python scripts to a cli"""

    app = typer.Typer()

    @classmethod
    def from_func(cls, func):
        """create a typer cli app from a function"""
        cls.app.command()(func)
        return cls.app

    @classmethod
    def from_class(cls, _class):
        """create a typer cli app from a class"""
        sub_app = typer.Typer()  # init a sub typer app
        class_name = (
            _class.__name__.lower()
        )  # get class name that will be used as a sub command name
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
            sub_app.command()(method)

        # add the sub cli app to the root app
        cls.app.add_typer(sub_app, name=class_name)
        return cls.app

    @classmethod
    def from_module(cls, module):
        """create a typer cli app from a python module"""
        sub_app = typer.Typer()  # init a sub typer app
        function_list = [
            func for (_, func) in inspect.getmembers(module, inspect.isfunction)
        ]
        sub_command_name = module.__name__.split(".")[-1]
        for func in function_list:
            sub_app.command()(func)
        cls.app.add_typer(sub_app, name=sub_command_name)
        return cls.app

    @classmethod
    def from_modules(cls, *modules, **kwargs):
        """create a typer cli app from multiple modules where module name is used as subcommand"""
        for module in modules:
            cls.from_module(module)
        return cls.app

    @classmethod
    def from_dir(cls, directory: str):
        pass
