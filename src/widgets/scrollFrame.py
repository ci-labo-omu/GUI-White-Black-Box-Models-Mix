"""
The ScrollFrame is a generic frame that has a scrollable menu and display new fields depending on
selected values.
"""

import customtkinter as ctk
from constants import Models, BOTH
from widgets.CTkScrollableDropdown.CTkScrollableDropdown.ctk_scrollable_dropdown import CTkScrollableDropdown

class ScrollFrame(ctk.CTkFrame):
    """
    This class represents a frame with a scollable menu. The said menu is constitued of provided elements.
    The frame display input fields depending on the element selected in the scrollable menu.
    
    :param master: the master frame/window of this frame
    :param name: displayed name at the top of the frame, default to "Scrollable Frame"
    :type name: str, optional
    :param models: list of models names (strings), used for display and frames loading, default to []
    :type models: [str]
    """
        
    def __init__(self, master, name="Scrollable Frame", models=[]):
        """
        Constructor method
        """

        super().__init__(master)

        self.grid_propagate(False) # Prevent the frame from changing size depending on widgets inside
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Display frame name
        ctk.CTkLabel(self, text=name).grid(row=0, column=0, padx=10, pady=10, sticky="ewn")

        # Values of the scrollable menu
        self.scrollValues = models

        # Scrollable menu
        self.optionmenu = ctk.CTkOptionMenu(self, width=250, values=["Select a classifier"])
        self.optionmenu.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.ctkscroll = CTkScrollableDropdown(self.optionmenu, values=self.scrollValues, command=self.on_dropdown_select)

        # Set up frames
        self.current_frame = None # Name of the frame currently displayed
        self.frames = {} # Dictionnary associating frame name to frame class
    
    def on_dropdown_select(self, frame):
        """
        Modify the displayed value on the scrollable menu and update displayed fields

        :param frame: selected element in the scrollable menu to display fields
        :type frame: str
        """
        self.optionmenu.set(frame)  
        self.update_fields(frame)


    def update_fields(self, frame):
        """
        Update displayed fields depending on the provided frame name

        :param frame: selected element in the scrollable menu to display fields
        :type frame: str
        """
        # Remove current displayed frame if existing
        if self.current_frame != None:
            self.frames[self.current_frame].grid_remove()

        # Instantiate the frame if not already existing (and stored in self.frames)
        if frame not in self.frames:
            self.frames[frame] =  BOTH[frame](self)


        self.current_frame = frame
        self.frames[frame].grid(row=2, column=0, padx=10, pady=10, sticky="ewns")


    def get(self):
        return self.current_frame, self.frames[self.current_frame].get()
    
    def freeze(self):
        """
        Freeze all fields (disable)
        """
        self.optionmenu.configure(state='disabled')
        if self.current_frame != None:
            self.frames[self.current_frame].freeze()

    def unfreeze(self):
        """
        Unfreeze all fields (enable)
        """
        self.optionmenu.configure(state='normal')
        if self.current_frame != None:
            self.frames[self.current_frame].unfreeze()