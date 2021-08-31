#!/usr/bin/bash

PATH="/bin:/usr/bin"

case "$1" in
    suspend|hibernate)
        exit 0
        ;;
    resume)
        su -c /home/<YOUR_USER_ID>/.local/bin/ite8291r3-restore <YOUR_USER_ID>
        exit 0
        ;;
    *)
        exit 1
esac
