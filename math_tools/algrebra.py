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
    if min(a, b) == 0:
        return max(a, b)
    d = 0
    while a % 2 == 0 and b % 2 == 0:
        d += 1
        a >>= 1
        b >>= 1
    a = make_odd(a)
    b = make_odd(b)
    while a != b:
        if a > b:
            a -= b
            a = make_odd(a)
        else:
            b -= a
            b = make_odd(b)
    return (1 << d) * a


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


def make_odd(num: int) -> int:
    """
    Divide by two until a number is odd.

    Parameters
    ----------
    num: int
        Number to make even

    Returns
    -------
    int

    Raises
    ------
    ZeroDivisionError
        If num is 0 can't make odd.

    Examples
    --------
    >>> make_odd(136)
    17
    >>> make_odd(16)
    1

    """
    if num == 0:
        raise ZeroDivisionError

    while num % 2 == 0:
        num >>= 1
    return num


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
