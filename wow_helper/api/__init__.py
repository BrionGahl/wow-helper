from enum import Enum


class Namespace(Enum):
    STATIC = 'static'
    DYNAMIC = 'dynamic'
    PROFILE = 'profile'


class Metrics(Enum):
    DPS = 'dps'
    HPS = 'hps'

