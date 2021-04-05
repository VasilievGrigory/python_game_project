import time
import curses
from enum import Enum
from curses.textpad import Textbox, rectangle

class Level(Enum):
        EASY = "EASY"
        MEDIUM = "MEDIUM"
        HARD = "HARD"

class Game():
    
    def __init__(self):
        self.level = Level.EASY.value 
        self.l = ["Easy", "Medium", "Hard"]
        self.player = ""
        self.time = 0
        self.mistakes = 0
        self.history = {}
        self.attempt = 0
        self.exit = False
        self.is_failed = False

    def start_game(self, main):
        curses.noecho()
        main.addstr("Hi! How are you? Ready to start? ")
        main.getch()
        main.clear()
        main.addstr(0, 0, "Enter YOUR name:"
                         "(hit Ctrl-G to send)")
        editwin = curses.newwin(5,30, 2,1)
        rectangle(main, 1,0, 1+5+1, 1+30+1)
        main.refresh()
        box = Textbox(editwin)
        box.edit()
        name = box.gather()
        main.clear()
        self.player = name
        while not self.exit:
            self.main_part(main)

    def main_part(self, main):
        self.attempt += 1
        level_  = self.pick_mode(main)
        if level_ == 0:
            self.level = Level.EASY.value
        elif level_ == 1:
            self.level = Level.MEDIUM.value
        else:
            self.level = Level.HARD.value
        main.clear()
        main.addstr("Your pick is {}".format(self.level))
        main.addstr("\nNow, we are ready to start!\n"
                          "Good luck, {}".format(self.player))
        main.getch()
        self.mode(main, self.level)
        main.addstr("\nPress 'p', if you want play one more time, press"
                         " 'h' to see history, or press any another key to leave\n\n")
        ans = main.getch()
        if chr(ans) == 'p':
            main.clear()
        elif chr(ans) == 'h':
            main.addstr(str(self.history))
            main.addstr('\n')
            main.addstr("\nPress 'p', if you want play one more time,"
                              " or press any another key to leave\n")
            ans1 = main.getch()
            if chr(ans1) == 'p':
                main.clear()
            else:
                self.exit = True
        else:
            self.exit = True

    def pick_mode(self, main):
        curses.noecho()
        exit = False
        choice = 0
        while(not exit):
            main.clear()
            main.addstr("Now time to pick mode:\n")
            for i in range(3):
                if i == choice:
                    main.addstr('>')
                else:
                    main.addstr(' ')
                main.addstr(self.l[i])
            main.addstr("\n(To iterate use: KEY_LEFT and KEY_RIGHT)")
            main.addstr("\n(To pick click KEY_UP)")
            ans = main.getch()
            if chr(ans) == 'D':
                if choice >= 1:
                    choice -= 1
            elif chr(ans) == 'C':
                if choice != 2:
                    choice += 1
            elif chr(ans) == 'A':
                exit = True
        return choice

    def mode(self, main, mode_ = Level.EASY.value):
        s = self.reading_mode_file(mode_)
        self.player_printing(main, s)
        main.addstr("Your results:\nTime: {}\n"
                          "Mistakes: {}\n".format(str(self.time),str(self.mistakes)))
        if self.is_failed:
            self.history[self.attempt] = [self.level, self.time, self.mistakes, "failed"]
        else:
             self.history[self.attempt] = [self.level, self.time, self.mistakes, "completed"]
        self.time = 0
        self.mistakes = 0
        main.getch()

    def reading_mode_file(self, mode_ = Level.EASY.value):
        if mode_ == Level.EASY.value:
            with open('easy_mode.txt', mode = 'r') as f:
                s = f.read()
        elif mode_ == Level.MEDIUM.value:
           with open('medium_mode.txt', mode = 'r') as f:
                s = f.read()
        else:
            with open('hard_mode.txt', mode = 'r') as f:
                s = f.read()
        return s

    def player_printing(self, main, s):
        start = time.time()
        s_const = s
        while len(s) >= 1:
            main.clear()
            main.addstr(s_const)
            main.addstr('\n')
            if s.find(' ') == -1:
                s_curr = s
                s = ""
                s_curr = s_curr[:len(s_curr) - 1]
            else:
                s_curr = s[:s.find(' ') + 1]
                s = s[s.find(' ') + 1:]
            main.addstr("If you want to leave, press 'b'\n")
            main.addstr(s_curr)
            main.addstr('\n')
            temp = 0
            while temp < len(s_curr):
                ans = main.getch()
                if s_curr[temp] == chr(ans):
                    main.addstr(s_curr[temp])
                    temp += 1
                elif 'b' == chr(ans):
                    self.is_failed = True
                    s = ""
                    break
                else:
                    self.mistakes += 1
        self.time = time.time() - start
        main.clear()

def main():
    main = curses.initscr()
    g = Game()
    g.start_game(main)
    curses.endwin()

if __name__ == "__main__":
    main()
