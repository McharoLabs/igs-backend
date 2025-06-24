from enum import Enum

class ACCESS_ROAD_TYPE(Enum):
    PAVED = 'Barabara ya lami'
    GRAVEL = 'Barabara ya kokoto'
    DIRT = 'Barabara ya udongo'
    NONE = 'Hakuna barabara'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.PAVED.name
