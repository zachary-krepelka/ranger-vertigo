# Ranger Vertigo

<!--
	FILENAME: README.md
	AUTHOR: Zachary Krepelka
	DATE: Saturday, March 9th, 2024
	ABOUT: A better way to move vertically in ranger
	ORIGIN: https://github.com/zachary-krepelka/ranger-vertigo.git
	UPDATED: Sunday, September 7th, 2025 at 2:04 AM
-->

`plugin_vertigo.py` is a port of `vertigo.vim` to ranger.

- [Background](#background)
- [Introduction](#introduction)
- [Usage](#usage)
- [Installation](#installation)
- [Customization](#customization)

<!----------------------------------------------------------------------------->

## Background

A background synopsis for the unacquainted.

* What is [Vim][1]?  Vim is a **programmable** text editor beloved by
  programmers.  It is extended using its own built-in scripting language, giving
  rise to a rich ecosystem of plugins. Vim inherits from a long lineage of text
  editors before it. It is a successor to the original vi text editor that
  shipped with the Unix operating system. It exists in both CLI and GUI
  environments.

* What is [ranger][2]?  Ranger is a file manager with a text-based user
  interface. Its keybindings take inspiration from the vi text editor.  Ranger
  can also be extended using plugins written in Python.

* What is [`vertigo.vim`][3]?  Vim Vertigo is a plugin for the Vim text editor
  that aims to improve an aspect of its user interface.  It resonates with touch
  typists who find comfort in keeping their hands on the homerow.

<!----------------------------------------------------------------------------->

## Introduction

`plugin_vertigo.py` is a plugin for ranger, an open source file manager for the
Linux console. It aims to port the functionality of Vim Vertigo to ranger.  To
appreciate this plugin, you should first try out the original Vim plugin.

> Vertigo.vim is a Vim plugin is based on a simple idea: that moving up and down
> using relative line numbers (e.g., 3j, 15k) is a very simple and precise way
> of moving around vertically, and shouldn't require your hands to leave home
> row.

<!----------------------------------------------------------------------------->

## Usage

The functionality of this plugin rests on a built-in feature of ranger.

```text
:set line_numbers relative
```

By typing the above command in ranger, the user will enable relative line
numbering. Each file in the center column is numbered relative to the currently
selected file to show the distance to any other file.  Let's examine how
navigation works with this feature, both with and without this plugin.

### Vanilla

Suppose you want to navigate to a particular file in the current directory.  In
ranger, you observe that the desired file is 14 entries below the currently
selected file using relative line numbering. To navigate to that file, it
suffices to type `14j`, employing the standard vi keybindings. This is a quick
and precise way to select a file, especially comparative to using a mouse in a
file manager having a graphical user interface.

### Modded

*Even so, we can do better.* Typing numbers is cumbersome. It is easier to keep
your fingers on the homerow.  With this plugin, type `K` for up or `J` for down
to activate jump mode.  Ranger then waits for two home-row keypresses
representing a two-digit number, mapping `asdfghjkl;` to `1234567890`.  So
instead of typing `14j`, you can type `Jaf`. For one-digit numbers, just hit
shift. For example, use `KF` to go up four.

<div align="center">

| left<br>pinky | left<br>ring | left<br>middle | left<br>index | left<br>index | right<br>index | right<br>index | right<br>middle | right<br>ring | right<br>pinky |
| -------- | - | - | - | - | - | - | - | - | - | - |
| Physical | a | s | d | f | g | h | j | k | l | ; |
| Virtual  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |

</div>


<!----------------------------------------------------------------------------->

## Installation

Installation is as easy as copying `plugin_vertigo.py` into the following
directory.

```text
~/.config/ranger/plugins
```

A single command should suffice, which you can easily copy and paste with the
button to your right.

```bash
wget -P ~/.config/ranger/plugins/ https://raw.githubusercontent.com/zachary-krepelka/ranger-vertigo/main/plugin_vertigo.py
```

<!----------------------------------------------------------------------------->

## Customization

Customization is achieved by altering constants in `plugin_vertigo.py`.

```python
UP = 'K'
DOWN = 'J'
QUIET = False
HOMEROW = 'asdfghjkl;'
```

These will be found at the top of the file.  Dvorak users will want to change
the `HOMEROW` variable.

```bash
sed -i 's/asdfghjkl;/aoeuidhtns/' ~/.config/ranger/plugins/plugin_vertigo.py
```

<!-- References and Footnotes ------------------------------------------------->

[1]: https://en.wikipedia.org/wiki/Vim_(text_editor)
[2]: https://en.wikipedia.org/wiki/Ranger_(file_manager)
[3]: https://github.com/prendradjaja/vim-vertigo.git
[4]: https://github.com/zachary-krepelka/ranger-vertigo.git
