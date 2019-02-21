import tkinter as tk
import tkinter.filedialog
import tkinter.ttk
import os
from threading import Thread
from CleanString import CleanString
from image_processor import ImageProcessor

# global variables
screen_height = 600
screen_width = 800


class App(tk.Frame):
    folder = tkinter.filedialog
    out_file_name = " "
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        # boolean for optional test
        self.run_half_angle = tkinter.IntVar()
        self.run_offset = tkinter.IntVar()
        self.run_wide_angle = tkinter.IntVar()
        self.create_widgets()
        self.HALF = 2
        self.WIDE = 5
        self.folder = self.folder
        
    def create_widgets(self):
        # create widgets and configure
        
        # create exit button
        self.btn_quit = tk.Button(self, text='Exit', command=self.quit, width=30, pady=5)
        
        # create open folder button
        self.btn_open_folder = tk.Button(self, text='Open Folder', command=self.open_folder, width=30, pady=5)
        
        # create process images button
        self.btn_process_images = tk.Button(self, text='Process Images', command=self.start_process_images, width=100)
        
        # create status text box
        self.status_text = tk.Text(self, width=80, height=10)
        
        # create progress bar
        self.progress_bar = tkinter.ttk.Progressbar(self, mode="determinate", length=screen_width)
        
        # create options label
        self.lbl_options = tkinter.Label(self, text="Scanner Options")
        
        # create check box array
        self.check_half_angle = tk.Checkbutton(self, text="Half Angle", variable=self.run_half_angle)
        self.check_wide_angle = tk.Checkbutton(self, text="Wide Angle", variable=self.run_wide_angle)
        self.check_offset = tk.Checkbutton(self, text="Offset", variable=self.run_offset)
        
        # place widgets
        self.btn_open_folder.grid(row=0, column=0, stick=tk.W, pady=5, padx=5)
        self.btn_quit.grid(row=0, column=3, stick=tk.E, pady=5, padx=5)
        self.status_text.grid(row=1, columnspan=4)
        self.lbl_options.grid(row=2, column=0, stick=tk.W)
        self.check_half_angle.grid(row=2, column=1, stick=tk.W)
        self.check_wide_angle.grid(row=2, column=2, stick=tk.W)
        self.check_offset.grid(row=2, column=3, stick=tk.W)
        self.btn_process_images.grid(row=4, column=0, columnspan=4)
        self.progress_bar.grid(row=3, columnspan=4)
        
        # initialize GUI widgets to default state
        self.btn_process_images.config(state="disabled")
        self.status_text.insert(1.0, "Please select folder...")
        
    def open_folder(self):
        # create file dialog object
        self.folder.directory = self.folder.askdirectory()
        
        # print folder name to dialog
        self.status_text.delete(1.0, "end")
        self.status_text.insert(1.0, "Ready to process images in directory: " + self.folder.directory + "\n")
        
        # enabled process button
        self.btn_process_images.config(state="normal")
        
    def process_images_(self):
        # set file name for writing data
        self.out_file_name = "_LED_DATA.txt"
        # configure status window
        self.status_text.configure(background="black", foreground="white")
        # print to status screen
        self.status_text.insert(2.0, "Writing data to " + self.out_file_name + '\n')
        
        # set base title string
        title = "File,Average_Luma,Luma_Center,Total_Area"

        # open data file for write operations
        self.out_file = open(str(self.folder.directory + '/' + self.out_file_name), 'w+')
        # cycle through files in directory

        if self.run_half_angle.get() == 1:
            # add additional field to title
            title += ",Half_Angle"

        if self.run_wide_angle.get() == 1:
            # add additional field to title
            title += ",Wide_Angle"

        if self.run_offset.get() == 1:
            # add additional field to title
            title += ",offset"
            
        # format strings for write
        title += '\n'
        
        # Write data to file CSV style
        self.out_file.write(title)
        for file in os.listdir(self.folder.directory):
            
            # locate image files of proper type
            if file.endswith(".jpg") or file.endswith(".png"):
                # print file name to UI
                self.status_text.insert(3.0, "Processing file: " + file + '\n')
                
                # generate file name for image
                image_name = self.folder.directory + '/' + file
                image_p = ImageProcessor(image_name, self.progress_bar)
                
                # run luma center scan
                brightest_pixel = str([image_p.get_brightest_pixel()])
                
                # generate string cleaner for pixel data
                clean_string = CleanString(brightest_pixel)
                
                # clean string
                brightest_pixel = clean_string.remove_token(',')

                # construct base data string
                data_string = "{0},{1},{2},{3}".format(file, image_p.get_average_luma(), brightest_pixel
                                                      , image_p.get_active_pixels())
                
                # run half angle can if checkbutton is selected
                if self.run_half_angle.get() == 1:
                    # add additional data item to data string
                    data_string += "," + str(image_p.luma_angle_scan(self.HALF))

                # run wide angle scan if user selects
                if self.run_wide_angle.get() == 1:
                    # add additional data item to data string
                    data_string += "," + str(image_p.luma_angle_scan(self.WIDE))
                    
                # run offset if user selects
                if self.run_offset.get() == 1:
                    # add additional data item to data string
                    data_string += "," + str(image_p.get_offset())
        
                data_string += '\n'
                # print file name to UI
                self.status_text.insert(3.0, "Complete! " + data_string)
                self.out_file.write(str(data_string))
                
        self.status_text.config(background="green", foreground="white")
        self.status_text.insert(3.0, "\n***ALL FILES PROCESSED***\n")
        self.out_file.close()

    def start_process_images(self):
        thread = Thread(target=self.process_images_)
        thread.start()


image_processor = App()
image_processor.master.title("Luma Scanner")
image_processor.master.maxsize(screen_width, screen_height)
image_processor.mainloop()
