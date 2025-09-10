import math


def distance(
    height_point_1: float,
    angle_point_1: float,
    height_point_2: float,
    angle_point_2: float,
    cone_large_end_diameter: float,
    cone_half_angle: float,
) -> float:
    """
    Find the shortest path between two points on a cone.

    Parameters
    ----------
    height_point_1 : float
        Height along the cone axis to the first point
    angle_point_1 : float
        Angle around the axis to the first point
    height_point_2 : float
        Height along the cone axis to the second point
    angle_point_2 : float
        Angle around the axis to the second point
    cone_large_end_diameter : float
        Diameter of the cone large end
    cone_half_angle : float
        Cone half angle

    Returns
    -------
    float

    Examples
    --------
    >>> distance(60, 15, 20, 7, 127, 30)
    46.503239630149544

    """
    # Convert all angles to radians
    cone_half_angle = math.radians(cone_half_angle)
    angle_point_1 = math.radians(angle_point_1)
    angle_point_2 = math.radians(angle_point_2)

    # Calculate the height of the cone
    apex_height = cone_large_end_diameter / (2 * math.tan(cone_half_angle))

    # Calculate the cone diameter at each point
    diameter1 = (apex_height - height_point_1) * cone_large_end_diameter / apex_height
    diameter2 = (apex_height - height_point_2) * cone_large_end_diameter / apex_height

    # Calculate the side length at each point.
    # This is the radius of the point location in the flat
    side1 = diameter1 / (2 * math.sin(cone_half_angle))
    side2 = diameter2 / (2 * math.sin(cone_half_angle))

    # Calculate the included angle between points in the flat
    # sine(cone_half_angle) gives the percent of a circle the cone covers in the flat
    angle = math.sin(cone_half_angle) * abs(angle_point_1 - angle_point_2)

    # Return side "c" from side-angle-side triangle formula
    return math.sqrt(side1**2 + side2**2 - (2 * side1 * side2 * math.cos(angle)))


def angle(dia_lg_end: float, dia_sm_end: float, length: float) -> float:
    """
    Calculate the cone half-angle.

    Parameters
    ----------
    dia_lg_end : float
        Diameter of the large end
    dia_sm_end : float
        Diameter of the small end
    length : float
        Axial length

    Returns
    -------
    float

    Examples
    --------
    >>> angle(30, 20, 8.66)
    30.000727780827372

    """
    delta = (dia_lg_end - dia_sm_end) / 2
    return math.degrees(math.atan(delta / length))


def radius_at_location(
    dia_lg_end: float, half_apex_angle: float, location_from_lg_end: float
) -> float:
    """
    Calculate the radius at a location on a cone.

    Parameters
    ----------
    dia_lg_end : float
        Diameter of the large end
    half_apex_angle : float
        Half apex angle
    location_from_lg_end : float
        Axial distance from the large end

    Returns
    -------
    float

    Examples
    --------
    >>> radius_at_location(174, 30, 58)
    53.51368438700171

    """
    return dia_lg_end / 2 - (math.tan(math.radians(half_apex_angle)) * location_from_lg_end)


def height(dia_lg_end: float, dia_sm_end: float, half_apex_angle: float) -> float:
    """
    Calculate the height of the frustum of the cone.

    Parameters
    ----------
    dia_lg_end : float
        Diameter of the large end
    dia_sm_end : float
        Diameter of the small end
    half_apex_angle : float
        Half apex angle

    Returns
    -------
    float

    Examples
    --------
    >>> height(228, 38, 60)
    164.54482671904336

    """
    annular_distance = abs((dia_lg_end - dia_sm_end) / 2)
    return annular_distance / math.tan(math.radians(half_apex_angle))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
