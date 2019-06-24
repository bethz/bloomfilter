from collections import namedtuple

Task = namedtuple('task','owner')
Task.__new__.__defaults__=(None)