# FILENAME: plugin_vertigo.py
# AUTHOR: Zachary Krepelka
# DATE: Saturday, March 9th, 2024
# ABOUT: A better way to move vertically in ranger
# ORIGIN: https://github.com/zachary-krepelka/ranger-vertigo.git
# UPDATED: Thursday, March 14th, 2024 at 2:05 AM

from __future__ import (absolute_import, division, print_function)
from ranger.api.commands import Command
import ranger.api
import curses

UP = 'K'
DOWN = 'J'
QUIET = False
HOMEROW = 'asdfghjkl;'

def input():

	input = ''

	window = curses.initscr()

	c = window.getch()

	if c == 27:
		raise Exception()
	else:
		input += chr(c)

	if input.isupper():

		return input

	input += window.getkey()

	return input

def translate(letters):

	if len(letters) == 1:

		return HOMEROW.upper().index(letters) + 1

	elif len(letters) == 2:

		helper = lambda letter: HOMEROW.lower().index(letter) + 1

		digit1, digit2 = helper(letters[0]), helper(letters[1])

		if digit2 == 10:

			digit2 = 0

		return digit1 * 10 + digit2

	else:

		raise Exception()

class Vertigo(Command):

	def execute(self):

		if self.fm.settings.line_numbers == 'false':

			self.fm.notify(
				"Please enable line numbering "
				"to use the vertigo plugin.",
				bad = True
			)

			return

		try:

			count = translate(input())

		except:

			if not QUIET:

				self.fm.notify('Vertigo Canceled', bad = True)

			return

		finally:

			curses.endwin()

		motion = self.arg(1)

		relative = self.fm.settings.line_numbers == 'relative'

		if motion == 'up' and relative:

			self.fm.move(up=count)

		elif motion == 'down' and relative:

			self.fm.move(down=count)

		else:

			motion = 'to'
			self.fm.move(to=count)

		if not QUIET:

			message = 'Vertigo ' + motion  + ' ' + str(count)

			self.fm.notify(message)

HOOK_INIT_OLD = ranger.api.hook_init

def hook_init(fm):

	cmd = "map {key} eval fm.execute_console('Vertigo {direction}')"

	fm.execute_console(cmd.format(key=UP, direction='up'))
	fm.execute_console(cmd.format(key=DOWN, direction='down'))

	HOOK_INIT_OLD(fm)

ranger.api.hook_init = hook_init
