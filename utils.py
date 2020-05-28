import csv, requests, bs4, pyperclip
from selenium import webdriver
from furigana.furigana import print_plaintext
import colorama
from colorama import Fore


## Gets all the raw data for processing

def get_keyword_by_kanji(kanji):
    res = requests.get(f"https://jisho.org/search/%23kanji {kanji}")
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    try:
        meanings = soup.select(".kanji-details__main-meanings")[0].get_text()
        keywordList = meanings.split(",")
        keywordList = [key.strip("\n") for key in keywordList]
        return keywordList
    except:
        return ''


def get_kanji_by_keywords(keyword):
    res = requests.get("https://jisho.org/search/%23kanji {}".format(keyword))
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    kanji = soup.select(".character")
    allKanji = [i.get_text() for i in kanji]
    return allKanji


def loadFrames():
    with open("Kanji Data.tsv", encoding="utf-8") as framef:
        reader = csv.reader(framef, delimiter="\t")
        return dict([x[:2] for x in reader])


kfmap = loadFrames()
fkmap = {v: k for k, v in kfmap.items()}


def kanji_to_frame(kanji):
    return kfmap[kanji]


def frame_to_kanji(frame):
    return fkmap[frame]


def lookup_eng_def(word):
    res = requests.get(f"https://jisho.org/search/{word}")
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    try:
        definitions = soup.select(".meaning-meaning")
    except:
        return []
    allDefs = []
    for i in definitions:
        allDefs.append(i.get_text())
    return allDefs


def gen_furigana(word, mode):
    print_plaintext(word, mode)


def kanjify(word):
    res = requests.get(f"https://jisho.org/search/{word}")
    soup = bs4.BeautifulSoup(res.text, features="lxml")
    try:
        kanjified = soup.select("div .text")[4:]
    except:
        return []
    possibleKanjified = [x.get_text() for x in kanjified]
    return possibleKanjified


def openDef(link):
    driver = webdriver.Firefox()
    driver.get(link)


def copy(output):
    pyperclip.copy(output)


def get_story(kanji):
    response = requests.get(f"https://hochanh.github.io/rtk/{kanji}/index.html")
    soup = bs4.BeautifulSoup(response.text, features="lxml")
    paragraphs = soup.select("p")[0].get_text()
    return paragraphs


colors = {"Normal": Fore.WHITE, "FireFox": Fore.GREEN, "Furigana": Fore.YELLOW, "Kanjify": Fore.LIGHTRED_EX,
          "Dictionary": Fore.CYAN, "Info": Fore.LIGHTBLUE_EX}


def printOutput(output, mode):
    colorama.init()
    print(colors[mode] + output)
