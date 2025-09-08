from __future__ import annotations

from enum import StrEnum, auto
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
        "ibeam_equalflange": section_modulus.Ibeam_equalflange,
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
    options = [opt for opt in choices]
    for idx, opt in enumerate(options, start=1):
        print(f"{idx} {opt}")
    while True:
        if is_valid_choice(picked := input(), len(choices)):
            print()
            return options[int(picked) - 1]
        print(f"Invalid choice {picked}, try again.")


def is_valid_choice(selected: str, max: int) -> bool:
    try:
        return 0 < int(selected) <= max
    except ValueError:
        return False


def execute[T](func: Callable[..., T]) -> T:
    while True:
        try:
            args = [
                float(v)
                for v in input("Enter the arguements as a space separated list: ").split(" ")
            ]
        except ValueError:
            print("Invalid input. Try again.")
        else:
            return func(*args)


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
