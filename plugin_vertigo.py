# FILENAME: plugin_vertigo.py
# AUTHOR: Zachary Krepelka
# DATE: Saturday, March 9th, 2024
# ABOUT: A better way to move vertically in ranger
# ORIGIN: https://github.com/zachary-krepelka/ranger-vertigo.git
# PORT OF: https://github.com/prendradjaja/vim-vertigo.git
# UPDATED: Monday, September 8th, 2025 at 2:18 PM


from __future__ import (absolute_import, division, print_function)
from ranger.api.commands import Command
import ranger.api
import curses


UP = 'K'                 #
DOWN = 'J'               # Change these variables
QUIET = False            # for customization
HOMEROW = 'asdfghjkl;'   #


class Vertigo(Command):

    """A command which provides movement via home-row keypresses.

    This command moves ranger's file selector using a non-conventional input
    method in the style of an existing Vim plugin.  The command waits for
    either one or two home-row keypresses to specify the magnitude of the
    movement, mapping 'asdfghjkl;' to '1234567890'.  The direction of the
    movement is specified as an input argument.

    Note:
        This command is not indented to be invoked directly; instead, it
        should be mapped to a key binding.  This is handled later on using
        ranger's initialization hook.  See the bottom of the file.

    Args:
        self.arg(1): The direction of the movement.

            Either 'up', 'down', or 'to'.

    Input:
        Either two lowercase, home-row keypresses representing a two-digit
        number; or one uppercase, home-row keypress representing a
        single-digit number.  The characters are received after invoking the
        command.

    Examples:
        Move the file selector up 12 files:

            :Vertigo up<Enter>as

        Move the file selector down 7 files:

            :Vertigo down<Enter>J

        Move the file selector to the 16th file from the top:

            :Vertigo to<Enter>ah

    Messages:
        The invocation of the command is always accompanied by a resulting
        message.  These can be silenced by setting QUIET = True.

            Vertigo {direction} {count}

                This message is issued under normal operation, indicating
                the direction and magnitude of the moment.

            Vertigo Canceled

                This message is displayed in red if the input is canceled
                via the escape key.

            Vertigo Untranslatable

                This message is displayed in red if the input is invalid.
    """


    @staticmethod
    def __getkey(window):

        """Accepts a single-character input.

        Args:
            window (obj): A curses window.

        Returns:
            str: A single-character input.

        Raises:
            KeyboardInterrupt: If the escape key is pressed.
        """

        if (key := window.getch()) == 27:

            raise KeyboardInterrupt()

        return chr(key)


    @staticmethod
    def __input():

        """Accepts a one-or-two-character input from the user.

        Returns:
            str: One input character if uppercase, two characters otherwise.

        Raises:
            KeyboardInterrupt: If the escape key is pressed.
        """

        window = curses.initscr()

        if (input := Vertigo.__getkey(window)).isupper(): return input

        input += Vertigo.__getkey(window)

        return input


    @staticmethod
    def __translate(letters):

        """Translates home-row keypresses into numbers.

        Args:
            letters (str): A sequence of one or two keys from the home-row.

        Returns:
            int: The home-row number translation.

        Raises:
            ValueError: If the input string is untranslatable.
        """

        caseify = lambda text, cond: text.upper() if cond else text.lower()
        convert = lambda letter, mode: caseify(HOMEROW, mode).index(letter) + 1

        match len(letters):

            case 1: return convert(letters, True)

            case 2:

                digit1, digit2 = [convert(letter, False) for letter in letters]

                return digit1 * 10 + (0 if digit2 == 10 else digit2)

            case _: raise ValueError("faulty length")


    def __notify(self, message, **kwargs):

        """Notify the user with a command-specific message"""

        if QUIET: return

        prefix = self.__class__.__name__

        self.fm.notify(prefix + ' ' + message, **kwargs)


    def execute(self):

        """Executes the command."""

        if self.fm.settings.line_numbers == 'false':

            self.__notify('requires line numbering', bad = True)

            return

        try:

            count = self.__translate(self.__input())

        except ValueError:

            self.__notify('Untranslatable', bad = True)

            return

        except KeyboardInterrupt:

            self.__notify('Canceled', bad = True)

            return

        finally:

            curses.endwin()

        motion = self.arg(1).lower()

        relative = self.fm.settings.line_numbers == 'relative'

        if motion == 'up' and relative:

            self.fm.move(up=count)

        elif motion == 'down' and relative:

            self.fm.move(down=count)

        else:

            motion = 'to'; self.fm.move(to=count)

        self.__notify(motion.capitalize() + ' ' + str(count))


HOOK_INIT_OLD = ranger.api.hook_init

def hook_init(fm):

    """Maps the Vertigo command to key bindings at startup."""

    cmd = "map {key} eval fm.execute_console('Vertigo {direction}')"

    fm.execute_console(cmd.format(key=UP, direction='up'))
    fm.execute_console(cmd.format(key=DOWN, direction='down'))

    HOOK_INIT_OLD(fm)

ranger.api.hook_init = hook_init
