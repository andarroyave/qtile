#!/bin/dash
picom &
nm-applet > /dev/null &>2 &
intern=eDP-1
extern=HDMI-2
if xrandr | grep "$extern connected"; then
    xrandr --output "$intern" --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-1 --off --output "$extern" --mode 1920x1080 --pos 1920x0 --rotate normal > /dev/null 2>&1 &
fi