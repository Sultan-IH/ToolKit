import os


def notify(tool, message, command=None, icon="tools.png"):
    path_to_icon = "~/Projects/Toolkit/Icons/" + icon
    print(path_to_icon)
    t = '-title ToolKit'
    s = f'-subtitle {tool}'
    m = f'-message "{message}"'
    e = f'-execute "{command}"'
    i = f"-appIcon {path_to_icon}"

    if command:
        os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s, e, i])))
    else:
        os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s, i])))
