from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


def update_tk_img(img):
    screen.pil_img = img
    img_tk = ImageTk.PhotoImage(img)
    screen.img_tk = img_tk
    canvas.create_image(300, 300, image=img_tk, anchor=CENTER)
    canvas.grid(row=1, column=1, columnspan=2, rowspan=2)
    add_text_button.grid(row=1, column=0)


def on_canvas_click(event):
    screen.text_x = event.x
    screen.text_y = event.y
    apply_text_to_image()
    # canvas.unbind("<Button-1>")


def save_img():
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                        ("All files", "*.*")])
    if save_path:
        screen.pil_img.save(save_path)
        messagebox.showinfo("Image Saved", f"Image saved to {save_path}")


def apply_text_to_image():
    if not hasattr(screen, 'text_color'):
        screen.text_color = "#000000"
    img = screen.original_img.copy()
    d = ImageDraw.Draw(img)
    font_path = screen.selected_font
    font_size = screen.selected_size
    # Attempt to load the font with the given path and size
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file could not be loaded. Using default font.")
        font = ImageFont.load_default()

    try:
        if "bold" in screen.selected_styles:
            font = ImageFont.truetype(font_path.replace(".ttf", "-bold.ttf"), font_size)
        if "italic" in screen.selected_styles:
            font = ImageFont.truetype(font_path.replace(".ttf", "-italic.ttf"), font_size)
    except IOError:
        print("Specified font style variant not found. Using default font.")
    d.text((screen.text_x, screen.text_y), screen.user_text, font=font, fill=screen.text_color)

    bbox = d.textbbox((screen.text_x, screen.text_y), screen.user_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    # Draw underline if specified
    if "underline" in screen.selected_styles:
        d.line(
            (screen.text_x, screen.text_y + text_height, screen.text_x + text_width, screen.text_y + text_height),
            fill=screen.text_color, width=2
        )
    update_tk_img(img)




def get_text_input():
    text_window = Toplevel(screen)
    text_window.title("Enter Text")
    text_window.config(bg="#D3D3D3")
    text_window.geometry(f"{400}x{400}")
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    text_window.geometry(f"+{int(screen_width / 2 - 400 / 2)}+{int(screen_height / 2 - 400 / 2)}")
    # Add widgets to the Toplevel window
    Label(text_window, text="Enter the text to add:", bg="#D3D3D3", font=("Helvetica", 11, "underline")).pack(pady=10)
    text_entry = Entry(text_window, width=35)
    text_entry.pack()
    img = Image.open("images/Text-Edit-icon.png")
    img = img.resize((240, 220), Image.LANCZOS)  # Resize the image if needed
    img_tk = ImageTk.PhotoImage(img)
    image_label = Label(text_window, image=img_tk, bg="#D3D3D3")
    image_label.image = img_tk
    image_label.pack(side=BOTTOM, pady=35)
    # Function to save the entered text and close the window
    def save_text():
        screen.user_text = text_entry.get()
        text_window.destroy()
        get_font_options()

    Button(text_window, text="Add Text", command=save_text).pack(pady=10)

def get_font_options():
    font_window = Toplevel(screen)
    font_window.title("Select Font, Size, Style and Color")
    window_icon_img = ImageTk.PhotoImage(file="icons/edittext.png")
    font_window.iconphoto(False, window_icon_img)
    font_window.config(bg="#D3D3D3")
    font_window.geometry(f"{500}x{425}")
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    font_window.geometry(f"+{int(screen_width / 2 - 250)}+{int(screen_height / 2 - 212.5)}")

    Label(font_window, text="Select Font:", bg="#D3D3D3", font=("Helvetica", 12)).pack(pady=10)
    # Scan for .ttf, .fon and .ttc font files in the system's fonts directory
    font_dir = os.path.join(os.environ['WINDIR'], 'Fonts')  # For Windows
    font_files = [f for f in os.listdir(font_dir) if f.endswith(('.fon', '.ttf', '.ttc'))]
    font_names = [os.path.splitext(f)[0] for f in font_files]  # Remove file extensions

    # font_menu = OptionMenu(font_window, font_var, *sorted(font_names))  # Font Menu
    def create_font_menu():
        font_menu = Menu(font_window, tearoff=0)
        for font_name in sorted(font_names):
            font_menu.add_command(label=font_name, command=lambda f=font_name: (font_var.set(f), font_button.config(text=f)))
        return font_menu
    font_var = StringVar(value="Helvetica")
    font_button = Button(font_window, text="Select Font", command=lambda: font_menu.post(font_button.winfo_rootx(),
                     font_button.winfo_rooty() + font_button.winfo_height()), bg="#F0F0F0", font=("Helvetica", 11))
    font_button.pack(pady=10)
    font_menu = create_font_menu()

    Label(font_window, text="Select Size:", bg="#F0F0F0", font=("Helvetica", 11)).pack(pady=10)
    size_var = IntVar(value=20)
    Scale(font_window, from_=10, to=100, orient=HORIZONTAL, variable=size_var).pack(pady=10)

    Label(font_window, text="Select Style:", bg="#F0F0F0", font=("Helvetica", 11, "bold")).pack(pady=10)
    bold_var = IntVar()
    underline_var = IntVar()
    italic_var = IntVar()
    Checkbutton(font_window, text="Bold", variable=bold_var, bg="#F0F0F0", font=("Helvetica", 10)).pack()
    Checkbutton(font_window, text="Underline", variable=underline_var, bg="#F0F0F0", font=("Helvetica", 10)).pack()
    Checkbutton(font_window, text="Italic", variable=italic_var, bg="#F0F0F0", font=("Helvetica", 10)).pack()

    def choose_color():
        color = askcolor()[1]
        screen.text_color = color
    Button(font_window, text="Choose Color", command=choose_color).pack(pady=10)

    def save_font_options():
        selected_font = font_var.get()
        font_path = os.path.join(font_dir, selected_font + (".ttf" if selected_font + ".ttf" in font_files else ".ttc"))
        screen.selected_size = size_var.get()
        screen.selected_font = font_path

        font_styles = []
        if bold_var.get():
            font_styles.append("bold")
        if underline_var.get():
            font_styles.append("underline")
        if italic_var.get():
            font_styles.append("italic")
        screen.selected_styles = font_styles

        print("Styles applied:", font_styles)
        print("Font path:", screen.selected_font)
        font_window.destroy()
        prompt_for_placement()

    Button(font_window, text="Next", command=save_font_options, font=("Helvetica", 12), bg="#008CBA", fg="white",
           width=15).pack(pady=10)


def prompt_for_placement():
    # Inform the user to click on the image
    messagebox.showinfo("Placement", "Click on the image to place the text.")
    canvas.bind("<Button-1>", on_canvas_click)
    save_image_button.grid(row=1, column=0, pady=(110, 0))


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
icon_img = ImageTk.PhotoImage(file="icons/brush.png")
screen.iconphoto(False, icon_img)

# Create a canvas to display the photo on
canvas = Canvas(screen, height=600, width=600, bg="#8C8C8C", highlightbackground="#8C8C8C", highlightcolor="#8C8C8C")
default_img = ImageTk.PhotoImage(file="images/default-img.png")
canvas.create_image(300, 300, image=default_img)
canvas.grid(row=1, column=1, columnspan=2, padx=20, pady=20)

# Create buttons with improved design
browse_button = Button(screen, text="Browse", command=browse_file, font=("Helvetica", 12, "bold"), width=15, height=2, borderwidth=1, relief="solid")
browse_button.grid(row=5, column=1, columnspan=2, pady=20)
add_text_button = Button(screen, text="Add Text", command=get_text_input, font=("Arial", 12), width=17, height=2, borderwidth=1, relief="solid")
save_image_button = Button(screen, text="Save Image", command=save_img, font=("Arial", 12, "bold"), width=15, height=2, borderwidth=1, relief="solid")

# Center the browse button at the bottom of the screen
screen.grid_rowconfigure(5, weight=1)
screen.grid_columnconfigure(0, weight=1)
screen.grid_columnconfigure(2, weight=1)

screen.mainloop()
