import tkinter.filedialog
import tkinter.ttk
from PIL import Image
import numpy as np
import math
import sys


class ImageProcessor:
    scanner_size = 100
    
    def __init__(self, image_name, progress_bar):
        # open image and convert
        try:
            self.image = Image.open(image_name).convert('L')
        
        except(TypeError, FileNotFoundError):
            print("Error: ", sys.exc_info()[0], " has occurred")
        
        # describes center point of brightest section
        self.high_luma_center = [0, 0]
        
        # describes center of image
        self.image_center = [0, 0]
        
        # create numpy array of image
        self.image_data = np.asarray(self.image)
        
        # store the brightest scan value
        self.high_luma_value = 0
        
        # store high luma pixel value
        self.high_luma_center = [0, 0]
        
        # get image center
        self.image_center = self.get_image_center()
        
        # track progress of scanner
        self.progress_bar = progress_bar
        
        # progress tracker
        self.progress = tkinter.IntVar()
    
    # Returns the number of black/0 pixels
    def get_null_pixels(self):
        null_pixels = np.where(self.image_data == 0)[0]
        return null_pixels.size
    
    # Returns the number of pixels value > 0
    def get_active_pixels(self):
        return self.image_data.size - self.get_null_pixels()
    
    # Returns the averages L value of pixels in the image
    def get_average_luma(self):
        return np.average(self.image_data)
    
    # Returns the position of the center element of the image
    def get_image_center(self):
        try:
            return self.image_data.shape[0] // 2, self.image_data.shape[1] // 2
        
        except(TypeError, ZeroDivisionError):
            print("Error: ", sys.exc_info()[0], " has occurrded")
            return [0, 0]
    
    # Returns the size of the image
    def get_image_size(self):
        return self.image_data.size
    
    # Returns the distance between the center of the image and center of the brightest area of the image
    def get_offset(self):
        # reset progress bar
        self.progress.set(0)
        x_distance = self.image_center[0] - self.high_luma_center[0]
        y_distance = self.image_center[1] - self.high_luma_center[1]
        
        return math.sqrt(x_distance * x_distance + y_distance * y_distance)
    
    # Return the center of the brightest area in the images
    def get_brightest_pixel(self):
        self.high_luma_value = 0
        current_luma = 0
        self.high_luma_center = [0, 0]
        scanner_width = scanner_height = self.scanner_size // 2
        
        self.progress_bar.config(maximum=self.image_data.shape[1], variable=self.progress)
        for x_axis in range(0, self.image_data.shape[1]):
            self.progress.set(x_axis)
            for y_axis in range(0, self.image_data.shape[0]):
                scanner = self.image_data[x_axis - scanner_width:x_axis + scanner_width,
                          y_axis - scanner_height:y_axis + scanner_height]
                current_luma = np.mean(scanner)
                if self.high_luma_value < current_luma:
                    self.high_luma_value = current_luma
                    self.high_luma_center = [x_axis, y_axis]
        
        return self.high_luma_center
    
    # Gets the radius of the ratio specified
    def luma_angle_scan(self, scan_ratio):
        neg_x = 0, 0
        pos_x = 0, 0
        neg_y = 0, 0
        pos_y = 0, 0
        h_pixel = 0
        v_pixel = 0
        
        while h_pixel < self.high_luma_center[1]:
            scanner = self.image_data[self.high_luma_center[0] - self.scanner_size // 2:
                                      self.high_luma_center[0] + self.scanner_size // 2,
                                      h_pixel - self.scanner_size // 2:
                                      h_pixel + self.scanner_size // 2]
            
            current_luma = np.mean(scanner)
            
            if current_luma > self.high_luma_value // scan_ratio:
                neg_x = self.high_luma_center[0], h_pixel
                h_pixel = self.high_luma_center[1]
            
            h_pixel += 1
        
        for h_pixel in range(self.high_luma_center[1], self.image_data.shape[0]):
            scanner = self.image_data[self.high_luma_center[0] - self.scanner_size // 2:
                                      self.high_luma_center[0] + self.scanner_size // 2,
                                      h_pixel - self.scanner_size // 2:
                                      h_pixel + self.scanner_size // 2]
            
            current_luma = np.mean(scanner)
            
            if current_luma > self.high_luma_value // scan_ratio:
                pos_x = self.high_luma_center[0], h_pixel
        
        while v_pixel < self.high_luma_center[0]:
            scanner = self.image_data[v_pixel - self.scanner_size // 2:
                                      v_pixel + self.scanner_size // 2,
                                      self.high_luma_center[1] - self.scanner_size // 2:
                                      self.high_luma_center[1] + self.scanner_size // 2]
            
            current_luma = np.mean(scanner)
            
            if current_luma > self.high_luma_value // scan_ratio:
                neg_y = v_pixel, self.high_luma_center[1]
                v_pixel = self.high_luma_center[0]
            
            v_pixel += 1
        
        for v_pixel in range(self.high_luma_center[0], self.image_data.shape[1]):
            scanner = self.image_data[v_pixel - self.scanner_size // 2:
                                      v_pixel + self.scanner_size // 2,
                                      self.high_luma_center[1] - self.scanner_size // 2:
                                      self.high_luma_center[1] + self.scanner_size // 2]
            
            current_luma = np.mean(scanner)
            if current_luma >= self.high_luma_value // scan_ratio:
                pos_y = v_pixel, self.high_luma_center[1]
        
        avg_diameter = ((pos_x[1] - neg_x[1]) + (pos_y[0] - neg_y[0])) // 2
        return avg_diameter
