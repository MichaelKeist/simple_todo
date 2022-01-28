#implementing the classes and methods created in todo_defs.py

import os
from datetime import datetime
from datetime import date
import pandas
from todo_defs import *
#import Console
from colorama import *
#from pynput import keyboard
import keyboard
import curses
from curses.textpad import Textbox, rectangle



#print('%s%s%s' % (pos(console_rows,1), Fore.WHITE, Style.NORMAL), end='')
#initializing the look of the console
#init()
#os.system("clear")
console_columns = os.get_terminal_size()[0] - 1
console_rows = os.get_terminal_size()[1] - 1
#pos = lambda y, x: Cursor.POS(x, y)

#validating name and date inputs
def almost_due(stdscr, item): #the scores for each date are not exactly the number of days since 01-01-0000 but eh
    month_lengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    today = str(date.today())
    today = today.split("-")
    today_score = (int(today[0]) - 1) * 365 + int(today[2])
    for i in range(0,int(today[1])):
        today_score += month_lengths[i]
    item_date = item.get_date()
    item_date = item_date.split("-")
    item_weight = (int(item_date[2]) - 1) * 365 + int(item_date[1])
    for i in range(0,int(item_date[0])):
        item_weight += month_lengths[i]
    if (item_weight - today_score) <= 3:
        return True
    else:
        return False

def get_global_index(begin_item, x, max_display, current_display):
    return (begin_item + (x-3) - (max_display - len(current_display)))

def init_input_box(stdscr, x, y, height):
    editwin = curses.newwin(height,29,y+2,1)
    rectangle(stdscr,y+1,0,y+2+height,30)
    return editwin

def edit_input_setup(stdscr, x, y, message, item):
    skip_next_char = False
    namestr = item.get_name()
    datestr = item.get_date()
    notestr = item.get_note()
    stdscr.addstr(0, 0, "Item name")
    stdscr.addstr(5, 0, "Item date")
    stdscr.addstr(10, 0, "Item notes")
    namewin = init_input_box(stdscr,0,0,1)
    datewin = init_input_box(stdscr,0,5,1)
    notewin = init_input_box(stdscr,0,10,15)
    stdscr.refresh()
    namebox = Textbox(namewin)
    datebox = Textbox(datewin)
    notebox = Textbox(notewin)
    for char in namestr:
        namebox._insert_printable_char(char)
    for char in datestr:
        datebox._insert_printable_char(char)
    i = 0
    while i < (len(notestr)):
        char = notestr[i]
        if char == "\\" and notestr[i+1] == "n": #test having a note ended by a \
            notebox._insert_printable_char(10)
            i += 2
        else:
            notebox._insert_printable_char(char)
            i += 1
    namebox.edit(enter_is_terminate)
    datebox.edit(enter_is_terminate)
    notebox.edit(enter_is_terminate)
    return namebox.gather(), datebox.gather(), notebox.gather()

def display_note(stdscr, x, current_display):
    if len(current_display) > 0:
        stdscr.addstr(console_rows // 3, 60, "Item notes:")
        note = current_display[get_current_item_index(console_rows,x)].get_note()
        note_lines = note.split("\\n")
        for i in range(len(note_lines)):
            stdscr.addstr((console_rows // 3) + 2 + i, 60, note_lines[i])
    return

def print_vertical_bar(column, row_start, stdscr):
    for rownum in range(row_start, console_rows + 1):
        stdscr.addstr(rownum, column, "|")
    return

def get_current_item_index(console_rows, x):
    return (-1 - (console_rows - x))

def name_validate(name):
    for char in name:
        if not ((97 <= ord(char) <= 122) or 65 <= ord(char) <= 90 or ord(char) == 32):
            return False
    return True

def date_validate(date):
    split_date = date.split("-")
    for num in split_date:
        if not (num.isnumeric()):
            return False
    if (len(split_date[0]) != 2) or (len(split_date[1]) != 2) or (len(split_date[2]) != 4) or (not 1 <= int(split_date[0]) <= 12):
        return False
    return True

def check_save(stdscr):
    stdscr.addstr(console_rows, 0, "Save this element? (y/n)")
    while True:
        key = stdscr.getkey()
        if key == "y":
            return True
        elif key == "n":
            return False

def check_delete(stdscr, current_display, console_rows, x):
    stdscr.addstr(0, 0, " " * console_columns)
    stdscr.addstr(0, 0, "Delete " + str(current_display[get_current_item_index(console_rows,x)]) + "? (y/n)")
    while True:
        key = stdscr.getkey()
        if key == "y":
            return True
        elif key == "n":
            return False

#helpful input window tips found here: https://stackoverflow.com/questions/36121802/python-curses-make-enter-key-terminate-textbox
#defining input window
def enter_is_terminate(x):
    if x == 7:
        x = 7
    return x

def input_setup(stdscr, x, y, message, height):
    stdscr.addstr(y,x,message)
    #stdscr.refresh()
    editwin = curses.newwin(height,29,y+2,1)
    rectangle(stdscr,y+1,0,y+2 + height,30)
    stdscr.refresh()
    box = Textbox(editwin)
    box.edit(enter_is_terminate)
    return box.gather()

#intializing keyboard listener
def on_press(key):
    try:
        print("test")
    except AttributeError:
        print('special key {0} pressed'.format(key))

def xbounds(x, todo_list):
    if console_rows - (len(todo_list) - 1) <= x <= console_rows:
        return x
    elif x > console_rows:
        return console_rows
    elif (x > console_rows) or (x <= console_rows - (len(todo_list) - 1)):#len(todo_list) - 1):
        output = console_rows if (len(todo_list) - 1 > console_rows) else console_rows - (len(todo_list) - 1)
        return output
    else:
        return console_rows

def ybounds(x, todo_list, num_displayed):
    #return (len(str(todo_list[-1 - (console_rows - x)])) - 1) + (len(str(console_rows - x) + ": "))
    return 0

def title():
    return "Simple To-do List\npress any key to enter\n" + "_" * console_columns

def instructions():
    return "q - exit | (a)dd item | (c)omplete item | (e)dit item\n" + "_" * console_columns

def initialize(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

def scroll(x, begin_item, end_item, date_sorted_list, max_display):
    if len(date_sorted_list) <= max_display:
        return begin_item, end_item
    elif (x > console_rows) and (end_item < (len(date_sorted_list))):
        begin_item += 1
        end_item += 1
        return begin_item, end_item
    elif (x < ((console_rows - max_display)) + 1) and begin_item != 0:
        begin_item -= 1
        end_item -= 1
        return begin_item, end_item
    else:
        return begin_item, end_item

def main():
    #defining constants and intializing variables
    user = True
    date_sorted_list = read_todo_list()
    date_sorted_list = date_sorted_list.due_sort()
    row_pos = 0
    col_pos = 0
    x = console_rows
    y = console_columns
    max_display = console_rows - 2
    begin_item = 0
    end_item = max_display
    first_loop = True
    stdscr = curses.initscr()
    initialize(stdscr)
    stdscr.addstr(0,0, title())
    waiter = stdscr.getkey()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    while user:
        begin_item,end_item = scroll(x,begin_item,end_item, date_sorted_list, max_display)
        stdscr.erase()
        print_vertical_bar(50, 3, stdscr)
        num_displayed = 0
        current_display = date_sorted_list[begin_item:end_item]
        x = xbounds(x, current_display)
        y = ybounds(x, current_display, num_displayed)
        display_note(stdscr, x, current_display)
        row_pos = console_rows - (len(current_display) - 1)
        stdscr.addstr(1,0, instructions())
        if len(current_display) > 0:
            if almost_due(stdscr, current_display[get_current_item_index(console_rows,x)]):
                stdscr.addstr(0,0, str(current_display[get_current_item_index(console_rows,x)]), curses.color_pair(1))
            else:
                stdscr.addstr(0,0, str(current_display[get_current_item_index(console_rows,x)]))
            for item in current_display:
                if num_displayed >= max_display:
                    num_displayed -= 1
                    row_pos -= 1
                    break
                if almost_due(stdscr, item):
                    stdscr.addstr(row_pos, 0, str(begin_item + num_displayed + 1) + ": " + str(item), curses.color_pair(1))
                else:
                    stdscr.addstr(row_pos, 0, str(begin_item + num_displayed + 1) + ": " + str(item))
                row_pos += 1
                num_displayed += 1
            stdscr.move(x,y)
            stdscr.refresh()
        key = stdscr.getkey()
        stdscr.refresh()
        #defining actions of keys
        if key == "q":
            user = False
        elif key == "k":
            x -= 1
        elif key == "j":
            x += 1
        elif key == "a":
            stdscr.erase()
            new_name = input_setup(stdscr, 0, 0, "Enter item name (no special characters please!): ", 1).strip()
            new_date = input_setup(stdscr, 0 , 5, "Enter a date for the item (mm-dd-yyyy)", 1).strip()
            new_note = repr(input_setup(stdscr, 0, 10, "Enter a note for the item (optional)", 15j))
            new_note = new_note[1:len(new_note) - 1]
            if check_save(stdscr):
                if name_validate(new_name) and date_validate(new_date):
                    new_item = todo_item(new_name, new_date, new_note)
                    date_sorted_list.add_item(new_item)
                    date_sorted_list = date_sorted_list.due_sort()
                    date_sorted_list.write_to_file()
                    stdscr.erase()
                else:
                    stdscr.addstr(0,0, " " * console_columns)
                    stdscr.addstr(0,0, "Invalid input, press any key to continue")
                    waiter = stdscr.getkey()
                    stdscr.erase()
        elif key == "c":
            if check_delete(stdscr, current_display, console_rows, x):
                date_sorted_list.remove(begin_item + (x-3) - (max_display - len(current_display)))
                date_sorted_list.write_to_file()
                if begin_item > 0:
                    begin_item -= 1
                    end_item -= 1
                if len(date_sorted_list) < max_display:
                    x += 1
        elif key == "e":
            stdscr.erase()
            new_name, new_date, new_note = edit_input_setup(stdscr, 0, 0, "Item name:", date_sorted_list[get_global_index(begin_item, x, max_display, current_display)]) 
            new_name = new_name.strip()
            new_date = new_date.strip()
            new_note = repr(new_note)
            new_note = new_note[1:len(new_note) - 1]
            if check_save(stdscr):
                if name_validate(new_name) and date_validate(new_date):
                    date_sorted_list[get_global_index(begin_item, x, max_display, current_display)].set_name(new_name)
                    date_sorted_list[get_global_index(begin_item, x, max_display, current_display)].set_date(new_date)
                    date_sorted_list[get_global_index(begin_item, x, max_display, current_display)].set_note(new_note)
                    date_sorted_list = date_sorted_list.due_sort()
                    date_sorted_list.write_to_file()
                    stdscr.erase()
                else:
                    stdscr.addstr(0,0, " " * console_columns)
                    stdscr.addstr(0,0, "Invalid input, press any key to continue")
                    waiter = stdscr.getkey()
                    stdscr.erase()


    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    

if __name__ == '__main__':
    main()