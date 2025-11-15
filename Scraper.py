import customtkinter as ctk
import threading
import time

# -----------------------
# App Configuration
# -----------------------
ctk.set_appearance_mode("dark")      # "light" or "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"


class JobScraperUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Job Scraper UI")
        self.geometry("800x550")

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

        # ------------------- Start Button -------------------
        self.start_button = ctk.CTkButton(
            main_frame,
            text="Start Scraping",
            command=self.start_scraper_thread,
            height=40
        )
        self.start_button.grid(row=3, column=0, columnspan=2, pady=20)

        # ------------------- Progress Bar -------------------
        self.progress = ctk.CTkProgressBar(main_frame)
        self.progress.set(0)
        self.progress.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # ------------------- Logging Panel -------------------
        self.log_box = ctk.CTkTextbox(main_frame, height=180)
        self.log_box.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    # ----------------------- Worker Thread -----------------------
    def start_scraper_thread(self):
        thread = threading.Thread(target=self.fake_scraper)
        thread.start()

    # ----------------------- Fake Task -----------------------
    def fake_scraper(self):
        self.log("Scraper started...\n")

        for i in range(1, 11):
            time.sleep(0.5)  # simulate work
            self.progress.set(i / 10)
            self.log(f"Progress: {i * 10}%\n")

        self.log("Scraper finished successfully!\n")

    # ----------------------- Logging Helper -----------------------
    def log(self, text):
        self.log_box.insert("end", text)
        self.log_box.see("end")


# Run the app
if __name__ == "__main__":
    app = JobScraperUI()
    app.mainloop()
