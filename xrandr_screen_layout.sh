#!/bin/dash

intern=eDP-1
extern=HDMI-2

if xrandr | grep "$extern connected 1920x1080+1920+0"; then
    xrandr --output "$intern" --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-1 --off --output "$extern" --mode 1920x1080 --pos 0x0 --rotate normal &
elif xrandr | grep "$extern connected 1920x1080+0+0"; then
    xrandr --output "$intern" --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-1 --off --output "$extern" --mode 1920x1080 --pos 1920x0 --rotate normal &
elif xrandr | grep "$extern connected (normal"; then
    xrandr --output "$intern" --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-1 --off --output "$extern" --mode 1920x1080 --pos 1920x0 --rotate normal &
elif xrandr | grep "$extern disconnected"; then
    xrandr --output "$intern" --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-1 --off --output "$extern" --off &
fi


