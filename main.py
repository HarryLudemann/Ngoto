# this script is to launch command line tool

if __name__ == '__main__':
    from ngoto.core.clt import CLT
    ngotoCLT = CLT()
    # ngotoCLT.main()
    print(ngotoCLT.curr_pos.num_children)
