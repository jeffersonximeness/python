import platform


def what_is_my_os():
    syst = platform.system()
    plt = platform.platform()

    if syst == 'Linux':
        print("Nice! You use Linux, see the stats below :D (I hope it's not Deepin...)\n")
        print(f'{plt}')

    # Not tested
    elif plt == 'Windows':
        print("Hm... I see you use Windows. No problem, but at least do a dualboot ;)\n")
        print(f'{plt}')
    
    # Not tested
    elif plt == 'Darwin':
        print("What a shame... It's not even worth the effort!\n")
    
    else:
            print("Unidentified system :O\n")

if __name__ == '__main__':
    what_is_my_os()
