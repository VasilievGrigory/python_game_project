import curses
import time
from curses.textpad import Textbox, rectangle

class Game():
    level = 0
    l = ["Easy", "Medium", "Hard"]
    player = ""
    time = 0
    mistakes = 0
    history = {}
    attempt = 0
    exit = False
    def start_game(self, main):
        curses.noecho()
        main.addstr("Hi! How are you? Ready to start? ")
        main.getch()
        main.clear()
        main.addstr(0, 0, "Enter YOUR name: (hit Ctrl-G to send)")
        editwin = curses.newwin(5,30, 2,1)
        rectangle(main, 1,0, 1+5+1, 1+30+1)
        main.refresh()
        box = Textbox(editwin)
        box.edit()
        name = box.gather()
        main.clear()
        self.player = name
        while (not self.exit):
            self.attempt += 1
            self.level = self.pick_mod(main)
            main.clear()
            main.addstr("Your pick is ")
            main.addstr(self.l[self.level])
            main.addstr("\nNow, we are ready to start!\nGood luck, ")
            main.addstr(self.player)
            main.getch()
            self.mode(main, self.level)
            main.addstr("\nPress 'p', if you want play one more time, press 'h' to see history, or press any another key to leave\n\n")
            ans = main.getch()
            if ans == ord('p'):
                main.clear()
            elif ans == ord('h'):
                main.addstr(str(self.history))
                main.addstr('\n')
                main.addstr("\nPress 'p', if you want play one more time, or press any another key to leave\n")
                ans1 = main.getch()
                if ans1 == ord('p'):
                    main.clear()
                else:
                    self.exit = True
            else:
                self.exit = True


    def pick_mod(self, main):
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
            if ans == ord('D'):
                if choice >= 1:
                    choice -= 1
            elif ans == ord('C'):
                if choice != 2:
                    choice += 1
            elif ans == ord('A'):
                exit = True
        return choice

    def mode(self, main, mode = 0):
        if mode == 0:
            f = open('easy_mode.txt', 'r')
            s = f.read()
        elif mode == 1:
            f = open('medium_mode.txt', 'r')
            s = f.read()
        else:
            f = open('hard_mode.txt', 'r')
            s = f.read()
        s_const = s
        start = time.time() 
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
            is_failed = False
            f = "failed"
            c = "completed"
            while temp < len(s_curr):
                ans = main.getch()
                if ord(s_curr[temp]) == ans:
                    main.addstr(s_curr[temp])
                    temp += 1
                elif ord('b') == ans:
                    is_failed = True
                    s = ""
                    break
                else:
                    self.mistakes += 1
        main.clear()
        self.time = time.time() - start
        main.addstr('\n')
        main.addstr("Your results:\n")
        main.addstr("Time: ")
        main.addstr(str(self.time))
        main.addstr('\n')
        main.addstr("Mistakes: ")
        main.addstr(str(self.mistakes))
        main.addstr('\n')
        if is_failed:
            self.history[self.attempt] = [self.l[self.level], self.time, self.mistakes, f]
        else:
             self.history[self.attempt] = [self.l[self.level], self.time, self.mistakes, c]
        self.time = 0
        self.mistakes = 0
        main.getch()
        return

main = curses.initscr()
g = Game()
g.start_game(main)
curses.endwin()
