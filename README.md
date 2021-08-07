# RTK-Lookup
What is RTK-Lookup? Well, if you've finished learning all the kanji, but you don't know how to read it, since you only know the english word accociated with it, this program can be quite handy. You can enter the following:
- A kanji
- A keyword
- A frame number

Of course, there's more options so lets have a look at some of the features. This is an inspired project from [here](https://github.com/klieret/rtk-lookup)

## Overview of available modes/ commands
So this is a command line prompt type program that works by changing modes and entering commands. Here are the commands that are available in the command:
- `--q` This is a simple command that just quits out of the program
- `--h` This command displays the help menu in case you want to know the available modes/commands
- `--hist` This command shows the history which displays all the commands you have entered in
- `--c` This is a helpful command that activates copying. Whenver you get output, you will be asked on which ouput you would like to have copied to the clipboard
- `--clear` This simply clears the command line once its getting cluttered

Those were the available commands, and now I will be showing the available modes. At all time you will be in atleast one mode and you can switch to different modes for different ouput

- Normal(`-n`) This goes back to normal mode which just displays the corresponding word that it formed from input.
- FireFox(`-b`) This is a mode that whenever you enter in input, a definition entry will be displayed on FireFox
- Furigana(`-f`) This is similar to the Normal mode except always displays furigana for ouput
- Kanjify(`-k`) This is a special mode that uses only hiragana input, and apply the proper kanji to it, and show it on the ouput
- Dictionary(`-d`) This is a mode that displays a set of definition entries found on the ouput for the input entered
- Info(`-i`) This is a mode that requires a kanji to be as an input, and will display all the follwing information for it, such as the keyword, frame, story

## Examples of Modes
### Normal
```
(Normal) finish わる
終わる
(Normal) 336 1103
警察
```
### Furigana
```
(Furigana) 喧嘩
喧嘩(けんか)
```
### Kanjify
```
(Kanjify) せいちょう
成長
```
### Dictionary
```
(Dictionary) 場所
place; location; spot; position
```
### Info
```
(Info) 後
-------後--------
Keywords:  behind, back, later, 
Frame:  1379
Story:  Line . . . cocoon . . . walking legs.
```
