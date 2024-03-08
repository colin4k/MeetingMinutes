import customtkinter
from customtkinter import filedialog

class MyFileDialogFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=5)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.entry_path = customtkinter.CTkEntry(self, placeholder_text="File path")
        self.entry_path.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")
        self.entry_path.configure(state="disabled")

        button = customtkinter.CTkButton(self, text="Choose file", command=self.select_file)
        button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    def select_file(self):
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='..',
            filetypes=(
                ('mkv files', '*.mkv'),
                ('mp3 files', '*.mp3'),
                ('All files', '*.*')))
        if filename:
            self.entry_path.configure(state="normal")
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, filename)
            self.entry_path.configure(state="disabled")

    def get(self):
        return self.entry_path.get()

class MyEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        for i, value in enumerate(self.values):
            nameEntry = customtkinter.CTkEntry(self, placeholder_text=value)
            nameEntry.grid(row=i+1, column=0, padx=10, pady=(0, 10), sticky="ew")
            self.checkboxes.append(nameEntry)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            checked_checkboxes.append(checkbox.get())
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Meeting Minutes")
        self.geometry("550x290")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.file_frame = MyFileDialogFrame(self, "File browser", values=["File"])
        self.file_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew", columnspan=2)

        self.names_frame = MyEntryFrame(self, "File names", values=["audio_[date].mp3", "meeting_minutes_[date].docx"])
        self.names_frame.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsew")
        self.times_frame = MyEntryFrame(self, "Start/End Times", values=["00:00:00", "59:59:59"])
        self.times_frame.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("names:", self.names_frame.get())
        print("times:", self.times_frame.get())
        print("path:", self.file_frame.get())


if __name__ == '__main__':
    app = App()
    app.mainloop()