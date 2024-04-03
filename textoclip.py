from io import BytesIO
import sys
import os
import subprocess
from appdirs import *
from PIL import Image

def send_to_clipboard(path):
    if sys.platform.startswith('win32'):
        import win32clipboard

        image = Image.open(path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    elif sys.platform.startswith("darwin"):
        from Foundation import NSData
        from AppKit import NSPasteboard, NSPasteboardTypePNG
        pasteboard = NSPasteboard.generalPasteboard()
        image_data = NSData.dataWithContentsOfFile_(path)

        pasteboard.clearContents()
        pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)


if (len(sys.argv)<1):
    sys.exit("No code to compile!")

code = R"""\nonstopmode
            \documentclass[convert={density=300},border=2mm]{standalone}
            \usepackage{amsmath,amsthm,amssymb,xcolor,physics}
            \pagecolor{white}
            \begin{document}
                $%s$
            \end{document}""" % str(sys.argv[1])

dir = user_cache_dir("TexToClip", "Marco Miralles")

if (not os.path.exists(dir)):
    os.makedirs(dir)

f = open(dir + "/img.tex", "w")
f.write(code)
f.close()

os.chdir(dir)
subprocess.run(["pdflatex", "-interaction=nonstopmode", "-shell-escape", dir + "/img.tex"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT) 

send_to_clipboard(dir + "/img.png")

print("Copied!")