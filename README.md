# Algorand State SDK

A python SDK to decode Algorand global, local and box states.

The goal is to have a ready-to-use library to decode the states on the Algorand blockchain, plus some useful methods to render the algod client responses as objects.

The decoding can be defined by a schema i.e. the `StateSchema`, in which to indicate the `key`, `type`, and the attributes that will be decoded from the state value ; The attributes (`attrs`) are defined by the `AttributeSchema` in which must be defined the `type`, `name`, `offset` and `size` of each.

### Example
#### Python
```python
from algostatesdk.models.states import StateSchema, AttributeSchema, StateType

state_custom = StateSchema(
    key='info', # global or local state key
    key_byte_length=None, # iif key is int 
    address=None, # iif it is a local state
    attrs=[
        AttributeSchema(AttributeType.STR, 8, 0, "name"),
        AttributeSchema(AttributeType.INT, 1, 8, "age"),
        AttributeSchema(AttributeType.ADDR, 32, 9, "algo_addr"),
        AttributeSchema(AttributeType.BYTES, 87, 41, "extra"),
    ],
    type=StateType.GLOBAL,
)
```
#### JSON
```json
{
    "key": "info",
    "key_byte_length": "",
    "address": "",
    "attrs": [
        {"type": "str", "size": 8, "offset": 0, "name":"name"},
        {"type": "int", "size": 1, "offset": 8, "name":"age"},
        {"type": "addr", "size": 32, "offset": 9, "name":"algo_addr"},
        {"type": "bytes", "size": 87, "offset": 41, "name":"extra"},
        ],
    "type":"global"
}
```

#### Decoding

```python
algod_client = ##
app_id = ###

algo_state_client = AlgoStateClient(algod_client)

state_custom = from_dict(StateSchema, state_json)

decoded_state = algo_state_client.get_state_custom(app_id, state_custom)
```