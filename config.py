# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

#Multi display from @ekollof

from typing import List  # noqa: F401
import os
import re
import subprocess
import socket

from Xlib import X, display
from Xlib.ext import randr
from pprint import pprint

d = display.Display()
s = d.screen()
r = s.root
res = r.xrandr_get_screen_resources()._data
lazy.spawn("sh ~/.config/qtile/xrandr_screen_layout.sh")
#Dynamic multiscreen! (Thanks XRandr)
num_screens = 0
for output in res['outputs']:
    print("Output %d:" % (output))
    mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
    print("%s: %d" % (mon['name'], mon['num_preferred']))
    if mon['num_preferred']:
        num_screens += 1

print("%d screens found!" % (num_screens))

try:
    from typing import List  # noqa: F401
except ImportError:
    pass

hostname = socket.gethostname()
homedir = os.getenv("HOME")
mod = "mod4"
colors = {"morado":"#393075", "gris":"#373737"}
keyboards = ['us', 'es']


    

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "b", lazy.spawn("rofi -show run")),
    Key([mod], "n", lazy.spawn("google-chrome-stable")),
    Key([mod], "c", lazy.spawn("code")),
    Key([mod], "f", lazy.spawn("io.elementary.files")),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "control"], "i", lazy.spawn("reboot")),
    Key([mod, "control"], "s", lazy.spawn("shutdown now")),
    Key([mod], "r", lazy.spawncmd()),
# Device shortcuts
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume 0 -2%")),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume 0 +2%")),
    Key([], "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute 0 toggle")),

    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10")),
    Key([], "Print", lazy.spawn("flameshot gui")),

    
    Key([mod], "l", lazy.spawn(f"sh {homedir}/.config/qtile/toggleKbd.sh")),
    Key([mod], "d", lazy.spawn(f"sh {homedir}/.config/qtile/xrandr_screen_layout.sh")),

]

#groups = [Group(i) for i in "123456789"]
def get_key(groupsDict, val): 
    for key, value in groupsDict.items(): 
         if val == value: 
             return key 
  
    return "1"


groupNames = {"1":"1.-Web", "2":"2.-Term", "3":"3", "4":"4", "5":"5", "6":"6", "7":"7", "8":"8", "9":"9"}
groups = [Group(i) for i in groupNames.values()]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], get_key(groupNames, i.name), lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], get_key(groupNames, i.name), lazy.window.togroup(i.name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    layout.Matrix(),
    layout.MonadTall(),
    layout.Floating(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Tile(),
    layout.TreeTab()
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = []
for screen in range(0, num_screens):
    prompt = "{0}@{1}: ".format(os.environ["USER"], hostname)
    screens.append(

#screens = [
        Screen(
            wallpaper="~/wallpapers/cowb.jpg",
            wallpaper_mode="fill",
            top=bar.Bar(
                
                [
                    
                    widget.WindowName(),
                    widget.Prompt(),
                    widget.Clock(format='%a, %-d %b %I:%M %p'),
                    widget.Spacer(length=500),
                    widget.KeyboardLayout(configured_keyboards= keyboards),
                    widget.Image(filename="~/.config/qtile/icons/volume_icon2.png"),
                    widget.Volume(),
                    widget.Spacer(length=25),
                    widget.Systray(),
                    widget.Spacer(length=20),
                    widget.BatteryIcon(update_interval=5, padding=5),
                    widget.Battery(format='{percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W',notify_below=0.2),
                    widget.Spacer(length=5),
                    widget.QuickExit(default_text="  "),
                    widget.Image(filename="~/.config/qtile/icons/power_icon2.png",margin=5),
                    widget.Spacer(length=20),
                ],
                27,
                opacity=0.80,
                background=colors["gris"],
            ),
            bottom=bar.Bar(
                
                [
                    widget.CurrentLayout(),
                    widget.GroupBox(),
                    
                ],
                24,
                opacity=0.70,
            ),
        )#,
    )       
#]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    subprocess.run(["sh", f"{homedir}/.config/qtile/autostart.sh"])



# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"