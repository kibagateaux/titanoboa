import contextlib
import sys

from boa.debugger import BoaDebug
from boa.environment import Env, enable_pyevm_verbose_logging, patch_opcode
from boa.interpret import BoaError, load, load_abi, load_partial, loads, loads_abi, loads_partial
from boa.precompile import precompile
from boa.test.strategies import fuzz
from boa.vyper.contract import check_boa_error_matches

# turn off tracebacks if we are in repl
# https://stackoverflow.com/a/64523765
if hasattr(sys, "ps1"):
    pass
    # sys.tracebacklimit = 0

env = Env.get_singleton()


@contextlib.contextmanager
def swap_env(new_env):
    old_env = env
    try:
        set_env(new_env)
        yield
    finally:
        set_env(old_env)


def set_env(new_env):
    global env
    env = new_env

    Env._singleton = new_env


def reset_env():
    set_env(Env())


def _breakpoint(computation):
    BoaDebug(computation).start()


patch_opcode(0xA6, _breakpoint)


@contextlib.contextmanager
def reverts(*args, **kwargs):
    try:
        yield
        raise ValueError("Did not revert")
    except BoaError as b:
        if args or kwargs:
            check_boa_error_matches(b, *args, **kwargs)


def eval(code):
    return loads("").eval(code)
