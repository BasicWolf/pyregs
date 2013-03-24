import re
import threading

IDLE = 0
RUNNING = 1
FINISHED_SUCCESS = 2
FINISHED_ERROR = 3

class RegExAnalyzer(threading.Thread):
    def __init__(self, pattern='', text='', flags=0):
        self._lock = threading.RLock()
        self._stop_flag_lock = threading.Lock()
        self._status = ''
        self._state = IDLE
        self._matches = []
        self._re_groups_count = 0
        self._re_groupindex = {}
        self._stop_flag = False

        self.pattern = pattern
        self.text = text
        self.flags = flags
        threading.Thread.__init__(self)

    def run(self, *args, **kwargs):
        self._set_state(RUNNING, 'Compiling...')

        try:
            reo = re.compile(self.pattern, self.flags)
        except Exception:
            self._set_state(FINISHED_ERROR,
                            'Error in regular expression pattern')
            return

        self._set_status('Analyzing (0%)')

        text_len = len(self.text)
        for mo in reo.finditer(self.text):
            with self._lock:
                self._matches.append(mo)
                self._set_status('Analyzing ({:.1%})'.format(mo.start() / text_len))
            # check whether we should continue at all
            with self._stop_flag_lock:
                if self._stop_flag == True:
                    return

        mcount = len(self._matches)
        self._re_groups_count = reo.groups
        self._re_groupindex = reo.groupindex


        self._set_state(FINISHED_SUCCESS,
                        'Analysis complete, {} {} found.'
                        .format(mcount, ['match', 'matches'][mcount != 1]))

    def stop(self):
        with self._stop_flag_lock:
            self._stop_flag = True

    def _set_state(self, state, status=None):
        with self._lock:
            self._state = state
            if status is not None:
                self._status = status

    def _set_status(self, status):
        with self._lock:
            self._status = status

    def _set_matches(self, matches):
        with self._lock:
            self._matches = matches

    @property
    def status(self):
        """Analyzer status string."""
        with self._lock:
            return self._status

    @property
    def state(self):
        """Returns the state of the analyzer, e.g.:

        * RUNNING
        * FINISHED_SUCCESS
        * FINISHED_ERROR
        """
        with self._lock:
            return self._state

    @property
    def matches(self):
        with self._lock:
            return self._matches

    @property
    def re_groups_count(self):
        with self._lock:
            return self._re_groups_count

    @property
    def re_groupindex(self):
        with self._lock:
            return self._re_groupindex

    def __del__(self):
        self.stop()
