import importlib
import unittest

class BoundaryCase(unittest.TestCase):
    def module(self, name):
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError as exc:
            self.fail(f'Required production boundary absent: {exc.name}')
