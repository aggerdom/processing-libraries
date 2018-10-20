import processing_utilities


def test_pattern_match():
    pattern_match = processing_utilities.multidispatch.pattern_match
    assert pattern_match((int, (str, str)), (3, ('a', 'a'))), "Valid match"
    assert not pattern_match((int, (str, str)), (3, ('a', 3))), "Invalid Match"
    assert pattern_match((int, ("ANY", str)), (3, ('a', 'a'))), "ANY matches"
    assert not pattern_match((int,), (3, 4)), "Different length signatures"
    assert not pattern_match((int, int), (3,)), "Different length signatures"


def test_pmultidispatch():
    last_called = []

    @processing_utilities.multidispatch.pmultidispatch
    def concat(a, b):
        last_called.append("default")
        a = a
        b = str(b)
        return a + b

    @concat.register(str, int)
    @concat.register(int, str)
    def _(a, b):
        last_called.append("stacked")
        a = str(a)
        b = str(b)
        return a + b

    @concat.register(int, int)
    def _(a, b):
        last_called.append("last")
        a = str(a)
        b = str(b)
        return a + b

    assert concat('1', '2') == '12'
    assert last_called[-1] == 'default'

    assert concat('1', 3) == '13'
    assert last_called[-1] == 'stacked'

    assert concat(1, 3) == '13'
    assert last_called[-1] == 'last'

    assert concat(1, '3') == '13'
    assert last_called[-1] == 'stacked'


def test_pmultidispatch_vector():
    class Vector(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    from math import sqrt
    @processing_utilities.multidispatch.pmultidispatch
    def distance(x1, y1, x2, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @distance.register(Vector, Vector)
    def _(p, q):
        return distance(p.x, p.y, q.x, q.y)

    assert distance(1, 2, 3, 4) == distance(Vector(1, 2), Vector(3, 4))


def test_multidispatch():
    last_called = []

    @processing_utilities.multidispatch.multidispatch
    def concat(a, b):
        last_called.append("default")
        a = a
        b = str(b)
        return a + b

    @concat.register(str, int)
    @concat.register(int, str)
    def _(a, b):
        last_called.append("stacked")
        a = str(a)
        b = str(b)
        return a + b

    @concat.register(int, int)
    def _(a, b):
        last_called.append("last")
        a = str(a)
        b = str(b)
        return a + b

    assert concat('1', '2') == '12'
    assert last_called[-1] == 'default'

    assert concat('1', 3) == '13'
    assert last_called[-1] == 'stacked'

    assert concat(1, 3) == '13'
    assert last_called[-1] == 'last'

    assert concat(1, '3') == '13'
    assert last_called[-1] == 'stacked'


def test_multidispatch_vector():
    class Vector(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    from math import sqrt
    @processing_utilities.multidispatch.multidispatch
    def distance(x1, y1, x2, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @distance.register(Vector, Vector)
    def _(p, q):
        return distance(p.x, p.y, q.x, q.y)

    assert distance(1, 2, 3, 4) == distance(Vector(1, 2), Vector(3, 4))
