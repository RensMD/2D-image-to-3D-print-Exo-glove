import glob
import os
import shutil
from tkinter import *
from tkinter import filedialog

from LineDetect import line_detection


class CreateGui:
    """ Create the GUI """

    # # Init variables
    def __init__(self, root):

        # Initiation of GUI
        self.root = root
        root.title("2D Hand Scanner")
        self.mainframe = Frame(self.root)

        # Browse button to path containing test folders
        self.tkvar_path_top = StringVar(self.root)
        self.tkvar_browse = BooleanVar(self.root)
        self.tkvar_browse = False

        self.browse_label = Label(self.mainframe, text="1. Locate folder with photos")
        self.browse_button = Button(self.mainframe, text="Browse", command=self.start_browse_button)

        # Start button
        self.start_label = Label(self.mainframe, text="Start Processing")
        self.start_button = Button(self.mainframe, text="START", height=1, bg='green', fg="white", font=('Sans', '9', 'bold'), command=self.start_analysis)


    def run(self):
        """ Build GUI """

        # initiation of GUI
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S), columnspan=2, rowspan=17, padx=20, pady=20)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.root.minsize(400, 150)

        # Browse for folder containing test folders
        self.browse_label.grid(row=3, column=1, sticky=W)
        self.browse_button.grid(row=3, column=2, sticky=EW, pady=2)

        # Start button
        self.start_label.grid(row=17, column=1, sticky=W)
        self.start_button.grid(row=17, column=2, sticky=EW)

        self.root.mainloop()

    # # GUI Functionality
    def start_browse_button(self):
        """ Select image """

        self.tkvar_browse = True
        self.tkvar_path_top = str(filedialog.askopenfilename())
        self.browse_button["text"] = os.path.basename(self.tkvar_path_top)

    def start_analysis(self):
        """ Start line detection if image is chosen """

        if not self.tkvar_browse or not self.tkvar_path_top:
            print('\n ERROR: No path selected!')
        else:
            line_detection(self.tkvar_path_top)

def main():
    """ Run code """

    root = Tk()
    gui = CreateGui(root)
    gui.run()


if __name__ == "__main__":
    main()
