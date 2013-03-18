class RegExAnalyzer:
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def status(self):
        pass

    @property
    def state(self):
        """Returns the state of the analyzer, e.g.:

        * RUNNING
        * FINISHED_SUCCESS
        * FINISHED_ERROR
        """
        pass

    def __del__(self):
        self.stop()
