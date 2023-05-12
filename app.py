version = "1.0.0"

# From Imports
from tkinter import PhotoImage
from typing import Literal, Optional, Tuple, Union
from PIL import Image
from customtkinter.windows.widgets.font import CTkFont
from windows_toasts import WindowsToaster, ToastImageAndText1, ToastDisplayImage

# Imports
import requests
import customtkinter as ctk
import ctypes
import datetime
import sys
import platform
import webbrowser

# Load theme prefs
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Init main windows toaster
toaster = WindowsToaster('WEAO Desktop Widget')
mainToast = ToastImageAndText1()

# Get the absolute path of the app
import os
app_path = os.path.dirname(os.path.abspath(__file__))

# Set the app icon for toasts
mainToast.AddImage(ToastDisplayImage.fromPath(os.path.join(app_path, "assets/logo.png"), "logo"))


class WEAOExploitsScrollabelFrame(ctk.CTkScrollableFrame):
    cachedExploits = {}
    firstLoad = True
    def get_exploits_online(self) -> dict:
        # Get the exploits online
        r = requests.get("https://api.whatexploitsare.online/status")
        r = r.json()

        # Return the exploits online
        return r

    def reload_exploits(self, shouldNotify: bool = False):
        # Destroy existing cards in the scrollable frame
        for child in self.winfo_children():
            child.destroy()

        # Get the latest exploits online
        statuses = self.get_exploits_online()

        for exploit in statuses:
            name = list(exploit.keys())[0]

            if name == "ROBLOX":
                continue

            exploit_info = exploit[name]

            card_frame = ctk.CTkFrame(self)
            card_frame.pack(pady=10, padx=10, fill="x")

            name_label = ctk.CTkLabel(
                card_frame, text=name, font=("Arial", 14, "bold"))
            name_label.pack(anchor="w")

            version_text = f"Current Version: {exploit_info['exploit_version']} ({exploit_info['roblox_version']})"
            version_label = ctk.CTkLabel(
                card_frame, text=version_text, font=("Arial", 12))
            version_label.pack(anchor="w")

            status_text = " Working " if exploit_info['updated'] else " Not Working "
            status_color = "green" if exploit_info['updated'] else "red"
            status_label = ctk.CTkLabel(card_frame, text=status_text, font=(
                "Arial", 12), corner_radius=10, fg_color=status_color)
            status_label.pack(anchor="w")

            # TEST: Notify the user if the status is cached and the status is different always
            exploitStatusLive = bool(exploit_info['updated'])
            exploitStatusCached = True

            if shouldNotify and exploitStatusCached and exploitStatusLive != exploitStatusCached and not self.firstLoad:
                print(f"Status of {name} has changed to {status_text.lower()} - notifying user")
                mainToast.SetHeadline("Exploit Status Changed")
                mainToast.SetBody(f"The status of {name} has changed to {status_text.lower()}!")
                toaster.show_toast(mainToast)

            # Cache the exploit status
            self.cachedExploits[name] = exploitStatusLive

            if self.firstLoad:
                self.firstLoad = False


    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.reload_exploits()


class WEAOSettingsPage(ctk.CTk):
    #TODO: Implement settings page later
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Add a title
        title_label = ctk.CTkLabel(
            self, text="Settings", font=("Arial", 20), pady=10)
        title_label.pack()

        # Add the settings
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="both", expand=True)

        # Add the settings
        settings_label = ctk.CTkLabel(
            settings_frame, text="Settings go here", font=("Arial", 12))
        settings_label.pack()


def update_check(showEvenIfUpToDate: bool = False):
    r = requests.get("https://raw.githubusercontent.com/SticksDev/WEAODesktopWidget/main/version.json")
    r = r.json()

    if r["latest"] != version:
        if r["forceupdate"]:   
            ctypes.windll.user32.MessageBoxW(0, f"An update is required to continue using the WEAO Desktop Widget. Please visit the releases page to download the latest version.\n\nCurrent Version: {version}\nLatest Version: {r['latest']}\nChanges: {r['changes']}", "WEAO Desktop Widget: Update Required", 0x10)
            webbrowser.open("https://github.com/SticksDev/WEAODesktopWidget/releases/")
            exit(0)
        else:
            ctypes.windll.user32.MessageBoxW(0, f"An update is available for the WEAO Desktop Widget. Please visit the releases page to download the latest version.\n\nCurrent Version: {version}\nLatest Version: {r['latest']}\nChanges: {r['changes']}", "WEAO Desktop Widget: Update Available", 0x40)
            webbrowser.open("https://github.com/SticksDev/WEAODesktopWidget/releases/")
    else:
        if showEvenIfUpToDate:
            ctypes.windll.user32.MessageBoxW(0, f"You are running the latest version of the WEAO Desktop Widget.\n\nCurrent Version: {version}\nLatest Version: {r['version']}", "WEAO Desktop Widget: Up To Date", 0x40)


class WEAODesktopWidgetApp(ctk.CTk):
    refreshTimerUserPref = 250
    refreshTimer = refreshTimerUserPref
    shouldRunTimer = True
    shouldNotifyOnUpdate = False
    shouldNotifyOnRefresh = False
    refreshTextWidget = None
    exploitStatusesWidget = None
    rbx_version = "Fetching..."

    def _refreshTimerTick(self):
        # If not zero, decrement the timer and update the text
        if self.refreshTimer != 0:
            self.refreshTimer -= 1
            self.refreshTextWidget.configure(
                text=f"Refresh in {self.refreshTimer} seconds")
            self.after(1000, self._refreshTimerTick)
        else:
            # Reset the timer
            self.refreshTimer = self.refreshTimerUserPref

            # Inform the user that the exploits are being reloaded
            self.refreshTextWidget.configure(
                text=f"Reloading data, please wait...")

            self.update()

            # Reload the exploits
            self.exploitStatusesWidget.reload_exploits(self.shouldNotifyOnUpdate)

            # Inform the user that the exploits have been reloaded
            self.refreshTextWidget.configure(
                text=f"Refresh succesful! Refresh in {self.refreshTimer} seconds")
            
            # Notify the user if they want to be notified
            if self.shouldNotifyOnRefresh:
                mainToast.SetHeadline("Refresh Complete")
                mainToast.SetBody("The exploits have been reloaded successfully!")
                toaster.show_toast(mainToast)


            # Restart the timer
            self.after(1000, self._refreshTimerTick)

    def handleChecked(self, event: str, value: int):
        value = bool(value)
        
        if event == "update":
            self.shouldNotifyOnUpdate = value
        elif event == "notify":
            self.shouldNotifyOnRefresh = value

    def getRobloxVersion(self) -> str:
        # Get the roblox version
        r = requests.get("https://setup.rbxcdn.com/version")
        r = r.text

        # Return the roblox version
        return r
    
    def handleSetDelay(self):
       dialog = ctk.CTkInputDialog(text="Please set a refresh delay (in seconds).\nCannot be less then 100", title="Set Delay")
       result = dialog.get_input()
       
       if result is not None:
              try:
                result = int(result)
              except:
                ctypes.windll.user32.MessageBoxW(0, "Please enter a valid number.", "WEAO Desktop Widget: Error", 0x10)
                return
    
              if result < 100:
                ctypes.windll.user32.MessageBoxW(0, "Please enter a number greater then 100.", "WEAO Desktop Widget: Error", 0x10)
                return
              
              self.refreshTimer = result
              self.refreshTimerUserPref = result
              ctypes.windll.user32.MessageBoxW(0, f"Refresh delay set to {result} seconds and timer reset.", "WEAO Desktop Widget: Success", 0x40)
              return

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        print("WEAO Desktop Widget Initializing...")
        super().__init__(fg_color, **kwargs)

        # Load logo
        logoImg = Image.open("assets/logo.png")
        settingsSvg = Image.open("assets/settings.png")

        # Set the icon
        self.iconphoto(True, PhotoImage(file="assets/logo.png"))
        self.iconbitmap(bitmap="assets/logo.ico")

        # Set window title
        self.title("WEAO Desktop Widget")

        # Set window size and position
        self.geometry("600x500")
        self.resizable(False, False)

        # Gridconfigure
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set widget
        self.exploitStatusesWidget = WEAOExploitsScrollabelFrame(self)

        # Get the roblox version
        rbx_version = self.getRobloxVersion()

        # Add a logo
        logo = ctk.CTkImage(dark_image=logoImg,
                            light_image=logoImg, size=(100, 100))
        logoUi = ctk.CTkLabel(self, image=logo, text="")
        logoUi.pack(side="top", pady=10)

        # Add the text label
        text_label = ctk.CTkLabel(
            self, text="What Exploits Are Online", font=("Arial", 20), pady=10)
        text_label.pack()

        # Checkbox to notify the user if there is an update
        update_checkbox = ctk.CTkCheckBox(
            self, text="Notify me when an exploit status changes", font=("Arial", 12), command=(lambda: self.handleChecked("update", update_checkbox.get())), checkbox_height=20, checkbox_width=20)
        update_checkbox.pack(pady=3)

        # Notify when refresh complete
        notify_checkbox = ctk.CTkCheckBox(
            self, text="Notify me when refresh is complete", font=("Arial", 12), command=(lambda: self.handleChecked("notify", notify_checkbox.get())), checkbox_height=20, checkbox_width=20)
        notify_checkbox.pack(pady=3)

        # Add set delay button
        set_delay_button = ctk.CTkButton(
            self, text="Set Refresh Delay", font=("Arial", 12), command=self.handleSetDelay)
        set_delay_button.place(x=10, y=10)

        # Refresh in text label
        refresh_in_label = ctk.CTkLabel(
            self, text=f"Refresh in {self.refreshTimer} seconds", font=("Arial", 12))
        refresh_in_label.pack()

        self.refreshTextWidget = refresh_in_label

        # Add software and Roblox version information
        version_label = ctk.CTkLabel(
            self, text=f"Software Version: 1.0\nRoblox Version: {rbx_version}", font=("Arial", 10))
        version_label.pack(side="bottom", pady=10, padx=10)

        print("WEAO Desktop Widget Initialized!")
        print("Getting Exploits Online...")

        # Add the scrollable frame
        scrollable_frame = WEAOExploitsScrollabelFrame(self)
        self.exploitStatusesWidget = scrollable_frame

        # Pack the scrollable frame
        scrollable_frame.pack(fill="both", expand=True)
        self.after(1000, self._refreshTimerTick)


if __name__ == "__main__":
    try: 
        # Check for updates BEFORE the app is initialized
        update_check()
        app = WEAODesktopWidgetApp()
        app.mainloop()
    except Exception as e:
        # Show a windows message box
        ctypes.windll.user32.MessageBoxW(0, f"An error occured while running the app: {e}\n\nPlease send the crashlog-<DATE> file to sticks#2701 in the WEAO discord.", "WEAO Desktop Widget: Critcal Error", 0x10)

        # Generate a crashlog-date file
        with open(f"crashlog-{datetime.datetime.now().strftime('%Y-%m-%d')}.txt", "w") as f:
            f.write("WEAO Desktop Widget Crashlog\n")
            f.write(f"OS Platform: {platform.platform()} on {platform.processor()}\n")
            f.write(f"Python Version: {sys.version}\n")
            f.write("========================================\n")
            f.write(f"Stacktrace: {e}\n")
            f.write("========================================\n")

        print("[ERR]: An error occured while running the app: " + str(e))
        # Exit the app
        exit(1)
