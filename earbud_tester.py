import tkinter as tk
import bluetooth
from pydbus import SystemBus
import subprocess
import time
import threading
def find_devices():
    
    print("Scanning for Bluetooth devices...")
    for widget in discovery_frame.winfo_children():
        if isinstance(widget,scanlist_object):
            widget.destroy()

    devices = bluetooth.discover_devices(duration=1, lookup_names=True)

    for addr, name in devices:
        print(f"Found: {name} [{addr}]")
        scanlist_object(discovery_frame, name, addr)
    global scanned
    scanned = devices

def open_databox(name,mac):
    databox(name,mac)

def keep_scanning():
    btctl = subprocess.Popen(
        ['bluetoothctl'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Send commands
    btctl.stdin.write('power on\n')
    btctl.stdin.write('scan on\n')
    btctl.stdin.flush()

    # Read output in a loop (optional, or just keep alive)
    while True:
        output = btctl.stdout.readline()
        if output == '' and btctl.poll() is not None:
            break
  

# Run in a background thread so your main app remains responsive
threading.Thread(target=keep_scanning, daemon=True).start()


def connect_device(mac):
    subprocess.run((["bluetoothctl","connect",mac]))

def get_battery(self,mac):
    btctl = subprocess.Popen(
    ['bluetoothctl'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

    # Send commands
    btctl.stdin.write('info\n')
    
    btctl.stdin.flush()

    # Read output in a loop (optional, or just keep alive)
    while True:
        for line in btctl.stdout:
            if "Battery" in line:
                break
            start = line.find('(')
            end = line.find(')')
            if start != -1 and end != -1:
                battery_level = line[start+1:end].strip()
                break
    
        




class databox(tk.Toplevel): #databox uusi ikkuna joka laitteelle joka on yhdistetty
    def __init__(self,name,MAC):
        super().__init__()
    
 

        self.geometry("400x400")
        self.name = tk.StringVar()
        self.MAC = tk.StringVar()

        self.name.set(name)
        self.MAC.set(MAC)
    # ========= name-frame========= #
        name_frame = tk.Frame(self)
        name_entry = tk.Entry(name_frame,textvariable=self.name,justify="center")
        address_label = tk.Label(name_frame,textvariable=self.MAC,justify="center")

        name_entry.grid   (row=0,column=0)
        address_label.grid(row=1,column=0)
        name_frame.pack()

        connect_device(MAC)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def on_close(self):
        subprocess.run(["bluetoothctl","disconnect",self.MAC.get()])
        self.destroy()

class scanlist_object(tk.Frame): #laiteikkuna joka händlää laitteet ja niiden palautuksen

    def __init__(self, parent,name,MAC):
        
        self.name = tk.StringVar()
        self.MAC = tk.StringVar()

        self.name.set(name)
        self.MAC.set(MAC)

        tk.Frame.__init__(self, parent)
        device_name = tk.Label(self, textvariable=self.name,justify="left")
        device_mac = tk.Label(self,textvariable=self.MAC,justify="right")
        connect_button = tk.Button(self,text="Connect",command=lambda:open_databox(name,MAC))
        
        device_name.grid(column=0,row=0)
        device_mac.grid(column=1,row=0)
        connect_button.grid(column=2, row=0)
        self.pack()
        



app = tk.Tk()
scanned=None
app.geometry("280x280")

discovery_frame = tk.Frame(app)


hae_laitteet_nappi = tk.Button(discovery_frame,text="Hae Laitteet",justify="center",command=find_devices)
hae_laitteet_teksti = tk.Label(discovery_frame,text="Hae laitteet",justify="center")

hae_laitteet_teksti.pack()
hae_laitteet_nappi.pack()


discovery_frame.pack()



app.mainloop()





