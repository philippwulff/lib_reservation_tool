class WebpageLocatorError(Exception):
    def __int__(self, msg, error=None):
        """Exception to be thrown, when a web page element is not found due to a change in the structure of the website.

        Parameters
        ----------
        msg : str
            The error message to be passed along to the base exception class.
        error : subclass of Exception
            The original exception.
        Returns
        -------
        None
        """
        super(WebpageLocatorError, self).__init__(msg)

        self.error = error


