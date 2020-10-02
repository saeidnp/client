from types import ModuleType


class Dummy():
    def __init__(self, *args, **kwargs):
        binary_ops = ["add", "sub", "mul", "floordiv", "mod", "pow", "lshift", "rshift", "and", "xor", "or", "truediv"]
        for op in binary_ops:
            setattr(self, "__{}__".format(op), lambda *_: Dummy())
        for i in range(len(binary_ops) - 1):
            setattr(self, "__i{}__".format(binary_ops[i]), lambda *_: None)
        self.__idiv__ = lambda *_: None
        unary_ops = ["neg", "pos", "abs", "invert", "complex", "int", "long", "float", "oct", "hex"]
        for op in unary_ops:
            setattr(self, "__{}__".format(op), lambda: Dummy())
        compare_ops = ["lt", "le", "eq", "ne", "gt", "ge"]
        for op in compare_ops:
            setattr(self, "__{}__".format(op), lambda _: True)
        self.___dict = {}

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            dummy = Dummy()
            setattr(self, attr, dummy)
            return dummy

    def __getitem__(self, key):
        if key in self.__dict:
            return self.___dict[key]
        dummy = Dummy()
        self.___dict[key] = dummy
        return dummy

    def __setitem__(self, key, value):
        self.___dict[key] = value

    def __call__(self, *args, **kwargs):
        return Dummy()

    def __len__(self):
        return 1

    def __str__(self):
        return ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is None


class DummyModule(Dummy, ModuleType):
    pass
