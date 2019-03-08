# -*- coding: utf-8 -*-

import pyglet

class Countdown():
    def __init__(self, hrs, mins, secs, window, option):
        self.hours = hrs
        self.minutes = mins
        self.seconds = secs
        self.hrs = hrs
        self.mins = mins
        self.secs = secs
        self.start = 'Press Enter to Start!'
        self.resume = 'Press Enter to Resume!'
        self.label_1 = pyglet.text.Label(self.start, font_size = 16,
                                         x = window.width//2, y = window.height//2,
                                         anchor_x = 'center', anchor_y = 'center')
        self.label_2 = pyglet.text.Label('', font_size = 10, x = window.width//2,
                                         y = window.height//2 - 50,
                                         anchor_x = 'center', anchor_y = 'center')
        self.label_3 = pyglet.text.Label('', font_size = 10, x = window.width//2,
                                         y = window.height//2 - 75,
                                         anchor_x = 'center', anchor_y = 'center')
        self.reset(option)
        
    def reset(self, option):
        self.begin = False
        if option == 0: # The Countdown restarts so, we need the initial values.
            self.secs = self.seconds
            self.mins = self.minutes
            self.hrs = self.hours
            self.label_1.text = self.start
        if option == 1: # The Countdown resumes from the point it was left.
            self.label_1.text = self.resume
        self.label_1.color = (255, 255, 255, 255)
        self.label_1.font_size = 16
    
    def update(self, dt, window):
        if self.begin:
            if self.secs < 0 and self.mins != 0:
                self.secs = 59
                self.mins -= 1
            if self.mins < 0 and self.hrs != 0:
                self.mins = 59
                self.hrs -= 1
            # Flashing for the last 30 seconds.
            if (self.hrs == 0) and (self.mins == 0) and (self.secs <= 30):
                if self.secs%2:
                    self.label_1.color = (255, 0, 0, 255)
                else:
                    self.label_1.color = (255, 255, 255, 255)
            if (self.hrs <= 0) and (self.mins <= 0) and (self.secs <= 0):
                self.secs = 0
                self.begin = False
            self.label_1.text = '{:02d}:{:02d}:{:02d}'.format(int(self.hrs),
                                                              int(self.mins),
                                                              int(self.secs))
            self.label_2.text = 'Press Enter to Restart'
            self.label_3.text = 'Press Space to Pause'
            self.secs -= int(dt)

def main(hrs, mins, secs):

    window = pyglet.window.Window(width = 320, height = 240) #Window size
    option = 0

    countdown = Countdown(abs(int(hrs)), abs(int(mins)), abs(int(secs)), window, option)

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            option = 0
            if countdown.begin:
                countdown.reset(option)
            else:
                countdown.begin = True
        elif symbol == pyglet.window.key.SPACE:
            option = 1
            if countdown.begin:
                countdown.reset(option)
        elif symbol == pyglet.window.key.ESCAPE:
            window.close()
            
    @window.event
    def on_draw():
        window.clear()
        countdown.label_1.draw()
        if countdown.begin:
            countdown.label_2.draw()
            countdown.label_3.draw()
        
    pyglet.clock.schedule_interval(countdown.update, 1, window)
    pyglet.app.run()

if __name__ == '__main__':

    hours   = int(input("Hours to countdown:"))
    minutes = int(input("Minutes to countdown (0-59):"))
    seconds = int(input("Seconds to countdown (0-59):"))
    
    if seconds >= 60:
        new_min, seconds = divmod(seconds, 60)
        minutes = minutes + new_min

    if minutes >= 60:
        new_hrs, minutes = divmod(minutes, 60)
        hours = hours + new_hrs

    main(hours, minutes, seconds)
