# DiskManager

DiskManager is a Python-based GUI application designed to simplify disk management tasks using the Windows `diskpart` utility. It features a modern, dark-themed interface and automates common disk repair/format operations.

## Features

*   **User-Friendly Interface**: Built with `customtkinter` for a modern look and feel.
*   **Disk Detection**: Automatically identifies removable USB drives.
*   **Quick Fix**: Automates the process of cleaning and formatting drives (Clean -> Create Partition -> Format FS=NTFS -> Quick).
*   **Safety Checks**: Only lists removable drives to prevent accidental data loss on system drives.
*   **Admin Elevation**: Automatically requests administrator privileges required for low-level disk operations.

## executable File

You can find the standalone executable in the `dist` directory. This allows you to run the application without installing Python.

**[Download/Open DiskManager.exe](dist/DiskManager.exe)**

> **Note**: You must run this application on Windows.

## Installation & Running from Source

If you prefer to run the source code or contribute:

### Prerequisites

*   Python 3.8 or higher
*   Windows OS

### Steps

1.  **Clone the repository** (if applicable) or download the source.

2.  **Install Dependencies**:
    ```bash
    pip install customtkinter pillow packaging
    ```

3.  **Run the Application**:
    ```bash
    python main.py
    ```

## Building the Executable

If you want to rebuild the `.exe` yourself (e.g., after modifying code):

1.  Install `pyinstaller`:
    ```bash
    pip install pyinstaller
    ```

2.  Run the build command:
    ```bash
    pyinstaller DiskManager.spec
    ```
    Or manually:
    ```bash
    pyinstaller --noconfirm --onedir --windowed --icon "assets/icon.ico" --name "DiskManager" --add-data "c:/Users/gupta/AppData/Local/Programs/Python/Python312/Lib/site-packages/customtkinter;customtkinter/" "main.py"
    ```
    *(Note: Using the `.spec` file is recommended if available)*

## Troubleshooting

*   **"Access Denied"**: Ensure you accept the UAC (User Account Control) prompt. `diskpart` requires Administrator privileges.
*   **No Disks Found**: Ensure your USB drive is plugged in. The tool filters for 'Removable' drives to protect your system disk.
