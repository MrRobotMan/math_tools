from dataclasses import dataclass
from math import pi
from typing import Iterable


@dataclass(slots=True, frozen=True)
class Section:
    centroid: tuple[tuple[float, float], tuple[float, float]] = (
        (0, 0),
        (0, 0),
    )
    area: float = 0
    moment_of_inertia: tuple[float, float] = (0, 0)

    @property
    def Ixx(self) -> float:
        return self.moment_of_inertia[0]

    @property
    def Iyy(self) -> float:
        return self.moment_of_inertia[1]

    @property
    def Sx(self) -> tuple[float, float]:
        return self.Ixx / self.centroid[1][0], self.Ixx / self.centroid[1][1]

    @property
    def Sy(self) -> tuple[float, float]:
        return self.Iyy / self.centroid[0][0], self.Iyy / self.centroid[0][1]

    def __str__(self) -> str:
        return f"""CG X: {self.centroid[0][0]:0.3f}\t{self.centroid[0][1]:0.3f}
CG Y: {self.centroid[1][0]:0.3f}\t{self.centroid[1][1]:0.3f}
Area: {self.area:0.3f}
Ixx: {self.Ixx:0.3f}
Iyy: {self.Iyy:0.3f}
Sx: {self.Sx[0]:0.3f}\t{self.Sx[1]:0.3f}
Sy: {self.Sy[0]:0.3f}\t{self.Sy[1]:0.3f}"""


def bar(depth: float, thickness: float) -> Section:
    """
    Calculate the properties of a bar.

    Parameters
    ----------
    depth : float
    thickness: float

    Returns
    -------
    Section

    Examples
    --------
    >>> bar(2, 0.5)
    Section(centroid=((0.25, 0.25), (1.0, 1.0)), area=1.0, moment_of_inertia=(0.3333333333333333, 0.020833333333333332))
    """
    y = depth / 2
    x = thickness / 2
    area = depth * thickness
    Ixx = depth**3 * thickness / 12
    Iyy = thickness**3 * depth / 12
    return Section(
        centroid=((x, x), (y, y)),
        area=area,
        moment_of_inertia=(Ixx, Iyy),
    )


def tbeam(depth: float, web_thick: float, flg_width: float, flg_thick: float) -> Section:
    """
    Calculate the properties of a T beam.

    Parameters
    ----------
    depth : float
    web_thick : float
    flg_width : float
    flg_thick : float

    Returns
    -------
    Section
    """
    height = depth - web_thick
    area = flg_width * flg_thick + height * web_thick
    sum_b_d_squared = depth**2 * web_thick + flg_thick**2 * (flg_width - web_thick)
    y = depth - sum_b_d_squared / (2 * area)
    x = flg_width / 2
    b_d_cubed = (
        web_thick * y**3
        + flg_width * (depth - y) ** 3
        - (flg_width - web_thick) * (depth - y - flg_thick) ** 3
    )
    Ixx = 1 / 3 * b_d_cubed
    Iyy = web_thick**3 * height / 12 + flg_width**3 * flg_thick / 12
    return Section(
        centroid=((x, x), (y, depth - y)),
        area=area,
        moment_of_inertia=(Ixx, Iyy),
    )


def angle(long_leg: float, short_leg: float, thick: float) -> Section:
    """
    Calculate the properties of an angle.

    Parameters
    ----------
    long_leg : float
    short_leg : float
    thick : float

    Returns
    -------
    Section
    """
    area = (long_leg + short_leg - thick) * thick
    i_xnaught = (thick / 3) * (short_leg * thick**2 + long_leg**3 - thick**3)
    i_ynaught = (thick / 3) * (long_leg * thick**2 + short_leg**3 - thick**3)
    x = (1 / area) * ((thick / 2) * (short_leg**2 + long_leg * thick - thick**2))
    y = (1 / area) * ((thick / 2) * (long_leg**2 + short_leg * thick - thick**2))
    Ixx = i_xnaught - area * y**2
    Iyy = i_ynaught - area * x**2
    return Section(
        centroid=((x, short_leg - x), (y, long_leg - y)),
        area=area,
        moment_of_inertia=(Ixx, Iyy),
    )


def pipe(od: float, thickness: float) -> Section:
    """
    Calculate the properties of a pipe.

    Parameters
    ----------
    od : float
    thickness: float

    Returns
    -------
    Section
    """
    outer = circle(od / 2)
    inner = circle(od / 2 - thickness)
    return Section(
        centroid=outer.centroid,
        area=outer.area - inner.area,
        moment_of_inertia=(outer.Ixx - inner.Ixx, outer.Iyy - inner.Iyy),
    )


def circle(radius: float) -> Section:
    """
    Calculate the properties of a solid circle.

    Parameters
    ----------
    radius : float

    Returns
    -------
    Section
    """
    return Section(
        centroid=((radius, radius), (radius, radius)),
        area=pi * radius**2,
        moment_of_inertia=(pi * (radius**4) / 64, pi * (radius**4) / 64),
    )


def Ibeam_equalflange(
    depth: float, web_thick: float, flg_width: float, flg_thick: float
) -> Section:
    """
    Calculate the properties of a T beam.

    Parameters
    ----------
    depth : float
    web_thick : float
    flg_width : float
    flg_thick : float

    Returns
    -------
    Section
    """
    h = depth - web_thick
    y = depth / 2
    x = flg_width / 2
    area = 2 * flg_width * flg_thick + h * web_thick
    Ixx = (flg_width * depth**3 - h**3 * (flg_width - web_thick)) / 12
    Iyy = (2 * flg_thick * flg_width**3 + h * web_thick**3) / 12
    return Section(
        centroid=((x, x), (y, y)),
        area=area,
        moment_of_inertia=(Ixx, Iyy),
    )


def parallel_axis(
    widths: Iterable[float], heights: Iterable[float], axis_offset: float = 0
) -> tuple[Section, float]:

    prev = axis_offset
    area = moment = Ide = 0
    for width, height in zip(widths, heights):
        area += width * (height - prev)
        moment += width * (height**2 - prev**2) / 2
        Ide += width * (height**3 - prev**3) / 3
        prev = height

    d = moment / area
    Ixx = Ide - area * d**2
    return (
        Section(
            centroid=((0, 0), (d, prev - d)),
            area=area,
            moment_of_inertia=(Ixx, 0),
        ),
        Ide,
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
