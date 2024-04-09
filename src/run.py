import sys
import core.gui.guimanager as gm
import core.ime.imemanager as im
if __name__ == '__main__':
    im.onStart()
    gm.onStart(sys.argv)

