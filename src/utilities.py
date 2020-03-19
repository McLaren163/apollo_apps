import src.config as CFG
import os


def get_filepath(folder, filename):
    return os.path.join(folder, filename)


class FilterByDict():
    def __init__(self, data):
        self._data = data
        self._results = []
        self._count = 0
        self._current_gen = None

    @property
    def count(self):
        return self._count

    def apply_filter(self, filter):
        self._count = 0
        self._results = []
        for elem in self._data:
            flag = True
            for key in filter:
                if key not in elem:
                    flag = False
                    break
                if filter[key] not in elem[key]:
                    flag = False
                    break
            if flag:
                self._count += 1
                self._results.append(elem)
        self._current_gen = self._gen_for_results(self._results)
        return self._count

    def get_next(self):
        if not self._current_gen:
            raise StopIteration
        return next(self._current_gen)

    def get_results(self):
        return self._gen_for_results(self._results)
    
    def _gen_for_results(self, results):
        for res in results:
            yield res
