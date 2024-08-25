from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


def update_tk_img(img):
    screen.pil_img = img
    img_tk = ImageTk.PhotoImage(img)
    screen.img_tk = img_tk
    canvas.create_image(300, 300, image=img_tk, anchor=CENTER)
    canvas.grid(row=1, column=1, columnspan=2, rowspan=2)
    add_text_button.grid(row=1, column=0)


def save_img():
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if save_path:
        screen.pil_img.save(save_path)
        messagebox.showinfo("Image Saved", f"Image saved to {save_path}")


def add_text():
    # Copying original img for reference
    img = screen.original_img.copy()
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((0, 0), screen.user_text, font=font, fill=(255, 255, 255, 128))
    update_tk_img(img)
    save_image_button.grid(row=1, column=0, pady=(110, 0))


def get_text_input():
    # Create a new Toplevel window
    text_window = Toplevel(screen)
    text_window.title("Enter Text")
    # Create an Entry widget to accept user input
    Label(text_window, text="Enter the text to add:").grid(row=0, column=0, padx=10, pady=10)
    text_entry = Entry(text_window, width=30)
    text_entry.grid(row=1, column=0, padx=10, pady=10)
    # Function to save the entered text and close the window
    def save_text():
        screen.user_text = text_entry.get()
        text_window.destroy()
        add_text()

    Button(text_window, text="Add Text", command=save_text).grid(row=2, column=0, padx=10, pady=10)


def browse_file():
    # Open file explorer and allow user to select a file
    file_path = filedialog.askopenfilename(
        title="Select a Photo",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
    )
    if file_path:
        canvas.delete("all")
        img = Image.open(file_path)
        # Maintaining Image proportion
        original_width, original_height = img.size
        max_width, max_height = 600, 600
        scale = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        screen.original_img = img
        update_tk_img(img)


# Create the main window
screen = Tk()
screen.title("Photo Watermark Editor")
screen.config(height=900, width=1600, padx=20, pady=20, bg="#8C8C8C")

# Create a canvas to display the photo on
canvas = Canvas(screen, height=600, width=600, bg="#8C8C8C", highlightbackground="#8C8C8C", highlightcolor="#8C8C8C")
default_img = ImageTk.PhotoImage(file="default-img.png")
canvas.create_image(300, 300, image=default_img)
canvas.grid(row=1, column=1, columnspan=2, padx=20, pady=20)

# Create buttons with improved design
browse_button = Button(screen, text="Browse", command=browse_file, font=("Helvetica", 12, "bold"), width=15, height=2, borderwidth=1, relief="solid")
browse_button.grid(row=5, column=1, columnspan=2, pady=20)
add_text_button = Button(screen, text="Add Text", command=get_text_input, font=("Helvetica", 12), width=17, height=2, borderwidth=1, relief="solid")
save_image_button = Button(screen, text="Save Image", command=save_img, font=("Helvetica", 12, "bold"), width=15, height=2, borderwidth=1, relief="solid")

# Center the browse button at the bottom of the screen
screen.grid_rowconfigure(5, weight=1)
screen.grid_columnconfigure(0, weight=1)
screen.grid_columnconfigure(2, weight=1)

screen.mainloop()
