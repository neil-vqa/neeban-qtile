
import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy


# Custom commands to spawn
class Commands:
    browser = "sidekick-browser"
    file_manager = "nautilus --no-desktop"
    pycharm = "pycharm"
    runner = "krunner"
    terminal = "gnome-terminal"
    vscode = "code"


mod = "mod4"


keys = [
    # Switch between windows
    # Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    # Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    # Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    # Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Custom commands bindings
    Key([mod], "b", lazy.spawn(Commands.browser), desc="Launch browser"),
    Key([mod], "f", lazy.spawn(Commands.file_manager), desc="Launch files"),
    Key([mod], "p", lazy.spawn(Commands.pycharm), desc="Launch pycharm"),
    Key([mod], "t", lazy.spawn(Commands.terminal), desc="Launch terminal"),
    Key([mod], "v", lazy.spawn(Commands.vscode), desc="Launch vs code"),
    # Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "space", lazy.spawn(Commands.runner), desc="Launch krunner"),

    # Kill, restart, shutdown
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Cycle through windows
    Key([mod, "control"], "c", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "control"], "j", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "control"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "control"], "i", lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod, "control"], "n", lazy.layout.normalize(),
        desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "control"], "s", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + control + letter of group = switch to & move focused window to group
        Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.Columns(
        border_focus="#ffffff",
        border_width=3,
        margin=5
    ),
    layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Montserrat',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    scale=0.7,
                    padding=10
                ),
                widget.GroupBox(
                    active="000000",
                    borderwidth=0,
                    disable_drag=True,
                    highlight_method="block",
                    block_highlight_text_color="000000",
                    this_current_screen_border="A0E6FF",
                    background="74A3D2",
                    inactive="#ffffff",
                    margin_x=7,
                    padding_x=7
                ),
                # widget.Prompt(
                #     background="#869FAA",
                #     foreground="000000",
                #     padding=10
                # ),
                widget.WindowName(
                    font="Montserrat Bold",
                    padding=10
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Clock(
                    format='%A, %b-%d-%Y | %I:%M %p',
                    padding=10
                ),
                widget.QuickExit(
                    default_text="SHUTDOWN",
                    countdown_format="{} sec"
                ),
            ],
            35,
            background="#002863"
        ),
    ),
]

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
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
