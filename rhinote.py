#!/usr/bin/python
# Filename : rhinote.py

# Rhinote version 0.7.2 A simple "sticky notes" application; Linux version.

# Copyright 2006 by Marv Boyes - greyspace@tuxfamily.org
# http://rhinote.tuxfamily.org
# Please see the file COPYING for license details.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
from os import system

# the root window:
def Rhinote():
	r = Tk()
	t = TextWidget(r, font = ("Helvetica 11"), bg = "#f9f3a9", wrap = "word")
	t.pack(fill='both', expand=1)
	r.geometry("220x235")
	r.title('Rhinote')
	r.mainloop()

# the text widget, and all of its functions.
class TextWidget(Text):
	
	def save_file(self, whatever = None):
		if (self.filename == ""):
			self.save_file_as()
			self.master.title('Rhinote %s' % self.filename)
		else:
			f = open(self.filename, "w")
			f.write(self.get("1.0","end"))
			f.close()
			self.master.title('Rhinote %s' % self.filename)
			# comment out the following line if you don't want a
			# pop-up message every time you save a file:
			tkMessageBox.showinfo ("FYI","File Saved")
	
	def save_file_as(self, whatever=None):
		self.filename = tkFileDialog.asksaveasfilename(filetypes=self._filetypes)
		f = open(self.filename, "w")
		f.write(self.get("1.0", "end"))
		f.close()
		self.master.title('Rhinote %s' % self.filename)
		# comment out the following line if you don't want a
		# pop-up message every time you save a file:
		tkMessageBox.showinfo ("FYI","File Saved")

	def open_file(self, whatever = None, filename=None):
		if not filename:
			self.filename=tkFileDialog.askopenfilename(filetypes=self._filetypes)
			self.master.title('Rhinote %s' % self.filename)
		else:
			self.filename = filename
			self.master.title('Rhinote %s' % self.filename)
		if not (self.filename==""):
			f = open(self.filename, "r")
			f2 = f.read()
			self.delete("1.0", "end")
			self.insert("1.0", f2)
			f.close()
			self.master.title('Rhinote %s' % self.filename)

	def bufferfile(self,event):
		f=open(self.bufferfilename,'w')
		f.write(self.get('1.0','end'))
		self.master.title('Rhinote * %s' % self.filename)
		f.close
	
	def copy(self, event=None):
		self.clipboard_clear()
		text = self.get("sel.first", "sel.last")
		self.clipboard_append(text)

	def cut(self, event):
		self.copy()
		self.delete("sel.first", "sel.last")

	def paste(self, event):
		text = self.selection_get(selection='CLIPBOARD')
		self.insert('insert', text)

	def new_window(self, event):
		Rhinote()

	def printfile(self, whatever=None):
		f=open(self.printfilename, 'w')
		f.write(self.get('1.0','end'))
		f.close
		# 'enscript' formats the text; 'lpr' sends it to the default printer:
		# enscript's -B option suppresses page headers.
		system('enscript -B --word-wrap $HOME/.Rhinoteprintfile > lpr &')
			
	def help(self, whatever=None):
		tkMessageBox.showinfo("Rhinote Help", '''
Ctrl-x : Cut highlighted text
Ctrl-c : Copy highlighted text
Ctrl-v : Paste highlighted text
Ctrl-n : Open new Rhinote note
Ctrl-o : Open file
Ctrl-s : Save current file
Ctrl-a : Save current file as 
   <filename>
Ctrl-p : Print current text
Ctrl-h : Display this help 
   window
''')

	def __init__(self, master, **kw):
		Text.__init__(self, master, **kw)
		self.bind('<Control-c>', self.copy)
		self.bind('<Control-x>', self.cut)
		self.bind('<Control-v>', self.paste)
		self.bind('<Control-n>', self.new_window)
		self.bind('<Control-o>', self.open_file)
		self.bind('<Control-s>', self.save_file)
		self.bind('<Control-a>', self.save_file_as)
		self.bind('<Control-p>', self.printfile)
		self.bind('<Control-h>',self.help)
		self.bind('<KeyPress>',self.bufferfile)  # for use in future features...
		self.bind('<Control-C>', self.copy)
		self.bind('<Control-X>', self.cut)
		self.bind('<Control-V>', self.paste)
		self.bind('<Control-N>', self.new_window)
		self.bind('<Control-O>', self.open_file)
		self.bind('<Control-S>', self.save_file)
		self.bind('<Control-A>', self.save_file_as)
		self.bind('<Control-P>', self.printfile)
		self.bind('<Control-H>',self.help)
		self.master = master
		self.filename = ""
		self.printfilename=os.environ['HOME']+"/.Rhinoteprintfile"
		self.bufferfilename=os.environ['HOME']+"/.Rhinotebufferfile"
		self._filetypes = [
	    ("Text / ASCII","*.txt"),
	    ("Rhinote files","*.rhi"),
            ("All Files","*"),
            ]

# make it so:
if __name__ == '__main__':
	Rhinote()
