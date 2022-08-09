import cmd
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
    
from ngoto.core.clt import CLT


def test_command_names():
    """Test there are no conflicting command names"""
    cmd_names: list = [cmd for cmd_list in [cmd.get_actions() for cmd in CLT().commands] for cmd in cmd_list]
    assert len(cmd_names) == len(set(cmd_names))
    return len(cmd_names) == len(set(cmd_names))
