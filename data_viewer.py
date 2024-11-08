import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import textwrap
import subprocess

# Connect to SQLite database and read data
conn = sqlite3.connect('data_engineer_jobs.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM data_engineer_jobs")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
conn.close()

class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Engineer Jobs - Data Viewer")
        self.data = rows  # Save data here
        self.columns = columns  # Save column names here

        # Set initial window size
        self.root.geometry("1600x1000")

        # Set window icon
        self.set_window_icon()

        # Style configurations
        style = ttk.Style()
        style.configure("Treeview", rowheight=60, font=('Arial', 16), bordercolor="#D3D3D3", borderwidth=5)
        style.configure("Treeview.Heading", font=('Arial', 18, 'bold'))
        style.configure("Treeview", background="#F5F5F5", foreground="#000000", fieldbackground="#FFFFFF")
        style.configure('TButton', font=('Arial', 16), padding=10)
        style.configure('TLabel', font=('Arial', 16))
        style.configure('TEntry', font=('Arial', 16))

        # Create a main frame
        main_frame = tk.Frame(root, bg="#EAEAEA")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Create filter frame
        filter_frame = tk.Frame(main_frame, bg="#EAEAEA")
        filter_frame.grid(row=0, column=0, sticky="ew")

        # Add a label and entry for filtering
        self.filter_label = tk.Label(filter_frame, text="Filter (Column:Value):", bg="#EAEAEA", font=('Arial', 16))
        self.filter_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.filter_entry = tk.Entry(filter_frame, width=40, font=('Arial', 16))
        self.filter_entry.grid(row=0, column=1, padx=10, pady=10)

        self.filter_button = tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter, font=('Arial', 16))
        self.filter_button.grid(row=0, column=2, padx=10, pady=10)

        # Result Display as a table
        self.tree = ttk.Treeview(main_frame, columns=self.columns, show='headings')
        self.tree.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        # Scrollbars
        self.vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.vsb.grid(row=1, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.hsb.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.tree.configure(xscrollcommand=self.hsb.set)

        # Set column headings and initial column width
        for col in self.columns:
            self.tree.heading(col, text=col)
            if col == "description":  # Adjust width for description column
                self.tree.column(col, width=300, stretch=tk.YES)  # Set wider width for this column
            else:
                self.tree.column(col, width=100, stretch=tk.YES)  # Set initial width for other columns

        self.auto_adjust_column_width()

        # Row count label
        self.row_count_label = tk.Label(main_frame, text=f"# rows: {len(self.data)}", font=('Arial', 16, 'bold'), bg="#EAEAEA")
        self.row_count_label.grid(row=2, column=0, pady=20, sticky="w")

        # Configure grid weights
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Make the main window resize with the content
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Display the full data
        self.display_results(self.data)

        # Bind the click event to the open_url function
        self.tree.bind("<Button-1>", self.open_url)

    def set_window_icon(self):
        try:
            # Load and set the window icon
            self.icon_image = tk.PhotoImage(file='arbets_logo.png')  # Path to your icon file
            self.root.iconphoto(True, self.icon_image)
        except tk.TclError:
            # Handle error if icon cannot be loaded
            print("Error loading icon image. Make sure the file path is correct and the file is a valid image format.")

    def auto_adjust_column_width(self):
        # Create a label for text measurement
        label = tk.Label(self.root, font=('Arial', 16))
        max_width = {col: len(self.tree.heading(col, 'text')) * 5 for col in self.tree["columns"]}

        # Check all column values
        for item in self.tree.get_children():
            row_values = self.tree.item(item, 'values')
            for col, value in zip(self.tree["columns"], row_values):
                if col == "description":  # Skip the description column
                    continue
                label.config(text=value)
                text_width = label.winfo_reqwidth()
                max_width[col] = max(max_width[col], text_width)

        # Set column width based on the widest content
        for col, width in max_width.items():
            if col == "description":  # Skip the description column
                continue
            self.tree.column(col, width=width + 10)  # Add extra padding

    def wrap_text(self, text, width):
        return '\n'.join(textwrap.wrap(text, width))

    def display_results(self, data_to_display):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Display results
        for i, row in enumerate(data_to_display):
            wrapped_row = [self.wrap_text(str(cell), 100) for cell in row]  # Adjust the width as needed
            tag = 'oddrow' if i % 2 == 0 else 'evenrow'
            self.tree.insert("", "end", values=wrapped_row, tags=(tag,))

        # Configure row tags for alternating colors
        self.tree.tag_configure('oddrow', background='#F5F5F5')
        self.tree.tag_configure('evenrow', background='#DFDFDF')

    def apply_filter(self):
        filter_text = self.filter_entry.get()
        if not filter_text:
            self.filtered_data = self.data  # If filter is empty, reset to full data
        else:
            try:
                column, value = filter_text.split(':', 1)
                column = column.strip()
                value = value.strip()
                if column in self.columns:
                    self.filtered_data = [row for row in self.data if value.lower() in str(row[self.columns.index(column)]).lower()]
                else:
                    messagebox.showwarning("Invalid Column", f"Column '{column}' does not exist.")
                    self.filtered_data = self.data
            except ValueError:
                messagebox.showwarning("Invalid Filter", "Filter format should be 'Column:Value'.")
                self.filtered_data = self.data

        # Update the display with filtered data
        self.display_results(self.filtered_data)
        self.row_count_label.config(text=f"# rows: {len(self.filtered_data)}")

    def export_to_csv(self):
        # Ask user for a file name and location
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_path:
            return  # User canceled the save dialog

        try:
            # Export data to CSV
            with open(file_path, 'w', encoding='utf-8-sig') as f:
                # Write the column headers
                f.write(','.join(self.columns) + '\n')
                # Write the data rows
                for row in self.filtered_data:
                    f.write(','.join(map(str, row)) + '\n')
            messagebox.showinfo("Export Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting the data:\n{e}")

    # Function to open the URL in the default browser
    def open_url(self, event):
        item = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify_column(event.x)
        col_index = int(column.replace('#', '')) - 1
        if col_index == self.columns.index('webpage'):
            url = self.tree.item(item, 'values')[col_index]
            try:
                # Use Windows default browser to open the URL
                subprocess.run(['explorer.exe', url])
            except Exception as e:
                print(f"Failed to open URL: {e}")

# Create the application window
root = tk.Tk()
app = DataViewerApp(root)
root.mainloop()