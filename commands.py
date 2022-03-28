import inspect

from storage import Storage


class Command:

    def __init__(self):
        self.storage = Storage.get_instance()
    
    def start(self, *argv):
        arg_spec = inspect.getfullargspec(self.run)
        required_args = arg_spec.args[1:]
        if len(argv) < len(required_args):
            formatted_args = [f'<{arg}>' for arg in required_args]
            print(f"requires {' '.join(formatted_args)}")
            return
        
        self.run(*argv)

    def run(self, *argv):
        raise NotImplementedError


class GetCommand(Command):

    def run(self, key, *argv):
        if key in self.storage:
            print(self.storage[key])
        else:
            print('NULL')


class SetCommand(Command):

    def run(self, key, value, *argv):
        self.storage[key] = value


class UnsetCommand(Command):

    def run(self, key, *argv):
        del self.storage[key]


class NumEqualToCommand(Command):

    def run(self, value, *argv):
        num = self.storage.num_equal_to(value)
        print(num)


class EndCommand(Command):

    def run(self, *argv):
        exit(0)


class BeginCommand(Command):
    
    def run(self, *argv):
        self.storage.begin()

class CommitCommand(Command):

    def run(self, *argv):
        if not self.storage.has_transaction():
            print('NO TRANSACTION')
        else:
            self.storage.commit()

class RollbackCommand(Command):

    def run(self, *argv):
        if not self.storage.has_transaction():
            print('NO TRANSACTION')
        else:
            self.storage.rollback()
