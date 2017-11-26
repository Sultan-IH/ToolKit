import os


def notify(tool, message, command=None, icon="./Icons/tools.png"):
    t = '-title ToolKit'
    s = f'-subtitle {tool}'
    m = f'-message "{message}"'
    e = f'-execute "{command}"'
    i = f"-appIcon {icon}"

    if command:
        os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s, e, i])))
    else:
        os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s, i])))
