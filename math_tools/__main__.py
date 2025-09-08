from __future__ import annotations

from enum import StrEnum, auto
from inspect import signature
from typing import TYPE_CHECKING

from . import cones, section_modulus

if TYPE_CHECKING:
    from collections.abc import Callable

FUNCTIONS = {
    "cones": {
        "distance": cones.distance,
        "angle": cones.angle,
        "radius": cones.radius_at_location,
        "height": cones.height,
    },
    "section_modulus": {
        "bar": section_modulus.bar,
        "tbeam": section_modulus.tbeam,
        "angle": section_modulus.angle,
        "pipe": section_modulus.pipe,
        "circle": section_modulus.circle,
        "I beam equal flange": section_modulus.i_beam_equalflange,
    },
}


def main() -> None:
    print("Welcome to math tools")
    print("=====================")
    while True:
        modules = {"cones": Cones, "section_modulus": SectionModulus, "back": Mod}
        choice = str(menu(Mod, "Welcome to mathtools. Select an option:"))
        if choice == "quit":
            break
        while True:
            item = str(menu(modules[choice], "Select a function:"))
            if item == "back":
                break
            if item == "quit":
                return
            func = FUNCTIONS[choice][item]
            print(func.__doc__)
            res = execute(func)
            print(f"\n{res}\n")


def menu[T: type[StrEnum]](choices: T, msg: str) -> T:
    print(msg)
    options = list(choices)
    for idx, opt in enumerate(options, start=1):
        print(f"{idx} {opt}")
    while True:
        if is_valid_choice(picked := input(), len(choices)):
            print()
            return options[int(picked) - 1]
        print(f"Invalid choice {picked}, try again.")


def is_valid_choice(selected: str, max_limit: int) -> bool:
    try:
        return 0 < int(selected) <= max_limit
    except ValueError:
        return False


def execute[T](func: Callable[..., T]) -> T:
    params = signature(func).parameters
    args = [get_param(k, v.annotation) for (k, v) in params.items()]
    return func(*args)


def get_param[T](param: str, param_type: Callable[[str], T]) -> T:
    try:
        return param_type(input(f"{param}: "))
    except ValueError:
        print("Invalid Input, try again.")
        return get_param(param, param_type)


class Mod(StrEnum):
    CONES = auto()
    SECTION_MODULUS = auto()
    QUIT = auto()


class Cones(StrEnum):
    DISTANCE = auto()
    ANGLE = auto()
    RADIUS = auto()
    HEIGHT = auto()
    BACK = auto()
    QUIT = auto()


class SectionModulus(StrEnum):
    BAR = auto()
    TBEAM = auto()
    ANGLE = auto()
    PIPE = auto()
    CIRCLE = auto()
    IBEAM_EQUALFLANGE = auto()
    BACK = auto()
    QUIT = auto()


if __name__ == "__main__":
    try:
        main()
        print("Goodbye")
    except KeyboardInterrupt:
        print("Goodbye")
