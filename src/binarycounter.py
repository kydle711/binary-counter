import os.path

import tkinter as tk
import customtkinter as ctk

from PIL import Image

from settings import Settings


class BinaryCounter:
    """ Configurable app to display a counter in binary """

    def __init__(self):
        """ INIT """

        """ Instantiate widget variables """
        self.binary_frame = None
        self.hex_frame = None
        self.base_frame = None
        self.decimal_label = None
        self.hex_label = None
        self.reset_button = None
        self.pause_play_button = None
        self.speed_selection = None
        self.hex_counter_checkbox = None
        self.bit_selection_menu = None

        """ Settings """
        self.speed = Settings.speed
        self.num_bits = Settings.num_bits  # Defaults to 8
        self.hex_display_flag = Settings.hex_display  # Defaults to False
        self.reset_button_color = Settings.RESET_BUTTON_COLOR
        self.button_font = Settings.BUTTON_FONT
        self.text_color = Settings.TEXT_COLOR
        self.display_font = Settings.DISPLAY_FONT
        self.bg_color = Settings.BACKGROUND_COLOR
        self.icon_size = Settings.ICON_SIZE
        self.play_button_color = Settings.PLAY_BUTTON_COLOR
        self.pause_button_color = Settings.PAUSE_BUTTON_COLOR

        """ Setup """
        self.count = 0
        self.pause_flag = False
        self.bit_list = []
        self.max_num = 2 ** self.num_bits - 1

        self.app = ctk.CTk()
        self.icon_photo_path = os.path.join("assets", "icon.png")
        self.pause_icon = ctk.CTkImage(Image.open(os.path.join("assets", "pause.png")),
                                       size=self.icon_size)
        self.play_icon = ctk.CTkImage(dark_image=Image.open(os.path.join("assets", "play.png")),
                                      size=self.icon_size)

        self.configure_app()
        self.setup_base_frame()
        self.setup_binary_display()
        self.configure_permanent_widgets()
        self.grid_permanent_widgets()

    def update_counter(self):
        if self.count == self.max_num:
            self.count = 0
        else:
            self.count += 1

        self.update_display()

        if not self.pause_flag:
            self.app.after(self.speed, self.update_counter)

    def update_display(self):
        bit_size = '0' + str(self.num_bits) + 'b'
        my_bin_num = f"{self.count:{bit_size}}"
        for i in range(self.num_bits):
            self.bit_list[i].configure(text=my_bin_num[i])

        self.decimal_label.configure(text=str(self.count))

    def reset_counter(self):
        self.count = 0
        self.update_display()

    def start_stop_count(self):
        if not self.pause_flag:
            self.pause_flag = True
            self.pause_play_button.configure(image=self.play_icon,
                                             fg_color=self.play_button_color)
        else:
            self.pause_flag = False
            self.pause_play_button.configure(image=self.pause_icon,
                                             fg_color=self.pause_button_color)
            self.update_counter()

    def configure_app(self):
        self.app.geometry(f"{self.num_bits * 44}x250")
        self.app.title("Binary Counter")
        self.app.iconphoto(True, tk.PhotoImage(file=self.icon_photo_path))
        self.app.configure(fg_color=self.bg_color)

    def setup_base_frame(self):
        self.base_frame = ctk.CTkFrame(self.app, fg_color=self.bg_color)
        self.base_frame.pack(fill='both', expand=True, padx=30, pady=30)
        for i in range(4):
            self.base_frame.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.base_frame.grid_columnconfigure(i, weight=1)

    def setup_binary_display(self):
        self.binary_frame = ctk.CTkFrame(self.base_frame, fg_color=self.bg_color)
        self.binary_frame.grid(row=0, column=0, columnspan=4)

        for i in range(0, self.num_bits):
            self.binary_frame.grid_columnconfigure(i, weight=1)
            bit_label = ctk.CTkLabel(master=self.binary_frame,
                                     font=self.display_font,
                                     text_color=self.text_color,
                                     bg_color=self.bg_color,
                                     text='0', padx=5)
            self.bit_list.append(bit_label)
            bit_label.grid(row=1, column=i)

    def setup_hex_display(self):
        self.hex_frame = ctk.CTkFrame(master=self.base_frame, fg_color=self.bg_color)

    def configure_permanent_widgets(self):
        self.reset_button = ctk.CTkButton(self.base_frame, text="RESET",
                                          font=self.button_font,
                                          text_color=self.text_color,
                                          fg_color=self.reset_button_color,
                                          hover_color='dark red',
                                          command=self.reset_counter)

        self.decimal_label = ctk.CTkLabel(self.base_frame, font=self.display_font,
                                          text_color=self.text_color,
                                          bg_color=self.bg_color, text=str(self.count))

        self.pause_play_button = ctk.CTkButton(self.base_frame,
                                               font=self.button_font,
                                               text_color=self.text_color,
                                               bg_color=self.bg_color,
                                               fg_color=self.pause_button_color,
                                               width=80, height=80, text="",
                                               image=self.pause_icon,
                                               command=self.start_stop_count)

    def grid_permanent_widgets(self):
        self.reset_button.grid(row=2, column=0)
        self.decimal_label.grid(row=3, column=0, columnspan=self.num_bits)
        self.pause_play_button.grid(row=2, column=1)
