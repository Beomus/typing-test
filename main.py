import curses
from curses import wrapper
import time


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Speed Typing Test")
    stdscr.addstr("\nPress any key to start")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        color = curses.color_pair(1) if char == target[i] else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr):
    target_text = 'hello world this is a test text line!'
    current_text = []
    wpm = 0
    start_time = time.time()

    # no delay so WPM can be continuously calculated
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)

        # chars per minutes divided by 5 is wpm assuming avg word has 5 chars
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            # re-enable delay
            stdscr.nodelay(False)
            break

        # since there's no delay, this will throw an error
        # handling that error by using "try"
        try:
            key = stdscr.getkey()
        except:
            continue
        
        # check for esc key
        if ord(key) == 27:
            break
        
        # handle backspaces
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(2, 0, "Done. \nPress any key to continue [escape to quit].")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


if __name__ == "__main__":
    wrapper(main)
