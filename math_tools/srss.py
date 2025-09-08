import math


def srss(*args: float) -> float:
    """
    Calculate the square-root-sum-of-squares of floats.

    Returns:
        float

    Example:
        >>> srss(*range(5))
        5.477225575051661
        >>> srss(8.3, 7.25)
        11.020548988140291

    """
    return math.sqrt(sum(num**2 for num in args))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
