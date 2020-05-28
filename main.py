from colorama import Fore
import cmd, sys
import datetime

from utils import *
import string


class SearchResult():
    def __init__(self, search_string):
        self.search = search_string
        '''
        format of end search result:
        word
        '''

    def is_eng(self, arg):
        for i in arg:
            if i in string.ascii_letters:
                return True
            continue
        return False

    def is_frame(self, arg):
        return isinstance(arg, int)

    def search_basic(self):
        full = ""
        for arg in self.search:
            if self.is_frame(arg):
                kanji = frame_to_kanji(arg)
                full += kanji

            elif self.is_eng(arg):
                kanji = get_kanji_by_keywords(arg)[0]
                full += kanji

            else:
                full += arg

        return full


class MainCli(cmd.Cmd):
    """The command line interface (Cli). """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.cmd_seperator = "-"
        self.defaultmode = "Normal"
        self.mode = self.defaultmode
        self.update_CLI()
        self.copyon = False
        self.modes = {'Normal': ['-n', 'No change'],
                      'FireFox': ['-b', 'View definition in FireFox'],
                      'Furigana': ["-f", 'Always generate furigana output'],
                      'Kanjify': ["-k", "Kanjify words from hirgana"],
                      'Dictionary': ["-d", "Display dictionary entries for search"],
                      "Info": ["-i", "Displays information about a kanji\n"]}

        self.history = dict()

    def update_CLI(self):
        self.prompt = colors[self.mode] + f"({self.mode}) "

    def default(self, line):
        line = line.strip().lower()
        if not line:
            self.emptyline()
        elif line.startswith(self.cmd_seperator):
            command = line.split(" ")[0]
            self.command(command)
        else:
            self.searchMain(line)

    def emptyline(self):
        print('')

    def change_mode(self, mode):
        if mode == self.mode:
            print(Fore.RED + f"Already in {mode} mode")
        else:
            self.mode = mode
            self.update_CLI()

    def command(self, command):
        currentDate = datetime.datetime.now()
        currentDate = currentDate.strftime("%H: %M: %S")
        self.history[currentDate] = command
        if command == "--h":
            print(Fore.RED + f"Available commands:\n"
                             f"--q:     Quits out of the program\n"
                             f"--h:     Displays the help menu\n"
                             f"--c:     Allows you to copy search results\n"
                             f"--hist   Look back into your history\n"
                             f"--clear  Clear commands\n\n"
                             f"Available modes:\n"
                  )
            for k, v in self.modes.items():
                print(f"    {k}({v[0]}):    {v[1]}")
            return
        elif command == "--q":
            sys.exit()
        elif command == "--clear":
            import os
            os.system("cls")
            return
        elif command == "--hist":
            for num, (time, cm) in enumerate(self.history.items()):
                print(f"{num}:   {cm}  (Time:   {time})")
            if self.copyon:
                try:
                    commandnum = input("Which command would you like to copy? (or type k to exit history) ")
                    commandnum = int(command)
                except:
                    if commandnum.lower() == "k":
                        return
                    else:
                        print("Invalid command. Exiting history...")
                        return
                else:
                    for num, (time, cm) in enumerate(self.history.items()):
                        if num == commandnum:
                            copy(cm)

            return

        elif command == "--c":
            self.copyon = True if not self.copyon else False
            return
        for mode in self.modes:
            if command == self.modes[mode][0]:
                self.change_mode(mode)
                return

        print(Fore.RED + "That was not an available command.\nPlease type --h and view the commands.")

    def searchMain(self, line):
        searchArgs = line.split(' ')
        searchObj = SearchResult(searchArgs)
        try:
            endres = searchObj.search_basic()
        except:
            print("No results...")
            return
        if self.mode == "Normal":
            printOutput(endres, self.mode)
            if self.copyon:
                copy(endres)
        elif self.mode == "FireFox":
            openDef(f"https://jisho.org/search/{endres}")
        elif self.mode == "Furigana":
            gen_furigana(endres, self.mode)
        elif self.mode == "Kanjify":
            kanjified = kanjify(endres)
            if not self.copyon:
                for kanjied in kanjified:
                    printOutput(kanjied, self.mode)
            else:
                for num in range(len(kanjified)):
                    printOutput(str(num) + ".\t" + kanjified[num], self.mode)
                while True:
                    entrynum = input("Entry num to copy")
                    if not isinstance(entrynum, int):
                        print("Invalid number. Try again.\n")
                        continue
                    else:
                        break

                copy(kanjified[entrynum].strip())
        elif self.mode == "Info":
            keywords = get_keyword_by_kanji(endres)
            outKeyw = ""
            for x in keywords:
                outKeyw += x.strip() + ", "
            print(
                f"-------{endres}--------\nKeywords:  {outKeyw}\nFrame:  {kanji_to_frame(endres)}\nStory:  {get_story(endres)}")
            if self.copyon:
                tocopy = input("Which part to copy? (k for keyword, f for frame, s for story) ")
                info = {"k": endres, "f": outKeyw, "s": kanji_to_frame(endres)}
                if tocopy.lower() in ["k", "f", "s"]:
                    copy(info[tocopy.lower()])
        else:
            dictEntry = lookup_eng_def(endres)
            if not self.copyon:
                for entry in dictEntry:
                    printOutput(entry, self.mode)
            else:
                for num in range(len(dictEntry)):
                    printOutput(str(num) + ".\t" + dictEntry[num], self.mode)
                while True:
                    entrynum = input("Entry num to copy:    ")
                    if not isinstance(entrynum, int):
                        print("Invalid number. Try again.\n")
                        continue
                    else:
                        break

                copy(dictEntry[entrynum].strip())


print(Fore.RED + "Loading rtk data...")
loadFrames()

MainCli().cmdloop()
