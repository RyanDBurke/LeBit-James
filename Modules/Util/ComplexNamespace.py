from types import SimpleNamespace


class ComplexNamespace(SimpleNamespace):

    @staticmethod
    def map_entry(entry):
        if isinstance(entry, dict):
            return ComplexNamespace(**entry)

        return entry

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        i = kwargs.items()
        for key, val in kwargs.items():
            if type(val) == dict:
                setattr(self, key, ComplexNamespace(**val))
            elif type(val) == list:
                setattr(self, key, list(map(self.map_entry, val)))
