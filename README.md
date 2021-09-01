# ite8291r3-gui

**Tested on Tuxedo Stellaris 15 and XMG Neo 17 E21**

**Still in development!**

**Image below may be outdated**

![](imgs/ss.png)

## Install

```bash
$ bash install.sh
```

- You can reboot and run `ite8291r3-ctl test-pattern` for testing if installation of `ite8291r3-ctl` was done correctly.

- Currently there is no saving feature. If you would like to setup a default mod then run `sudo crontab -e`  and add this line:

```
# DEFAULT KEYBOARD BACKLIGHT MODE AFTER REBOOT
@reboot /usr/local/bin/ite8291r3-ctl effect rainbow
```

- You can install files from systemd folder to restore keyboard state after resume/hibernate (needs howto). 

- Reboot



## Extra: Lightbar for Stellaris 15

Currently lightbar is not managed by this app. However you can add an animation to the lightbar.

- Make sure `tuxedo_keyboard` is installed.

```
sudo crontab -e
```

- Add this line then save

```
# ENABLE LIGHTBAR ANIMATION
@reboot echo 1 > /sys/devices/platform/tuxedo_keyboard/leds/lightbar_animation::status/brightness
```

- Reboot

