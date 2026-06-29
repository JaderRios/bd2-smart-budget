import customtkinter as ctk
from ui.app_window import AppWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = AppWindow()
    app.mainloop()
