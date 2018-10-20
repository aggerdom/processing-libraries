import itertools


# From itertools recipes: https://docs.python.org/2/library/itertools.html
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def divrange(start, stop, num_segments, inclusive=False):
    """
    Divide a distance into a given number of even segments.
    If inclusive is false, only points where divisions occur are returned.
    If inclusive is true, end points (start and stop) will divided as well.

    :param start: 1D point for start of range
    :param stop: 1D point for end of range
    :param num_segments: Number of segments to split range into
    :param inclusive: Whether to include endpoints
    :return: Generator for coordinates
    """
    stride = (stop - start) / float(num_segments)
    if inclusive:
        yield start

    for i in range(1, num_segments):
        yield start + (stride * i)

    if inclusive:
        yield stop


def interpolate_coords(start, stop, num_segments, inclusive=False):
    """
    Interpolate between two coordinates of arbitrary dimension.

    :param start: Coordinate for starting point
    :param stop: Coordinate for ending point
    :param num_segments: Number of segments to divide space into
    :param inclusive: Whether to include endpoints in results
    :return: Generator for coordinates
    """
    steppers = [
        divrange(p_i, q_i, num_segments, inclusive=inclusive)
        for p_i, q_i in zip(start, stop)
    ]
    while True:
        try:
            yield [next(component) for component in steppers]
        except StopIteration:
            break


def flatten(iterable):
    return itertools.chain(*iterable)
