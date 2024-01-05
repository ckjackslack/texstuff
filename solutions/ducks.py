import random
from abc import ABC, abstractmethod
from enum import Enum, auto
from pprint import pp

random.seed(0xDEADBEEF)


class Power(Enum):
    SPEED_BOOTS    = auto()
    STRONG_WILL    = auto()
    MONEY_MAKER    = auto()
    SUPER_STRENGTH = auto()


class QuackingCreature(ABC):
    @abstractmethod
    def get_priority():
        pass
    def __repr__(self):
        s = self.__class__.__name__
        if hasattr(self, "name"):
            s += f":{self.name}"
        return s


class WeaklingDuck(QuackingCreature):
    def get_priority(self):
        return 1


class Duck(QuackingCreature):
    def __init__(self, name):
        self.name = name
    def get_priority(self):
        return 2


class SuperDuck(Duck):
    def __init__(self, name, power):
        super().__init__(name)
        if isinstance(power, Power):
            self.power = power
        else:
            self.power = random.choice(list(Power))
    def get_priority(self):
        return 4 if self.power == Power.SPEED_BOOTS else 3


def main():
    d1 = WeaklingDuck()
    d2 = Duck("Huey")
    d3 = SuperDuck("Scrooge McDuck", Power.MONEY_MAKER)
    d4 = SuperDuck("Launchpad McQuack", Power.SPEED_BOOTS)
    ducks_in_a_row = [d2, d4, d3, d1]
    pp(ducks_in_a_row)
    pp(sorted(ducks_in_a_row, key=lambda d: -d.get_priority()))


if __name__ == '__main__':
    main()
