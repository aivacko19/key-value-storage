import commands


def print_welcome_screen():
    print(
        "\nRedis-like storage [Version 1.0.0]\n" \
        "Copyright (c) 2022 Aleksa Ivačko. All rights reserved.\n"
    )


if __name__ == '__main__':
    print_welcome_screen()

    command_pool = dict()
    command_pool['GET'] = commands.GetCommand()
    command_pool['SET'] = commands.SetCommand()
    command_pool['UNSET'] = commands.UnsetCommand()
    command_pool['NUMEQUALTO'] = commands.NumEqualToCommand()
    command_pool['END'] = commands.EndCommand()
    command_pool['BEGIN'] = commands.BeginCommand()
    command_pool['COMMIT'] = commands.CommitCommand()
    command_pool['ROLLBACK'] = commands.RollbackCommand()

    while True:
        # We suppose that distance between the arguments will be one space
        argv = input('>>>').split(' ')
        name, *argv = argv
        try:
            command = command_pool[name]
            command.start(*argv)
        except KeyError:
            print('error')
