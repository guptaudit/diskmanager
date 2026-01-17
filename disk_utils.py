import subprocess
import re

def run_diskpart_script(script_content):
    """
    Runs a diskpart script and returns the output.
    """
    try:
        # diskpart expects input via stdin or a script file. 
        # Using stdin via subprocess is cleaner for dynamic commands.
        process = subprocess.Popen(
            ['diskpart'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=script_content)
        return stdout, stderr
    except Exception as e:
        return "", str(e)

def list_disks():
    """
    Parses 'list disk' output from diskpart.
    Returns a list of dicts: [{'index': '0', 'size': '476 GB', 'free': '0 B', 'gpt': True}, ...]
    """
    script = "list disk"
    stdout, stderr = run_diskpart_script(script)
    
    disks = []
    # Regex to capture Disk ###, Size, Free. 
    # Typical line: "  Disk 0    Online          476 GB      0 B        *"
    # We'll simple split by lines and look for "Disk" followed by a number.
    
    lines = stdout.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("Disk") and len(line) > 5:
            # simple parsing strategy: split by multiple spaces
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 3:
                # Part 0: "Disk <N>"
                # Part 1: Status (Online/Offline)
                # Part 2: Size
                # Part 3: Free
                # ...
                
                # Let's use a robust regex instead
                match = re.search(r'Disk (\d+)\s+([A-Za-z]+)\s+([\d\w\s\.]+)\s+([\d\w\s\.]+)', line)
                if match:
                    disk_info = {
                        'index': match.group(1),
                        'status': match.group(2),
                        'size': match.group(3).strip(),
                        'data': line # keep full line for display
                    }
                    disks.append(disk_info)
    return disks

def fix_disk(disk_index):
    """
    Executes the clean and format sequence on the specified disk.
    WARNING: DESTRUCTIVE.
    """
    commands = [
        f"select disk {disk_index}",
        "clean",
        "create partition primary",
        "format fs=fat32 quick",
        "active",
        "assign",
        "exit"
    ]
    script = "\n".join(commands)
    return run_diskpart_script(script)
