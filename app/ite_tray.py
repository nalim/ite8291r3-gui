from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from ite8291r3_ctl import ite8291r3
import webbrowser
import os
import usb

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

home = os.environ['HOME']
config_file = home + "/.config/ite8291r3-ctl"
#print(home);

#ite = ite8291r3.get()
#ite_dev = ite8291r3.get()

def store_config(opts):
    f = open(config_file, "w")
    f.write(opts)
    f.close()

try:
    f = open(config_file)
    ite_cfg_data=f.read()
    f.close
    ite_cfg=ite_cfg_data.rstrip().split(',')
    del ite_cfg[-1]
except FileNotFoundError:
    ite_cfg = ["effect", "rainbow"]

#print(ite_cfg)
exit

#def brightness(delta):
#    d = ite()
#    d.set_brightness(d.get_brightness() + delta)

def effect(h, data):
    h.set_effect(data(**{"brightness": h.get_brightness()})) 

def cfg():
    return ite_cfg

def ite():
    return ite8291r3.get()
    #return ite_dev

def itel(l, cfg = None, brightness = False):
    h = ite()
    l(h)
    dev = h.channel.dev
    if cfg:
        ite_cfg=cfg
        cfg_data=",".join(cfg)
        #print(cfg_data)
        if brightness:
            b = h.get_brightness()
            cfg_data = cfg_data + ',' + str(b)
        store_config(cfg_data)
    dev._ctx.dispose(dev)

app = QApplication([])
app.setQuitOnLastWindowClosed(False)
  
# Adding an icon
icon = QIcon("icon.png")
  
# Adding item on the menu bar
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

menu = QMenu()


effect_menu = QMenu("Effects")

# Creating the options dynamically
qactions_effects = {}
for k,v in ite8291r3.effects.items():
    action = QAction(k.capitalize())
    qactions_effects[k] = action
    effect_menu.addAction(action)
    #action.triggered.connect(lambda checked, key=k, value=v : itel(lambda h: h.set_effect(value()), ["effect", key], True))
    action.triggered.connect(lambda checked, key=k, value=v : itel(lambda h: effect(h, value), ["effect", key], True))

menu.addMenu(effect_menu)


colors = {"white":  (255, 255, 255),
          "red":    (255,   0,   0),
          "orange": (255,  28,   0),
          "yellow": (255, 119,   0),
          "green":  (  0, 255,   0),
          "blue":   (  0,   0, 255),
          "teal":   (  0, 255, 255),
          "purple": (255,   0, 255),
          }

color_menu = QMenu("Mono Color")

qactions_colors = {}
for k,v in colors.items():
    action = QAction(k.capitalize())
    qactions_colors[k] = action
    color_menu.addAction(action)
    action.triggered.connect(lambda checked, key=k, value=v : itel(lambda h : h.set_color(value), ["monocolor", key], True))

menu.addMenu(color_menu)



menu.addSeparator() #================================================================


incbrightness = QAction("Increase Brightness")
menu.addAction(incbrightness)
incbrightness.triggered.connect(lambda: itel(lambda h : h.set_brightness(min(h.get_brightness() + 10, 50)), cfg(), True))

decbrightness = QAction("Decrease Brightness")
menu.addAction(decbrightness)
decbrightness.triggered.connect(lambda : itel(lambda h : h.set_brightness(max(h.get_brightness() - 10, 0)), cfg(), True))

menu.addSeparator() #================================================================


turnoff = QAction("Turn Off Keyboard Backlight")
menu.addAction(turnoff)
turnoff.triggered.connect(lambda : itel(lambda h : h.turn_off(), ["off"]))

#freeze = QAction("Freeze Animation")
#menu.addAction(freeze)
#freeze.triggered.connect(lambda: itel(lambda h : h.freeze()))

testpattern = QAction("Test Pattern")
menu.addAction(testpattern)
testpattern.triggered.connect(lambda : itel(lambda h : h.test_pattern()))

menu.addSeparator() #================================================================


about = QAction("About")
project_webpage_url = "https://github.com/salihmarangoz/ite8291r3-gui"
about.triggered.connect(lambda : webbrowser.open(project_webpage_url) )
menu.addAction(about)


def exit_confirmation():
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Question)
   msgBox.setText("Are you sure to exit?")
   msgBox.setWindowTitle("Keyboard Backlight GUI")
   msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Yes:
      app.quit()

# To quit the app
quit = QAction("Quit")
quit.triggered.connect(exit_confirmation)
menu.addAction(quit)


# Adding options to the System Tray
tray.setContextMenu(menu)
  
app.exec_()
