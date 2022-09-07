from ngoto.core.clt import CLT


def test_dup_action():
    """
        Check there are no duplicate command actions eg. 'b'
    """
    ngotoCLT = CLT()
    # get list of all actions
    commands = []
    for command in ngotoCLT.commands:
        commands += command.get_actions()
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
    ngotoCLT = CLT()
    root_pos = ngotoCLT.curr_pos.get_name()
    print(ngotoCLT.curr_pos.num_children)
    ngotoCLT.run_command('1', ['1'])  # open folder
    assert ngotoCLT.curr_pos.get_name() != root_pos


def test_back_command():
    """
        Check the back command works
    """
    ngotoCLT = CLT()
    root_pos = ngotoCLT.curr_pos.get_name()
    ngotoCLT.run_command('1', ['1'])  # open folder
    ngotoCLT.run_command('b')
    assert ngotoCLT.curr_pos.get_name() == root_pos
