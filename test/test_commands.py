from ngoto.core.ngoto import Ngoto


def test_dup_action():
    """
        Check there are no duplicate command actions eg. 'b'
    """
    ngoto = Ngoto()
    # get list of all actions
    commands = []
    for command in ngoto.commands:
        commands.append(command.name)
        for cmd in command.aliases:
            commands.append(cmd)
    # check for duplicates
    if len(commands) == len(set(commands)):
        assert True
    else:
        duplicates = []
        for command in commands:
            if commands.count(command) > 1:
                duplicates.append(command)
        print('Duplicate commands found: ' + str(duplicates))
        assert False


def test_open_folder_command():
    """
        Check the open folder command works
    """
    ngoto = Ngoto()
    root_pos = ngoto.curr_pos.get_name()
    print(ngoto.curr_pos.num_children)
    ngoto.run_command('1', ['1'])  # open folder
    assert ngoto.curr_pos.get_name() != root_pos


def test_back_command_1():
    """
        Check the back command works
    """
    ngoto = Ngoto()
    root_pos = ngoto.curr_pos.get_name()
    ngoto.run_command('1', ['1'])  # open folder
    ngoto.run_command('b')
    assert ngoto.curr_pos.get_name() == root_pos


def test_back_command_2():
    """
        Check the back command works
    """
    ngoto = Ngoto()
    ngoto.run_command('1', ['1'])  # open folder
    assert ngoto.run_command('b')


def test_clear_command():
    """
        Check the clear command works
    """
    ngoto = Ngoto()
    assert ngoto.run_command('clear')


def test_log_command():
    """
        Check the log command works
    """
    ngoto = Ngoto()
    assert ngoto.run_command('logs')


def test_options_command():
    """
        Check the options command works
    """
    ngoto = Ngoto()
    assert ngoto.run_command('options')
