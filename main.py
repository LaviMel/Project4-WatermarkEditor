from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


def update_tk_img(img):
    screen.pil_img = img
    img_tk = ImageTk.PhotoImage(img)
    screen.img_tk = img_tk
    canvas.create_image(200, 200, image=img_tk)
    canvas.grid(row=1, column=1, columnspan=2)

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
    save_img_button.grid(row=2, column=0, pady=20)


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
        img = Image.open(file_path)
        img = img.resize((300, 300))
        screen.original_img = img
        update_tk_img(img)
        add_text_button.grid(row=1, column=0)


# Create the main window
screen = Tk()
screen.title("Photo Watermark Editor")
screen.config(padx=20, pady=20)
# Create a 'Browse' button
browse_button = Button(text="Browse", command=browse_file)
browse_button.grid(row=2, column=1)
# Create a canvas to display the photo on
canvas = Canvas(height=400, width=400)
# default_img = PhotoImage(file="default-img.png")
# canvas.create_image(image=default_img)
# Create an add text button
add_text_button = Button(text="Add Text", command=get_text_input)
save_img_button = Button(text="Save Image", command=save_img)


screen.mainloop()
