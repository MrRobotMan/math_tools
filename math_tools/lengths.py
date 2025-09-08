from __future__ import annotations

from dataclasses import dataclass
import fractions
from functools import total_ordering
import re


@total_ordering
@dataclass(slots=True)
class USCustomary:
    """
    Class to store a length in US Customary units.

    Examples:
        >>> USCustomary(12, 0)
        USCustomary(feet=12, inch=0)
        >>> USCustomary(inch=15)
        USCustomary(feet=1, inch=3)
        >>> USCustomary(4.5)
        USCustomary(feet=4, inch=6.0)

    """

    feet: int = 0
    inch: float = 0

    def __post_init__(self) -> None:
        self._process_feet_and_inches()

    def _process_feet_and_inches(self) -> None:
        feet, inch_from_feet = divmod(self.feet, 1)
        feet_from_inch, self.inch = divmod(self.inch + inch_from_feet * 12, 12)
        self.feet = int(feet + feet_from_inch)

    @classmethod
    def from_str(cls, val: str) -> USCustomary:
        r"""
        Convert a string representation to the class.

        String should be in the format of x'-y" or xft-yin
        Inches can be either x y/z" or x.xxx"

        Returns:
            USCustomary

        Raises:
            ValueError: If the string format is invalid

        Examples:
            >>> USCustomary.from_str("12'-3 1/2\"")
            USCustomary(feet=12, inch=3.5)
            >>> USCustomary.from_str('15"')
            USCustomary(feet=1, inch=3.0)
            >>> USCustomary.from_str('12.375"')
            USCustomary(feet=1, inch=0.375)
            >>> USCustomary.from_str("12ft3 1/2in")
            USCustomary(feet=12, inch=3.5)
            >>> USCustomary.from_str("15in")
            USCustomary(feet=1, inch=3.0)
            >>> USCustomary.from_str("12.375in")
            USCustomary(feet=1, inch=0.375)

        """
        match_sym = re.search(r"""(?P<feet>.*')?-?(?P<inches>.*")""", val)
        match_chr = re.search(r"(?P<feet>.*ft)?-?(?P<inches>.*in)", val)
        match = match_sym or match_chr
        if not match:
            msg = f"Could not form USCustomary from {val}"
            raise ValueError(msg)
        feet = match.group("feet")
        feet = int(feet.replace("'", "").replace("ft", "")) if feet else 0
        inches = match.group("inches")
        inches = inches.replace('"', "").replace("in", "") if inches else "0"
        inches, *fraction = inches.split()
        inches = float(inches)
        if fraction:
            frac = fractions.Fraction(fraction[0])
            inches += int(frac.numerator) / int(frac.denominator)
        return cls(feet, inches)

    @property
    def as_metric(self) -> Metric:
        """
        Convert to Metric.

        Example:
            >>> USCustomary(12, 0).as_metric
            Metric(millimeters=3657.6)

        """
        return Metric(self.as_inches * 25.4)

    @property
    def as_feet(self) -> float:
        """
        Convert to feet only.

        Example:
            >>> USCustomary(8, 9).as_feet
            8.75

        """
        return self.feet + self.inch / 12

    @property
    def as_inches(self) -> float:
        """
        Convert to inches only.

        Example:
            >>> USCustomary(12, 3.5).as_inches
            147.5

        """
        return self.feet * 12 + self.inch

    def __add__(self, other: object) -> USCustomary:
        if isinstance(other, Metric):
            other = other.as_us_customary
        if not isinstance(other, USCustomary):
            raise NotImplementedError
        return USCustomary(inch=self.as_inches + other.as_inches)

    def __sub__(self, other: object) -> USCustomary:
        if isinstance(other, Metric):
            other = other.as_us_customary
        if not isinstance(other, USCustomary):
            raise NotImplementedError
        return USCustomary(inch=self.as_inches - other.as_inches)

    def __truediv__(self, val: float | USCustomary) -> USCustomary | float:
        if isinstance(val, USCustomary):
            return self.as_inches / val.as_inches
        return USCustomary(inch=self.as_inches / val)

    __rtruediv__ = __truediv__

    def __mul__(self, val: float | USCustomary) -> USCustomary | float:
        if isinstance(val, USCustomary):
            return self.as_inches * val.as_inches
        return USCustomary(inch=self.as_inches * val)

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Metric):
            other = other.as_us_customary
        if not isinstance(other, USCustomary):
            raise NotImplementedError
        return self.as_inches == other.as_inches

    def __gt__(self, other: object) -> bool:
        if isinstance(other, Metric):
            other = other.as_us_customary
        if not isinstance(other, USCustomary):
            raise NotImplementedError
        return self.as_inches > other.as_inches

    def __hash__(self) -> int:
        return hash((self.feet, self.inch))


@total_ordering
@dataclass(slots=True)
class Metric:
    """
    Class to store a length in Metric units.

    Examples:
        >>> Metric(3000)
        Metric(millimeters=3000)

    """

    millimeters: float = 0

    @property
    def as_us_customary(self) -> USCustomary:
        """
        Convert to US Customary.

        Example:
            >>> Metric(3000).as_us_customary
            USCustomary(feet=9, inch=10.110236220472444)

        """
        return USCustomary(inch=self.millimeters / 25.4)

    def __add__(self, other: object) -> Metric:
        if isinstance(other, USCustomary):
            other = other.as_metric
        if not isinstance(other, Metric):
            raise NotImplementedError
        return Metric(self.millimeters + other.millimeters)

    def __sub__(self, other: object) -> Metric:
        if isinstance(other, USCustomary):
            other = other.as_metric
        if not isinstance(other, Metric):
            raise NotImplementedError
        return Metric(self.millimeters - other.millimeters)

    def __truediv__(self, val: float | Metric) -> Metric | float:
        if isinstance(val, Metric):
            return self.millimeters / val.millimeters
        return Metric(self.millimeters / val)

    __rtruediv__ = __truediv__

    def __mul__(self, val: float | Metric) -> Metric | float:
        if isinstance(val, Metric):
            return self.millimeters * val.millimeters
        return Metric(self.millimeters * val)

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        if isinstance(other, USCustomary):
            other = other.as_metric
        if not isinstance(other, Metric):
            raise NotImplementedError
        return self.millimeters == other.millimeters

    def __gt__(self, other: object) -> bool:
        if isinstance(other, USCustomary):
            other = other.as_metric
        if not isinstance(other, Metric):
            raise NotImplementedError
        return self.millimeters > other.millimeters

    def __hash__(self) -> int:
        return hash(self.millimeters)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
