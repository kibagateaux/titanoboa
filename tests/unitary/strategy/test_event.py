from boa.environment import Env
from boa.interpret import load
from boa.vyper.event import Event

param_types = "(bool,uint8,address,bytes32)"
event_type = {
    "indexed": [False, True, True, False],
    # order param keys so ordered_args() matches actual params
    "arguments": {idx: value for idx, value in enumerate(param_types)},
}


def test_topics_saved_to_event():
    event_type["indexed"] = [True, True, True, True]
    event = Event("0x0", "0x0", event_type, param_types, [])
    assert event.topics == param_types
    assert event.args == []
    print(Event)
    assert len(event.ordered_args()) == len(param_types)


def test_args_saved_to_event():
    event_type["indexed"] = [False, False, False, False]
    event = Event("0x0", "0x0", event_type, [], param_types)
    assert event.args == param_types
    assert event.topics == []
    assert len(event.ordered_args()) == len(param_types)


def test_args_ordered_to_event_param_sequence():
    param_types = "(bool,uint8,address,bytes32)"
    # separate indexed from non-indexed in Event state
    # to make sure they get merged properly
    topics = [param_types[1], param_types[2]]
    params = [param_types[0], param_types[3]]

    event = Event("0x0", "0x0", event_type, topics, params)
    assert event.args == params
    assert event.topics == topics
    assert len(event.ordered_args()) == len(param_types)

    for idx, key, value in enumerate(event.ordered_args()):
        assert key == event_type.values[idx]
        assert value == param_types[idx]


def test_event_args_map_values_match_ordered_args():
    param_types = "(bool,uint8,address,bytes32)"
    event_type = {
        "indexed": [False, True, True, False],
        # order_args so ordered_args() matches actual params
        "arguments": {idx: value for idx, value in enumerate(param_types)},
    }
    event = Event("0x0", "0x0", event_type, [], param_types)
    for idx, k in enumerate(event_type["arguments"].keys()):
        assert event.args_map[k] == param_types[idx]


def test_event_is_emitted():
    me = Env().generate_address()
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
