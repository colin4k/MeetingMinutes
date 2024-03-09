import re
import shutil
import datetime

import customtkinter
from customtkinter import filedialog

from meetingMinutes import meeting_minutes_main
from convertMKVtoMP3 import convert_mkv_to_mp3, cutting_mp3


class MyFileDialogFrame(customtkinter.CTkFrame):
    """
    Make a frame to select a file.
    """

    def __init__(self, master, title, placeholder, button_text):
        """
        Initialise and configure the frame to select a file.
        :param master:
        :param title: Frame title
        :param placeholder: Text in the placeholder
        :param button_text: Text in the button
        """
        super().__init__(master)

        # Display configuration
        self.grid_columnconfigure(0, weight=5)

        self.title = title
        self.placeholder = placeholder
        self.button_text = button_text

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.entry_placeholder = customtkinter.CTkEntry(self, placeholder_text=self.placeholder)
        self.entry_placeholder.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")
        self.entry_placeholder.configure(state="disabled")

        # Button configuration
        button = customtkinter.CTkButton(self, text=self.button_text, command=self.select_file)
        button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

    def select_file(self):
        """
        Selecting a file.
        """
        filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=(
                ('mkv & mp3 files', '*.mkv *.mp3'),
                ('All files', '*.*')))

        if filename:
            self.entry_placeholder.configure(state="normal")
            self.entry_placeholder.delete(0, "end")
            self.entry_placeholder.insert(0, filename)
            self.entry_placeholder.configure(state="disabled")

    def get(self):
        """
        Get the path to the file.
        :return: Path to file
        """
        return self.entry_placeholder.get()


class MyEntryFrame(customtkinter.CTkFrame):
    """
    Make a frame to enter data.
    """

    def __init__(self, master, title, data_titles, placeholders):
        """
        Initialise and configure the frame to enter data.
        :param master:
        :param title: Frame title
        :param data_titles: Text in front of entry cells
        :param placeholders: Text in the placeholder
        """
        super().__init__(master)

        # Display configuration
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.title = title
        self.data_titles = data_titles
        self.placeholders = placeholders
        self.datas = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        for i, (data_title, placeholder) in enumerate(zip(self.data_titles, self.placeholders)):
            entry_data_title = customtkinter.CTkLabel(self, text=data_title)
            entry_data_title.grid(row=i + 1, column=0, padx=10, pady=(0, 10), sticky="w")
            entry_placeholder = customtkinter.CTkEntry(self, placeholder_text=placeholder)
            entry_placeholder.grid(row=i + 1, column=1, padx=10, pady=(0, 10), sticky="ew")
            self.datas.append(entry_placeholder)

    def get(self):
        """
        Get cell values.
        :return: Cell values
        """
        data_list = []
        for data in self.datas:
            data_list.append(data.get())
        return data_list


class MyRadioButtonFrame(customtkinter.CTkFrame):
    """
    Make a frame to select a radio button value.
    """

    def __init__(self, master, title, options):
        """
        Initialise and configure the frame to select a radio button value.
        :param master:
        :param title: Frame title
        :param options: Radio button options
        """
        super().__init__(master)

        # Display configuration
        self.grid_columnconfigure(0, weight=1)

        self.title = title
        self.options = options
        self.variable = customtkinter.StringVar(value="")

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.options):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")

    def get(self):
        """
        Get the value of the selected radio button.
        :return: Radio button value
        """
        return self.variable.get()

    def set(self, value):
        """
        Set the value of the selected radio button.
        """
        self.variable.set(value)


class App(customtkinter.CTk):
    """
    Main application code.
    """

    def __init__(self):
        """
        Initialise and configure the window.
        """
        super().__init__()

        # Window configuration
        self.title("Meeting Minutes")
        self.geometry("600x420")
        self.resizable(False, False)
        # self.iconbitmap("/mnt/d/PersonnalPrograms/PythonProjects/MeetingMinutes/src/icon.ico")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Building the grid
        self.file_selection_frame = MyFileDialogFrame(self, "File browser", placeholder="File path",
                                                      button_text="Choose file")
        self.file_selection_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew", columnspan=2)

        self.file_name_selection_frame = MyEntryFrame(self, "File names", data_titles=["Audio file:", "Meeting file:"],
                                                      placeholders=["audio_[date].mp3", "meeting_minutes_[date].docx"])
        self.file_name_selection_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)

        self.timecode_selection_frame = MyEntryFrame(self, "Start/End Times", data_titles=["Start:", "End:"],
                                                     placeholders=["00:00:00", "59:59:59"])
        self.timecode_selection_frame.grid(row=2, column=0, padx=(10, 5), pady=5, sticky="nsew")
        self.radio_button_selection_frame = MyRadioButtonFrame(self, "Transcription",
                                                               options=["Transcription only", "Full execution"])
        self.radio_button_selection_frame.grid(row=2, column=1, padx=(5, 10), pady=5, sticky="nsew")

        self.button = customtkinter.CTkButton(self, text="Run the program", command=self.code_execution)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        # Setup
        self.radio_button_selection_frame.set("Transcription only")

    def code_execution(self):
        """
        Code execution and processing.
        """
        # Getting data
        start_time = self.timecode_selection_frame.get()[0]
        end_time = self.timecode_selection_frame.get()[1]
        path = self.file_selection_frame.get()
        radio = self.radio_button_selection_frame.get()
        name_mp3 = self.file_name_selection_frame.get()[0]
        name_docx = self.file_name_selection_frame.get()[1]
        new_path = False

        # Checks whether the format of the start and end times is correct
        motif = r'^([0-5]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$'
        start_time_good = True if re.match(motif, start_time) else False
        end_time_good = True if re.match(motif, end_time) else False

        # Convert file to mp3
        if path.endswith('.mkv'):
            path = convert_mkv_to_mp3(path, name_mp3) if name_mp3 else convert_mkv_to_mp3(path)
            new_path = True

        # Cutting up the file
        if path.endswith('.mp3') and (start_time_good or end_time_good):
            cut_params = {}
            if name_mp3:
                cut_params['name_mp3_file'] = name_mp3
            if start_time_good:
                cut_params['start_time'] = start_time
            if end_time_good:
                cut_params['end_time'] = end_time

            path = cutting_mp3(path, **cut_params)
            new_path = True

        # Running the MeetingMinutes
        if path.endswith('.mp3'):
            name_docx = name_docx if name_docx != "" else None
            action_type = "Full" if radio == "Full execution" else "Transcription"

            meeting_minutes_main(path, action_type, name_docx)

            if not new_path:
                output_dir = "output"
                if name_mp3 == "":
                    now = datetime.datetime.now()
                    formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
                    shutil.copy(path, f"{output_dir}/audio_{formatted_date}.mp3")
                else:
                    shutil.copy(path, f"{output_dir}/{name_mp3}.mp3")
        elif path != "":
            print("Erreur sur le type de fichier")


if __name__ == '__main__':
    app = App()
    app.mainloop()
