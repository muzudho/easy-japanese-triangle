import time


class Stopwatch:
    _start_time = None
    _end_time = None

    def start(self):
        self._start_time = time.time()

    def end(self):
        self._end_time = time.time()

    @property
    def lapsed(self):
        return self._end_time - self._start_time

    def print(self):
        sec = self.lapsed

        mins = sec // 60
        sec = sec % 60
        hours = mins // 60
        mins = mins % 60
        print(f"Time Lapsed = {int(hours)}:{int(mins)}:{sec}")
