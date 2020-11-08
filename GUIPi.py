# -*- coding: utf-8 -*-

import pyowm
import serial
from tkinter import *
import urllib.request
import base64
import io
from datetime import datetime
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout= 0.01)

logger = ""

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()


owm = pyowm.OWM('x')
                                             
            


class magicScreen:
    def __init__(self):
        self.window = Tk()
        self.window.config(background = "#4C516D")
        self.window.attributes('-zoomed', True)
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        top_left_frame = Frame(self.window, width=420, background="#838996")
        top_left_frame.grid(row=0, column=0, padx=20, pady=15, sticky=N+S)
        mid_frame = Frame(self.window, width = 420, height= 900, bg= "#838996")
        mid_frame.grid(row=0, column=1, padx=20, pady=15, sticky=N+S)
        right_frame = Frame(self.window, width = 420, height= 900, bg= "#838996")
        right_frame.grid(row=0, column=2, padx=20, pady=15, sticky=N+S)

        #LEFT
        Todo=Label(top_left_frame, text="To-Do:", font=("Roboto Condensed", 30), width=10)
        Todo.grid(row=0, column=0, padx=30, pady=30, sticky=E+W)
        list = "Finish DM1588 Project.\nClean house.\nRecord Video.\nKeep being great.\nPolish Desk.\nDress Bed.\nMop Floor."
        Todolist = Label(top_left_frame, text = list, wraplength=380,
                         font=("Roboto Condensed", 20), justify=LEFT)
        Todolist.grid(row=1, column=0, padx=10, pady=20, sticky=E+W)


        #MID
        self.date = Label(mid_frame, text= "Time", font=("Roboto Condensed", 30), wraplength=380,
                          width=12)
        self.date.grid(row=0, column=0, padx= 15, pady=20, sticky=E+W)
        self.dub = Label(mid_frame, text= "weather1", font=("Roboto Condensed", 30), wraplength=380,
                          width=12)
        self.dub.grid(row=1, column=0, padx= 15, pady=20, sticky=E+W)
##        self.dub_img = Label(mid_frame)
##        self.dub_img.grid(row=1, column=1, padx= 5, pady=20)
        self.stock = Label(mid_frame, text= "weather2", font=("Roboto Condensed", 30), wraplength=380,
                          width=20)
        self.stock.grid(row=2, column=0, padx= 15, pady=20, sticky=E+W)
##        self.stock_img = Label(mid_frame)
##        self.stock_img.grid(row=2, column=1, padx= 5, pady=20)

        
        #RIGHT
        door_title = Label(right_frame, text= "Door Security Log", font=("Roboto Condensed", 30))
        door_title.grid(row=0, column=0, padx= 15, pady=10, sticky=E+W)
        self.door_log = Label(right_frame, text = logger, wraplength=380,
                         font=("Roboto Condensed", 20), justify=LEFT)
        self.door_log.grid(row=1, column=0, padx=10, pady=20, sticky=E+W)

        self.radio_comms()
        self.serialArdComms()
        self.getTimeString()
        self.weatherCheck()
        self.window.mainloop()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.window.attributes('-zoomed', self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.window.attributes('-zoomed', self.fullScreenState)

    def serialArdComms(self):
        global ser
        global logger
        read_data = ser.readline()
##        print(read_data)
        if len(read_data) > 0 and read_data != b'49\r\n':
            if ord(read_data) == 1:
    ##            print(read_data)
                logger += datetime.now().strftime("%X")
                logger += " Door has been opened from the interior.\n"
                self.door_log.config(text = logger)
        self.window.after(200, self.serialArdComms)

    def getTimeString(self):
        timeString = datetime.now().strftime("It is %A.\n %d/%m/%Y \n%H:%M")
        self.date.config(text = timeString)                                          
        self.window.after(1000, self.getTimeString)

    def weatherCheck(self):
        
        dub_string = "Dun Laoghaire"
        dub_obs = owm.weather_at_place(dub_string)
        dub_string = "Dublin: " + str(dub_obs.get_weather().get_temperature('celsius')['temp'])
        dub_string += "°\nWith " + str(dub_obs.get_weather().get_detailed_status())
        self.dub.config(text = dub_string)

##        dub_url= dub_obs.get_weather().get_weather_icon_url()
##        dub_image = urllib.request.urlopen(dub_url).read()
##        dub_b64 = base64.encodestring(dub_image)
##        dub_photo = PhotoImage(data=dub_b64)
##        self.dub_img.config(image = dub_photo)

        stock_string = "Stockholm"
        stock_obs = owm.weather_at_place(stock_string)
        stock_string = "Stockholm: " + str(stock_obs.get_weather().get_temperature('celsius')['temp'])
        stock_string += "°\nWith " + str(stock_obs.get_weather().get_detailed_status())
        self.stock.config(text = stock_string)
        
        self.window.after(1000, self.weatherCheck)
        

    def radio_comms(self):
        if radio.available(0):
            global logger
            global ser
            receivedMessage = []
            radio.read(receivedMessage, radio.getDynamicPayloadSize())
            #print(receivedMessage)
            stringGreet = ""
            if receivedMessage[0] == 1 :
                stringGreet = "Authorised User 1 Entered"
                ser.write(b'1')
                ser.flush()
            elif receivedMessage[0] == 3 :
                stringGreet = "Authorised User 2 Entered"
                ser.write(b'1')
                ser.flush()
            else:
                stringGreet = "Unauthorised User Attempted Entry"

            logger += datetime.now().strftime("%X")
            logger += " " + stringGreet + ".\n"

            self.door_log.config(text = logger)
        self.window.after(1000, self.radio_comms)

##leftFrame = Frame(root, )

##app = App()
##title_box = Box(app, align="top", width="fill")
##
##todo_box = Box(title_box, width="fill", height align="left", border=True)
##Text(title_box, text="To-Do")
##
##time_box
##
##door_box = Box(app, height="fill", align="right", width=(app.width / 3),
##               border=True)
##doorLog = Text(door_box, text="Door Box", align="top")
##doorLog.repeat(100, radio_comms)
##
##footer_box = Box(app, width="fill", align="bottom", border=True)
##Text(footer_box, text="Goodbye")

##app.set_full_screen()
                                                 
	    # Set up the layout:
	    #superBox = BoxLayout(spacing=10, orientation = 'horizontal')

            #col1 = BoxLayout(spacing=5, orientation='vertical')

	    #title1 = Button(text='To-do', size_hint(1, 0.15))
	    #body1 = Label(text='Finish DM1588 Project.\nClean house.\nRecord Video.\nKeep being great.',
            #              size_hint(1, 0.75), font_size ='20sp', halign='left, valign='top')
	    #col1.add_widget(title1)
            #col1.add_widget(body1)

	    #col2 = BoxLayout(spacing=5, orientation='vertical')
            #Clock.schedule_interval(TimeButton.update, 1.0)
            #Clock.schedule_interval(DublinButton.update, 5.0)
            #Clock.schedule_interval(SwedenButton.update, 5.0)
            #timeString = datetime.datetime.now().strftime("Today it is %a, %x\n%H:%M)
            #                                                  
            #title21 = TimeButton(text=timeString, size_hint(1, 0.3))
            #title22 = DublinButton(text='Dublin Placeholder', size_hint(1, 0.3))
	    #title23 = SwedenButton(text='Sweden Placeholder', size_hint(1, 0.3))
            #col2.add_widget(title21)
            #col2.add_widget(title22)
            #col2.add_widget(title23)


           # col3 = BoxLayout(spacing=5, orientation='vertical')

           # Clock.schedule_interval(LogLabel.update, 1.0/2.0)
           # title31 = Button(text='Door Logs', size_hint(1, 0.15))
	   # body31 = LogLabel(text=logger,
           #                   size_hint(1, 0.75), font_size ='20sp', halign='left, valign='top')
		
	    #col3.add_widget(title31)
            #col3.add_widget(body31)

            #superBox.add_widget(col1)
            #superBox.add_widget(col2)
            #superBox.add_widget(col3)

            #return superBox

		

if __name__ == '__main__':
	app = magicScreen()

#>
