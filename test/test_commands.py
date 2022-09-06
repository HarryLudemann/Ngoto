

def test_command_names():
    """Test there are no conflicting command names"""
    from ngoto.core.clt import CLT
    ngotoCLT = CLT()
    assert len(ngotoCLT.commands) > 0
