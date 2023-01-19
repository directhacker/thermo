from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Combobox
from tkinter.ttk import Notebook
import re
import tkinter.font
import math
import time
import RPi.GPIO as GPIO
import configparser
import helper



font = "Quicksand"

config = helper.read_config()
config_file = configparser.ConfigParser()

defaultTemp = float(config['Thermostat Defaults']['Default Temp'])


on = GPIO.HIGH
off = GPIO.LOW
set_temp = defaultTemp

class Widget1():

    def __init__(self, parent):
        self.gui(parent)

    def gui(self, parent):

        if parent == 0:
            self.w1 = Tk()
            self.w1.title("Thermostat")
            self.value = BooleanVar()
            self.r1_v = IntVar()
            self.w1.configure(bg = '#212121')
            self.w1.geometry('1150x740')
            self.w1.resizable(0,0)
        else:
            self.w1 = Frame(parent)
            self.w1.configure(bg = '#212121')
            self.w1.place(x = 0, y = 0, width = info_screenwidth(), height = winfo_screenheight())
        self.tab1 = Notebook(self.w1)

        self.tab1.place(x = -1, y = 0, width = 1160, height = 750)
        self.ta1 = Frame(self.tab1)
        self.ta1.configure(bg = "#212121")

        self.ta1.place(x = 0, y = 0, width = 1160, height = 740)
        self.tab1.add(self.ta1, text = "Home")
        self.ta2 = Frame(self.tab1)
        self.ta2.place(x = 0, y = 0, width = 1150, height = 740)
        self.ta2.configure(bg = "#212121")
        self.tab1.add(self.ta2, text = "Settings")

        self.up = Button(self.ta1, border = 0, highlightthickness = 0,text = "+", bg = "#333333", fg = "#FFFFFF", activebackground = "#111111", activeforeground= "#FFFFFF",font = tkinter.font.Font(family = font, size = 15, weight = 'bold'), cursor = "arrow", state = "normal")
        self.up.place(x = 40, y = 40, width = 510, height = 82)
        self.up['command'] = self.up_pressed
        self.down = Button(self.ta1, border = 0, highlightthickness = 0, text = "Lock", bg = "#333333", fg = "#FFFFFF",activebackground = "#111111", activeforeground= "#FFFFFF", font = tkinter.font.Font(family = font, size = 15, weight = 'bold'), cursor = "arrow", state = "normal")
        self.down.place(x = 40, y = 130, width = 250, height = 82)
        self.down['command'] = self.down_pressed
        self.set_temp = Label(self.ta1, anchor='w',text = "70", bg = "#212121", fg = "#ffffff", font = tkinter.font.Font(family = font, size = 12, weight = 'bold'), cursor = "arrow", state = "normal")
        self.set_temp.place(x = 40, y = 390, width = 130, height = 32)
        self.current_temp = Label(self.ta1, anchor='w', text = "70", bg = "#212121", fg = "#ffffff", font = tkinter.font.Font(family = font, size = 12, weight = 'bold'), cursor = "arrow", state = "normal")
        self.current_temp.place(x = 570, y = 40, width = 120, height = 32)
        self.current_hum = Label(self.ta1, anchor='w', text = "Cut Length", bg = "#212121", fg = "#ffffff", font = tkinter.font.Font(family = font, size = 12, weight = 'bold'), cursor = "arrow", state = "normal")
        self.current_hum.place(x = 570, y = 140, width = 110, height = 32)


    def settings_applied(self):
        print('settings_applied')
        config_file.read("configurations.ini")
        global defaultSoffitLength
        global jogSpeed
        global stepsPerIn
        global require_home
        config_file["Soffit Cutter Defaults"]["Require Home"] = str(self.value.get())
        config_file["Soffit Cutter Defaults"]["Jog Speed"] = str(self.jog_speed.get())
        config_file["Soffit Cutter Defaults"]["Steps Per Inch"] = str(self.step_per_in.get())
        config_file["Soffit Cutter Defaults"]["Default Soffit Length"] = str(convert_to_inch(self.default_soffit_length.get()))
        require_home = self.value.get()
        jogSpeed = int(config['Soffit Cutter Defaults']['Jog Speed'])
        defaultSoffitLength = convert_to_inch((config['Soffit Cutter Defaults']['Default Soffit Length']))
        stepsPerIn = int(config['Soffit Cutter Defaults']['Steps Per Inch'])
        with open("configurations.ini","w") as file_object:
            config_file.write(file_object)



    def up_pressed(self):
        ++set_temp
        self.set_temp.configure(set_temp)
        print(set_temp)

    def down_pressed(self):
        --set_temp
        self.set_temp.configure(set_temp)
        print(set_temp)


if __name__ == '__main__':
    a = Widget1(0)
    a.w1.mainloop()
