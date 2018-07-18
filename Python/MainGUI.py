import os
from tkinter import *
from tkinter import filedialog

from GetRatio import get_ratio
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
        self.tkvar_path_image = StringVar(self.root)
        self.tkvar_browse = BooleanVar(self.root)
        self.tkvar_browse = False

        self.browse_label = Label(self.mainframe, text="1. Locate folder with photos")
        self.browse_button = Button(self.mainframe, text="Browse", command=self.start_browse_button)

        # Measurement entry
        self.tkvar_measurement = IntVar(self.root)

        self.measurement_label = Label(self.mainframe, text="2. Set measurered length of hand in mm")
        self.tkvar_measurement_entry = Entry(self.mainframe, textvariable=self.tkvar_measurement, justify='center')
        self.tkvar_measurement.set(200)

        # Filename entry
        self.tkvar_filename = StringVar(self.root)

        self.filename_label = Label(self.mainframe, text="3. Set output filename")
        self.tkvar_filename_entry = Entry(self.mainframe, textvariable=self.tkvar_filename, justify='center')
        self.tkvar_filename.set("output")
        
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

        # Measurement Entry
        self.measurement_label.grid(row=4, column=1, sticky=W)
        self.tkvar_measurement_entry.grid(row=4, column=2, sticky=EW)

        # Filename Entry
        self.filename_label.grid(row=5, column=1, sticky=W)
        self.tkvar_filename_entry.grid(row=5, column=2, sticky=EW)

        # Start button
        self.start_label.grid(row=6, column=1, sticky=W)
        self.start_button.grid(row=6, column=2, sticky=EW)

        self.root.mainloop()

    # # GUI Functionality
    def start_browse_button(self):
        """ Select image """

        self.tkvar_browse = True
        self.tkvar_path_image = str(filedialog.askopenfilename())
        self.browse_button["text"] = os.path.basename(self.tkvar_path_image)

    def start_analysis(self):
        """ Start line detection if image is chosen """

        if not self.tkvar_browse or not self.tkvar_path_image:
            print('\n ERROR: No path selected!')
        else:
            line_detection(self.tkvar_path_image, self.tkvar_filename.get(),  get_ratio(self.tkvar_path_image, self.tkvar_measurement.get()))

def main():
    """ Run code """

    root = Tk()
    gui = CreateGui(root)
    gui.run()


if __name__ == "__main__":
    main()
