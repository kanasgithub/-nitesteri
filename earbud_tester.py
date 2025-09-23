import tkinter as tk
import bluetooth

def find_devices():
    
    print("Scanning for Bluetooth devices...")
    for widget in discovery_frame.winfo_children():
        if isinstance(widget,deviceWindow):
            widget.destroy()

    devices = bluetooth.discover_devices(duration=1, lookup_names=True)

    for addr, name in devices:
        print(f"Found: {name} [{addr}]")
        deviceWindow(discovery_frame, name, addr)
    global scanned
    scanned = devices


class deviceWindow(tk.Frame): #laiteikkuna joka händlää laitteet ja niiden palautuksen

    def __init__(self, parent,name,MAC):
        
        self.name = tk.StringVar()
        self.MAC = tk.StringVar()

        self.name.set(name)
        self.MAC.set(MAC)

        tk.Frame.__init__(self, parent)
        device_name = tk.Label(self, textvariable=self.name,justify="left")
        device_mac = tk.Label(self,textvariable=self.MAC,justify="right")
        
        device_name.grid(column=0,row=0)
        device_mac.grid(column=1,row=0)
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





