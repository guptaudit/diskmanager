import customtkinter as ctk
import threading
from tkinter import messagebox
from PIL import Image
import os
import disk_utils

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)

# Visual Settings - Material Dark Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue") 

# Material Colors
COLOR_BG = "#121212"
COLOR_SURFACE = "#1E1E1E"
COLOR_PRIMARY = "#BB86FC"       # Light Purple
COLOR_PRIMARY_VARIANT = "#3700B3"
COLOR_SECONDARY = "#03DAC6"     # Teal
COLOR_ERROR = "#CF6679"         # Red/Pink
COLOR_TEXT = "#FFFFFF"
COLOR_TEXT_SEC = "#B0B0B0"

class DiskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DiskManager - CyberRepair")
        self.geometry("700x700")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG)

        # Build path to asset
        self.asset_path = resource_path(os.path.join("assets", "header.png"))

        # Main Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Hero Image
        self.load_image()
        if self.header_image:
            self.image_label = ctk.CTkLabel(self, text="", image=self.header_image)
            self.image_label.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        # 2. Title Section
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.title_frame, 
            text="DiskManager // PRO", 
            font=ctk.CTkFont(family="Roboto Medium", size=28),
            text_color=COLOR_PRIMARY
        )
        self.title_label.pack(side="top", anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame, 
            text="Advanced USB Diagnostic & Repair Utility", 
            font=ctk.CTkFont(family="Roboto", size=14),
            text_color=COLOR_TEXT_SEC
        )
        self.subtitle_label.pack(side="top", anchor="w")

        # 3. Control Card
        self.card_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=COLOR_SURFACE, border_width=1, border_color="#333333")
        self.card_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.card_frame.grid_columnconfigure(1, weight=1)

        self.select_label = ctk.CTkLabel(
            self.card_frame, 
            text="TARGET DRIVE", 
            font=ctk.CTkFont(family="Roboto", size=12, weight="bold"),
            text_color=COLOR_SECONDARY
        )
        self.select_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.disk_option_menu = ctk.CTkOptionMenu(
            self.card_frame, 
            values=["Scanning..."], 
            command=self.disk_selected,
            width=300,
            height=35,
            font=ctk.CTkFont(family="Roboto", size=13),
            fg_color="#2C2C2C",
            button_color=COLOR_PRIMARY_VARIANT,
            button_hover_color=COLOR_PRIMARY
        )
        self.disk_option_menu.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ew")

        self.refresh_button = ctk.CTkButton(
            self.card_frame, 
            text="REFRESH", 
            command=self.load_disks,
            width=100,
            height=35,
            fg_color=COLOR_SECONDARY,
            text_color="black",
            hover_color="#018786",
            font=ctk.CTkFont(weight="bold")
        )
        self.refresh_button.grid(row=0, column=2, padx=20, pady=20)

        # 4. Action Area
        self.fix_button = ctk.CTkButton(
            self, 
            text="INITIALIZE REPAIR SEQUENCE", 
            font=ctk.CTkFont(family="Roboto", size=16, weight="bold"),
            fg_color=COLOR_ERROR, 
            hover_color="#B00020", 
            height=55,
            corner_radius=8,
            state="disabled", 
            command=self.confirm_fix
        )
        self.fix_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")

        # 5. Terminal Log
        self.log_textbox = ctk.CTkTextbox(
            self, 
            height=180, 
            fg_color="black", 
            text_color=COLOR_SECONDARY, 
            font=ctk.CTkFont(family="Consolas", size=12),
            activate_scrollbars=True,
            border_width=1,
            border_color="#333333"
        )
        self.log_textbox.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.selected_disk_index = None
        self.disks = []

        # Initial load
        self.log("System initialized.")
        self.log("Waiting for user input...")
        # Auto-load
        self.load_disks()

    def load_image(self):
        try:
            # Check if file exists
            if os.path.exists(self.asset_path):
                raw_img = Image.open(self.asset_path)
                # Resize to fit width (assuming 700 width window, maybe 700x150 banner)
                # Maintaining aspect ratio is better usually, but for banner we might crop or just standard fit.
                # Let's crop center to 700x200
                
                # Resize
                self.header_image = ctk.CTkImage(light_image=raw_img, dark_image=raw_img, size=(700, 200))
            else:
                self.header_image = None
                print(f"Asset not found: {self.asset_path}")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.header_image = None

    def log(self, message):
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")

    def load_disks(self):
        self.log("Scanning bus for storage devices...")
        self.refresh_button.configure(state="disabled")
        threading.Thread(target=self._load_disks_thread, daemon=True).start()

    def _load_disks_thread(self):
        self.disks = disk_utils.list_disks()
        
        if self.disks:
            values = [d['data'] for d in self.disks]
            self.after(0, lambda: self.update_disk_menu(values))
            self.after(0, lambda: self.log(f"Scan complete. {len(self.disks)} devices detected."))
        else:
            self.after(0, lambda: self.log("No removable storage found."))
            self.after(0, lambda: self.update_disk_menu(["No devices detected"]))
        
        self.after(0, lambda: self.refresh_button.configure(state="normal"))

    def update_disk_menu(self, values):
        self.disk_option_menu.configure(values=values)
        self.disk_option_menu.set(values[0])
        self.disk_selected(values[0])

    def disk_selected(self, choice):
        self.selected_disk_index = None
        self.fix_button.configure(state="disabled", text="SELECT TARGET DRIVE", fg_color="#444444")
        
        # Reset if no disks
        if choice == "No devices detected" or choice == "Scanning...":
            return

        for disk in self.disks:
            if disk['data'] == choice:
                self.selected_disk_index = disk['index']
                self.fix_button.configure(state="normal", text="EXECUTE REPAIR PROTOCOL", fg_color=COLOR_ERROR)
                break
    
    def confirm_fix(self):
        if not self.selected_disk_index:
            return

        confirm = messagebox.askyesno(
            "CONFIRM DESTRUCTION", 
            f"TARGET: DISK {self.selected_disk_index}\n"
            "OPERATION: CLEAN & FORMAT\n\n"
            "AUTHORIZATION REQUIRED: All data on this specific volume will be PERMANENTLY ERASED.\n\n"
            "Proceed?",
            icon='warning'
        )
        
        if confirm:
            self.run_fix()

    def run_fix(self):
        self.log(f"AUTH ACCEPTED. TARGETING DISK {self.selected_disk_index}...")
        self.fix_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled")
        self.disk_option_menu.configure(state="disabled")

        threading.Thread(target=self._run_fix_thread, daemon=True).start()

    def _run_fix_thread(self):
        stdout, stderr = disk_utils.fix_disk(self.selected_disk_index)
        
        self.after(0, lambda: self.log("--- DISKPART LOG START ---"))
        self.after(0, lambda: self.log(stdout))
        if stderr:
             self.after(0, lambda: self.log("--- ERROR STREAM ---"))
             self.after(0, lambda: self.log(stderr))
        
        self.after(0, lambda: self.log("Sequence finished."))
        self.after(0, lambda: self.fix_button.configure(state="normal", text="SEQUENCE COMPLETE"))
        self.after(0, lambda: self.refresh_button.configure(state="normal"))
        self.after(0, lambda: self.disk_option_menu.configure(state="normal"))
