import itertools

import pytest
from hypothesis import given
from hypothesis.strategies import SearchStrategy

<<<<<<< HEAD
<<<<<<< HEAD
from boa.environment import Env
from boa.interpret import load
=======
>>>>>>> 581e92e (add initial event tests)
=======
from boa.environment import Env
from boa.interpret import load
>>>>>>> 6dc7f78 (simplify tests)
from boa.test import strategy
from boa.vyper.event import Event

BASE_TYPES = ["address", "bool", "bytes32", "decimal", "int", "string", "uint"]


@pytest.mark.parametrize("base1,base2", itertools.product(BASE_TYPES, BASE_TYPES))
def test_strategy(base1, base2):
    # ensure we can test on tuples
    # tuple generates strategies for underlying types
    assert isinstance(strategy(f"({base1},({base2},{base1}))"), SearchStrategy)
    assert isinstance(strategy(f"({base1})"), SearchStrategy)
    assert isinstance(strategy(f"({base2},{base2})"), SearchStrategy)
    assert isinstance(strategy(f"(({base1},{base2}))"), SearchStrategy)


<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 6dc7f78 (simplify tests)
@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_topics_saved_to_event(args):
    event = Event("0x0", "0x0", "", args, [], {})
    assert event.topics == args
<<<<<<< HEAD
    assert event.args == []
    print(Event)
    assert len(event.ordered_args()) == len(args)


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_saved_to_event(args):
    event = Event("0x0", "0x0", "", [], args, {})
    assert event.args == args
    assert event.topics == []
    assert len(event.ordered_args()) == len(args)


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_ordered_to_event_param_sequence(args):
    # separate indexed from non-indexed in Event state
    # to make sure they get merged properly
    topics = [args[1], args[2]]
    params = [args[0], args[3]]
    event_type = {
        "indexed": [False, True, True, False],
        # order param keys so ordered_args() matches actual params
        "arguments": {idx: value for idx, value in enumerate(args)},
    }

    event = Event("0x0", "0x0", event_type, topics, params)
    assert event.args == params
    assert event.topics == topics
    assert len(event.ordered_args()) == len(args)

    for idx, key, value in enumerate(event.ordered_args()):
        assert key == event_type.values[idx]
        assert value == args[idx]


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_map_values_match_ordered_args(args):
    event_type = {
        "indexed": [False, True, True, False],
        # order args so ordered_args() matches actual params
        "arguments": {idx: value for idx, value in enumerate(args)},
    }
    event = Event("0x0", "0x0", event_type, [], args)
    for idx, k in enumerate(event_type["arguments"].keys()):
        assert event.args_map[k] == args[idx]


def test_event_is_emitted():
    me = Env.generate_address()
    token = load("examples/ERC20.vy", "test", "TEST", 18, 0, sender=me)
    token.mint(me, 100, sender=me)
    mint_events = token.get_logs()
    assert len(mint_events) == 1
    assert mint_events[0].args == (100)
    assert mint_events[0].topics == ("0x0000000000000000000000000000000000000000", me)
    assert mint_events[0].args_map == {
        "sender": "0x0000000000000000000000000000000000000000",
        "receiver": me,
        "value": 100,
    }
    assert mint_events[0].ordered_args() == [
        ("sender", "0x0000000000000000000000000000000000000000"),
        ("receiver", me),
        ("value", 100),
    ]
=======
@pytest.mark.parametrize(
    "param1,param2,param3,param4",
    itertools.product(BASE_TYPES, BASE_TYPES, BASE_TYPES, BASE_TYPES),
)
def test_topics_saved_to_event(param1, param2, param3, param4):
    topics = [param1, param2, param3, param4]
    event = Event("0x0", "0x0", "", topics, [], {})
    assert event.topics == topics
=======
>>>>>>> 6dc7f78 (simplify tests)
    assert event.args == []
    print(Event)
    assert len(event.ordered_args()) == len(args)


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_saved_to_event(args):
    event = Event("0x0", "0x0", "", [], args, {})
    assert event.args == args
    assert event.topics == []
    assert len(event.ordered_args()) == len(args)


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_ordered_to_event_param_sequence(args):
    # separate indexed from non-indexed in Event state
    # to make sure they get merged properly
    topics = [args[1], args[2]]
    params = [args[0], args[3]]
    event_type = {
        "indexed": [False, True, True, False],
        # order param keys so ordered_args() matches actual params
        "arguments": {idx: value for idx, value in enumerate(args)},
    }

    event = Event("0x0", "0x0", event_type, topics, params)
    assert event.args == params
    assert event.topics == topics
    assert len(event.ordered_args()) == len(args)

    for idx, key, value in enumerate(event.ordered_args()):
        assert key == event_type.values[idx]
        assert value == args[idx]


@given(args=strategy("(bool,uint8,address,bytes32)"))
def test_args_map_values_match_ordered_args(args):
    event_type = {
        "indexed": [False, True, True, False],
        # order args so ordered_args() matches actual params
        "arguments": {idx: value for idx, value in enumerate(args)},
    }
    event = Event("0x0", "0x0", event_type, [], args)
    for idx, k in enumerate(event_type["arguments"].keys()):
        assert event.args_map[k] == args[idx]


def test_event_is_emitted():
    me = Env.generate_address()
    token = load("examples/ERC20.vy", "test", "TEST", 18, 0, sender=me)
    token.mint(me, 100, sender=me)
    mint_events = token.get_logs()
    assert len(mint_events) == 1
    assert mint_events[0].args == (100)
    assert mint_events[0].topics == ("0x0000000000000000000000000000000000000000", me)
    assert mint_events[0].args_map == {
        "sender": "0x0000000000000000000000000000000000000000",
        "receiver": me,
        "value": 100,
    }
<<<<<<< HEAD
    event = Event("0x0", "0x0", event_type, [], args, {})
    print("get event __repr__", event.__repr__())
    # expected_repr = f"event "
    # assert event.__repr__() ==


@given(value=strategy("(uint8,(bool,bytes4),decimal[3])"))
def test_event_is_emitted(value):
    assert len(value) == 3
    # mock erc20 transfer
    # erc20.get_logs
    # event[0].topics ===
    # event[0].args ===
    # event[0].ordered_args ===
>>>>>>> 581e92e (add initial event tests)
=======
    assert mint_events[0].ordered_args() == [
        ("sender", "0x0000000000000000000000000000000000000000"),
        ("receiver", me),
        ("value", 100),
    ]
>>>>>>> 6dc7f78 (simplify tests)
