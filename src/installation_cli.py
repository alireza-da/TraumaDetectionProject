import click
from installation import Installation
import logging


@click.command()
@click.option('--os-name', default="windows", help="OS name which package will be installed on. Specify os name with "
                                                   "lowercase letters e.g. windows, linux, mac")
@click.option('--path', default=".", help="Installation Path")
def os(os_name, path):
    # logging.info(f"Installing Package on {os_name}")
    install = Installation(os_name, path, "app.py")
    install.install()


if __name__ == "__main__":
    os()
