import sys
import ctypes
import gui

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if is_admin():
        # Already admin, run the app
        app = gui.DiskManagerApp()
        app.mainloop()
    else:
        # Re-run the program with admin rights
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        # However, since we might be running the script directly or via python
        # We need to reconstruct the command.
        print("Requesting administrator privileges...")
        try:
            if getattr(sys, 'frozen', False):
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
            else:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
        except Exception as e:
            print(f"Error elevating privileges: {e}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
