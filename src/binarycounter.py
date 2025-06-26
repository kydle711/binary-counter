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
        self.hex_frame = None
        self.base_frame = None
        self.row1_frame = None
        self.row2_frame = None
        self.row3_frame = None
        self.decimal_label = None
        self.hex_label = None
        self.reset_button = None
        self.pause_play_button = None
        self.speed_selection_menu = None
        self.bit_selection_menu = None

        """ Settings """
        self.speed = 400  # Start at medium speed
        self.num_bits = Settings.num_bits  # Defaults to 8
        self.hex_display_flag = Settings.hex_display  # Defaults to False
        self.reset_button_color = Settings.RESET_BUTTON_COLOR
        self.hover_color = Settings.HOVER_COLOR
        self.button_font = Settings.BUTTON_FONT
        self.text_color = Settings.TEXT_COLOR
        self.display_font = Settings.DISPLAY_FONT
        self.speed_select_font = Settings.SPEED_SELECT_FONT
        self.speed_select_color = Settings.SPEED_SELECT_COLOR
        self.bit_select_color = Settings.BIT_SELECT_COLOR
        self.bit_select_font = Settings.BIT_SELECT_FONT
        self.bg_color = Settings.BACKGROUND_COLOR
        self.icon_size = Settings.ICON_SIZE
        self.play_button_color = Settings.PLAY_BUTTON_COLOR
        self.pause_button_color = Settings.PAUSE_BUTTON_COLOR
        self.speed_options = Settings.SPEED_OPTIONS

        """ Setup """
        self.count = 0
        self.hex_count = 0x00
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
        self.setup_row_frames()
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
        self.hex_label.configure(text=str(hex(self.count)))

    def reset_counter(self):
        self.count = 0
        self.update_display()

    def start_stop_count(self):
        if not self.pause_flag:
            self.pause_flag = True
            self.pause_play_button.configure(image=self.play_icon,
                                             border_color=self.play_button_color)
        else:
            self.pause_flag = False
            self.pause_play_button.configure(image=self.pause_icon,
                                             border_color=self.pause_button_color)
            self.update_counter()

    def reset_num_bits(self, new_num: str):
        self.reset_counter()
        self.num_bits = int(new_num)
        self.max_num = 2 ** self.num_bits - 1  # Reset max_num to new bit size
        for bit_label in self.bit_list:
            bit_label.destroy()
        self.bit_list = []
        self._set_app_size()
        self.setup_binary_display()

    def set_speed(self, new_speed: str):
        self.speed = self.speed_options[new_speed]

    def configure_app(self):
        self._set_app_size()
        self.app.title("Binary Counter")
        self.app.iconphoto(True, tk.PhotoImage(file=self.icon_photo_path))
        self.app.configure(fg_color=self.bg_color)

    def _set_app_size(self):
        size = (self.num_bits * 40 + 180, 350)
        self.app.geometry(f"{size[0]}x{size[1]}")
        self.app.minsize(width=size[0], height=size[1])

    def setup_base_frame(self):
        self.base_frame = ctk.CTkFrame(self.app, fg_color=self.bg_color)
        self.base_frame.pack(fill='both', expand=True, padx=30, pady=30)
        for i in range(3):
            self.base_frame.grid_rowconfigure(i, weight=1)

        self.base_frame.grid_columnconfigure(0, weight=1)

    def setup_row_frames(self):
        self.row1_frame = ctk.CTkFrame(self.base_frame, fg_color=self.bg_color)
        self.row2_frame = ctk.CTkFrame(self.base_frame, fg_color=self.bg_color)
        self.row3_frame = ctk.CTkFrame(self.base_frame, fg_color=self.bg_color)

        self.row1_frame.grid_rowconfigure(0, weight=1)
        self.row2_frame.grid_rowconfigure(0, weight=1)
        self.row3_frame.grid_rowconfigure(0, weight=1)

        for i in range(4):
            self.row2_frame.grid_columnconfigure(i, weight=1)

        for i in range(2):
            self.row3_frame.grid_columnconfigure(i, weight=1)

        self.row1_frame.grid(row=0, sticky='nsew')
        self.row2_frame.grid(row=1, sticky='nsew')
        self.row3_frame.grid(row=2, sticky='nsew')

    def setup_binary_display(self):
        for i in range(self.num_bits):
            self.row1_frame.grid_columnconfigure(i, weight=1)
            bit_label = ctk.CTkLabel(master=self.row1_frame,
                                     font=self.display_font,
                                     text_color=self.text_color,
                                     bg_color=self.bg_color,
                                     text='0', padx=5)
            self.bit_list.append(bit_label)
            bit_label.grid(row=0, column=i, sticky='nsew')

    def configure_permanent_widgets(self):
        self.reset_button = ctk.CTkButton(self.row2_frame, text="RESET",
                                          font=self.button_font,
                                          border_width=5, height=85, width=85,
                                          border_color=self.reset_button_color,
                                          text_color=self.reset_button_color,
                                          fg_color=self.bg_color,
                                          hover_color=self.hover_color,
                                          command=self.reset_counter)

        self.pause_play_button = ctk.CTkButton(self.row2_frame,
                                               fg_color=self.bg_color,
                                               border_width=5,
                                               border_color=self.pause_button_color,
                                               hover_color=self.hover_color,
                                               width=85, height=85, text="",
                                               image=self.pause_icon,
                                               command=self.start_stop_count)

        self.bit_selection_menu = ctk.CTkOptionMenu(self.row2_frame,
                                                    fg_color=self.bg_color,
                                                    width=40, height=50,
                                                    dropdown_fg_color=self.bg_color,
                                                    button_color=self.bg_color,
                                                    button_hover_color=self.hover_color,
                                                    text_color=self.bit_select_color,
                                                    dropdown_text_color=self.bit_select_color,
                                                    font=self.bit_select_font,
                                                    anchor='center',
                                                    dropdown_font=self.button_font,
                                                    values=[str(num) for num in [8, 16, 32]],
                                                    command=self.reset_num_bits)

        self.bit_selection_menu.set(value=str(self.num_bits))

        self.speed_selection_menu = ctk.CTkOptionMenu(self.row2_frame,
                                                      fg_color=self.bg_color,
                                                      width=40, height=50,
                                                      dropdown_fg_color=self.bg_color,
                                                      button_color=self.bg_color,
                                                      button_hover_color=self.hover_color,
                                                      text_color=self.speed_select_color,
                                                      dropdown_text_color=self.speed_select_color,
                                                      font=self.speed_select_font,
                                                      anchor='center',
                                                      dropdown_font=self.button_font,
                                                      values=[key for key in self.speed_options.keys()],
                                                      command=self.set_speed)

        self.speed_selection_menu.set(value='MED')

        self.decimal_label = ctk.CTkLabel(self.row3_frame, font=self.display_font,
                                          text_color=self.text_color,
                                          bg_color=self.bg_color, text=str(self.count))

        self.hex_label = ctk.CTkLabel(self.row3_frame, font=self.display_font,
                                      text_color=self.text_color,
                                      bg_color=self.bg_color, text=str(self.hex_count))

    def grid_permanent_widgets(self):
        self.reset_button.grid(row=0, column=0, stick='ew', padx=5)
        self.decimal_label.grid(row=0, column=0, sticky='nsew', padx=5)
        self.hex_label.grid(row=0, column=1, sticky='nsew', padx=5)
        self.pause_play_button.grid(row=0, column=1, sticky='ew', padx=5)
        self.bit_selection_menu.grid(row=0, column=2, sticky='ew', padx=5)
        self.speed_selection_menu.grid(row=0, column=3, sticky='ew', padx=5)
