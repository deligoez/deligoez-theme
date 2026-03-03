"""Deligoez theme generators package."""

from .ghostty import generate_ghostty
from .zed import generate_zed
from .phpstorm import generate_phpstorm
from .terminal_app import generate_terminal_app


def generate_all(palette):
    generate_ghostty(palette)
    generate_zed(palette)
    generate_phpstorm(palette)
    generate_terminal_app(palette)
