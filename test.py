# from pynput import keyboard
# import time
# message = ''


# def on_press(key):
#     global message
#     try:
#    	    message += key.char
#     except AttributeError:
#     	print('special key {0} pressed'.format(key))

# def on_release(key):
#     print('{0} released'.format(key))

#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# time.sleep(5)

# ans = int(input("end? (1 = yes, 0 = no): "))

# if ans == 1:
#     print(message)

# -*- coding: utf-8 -*-
from simple_term_menu import TerminalMenu

def main():
    options = ["entry 1", "entry 2", "entry 3"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()