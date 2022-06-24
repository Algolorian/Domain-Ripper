import clipboard
import pyautogui
import keyboard
import time

pyautogui.FAILSAFE = False

file = open('error.txt', 'r')
error = file.read()
file.close()

file = open("web-ripped-urls.txt", 'w')
file.write('')
file.close()


file = open('web-urls.txt', 'r')
urls_todo = file.read().split('\n')
file.close()

urls_done = []
urls_todo_next = []
sources = []
source_book = ''
book = ''
book_condensed = ''
phase = 0


def browse(address):
    print('Address:', address)
    pyautogui.hotkey('win', 'r')
    time.sleep(0.2)
    pyautogui.typewrite('chrome')
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.2)
    pyautogui.typewrite(address)
    time.sleep(0.2)
    pyautogui.press('backspace')
    time.sleep(0.2)
    pyautogui.press('enter')


def get_page():
    global error
    loop = 0
    while True:
        if loop % 10 == 0:
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'l')
            time.sleep(0.2)
            pyautogui.press('enter')
        loop += 1
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'u')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.2)
        if clipboard.paste() == error:
            continue
        else:
            break
    pyautogui.hotkey('ctrl', 'w')
    return clipboard.paste()


def collect(address):
    global urls_done, urls_todo, urls_todo_next, book, phase, complete, book_condensed, source_book
    level = address
    browse(address)
    loop = 0

    while True:
        loop += 1
        page = get_page()
        if loop == 20:
            browse(address)
        book += page
        source_count = 0
        url_count = 0
        for line in book.split('\n'):
            if '<a ' in line:
                book_condensed += line + '\n'
            if '<source' in line:
                source_book += line + '\n'
        try:
            for line in book_condensed.split('\n'):
                line = line[line.index('href="') + 6:]
                line = line[:line.index('"')]

                link = level + '/' + line + '/'
                if link not in urls_done:
                    # print(link)
                    url_count += 1
                    urls_done.append(link)
                    urls_todo_next.append(link)
        except:
            pass
        try:
            for line in source_book.split('\n'):
                line = line[line.index('src="') + 5:]
                line = line[:line.index('"')]

                link = level + '/' + line
                if link not in sources:
                    # print(link)
                    source_count += 1
                    urls_done.append(link)
                    urls_todo_next.append(link)
                    sources.append(link)
        except:
            pass

        if keyboard.is_pressed('esc'):
            break
        elif keyboard.is_pressed('shift'):
            time.sleep(60)
        if url_count == 0 and source_count == 0:
            continue
        else:
            break


while True:
    phase += 1
    for url in urls_todo:
        print('Phase:', phase, 'URL:', urls_todo.index(url) + 1, 'URLs:', len(urls_todo))
        source_book = ''
        book = ''
        book_condensed = ''
        collect(url)

    # print('Saving URLs')
    file = open("web-ripped-urls.txt", 'w')
    for line in urls_todo_next:
        if line not in sources:
            file.write(line + '\n')
    file.close()

    urls_todo_next = []

    # print('Saving Media')
    file = open("web-ripped-media.txt", 'a')
    for line in sources:
        file.write(line + '\n')
    file.close()

    file = open('web-ripped-urls.txt', 'r')
    urls_todo = file.read().split('\n')
    file.close()
    urls_todo = urls_todo[:-1]

    file = open("web-ripped-urls.txt", 'w')
    file.write('')
    file.close()

    if len(urls_todo) == 0:
        break
