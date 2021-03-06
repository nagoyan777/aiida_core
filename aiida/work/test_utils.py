

from aiida.work.process import Process


class DummyProcess(Process):
    """
    A Process that does nothing when it runs.
    """
    @classmethod
    def define(cls, spec):
        super(DummyProcess, cls).define(spec)
        spec.dynamic_input()
        spec.dynamic_output()

    def _run(self, **kwargs):
        pass


class BadOutput(Process):
    """
    A Process that emits an output that isn't part of the spec raising an
    exception.
    """
    @classmethod
    def define(cls, spec):
        super(BadOutput, cls).define(spec)
        spec.dynamic_output()

    def _run(self):
        self.out("bad_output", 5)


class ExceptionProcess(Process):
    def _run(self):
        raise RuntimeError("CRASH")