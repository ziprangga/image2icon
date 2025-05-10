import os
import customtkinter as ctk
from customtkinter import CTkImage, filedialog
from tkinter import messagebox
from pysrc.image2icon import Image2IconLib
from PIL import Image


class ConverterGui:
    def __init__(self, image2icon_lib: Image2IconLib) -> None:
        self.image2icon_lib = image2icon_lib
        self.root = ctk.CTk()
        self.root.title("image2icon")
        self.root.geometry("500x350")
        self.root.minsize(500, 350)
        self.root.maxsize(500, 350)
        self.root.resizable(True, True)

        self.iconset_folder = None
        self.input_image_path = None

        self.bg_frame = ctk.CTkFrame(self.root)
        self.bg_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.content_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.content_frame.grid_columnconfigure(0, weight=1, minsize=250)

        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.select_button_image = ctk.CTkButton(
            self.button_frame, text="Select Image", command=self.select_image
        )
        self.select_button_image.grid(row=1, column=0, pady=10)

        self.select_button_folder = ctk.CTkButton(
            self.button_frame, text="Select iconset folder", command=self.select_iconset
        )
        self.select_button_folder.grid(row=2, column=0, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Create Iconset",
            command=self.create_iconset_gui,
            fg_color="blue",
            text_color="white",
        ).grid(row=3, column=0, pady=10)

        ctk.CTkButton(
            self.button_frame,
            text="Convert",
            command=self.run_command,
            fg_color="purple",
            text_color="white",
        ).grid(row=4, column=0, pady=10)

        self.preview_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="")
        self.preview_label.grid(row=1, column=1, pady=10)

        self.entry_label = ctk.CTkLabel(
            self.preview_frame, text="Select a folder or image"
        )
        self.entry_label.place(relx=0.5, rely=0.5, anchor="center")

        self.clear_button = ctk.CTkButton(
            self.preview_frame,
            text="Clear Selection",
            command=self.clear_selection,
            fg_color="red",
            text_color="white",
        )
        self.clear_button.grid(row=2, column=1, pady=10)

    def select_iconset(self):
        selected_path = filedialog.askdirectory(title="Select iconset folder")

        if not selected_path:
            return

        self.iconset_folder = selected_path
        self.entry_label.configure(text=f"📂 {selected_path}")

    def select_image(self):
        selected_path = filedialog.askopenfilename(
            title="Select Image", filetypes=[("All Files", "*.*")]
        )

        if not selected_path:
            return

        self.input_image_path = selected_path
        self.entry_label.place_forget()
        self.display_image_preview(selected_path)

    def clear_selection(self):
        self.input_image_path = None
        self.iconset_folder = None
        self.entry_label.configure(text="Select a folder or image")
        self.entry_label.place(relx=0.5, rely=0.5, anchor="center")
        self.preview_label.configure(image=None, text="")
        self.preview_label.image = None

    def display_image_preview(self, input_image_path):
        try:
            image = Image.open(input_image_path)
            image.thumbnail((150, 150))
            photo = CTkImage(light_image=image, size=image.size)

            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image preview: {e}")

    def run_command(self):
        if self.input_image_path:
            self.convert_image_gui()

        if self.iconset_folder:
            self.convert_iconset_gui()

    def convert_iconset_gui(self):
        if not self.iconset_folder:
            messagebox.showerror("Error", "Choose .iconset folder first!")
            return

        ico_path = filedialog.asksaveasfilename(
            defaultextension=".icns",
            filetypes=[("ICNS Files", "*.icns"), ("ICO Files", "*.ico")],
        )
        if ico_path:
            if ico_path.lower().endswith(".ico"):
                format = Image2IconLib.FORMAT_ICO
            else:
                format = Image2IconLib.FORMAT_ICNS

            success = self.image2icon_lib.convert_iconset(
                self.iconset_folder, ico_path, format=format
            )

            if success == 0:
                messagebox.showinfo(
                    "Success", f"✅ Convert finished!\nFile saved here:\n{ico_path}"
                )
            else:
                messagebox.showerror("Error", "Conversion failed!")

    def create_iconset_gui(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Select an image to create iconset!")
            return

        folder_path = filedialog.askdirectory(title="Select Output Folder for Iconset")
        if folder_path:
            success = self.image2icon_lib.create_iconset(
                self.input_image_path, folder_path
            )
            if success == 0:
                messagebox.showinfo(
                    "Success",
                    f"✅ Iconset created successfully!\nSaved to {folder_path}",
                )
            else:
                messagebox.showerror("Error", "Failed to create iconset!")

    def convert_image_gui(self):
        if not self.input_image_path:
            messagebox.showerror("Error", "Select an image to convert!")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".icns",
            filetypes=[("ICNS Files", "*.icns"), ("ICO Files", "*.ico")],
        )
        if output_path:
            if output_path.lower().endswith(".ico"):
                format = Image2IconLib.FORMAT_ICO
            else:
                format = Image2IconLib.FORMAT_ICNS

            success = self.image2icon_lib.convert_image(
                self.input_image_path, output_path, format
            )
            if success == 0:
                messagebox.showinfo(
                    "Success",
                    f"✅ Image conversion finished!\nFile saved here:\n{output_path}",
                )
            else:
                messagebox.showerror("Error", "Image conversion failed!")

    def run(self):
        self.root.mainloop()
