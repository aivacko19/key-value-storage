from collections import defaultdict


class AbstractStorage:

    def __contains__(self, key: str) -> bool:
        pass

    def __getitem__(self, key: str) -> str:
        pass

    def __setitem__(self, key: str, value: str) -> None:
        pass

    def __delitem__(self, key: str) -> None:
        pass

    def num_equal_to(self, value: str) -> int:
        pass


class HashTableStorage(AbstractStorage):

    def __init__(self) -> None:
        self._storage = dict()
        self._value_count = defaultdict(lambda: 0)

    def __contains__(self, key: str) -> bool:
        return key in self._storage

    def __getitem__(self, key: str) -> str:
        return self._storage[key]

    def __setitem__(self, key: str, value: str) -> None:
        if key in self._storage:
            old_value = self._storage[key]
            self._value_count[old_value] -= 1
        self._value_count[value] += 1
        self._storage[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self._storage:
            old_value = self._storage[key]
            self._value_count[old_value] -= 1
            self._storage.pop(key)

    def num_equal_to(self, value: str) -> int:
        return self._value_count[value]
