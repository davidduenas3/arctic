from enum import Enum, Flag

class Bound(Flag):
    CLOSED = 1
    OPEN = 2

class Intervals(Enum):
    (OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED) = range(1101, 1105)

    @classmethod
    def _missing_(cls, value):
        try:
            return dict(zip(('right', 'left', 'neither', 'both'), cls))[value]
        except KeyError:
            pass
        return super()._missing_(value)

    @property
    def bounds(self):
        return [*map(Bound.__getitem__, str.split(self.name, '_'))]

    @classmethod
    def from_bounds(cls, bounds):
        """
            start,end: tipo Bound
            returns: Intervals
        """

        return ({i for i in cls if i.bounds[0] is Bound(bounds[0])} &
                {i for i in cls if i.bounds[1] is Bound(bounds[1])}).pop()

    @classmethod
    def from_openbounds(cls, start, end):
        """
            start,end: booleanos
            returns: Intervals
        """

        return cls.from_bounds((Bound.OPEN if start else Bound.CLOSED,
                                Bound.OPEN if end else Bound.CLOSED))

    @classmethod
    def from_closedbounds(cls, start, end):
        """
            start,end: booleanos
            returns: Intervals
        """
        return cls.from_bounds((Bound.CLOSED if start else Bound.OPEN,
                                Bound.CLOSED if end else Bound.OPEN))

(OPEN_CLOSED, CLOSED_OPEN, OPEN_OPEN, CLOSED_CLOSED) = INTERVALS = Intervals.__members__.values()



class GeneralSlice(object):
    """General slice object, supporting open/closed ranges:

    =====  ====  ============================  ===============================
    start  end  interval                      Meaning
    -----  ----  ----------------------------  -------------------------------
    None   None                                any item
    a      None  CLOSED_CLOSED or CLOSED_OPEN  item >= a
    a      None  OPEN_CLOSED or OPEN_OPEN      item > a
    None   b     CLOSED_CLOSED or OPEN_CLOSED  item <= b
    None   b     CLOSED_OPEN or OPEN_OPEN      item < b
    a      b     CLOSED_CLOSED                 item >= a and item <= b
    a      b     OPEN_CLOSED                   item > a and item <= b
    a      b     CLOSED_OPEN                   item >= a and item < b
    a      b     OPEN_OPEN                     item > a and item < b
    =====  ====  ============================  ===============================
    """

    def __init__(self, start, end, step=None, interval=CLOSED_CLOSED):
        self.start = start
        self.end = end
        self.step = step
        bounds = Intervals(interval).bounds
        if start is None:
            bounds[0] = Bound.CLOSED
        if end is None:
            bounds[1] = Bound.CLOSED
        self.interval = Intervals.from_bounds(bounds)

    @property
    def startopen(self):
        """True if the start of the range is open (item > start),
        False if the start of the range is closed (item >= start)."""
        return self.interval in (OPEN_CLOSED, OPEN_OPEN)

    @property
    def endopen(self):
        """True if the end of the range is open (item < end),
        False if the end of the range is closed (item <= end)."""
        return self.interval in (CLOSED_OPEN, OPEN_OPEN)
    