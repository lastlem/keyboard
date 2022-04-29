from tkinter import *
from tkinter.ttk import *

with open('keyboard.txt') as file:
    keys_english = []
    keys_russian = []
    keyboards = [keys_english, keys_russian]
    keyboard = keys_english
    for line in file.readlines():
        if line == '\n':
            keyboard = keys_russian
            continue
        keyboard.append(line.strip().split('//'))

keyboard = keys_english
switch_lock = False
switch_keyboard = False


def return_state(event):
    return 'active' if event.type == '2' else 'normal'


def change_to_lock_keyboard(event) -> None:
    global switch_lock
    if event.type == '2':
        switch_lock = not switch_lock
        for index_array, button_array in enumerate(buttons):
            for index_button, button in enumerate(button_array):
                new_text, _, _, _= keyboard[index_array][index_button].split(', ')
                button['text'] = new_text.upper() if len(new_text) == 1 and switch_lock else new_text


def return_to_lock_after_shift(text_shift, text_normal, button):
    button['text'] = text_normal.upper() if len(text_shift) == 1 else text_normal


def change_to_shift_keyboard(event):
    for index_array, button_array in enumerate(buttons):
        for index_button, button in enumerate(button_array):
            text_normal, text_shift, _, _ = keyboard[index_array][index_button].split(', ')

            if switch_lock:
                button['text'] = text_shift.lower() if len(text_shift) < 2 and event.type == '2' else return_to_lock_after_shift(text_shift, text_normal, button)
            else:
                button['text'] = text_shift if event.type == '2' else text_normal


def change_button_state(index_list, index_item, event):
    buttons[index_list][index_item]['state'] = return_state(event)


def change_buttons_state_lock(index_list, index_item, event):
    change_button_state(index_list, index_item, event)
    change_to_lock_keyboard(event)


def change_buttons_state_shift(index_list, index_item, event):
    change_button_state(index_list, index_item, event)
    change_to_shift_keyboard(event)


def call_special_buttons(event, index_list, index_item, item):
    array = [
        ('Caps_Lock', 'Caps_Lock', change_buttons_state_lock),
        ('Shift', 'Shift', change_buttons_state_shift),
        ('Control', 'Ctrl', change_button_state),
        ('Alt', 'Alt', change_button_state),
        ('Win', 'Win', change_button_state),
        ('Return', 'Enter', change_button_state)
    ]
    for key_event, key_name, func in array:
        if key_event in event.keysym and key_name in item:
            func(index_list, index_item, event)


def change_state(event):

    for index_list, key_list in enumerate(keyboard):
        for index_item, item in enumerate(key_list):
            text_button, text_shift_button, keycode, _ = item.split(', ')
            call_special_buttons(event, index_list, index_item, item)
            if int(keycode) == event.keycode:
                change_button_state(index_list, index_item, event)


def change_keyboard(event):
    global switch_keyboard, keyboard
    switch_keyboard = not switch_keyboard
    keyboard = keyboards[switch_keyboard]


root = Tk()

text = Text(width=30, height=10)
text.bind('<Key>', change_state)
text.bind('<KeyRelease>', change_state)
text.pack(fill=BOTH)

frame_keyboard = Frame()
frame_keyboard.pack()

for i in range(27):
    Label(frame_keyboard, text=i).grid(column=i, row=3)

buttons = []
for y, key_array in enumerate(keyboard):
    column_grid = 0
    buttons_temp = []
    for x, key in enumerate(key_array):
        text, _, _, column_span = key.split(', ')
        column_span = int(column_span)
        button_temp = Button(frame_keyboard, text=text)
        buttons_temp.append(button_temp)
        button_temp.grid(column=column_grid, row=y, sticky=NSEW, columnspan=column_span)
        column_grid += column_span
    buttons.append(buttons_temp)

root.bind('<Alt-Shift_L>', change_keyboard)
root.mainloop()
