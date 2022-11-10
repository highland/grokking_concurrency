"""The best known way to see the future is to wait"""


class Future:
    def __init__(self, loop) -> None:
        self.loop = loop
        self.done = False

    def set_coroutine(self, co):
        self.co = co

    def set_result(self, result):
        self.done = True
        self.result = result

        if self.co:
            self.loop.add_coroutine(self.co)

    def __await__(self):  # This 'Magic Method' is what makes Future a future
        if not self.done:
            yield self
        return self.result
    