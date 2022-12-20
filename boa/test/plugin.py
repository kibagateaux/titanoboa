import contextlib
from typing import Generator

import hypothesis
import pytest

import boa
from boa.profiling import print_call_profile
from boa.vm.gas_meters import ProfilingGasMeter

# monkey patch HypothesisHandle. this fixes underlying isolation for
# hypothesis.given() and also hypothesis stateful functionality.
_old_init = hypothesis.core.HypothesisHandle.__init__


@contextlib.contextmanager
def _toggle_profiling(yes: bool = False):
    if yes:
        with boa.env.gas_meter_class(ProfilingGasMeter):
            yield
    else:
        yield


def _HypothesisHandle__init__(self, *args, **kwargs):
    _old_init(self, *args, **kwargs)

    t = self.inner_test

    def f(*args, **kwargs):
        with boa.env.anchor():
            t(*args, **kwargs)

    self.inner_test = f


hypothesis.core.HypothesisHandle.__init__ = _HypothesisHandle__init__  # type: ignore


def pytest_configure(config):
    config.addinivalue_line("markers", "ignore_isolation")
    config.addinivalue_line("markers", "call_profile")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator:

    ignore_isolation = item.get_closest_marker("ignore_isolation") is not None
    profiling_flag = item.get_closest_marker("call_profile") is not None

    with _toggle_profiling(profiling_flag):
        if not ignore_isolation:
            with boa.env.anchor():
                yield
        else:
            yield


def pytest_sessionfinish(session, exitstatus):

    breakpoint()

    if boa.env._cached_call_profiles:
        print_call_profile(boa.env)
