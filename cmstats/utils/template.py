import locale
locale.setlocale(locale.LC_ALL, "")

def number(input):
    return locale.format("%d", int(input), True)
