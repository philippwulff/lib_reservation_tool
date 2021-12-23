class LocatorError(Exception):
    def __int__(self, msg, error=None):
        super(LocatorError, self).__init__(msg)

        self.error = error


