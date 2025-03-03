import customtkinter as ctk

NUM_BITS = 16
FONT = ('Arial', 64)
count = 0
max_num = 2**NUM_BITS-1

app = ctk.CTk()
app.geometry("400x200")
app.title("Binary Counter")
counter_frame = ctk.CTkFrame(app)
counter_frame.pack(fill='both', expand=True, padx=30, pady=30)
bit_list = []

for i in range(4):
    counter_frame.grid_rowconfigure(i, weight=1)

for i in range(0, NUM_BITS):
    counter_frame.grid_columnconfigure(i, weight=1)
    bit_label = ctk.CTkLabel(master=counter_frame, font=FONT, text='0',
                             padx=5)
    bit_list.append(bit_label)
    bit_label.grid(row=1, column=i)


def reset_counter():
    global count
    count = 0


reset_button = ctk.CTkButton(counter_frame, text="RESET", font=('Arial', 24),
                             command=reset_counter)
reset_button.grid(row=2, column=0, columnspan=NUM_BITS)

decimal_label = ctk.CTkLabel(counter_frame, font=FONT, text=str(count))
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
