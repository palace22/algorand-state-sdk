# Algorand State SDK

A python SDK to decode Algorand global and local states.

### Example
#### Python
```python
from algostatesdk.models.states import StateCustom, AttributeCustom, StateCustomType

state_custom = StateCustom(
    key='info', # global or local state key
    key_byte_length=None, # iif key is int 
    address=None, # iif it is a local state
    attrs=[
        AttributeCustom("str", 8, 0, "name"),
        AttributeCustom("int", 1, 8, "age"),
        AttributeCustom("addr", 32, 9, "algo_addr"),
        AttributeCustom("bytes", 87, 41, "extra"),
    ],
    type=StateCustomType.BOX,
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
algod_token = ###
algod_address = ###
app_id = ###

algo_state_client = AlgoStateClient(algod_token, algod_address)

# state_custom = from_dict(StateCustom, state_json)

decoded_state = algo_state_client.app.get_state_custom(app_id, state_custom)
```