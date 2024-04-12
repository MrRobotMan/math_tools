import math


def distance(
    height_point_1: float,
    angle_point_1: float,
    height_point_2: float,
    angle_point_2: float,
    cone_large_end_diameter: float,
    cone_half_angle: float,
) -> float:
    """Find the shortest path between two points on a cone

    example:
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
    """Calculate the cone half-angle

    example:
        >>> angle(30, 20, 8.66)
        30.000727780827372
    """
    delta = (dia_lg_end - dia_sm_end) / 2
    return math.degrees(math.atan(delta / length))


def radius_at_location(
    dia_lg_end: float, apex_angle: float, location_from_lg_end: float
) -> float:
    """Calculate the radius at a location on a cone.

    example:
        >>> radius_at_location(174, 60, 58)
        53.51368438700171
    """
    return dia_lg_end / 2 - (
        math.tan(math.radians(apex_angle / 2)) * location_from_lg_end
    )


def height(dia_lg_end: float, dia_sm_end: float, apex_angle: float) -> float:
    """Calculate the height of the frustum of the cone.

    example:
        >>> height(228, 38, 60)
        164.54482671904336
    """
    half_angle = math.radians(apex_angle / 2)
    annular_distance = abs((dia_lg_end - dia_sm_end) / 2)
    return annular_distance / math.tan(half_angle)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
