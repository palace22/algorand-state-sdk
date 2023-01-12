class WrongAttributeCustomType(Exception):
    def __init__(self, attr_type):
        Exception.__init__(
            self,
            "Wrong attribute type: {attr_type}".format(attr_type),
        )


class NoBoxFound(Exception):
    def __init__(self, app_id, key):
        Exception.__init__(
            self,
            "No box found in app: {} with key: {}".format(app_id, key),
        )


class NoLocalStatesFound(Exception):
    def __init__(self, app_id, addr):
        Exception.__init__(
            self,
            "No local states found in app: {} for address: {}".format(app_id, addr),
        )


class NoGlobalStateMatch(Exception):
    def __init__(self, app_id, key):
        Exception.__init__(
            self,
            "No global state match in app: {} with key: {}".format(app_id, key),
        )


class NoLocalStateMatch(Exception):
    def __init__(self, app_id, key, addr):
        Exception.__init__(
            self,
            "No local state match in app: {} for address: {} with key: {}".format(app_id, addr, key),
        )
