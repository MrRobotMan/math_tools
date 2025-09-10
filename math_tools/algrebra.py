def gcd(a: int, b: int) -> int:
    """
    Calculate the greatest common divisor of two integers.

    Parameters
    ----------
    a: int
        First number
    b: int
        Second number

    Returns
    -------
    int

    Examples
    --------
    >>> gcd(48, 18)
    6
    >>> gcd(48, -18)
    6
    >>> gcd(17, 19)
    1
    >>> gcd(0, -7)
    7

    """
    a = abs(a)
    b = abs(b)
    if b > a:
        (a, b) = (b, a)
    if b == 0:
        return a
    return gcd(b, a % b)


def lcm(a: int, b: int) -> int:
    """
    Calculate the least common multiple of two integers.

    Parameters
    ----------
    a: int
        First number
    b: int
        Second number

    Returns
    -------
    int


    Examples
    --------
    >>> lcm(48, 18)
    144
    >>> lcm(3, 5)
    15

    """
    return a * b // gcd(a, b)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
