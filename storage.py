from collections import defaultdict


class State:

    def __init__(self) -> None:
        self.table = dict()
        self.counters = defaultdict(lambda: 0)


class BaseManager:

    def __init__(self, state: State) -> None:
        self._state = state
        
    def has_key(self, key: str) -> bool:
        return key in self._state.table

    def get(self, key: str) -> str:
        return self._state.table[key]

    def set(self, key: str, value: str) -> None:
        # Decrement counter for existing value
        if key in self._state.table:
            old_value = self._state.table[key]
            self._state.counters[old_value] -= 1
        
        # Add key-value entry
        self._state.table[key] = value

        # Increment counter for new value
        self._state.counters[value] += 1

    def unset(self, key: str) -> None:
        # No change if key does not exist
        if key not in self._state.table:
            return 

        # Decrement counter for old value
        old_value = self._state.table[key]
        self._state.counters[old_value] -= 1

        # Remove key-value entry
        self._state.table.pop(key)

    def num_equal_to(self, value: str) -> int:
        return self._state.counters[value]

    def commit(self) -> bool:
        return False  # Not supported


class TransactionManager(BaseManager):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stage = State()
        self._unset_tracker = list()
    
    def has_key(self, key: str) -> bool:
        if key in self._unset_tracker:
            return False
        elif key in self._stage.table:
            return True
        return super().has_key(key)

    def get(self, key: str) -> str:
        if key in self._unset_tracker:
            return KeyError
        elif key in self._stage.table:
            return self._stage.table[key]
        return super().get(key)

    def set(self, key: str, value: str) -> None:
        # Decrement counter for old value
        if self.has_key(key):
            old_value = self.get(key)
            self._stage.counters[old_value] -= 1
        
        # Remove unset tracker
        if key in self._unset_tracker:
            self._unset_tracker.remove(key)

        # Add key-value entry in staging state
        self._stage.table[key] = value
        
        # Increment counter for new value
        self._stage.counters[value] += 1

    def unset(self, key: str) -> None:
        # No change if key does not exist
        if not self.has_key(key):
            return

        # Decrement counter for old value
        old_value = self.get(key)
        self._stage.counters[old_value] -= 1
        
        # Set unset tracker
        if super().has_key(key) and key not in self._unset_tracker:
            self._unset_tracker.append(key) 

        # Remove key-value entry from staging state
        if key in self._stage.table:
            del self._stage.table[key]

    def num_equal_to(self, value: str) -> int:
        # Get original counter
        count = super().num_equal_to(value)

        # Add (or subtract if it is negative) staging counter
        count += self._stage.counters[value]

        return count

    def commit(self) -> bool:
        # Add staging key-value entries
        for key, value in self._stage.table.items():
            super().set(key, value)

        # Remove key-value entries assinged for removal
        for key in self._unset_tracker:
            super().unset(key)

        # Reset stage
        self._stage = State()
        self._unset_tracker = list()

        return True


class Storage:
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def __init__(self) -> None:
        self.state = State()
        self.manager = BaseManager(self.state)
    
    def __contains__(self, key: str) -> bool:
        return self.manager.has_key(key)

    def __getitem__(self, key: str) -> str:
        return self.manager.get(key)

    def __setitem__(self, key: str, value: str) -> None:
        self.manager.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.manager.unset(key)

    def num_equal_to(self, value: str) -> int:
        return self.manager.num_equal_to(value)

    def has_transaction(self) -> bool:
        return isinstance(self.manager, TransactionManager)

    def begin(self) -> None:
        if self.has_transaction():
            return

        self.manager = TransactionManager(self.state)
    
    def rollback(self) -> None:
        self.manager = BaseManager(self.state)

    def commit(self) -> None:
        self.manager.commit()
        self.manager = BaseManager(self.state)
