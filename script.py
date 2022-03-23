import commands
from storage import HashTableStorage


def print_welcome_screen():
    print(
        "\nRedis-like storage [Version 1.0.0]\n" \
        "Copyright (c) 2022 Aleksa Ivačko. All rights reserved.\n"
    )


if __name__ == '__main__':
    print_welcome_screen()

    storage = HashTableStorage()
    command_pool = dict()
    command_pool['GET'] = commands.GetCommand(storage)
    command_pool['SET'] = commands.SetCommand(storage)
    command_pool['UNSET'] = commands.UnsetCommand(storage)
    command_pool['NUMEQUALTO'] = commands.NumEqualToCommand(storage)
    command_pool['END'] = commands.EndCommand()

    while True:
        # We suppose that distance between the arguments will be one space
        argv = input('>>>').split(' ')
        name, *argv = argv
        try:
            command = command_pool[name]
            command.start(*argv)
        except IndexError:
            print('error')
