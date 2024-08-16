import customtkinter as ctk
from tkinter import filedialog, messagebox, scrolledtext, Menu
import subprocess
import sys
import os
import keyword

class CodeEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.title("cnvcode v1")
        self.geometry("800x600")

        # Create a menu bar
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        # Create File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)

        # Create Run menu
        self.run_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self.run_menu.add_command(label="Run Code", command=self.run_code)

        # Create a text area for code input
        self.text_area = scrolledtext.ScrolledText(self, wrap='word', bg="#1E1E1E", fg="#FFFFFF", font=("Courier", 12))
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)
        self.text_area.bind("<KeyRelease>", self.on_key_release)

        # Output area for displaying results
        self.output_area = scrolledtext.ScrolledText(self, wrap='word', bg="#1E1E1E", fg="#FFFFFF", font=("Courier", 12), height=10)
        self.output_area.pack(expand=False, fill='x', padx=10, pady=10)
        self.output_area.config(state='disabled')  # Make output area read-only

        # Syntax highlighting
        self.highlight_keywords()

    def new_file(self):
        if self.text_area.get("1.0", "end-1c").strip():
            if messagebox.askyesno("Unsaved Changes", "You have unsaved changes. Do you want to continue?"):
                self.text_area.delete("1.0", "end")
                self.title("cnvcode v1 - Untitled")
        else:
            self.text_area.delete("1.0", "end")
            self.title("cnvcode v1 - Untitled")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".py",
                                                filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("insert", content)
                self.title(f"cnvcode v1 - {file_path}")
                self.highlight_keywords()

    def save_file(self):
        current_file_path = self.title().split(" - ")[-1]
        if current_file_path == "Untitled":
            self.save_as_file()
        else:
            with open(current_file_path, "w") as file:
                content = self.text_area.get("1.0", "end")
                file.write(content)

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                   filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_area.get("1.0", "end")
                file.write(content)
                self.title(f"cnvcode v1 - {file_path}")

    def run_code(self):
        code = self.text_area.get("1.0", "end-1c")
        if not code.strip():
            messagebox.showwarning("No Code", "Please enter some Python code to run.")
            return

        # Clear previous output
        self.output_area.config(state='normal')
        self.output_area.delete("1.0", "end")

        # Save the code to a temporary file and execute it
        temp_file = 'temp_script.py'
        with open(temp_file, 'w') as f:
            f.write(code)

        # Execute the script and capture output
        try:
            result = subprocess.run([sys.executable, temp_file], capture_output=True, text=True)
            output = result.stdout + result.stderr  # Combine standard output and error
            self.output_area.insert("insert", output)
        except Exception as e:
            self.output_area.insert("insert", f"Error: {str(e)}")
        finally:
            os.remove(temp_file)  # Clean up temporary file

        self.output_area.config(state='disabled')  # Make output area read-only

    def highlight_keywords(self):
        keywords = keyword.kwlist  # Get Python keywords
        for kw in keywords:
            start = '1.0'
            while True:
                start = self.text_area.search(r'\b' + kw + r'\b', start, stopindex='end', regexp=True)
                if not start:
                    break
                end = f"{start}+{len(kw)}c"
                self.text_area.tag_add("keyword", start, end)
                start = end
        self.text_area.tag_config("keyword", foreground="cyan")  # Set keyword color

    def on_key_release(self, event):
        # Auto-complete characters
        if event.char in ["'", '"', "(", "[", "{"]:
            self.text_area.insert("insert", self.get_matching_character(event.char))
        
        # Highlight keywords after every key release
        self.highlight_keywords()

    def get_matching_character(self, char):
        # Return the matching character
        if char == "'":
            return "'"
        elif char == '"':
            return '"'
        elif char == "(":
            return ")"
        elif char == "[":
            return "]"
        elif char == "{":
            return "}"
        return ""

if __name__ == "__main__":
    app = CodeEditor()
    app.mainloop()
