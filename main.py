import customtkinter as ctk
import tkinter as tk

NUM_BITS = 16
FONT = "American Typewriter"
DISPLAY_FONT = (FONT, 64)
count = 0
max_num = 2**NUM_BITS-1
TEXT_COLOR = '#2FBA2F'
BACKGROUND_COLOR = '#0b0b0b'
BUTTON_TEXT_COLOR = '#08AF08'
BUTTON_COLOR = '#0A193B'

app = ctk.CTk()
app.geometry(f"{NUM_BITS * 44}x250")
app.title("Binary Counter")
app.iconphoto(True, tk.PhotoImage(file='icon.png'))
counter_frame = ctk.CTkFrame(app, fg_color=BACKGROUND_COLOR)
counter_frame.pack(fill='both', expand=True, padx=30, pady=30)
bit_list = []

for i in range(4):
    counter_frame.grid_rowconfigure(i, weight=1)

for i in range(0, NUM_BITS):
    counter_frame.grid_columnconfigure(i, weight=1)
    bit_label = ctk.CTkLabel(master=counter_frame, font=DISPLAY_FONT,
                             text_color=TEXT_COLOR, bg_color=BACKGROUND_COLOR,
                             text='0', padx=5)
    bit_list.append(bit_label)
    bit_label.grid(row=1, column=i)


def reset_counter():
    global count
    count = 0


reset_button = ctk.CTkButton(counter_frame, text="RESET", font=(FONT, 24),
                             text_color=BUTTON_TEXT_COLOR, bg_color=BACKGROUND_COLOR,
                             fg_color=BUTTON_COLOR,
                             hover_color='dark red',
                             command=reset_counter)
reset_button.grid(row=2, column=0, columnspan=NUM_BITS)

decimal_label = ctk.CTkLabel(counter_frame, font=DISPLAY_FONT, text_color=TEXT_COLOR,
                             bg_color=BACKGROUND_COLOR, text=str(count))
decimal_label.grid(row=3, column=0, columnspan=NUM_BITS)


def update_counter():
    global count
    bitsize = '0' + str(NUM_BITS) + 'b'
    my_bin_num = f"{count:{bitsize}}"

    for i in range(NUM_BITS):
        bit_list[i].configure(text=my_bin_num[i])

    decimal_label.configure(text=str(count))
    if count == max_num:
        count = 0
    else:
        count += 1

    app.after(400, update_counter)


if __name__ == '__main__':
    update_counter()
    app.mainloop()
