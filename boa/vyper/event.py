from dataclasses import dataclass
<<<<<<< HEAD
from typing import Any, Dict, List, Tuple

from vyper.utils import cached_property
<<<<<<< HEAD
=======
from typing import Any, List, Dict

>>>>>>> 7fe0723 (add key-value pair of event variable name to data emitted to all boa.Event objects)
=======
>>>>>>> 581e92e (add initial event tests)


@dataclass
class Event:
    log_id: int  # internal py-evm log id, for ordering purposes
    address: str  # checksum address
    event_type: Any  # vyper.semantics.types.user.Event
    event_name: str # human readable output
    topics: List[Any]  # list of decoded topics
    args: List[Any]  # list of decoded args
    args_map: Dict[str, Any]  # Mapping of decoded args

    def __repr__(self):
        args = ", ".join(f"{k}={v}" for k, v in self.ordered_args())
        return f"{self.event_type.name}({args})"

    @cached_property
    def args_map(self) -> Dict[str, str | int]:
        return dict(self.ordered_args())

    def ordered_args(self) -> List[Tuple[str, str | int]]:
        t_i = 0
        a_i = 0
        b = []
        # align the evm topic + args lists with the way they appear in the source
        # ex. Transfer(indexed address, address, indexed address)
        for is_topic, k in zip(
            self.event_type.indexed, self.event_type.arguments.keys()
        ):
            if is_topic:
                b.append((k, self.topics[t_i]))
                t_i += 1
            else:
                b.append((k, self.args[a_i]))
                a_i += 1

        return b


class RawEvent:
    event_data: Any
