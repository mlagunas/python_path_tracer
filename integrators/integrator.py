class Integrator():
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError

    def _get_color(self):
        raise NotImplementedError

    def prepare_call(self, name, args):  # creates a 'remote call' package for each argument
        for arg in args:
            yield [self.__class__.__name__, self.__dict__, name, arg]


