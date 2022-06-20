import msvcrt

num = 0
done = False
while not done:

    if msvcrt.kbhit():
        key = ord(msvcrt.getch())
        
        if key == 27: #ESC
                done = True
        elif key == 13: #Enter
            print("enter")
        elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
            key = ord(msvcrt.getch())
            if key == 80: #Down arrow
                print("down")
            elif key == 72: #Up arrow
                print("up")
        else:
            print(chr(key))
