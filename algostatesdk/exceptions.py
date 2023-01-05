class NoLocalStatesFound(Exception):
    def __init__(self, app_id, addr):
        Exception.__init__(
            self,
            "No local states found in app: {} for address: {}".format(app_id, addr),
        )


class NoLocalStateMatch(Exception):
    def __init__(self, key, app_id, addr):
        Exception.__init__(
            self,
            "No local state match with key: {} in app: {} for address: {}".format(key, app_id, addr),
        )
