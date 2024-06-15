import tkinter as tk
from tkinter import ttk
from fpdf import FPDF

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Calendar")
        
        self.check_vars = []
        self.text_entries = []

        for i in range(31):
            frame = ttk.Frame(root)
            frame.grid(row=i//7, column=i%7, padx=5, pady=5, sticky="w")

            var = tk.BooleanVar()
            check = ttk.Checkbutton(frame, variable=var)
            check.grid(row=0, column=0, sticky="w")
            self.check_vars.append(var)
            
            label = ttk.Label(frame, text=f"{i + 1:02d}")
            label.grid(row=0, column=1, sticky="w")
            
            text_entry = ttk.Entry(frame, width=20)
            text_entry.grid(row=0, column=2, padx=5, pady=5)
            self.text_entries.append(text_entry)

        # Save and Load buttons
        self.save_button = ttk.Button(root, text="Save", command=self.save_tasks)
        self.save_button.grid(row=5, column=0, pady=10)
        
        self.load_button = ttk.Button(root, text="Load", command=self.load_tasks)
        self.load_button.grid(row=5, column=1, pady=10)
        
        self.save_pdf_button = ttk.Button(root, text="Save as PDF", command=self.save_as_pdf)
        self.save_pdf_button.grid(row=5, column=2, pady=10)

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for i in range(31):
                completed = self.check_vars[i].get()
                task_text = self.text_entries[i].get()
                file.write(f"{completed},{task_text}\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                for i, line in enumerate(file):
                    completed, task_text = line.strip().split(",", 1)
                    self.check_vars[i].set(completed == 'True')
                    self.text_entries[i].delete(0, tk.END)
                    self.text_entries[i].insert(0, task_text)
        except FileNotFoundError:
            pass
    
    def save_as_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Task Calendar", ln=True, align='C')
        
        for i in range(31):
            completed = "X" if self.check_vars[i].get() else " "
            task_text = self.text_entries[i].get()
            pdf.cell(0, 10, txt=f"{i + 1:02d}: [{completed}] {task_text}", ln=True)
        
        pdf.output("tasks.pdf")
        print("Tasks saved as tasks.pdf")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
