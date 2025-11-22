import customtkinter as ctk
import threading
import time
from datetime import datetime
import csv
from tkinter import filedialog, messagebox

# -----------------------
# App Configuration
# -----------------------
ctk.set_appearance_mode("system")      # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class JobScraperUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Job Scraper UI")
        self.geometry("800x550")

        # Initialize variables
        self.job_listings = []
        self.scraping_active = False

        # -------------- Layout --------------
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title Label
        title = ctk.CTkLabel(self, text="Job Scraper", font=("Arial", 24, "bold"))
        title.grid(row=0, column=0, pady=15)

        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        main_frame.grid_columnconfigure(1, weight=1)

        # ------------------- Input Fields -------------------
        ctk.CTkLabel(main_frame, text="Job Title:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.job_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g. Software Developer")
        self.job_entry.grid(row=0, column=1, sticky="ew", padx=10)

        ctk.CTkLabel(main_frame, text="Location:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.location_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g. Lagos")
        self.location_entry.grid(row=1, column=1, sticky="ew", padx=10)

        ctk.CTkLabel(main_frame, text="Website:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.site_option = ctk.CTkOptionMenu(
            main_frame,
            values=["Indeed", "LinkedIn", "Glassdoor"],
        )
        self.site_option.grid(row=2, column=1, sticky="ew", padx=10)

        # ------------------- Buttons -------------------
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # ------------------- Start Button -------------------
        self.start_button = ctk.CTkButton(
            main_frame,
            text="Start Scraping",
            command=self.start_scraper_thread,
            height=40
        )
        self.start_button.grid(row=3, column=0, columnspan=2, pady=20)

        #------------------- Stop Scraping Button -------------------
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="Stop Scraping",
            command=self.stop_scraping,
            height=40,
            state=ctk.DISABLED
        )
        self.stop_button.pack(side=ctk.LEFT, padx=(0, 10))

        #------------------- Export Results Button -------------------
        self.export_button = ctk.CTkButton(
            buttons_frame,
            text="Export Results",
            command=self.export_results,
            height=40,
            state=ctk.DISABLED
        )
        self.export_button.pack(side=ctk.LEFT, padx=(0, 10))

        # ------------------- Progress Bar -------------------
        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.set(0)
        self.progress.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # ------------------- Logging Panel -------------------
        self.log_box = ctk.CTkTextbox(main_frame, height=180)
        self.log_box.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        # ------------------- Status Label -------------------
        self.status_var = ctk.StringVar(value="Ready to scrape job listings")
        self.status_label = ctk.CTkLabel(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))


    # ----------------------- Worker Thread -----------------------
    def start_scraper_thread(self):
        # Start the scraping process in a separate thread
        if not self.job_entry.get().strip():
            messagebox.showerror("Error", "Please enter a job title to search for.")
            return

        # Disable start button and enable stop button
        self.start_button.configure(state=ctk.DISABLED)
        self.stop_button.configure(state=ctk.NORMAL)
        self.export_button.configure(state=ctk.DISABLED)

        # Clear previous results
        self.job_listings = []
        self.progress.set(0)

        # Start scraping in a separate thread
        self.scraping_active = True
        """ 
            in 'target=self.fake_scraper' 
            replace 'fake_scraper' 
            with the actual scraping function name eg. 'start_scraping'
        """
        self.scraping_thread = threading.Thread(target=self.fake_scraper)
        self.scraping_thread.daemon = True
        self.scraping_thread.start()

    def stop_scraping(self):
        # Stop the scraping process
        self.scraping_active = False
        self.status_var.set("Scraping stopped by user")
        self.log_message("Scraping stopped by user")

        # Immediately disable stop button and re-enable start button
        self.stop_button.configure(state=ctk.DISABLED)
        self.start_button.configure(state=ctk.NORMAL)
        
        # If we have some results, enable export button
        if self.job_listings:
            self.export_button.configure(state=ctk.NORMAL)


    def log_message(self, message):
        # Add a message to the output text widget
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")
        self.update_idletasks()


    def start_scraping(self):
            """
            Main scraping function - runs in a separate thread
            DEVELOPERS  / WEBSCRAPER: Implement your scraping logic here
            """


    # ----------------------- Fake Task -----------------------
    def fake_scraper(self):

        # Simulate progress
        for i in range(1, 6):
            if not self.scraping_active:
                break
            time.sleep(1)
            progress = i / 5
            self.progress.set(progress)
            self.log_message(f"SIMULATION: Progress {int(progress * 100)}%")
            
       

    def enable_buttons(self):
        # Re-enable buttons after scraping is complete
        self.start_button.configure(state=ctk.NORMAL)
        self.stop_button.configure(state=ctk.DISABLED)
        if self.job_listings:
            self.export_button.configure(state=ctk.NORMAL)

    def export_results(self):
        # Export the scraped job listings to a CSV file
        if not self.job_listings:
            messagebox.showwarning("No Data", "No job listings to export.")
            return
            
        # Ask user for file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save job listings as CSV"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Title', 'Company', 'Location', 'Description', 'Apply Link', 'Source']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for job in self.job_listings:
                        writer.writerow(job)
                        
                self.log_message(f"Job listings exported to {filename}")
                messagebox.showinfo("Export Successful", f"Job listings exported to {filename}")
            except Exception as e:
                self.log_message(f"Error exporting to CSV: {str(e)}")
                messagebox.showerror("Export Error", f"Failed to export job listings: {str(e)}")


# Run the app
if __name__ == "__main__":
    app = JobScraperUI()
    app.mainloop()

#Testing