import pyautogui
import time
from PIL import ImageGrab, Image
import tkinter as tk
import threading
import keyboard
import pystray
from pystray import MenuItem as item

class AutoAcceptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Accept - By Pedro")
        self.root.geometry("370x380")
        self.root.configure(bg="#06122b")
        self.status_color = "#FFFFFF"
        self.button_color = "#0a1b40"
        self.button_hover_color = "#0e317d"
        self.searching = True

        self.root.config(cursor="arrow")

        self.status_text = tk.Text(self.root, wrap=tk.WORD, width=60, height=15, bg="#06122b", fg=self.status_color, font=("Comic Sans M", 12, "bold"), bd=0, padx=10)
        self.status_text.pack(pady=10)
        self.status_text.insert(tk.END, "Status: Aceitando automaticamente...\n")
        self.status_text.config(state=tk.DISABLED)

        self.status_text.config(cursor="arrow")

        self.button_frame = tk.Frame(self.root, bg="#06122b")
        self.button_frame.pack(pady=10)

        self.toggle_button = tk.Button(self.button_frame, text="Desativar", command=self.toggle_searching, height=2, width=10, bg=self.button_color, fg="white", font=("Comic Sans M", 12, "bold"))
        self.toggle_button.pack(side=tk.LEFT, padx=10)

        self.close_button = tk.Button(self.button_frame, text="Fechar", command=self.close_program, height=2, width=10, bg=self.button_color, fg="white", font=("Comic Sans M", 12, "bold"))
        self.close_button.pack(side=tk.LEFT, padx=10)

        self.gear_button = tk.Button(self.root, text="⚙️", command=self.gear_button_action, height=1, width=3, bg=self.root.cget("bg"), fg="white", font=("Comic Sans M", 12, "bold"), bd=0,
                                     highlightthickness=0, highlightbackground=self.root.cget("bg"), relief="flat")
        self.gear_button.place(x=5, y=345)

        self.theme_menu = tk.Menu(self.root, tearoff=0)
        self.theme_menu.add_command(label="Claro", command=self.set_light_theme)
        self.theme_menu.add_command(label="Dark", command=self.set_dark_theme)

        self.toggle_button.bind("<Enter>", self.on_button_hover)
        self.toggle_button.bind("<Leave>", self.on_button_leave)

        self.close_button.bind("<Enter>", self.on_button_hover)
        self.close_button.bind("<Leave>", self.on_button_leave)

        self.gear_button.bind("<Enter>", self.on_gear_button_hover)
        self.gear_button.bind("<Leave>", self.on_gear_button_leave)

        self.stop_event = threading.Event()

        self.run_thread = threading.Thread(target=self.click_accept_button)
        self.run_thread.daemon = True
        self.run_thread.start()

        self.monitor_key_thread = threading.Thread(target=self.monitor_keys)
        self.monitor_key_thread.daemon = True
        self.monitor_key_thread.start()

        self.icon = pystray.Icon("auto_accept", Image.open("icon.png"), menu=None)
        self.icon_thread = threading.Thread(target=self.icon.run)
        self.icon_thread.daemon = True
        self.icon_thread.start()

        self.icon.icon = Image.open("icon.png")
        self.icon.visible = True
        self.icon.menu = pystray.Menu(item("Abrir", self.restore_window), item("Fechar", self.close_program))

    def toggle_searching(self):
        self.searching = not self.searching
        if self.searching:
            self.toggle_button.config(text="Desativar")
            self.update_status("Status: Aceitando automaticamente...\n")
        else:
            self.toggle_button.config(text="Ativar")
            self.update_status("Status: Desativado.\n")

    def update_status(self, status_text):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, status_text)
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)

    def click_accept_button(self):
        while not self.stop_event.is_set():
            if self.searching:
                try:
                    screenshot = ImageGrab.grab(all_screens=True)
                    accept_button_location = pyautogui.locate("aceitar.png", screenshot, confidence=0.7)

                    if accept_button_location:
                        self.update_status("Partida aceita!\n")
                        accept_button_center = pyautogui.center(accept_button_location)
                        pyautogui.mouseDown(x=accept_button_center[0], y=accept_button_center[1])
                        pyautogui.mouseUp(x=accept_button_center[0], y=accept_button_center[1])

                        self.update_status("Aceitando novamente...\n")
                        time.sleep(1)

                except Exception as e:
                    pass

            time.sleep(12)

    def minimize_to_tray(self):
        self.root.withdraw()

    def restore_window(self, icon, item):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def close_program(self, _=None):
        self.stop_event.set()
        self.icon.stop()
        self.root.quit()

    def monitor_keys(self):
        while not self.stop_event.is_set():
            if self.root.focus_get() is not None and keyboard.is_pressed('ctrl+w'):
                self.close_program()
                break
            time.sleep(0.1)

    def gear_button_action(self):
        self.theme_menu.post(self.gear_button.winfo_rootx(), self.gear_button.winfo_rooty())

    def set_light_theme(self):
        self.root.configure(bg="white")
        self.status_text.config(bg="white", fg="black")
        self.button_color = "#f0f0f0"
        self.button_hover_color = "#d1d1d1"
        self.toggle_button.config(bg=self.button_color, fg="black")
        self.close_button.config(bg=self.button_color, fg="black")
        self.gear_button.config(bg="white", fg="black")
        self.button_frame.config(bg="white")
        self.update_status("Tema claro ativado.\n")

    def set_dark_theme(self):
        self.root.configure(bg="#06122b")
        self.status_text.config(bg="#06122b", fg="white")
        self.button_color = "#0a1b40"
        self.button_hover_color = "#0e317d"
        self.toggle_button.config(bg=self.button_color, fg="white")
        self.close_button.config(bg=self.button_color, fg="white")
        self.gear_button.config(bg="#06122b", fg="white")
        self.button_frame.config(bg="#06122b")
        self.update_status("Tema dark ativado.\n")

    def on_button_hover(self, event):
        event.widget.config(bg=self.button_hover_color)
        event.widget.config(cursor="hand2")

    def on_button_leave(self, event):
        event.widget.config(bg=self.button_color)
        event.widget.config(cursor="arrow")

    def on_gear_button_hover(self, event):
        event.widget.config(cursor="hand2")

    def on_gear_button_leave(self, event):
        event.widget.config(cursor="arrow")


root = tk.Tk()
app = AutoAcceptApp(root)
root.protocol("WM_DELETE_WINDOW", app.minimize_to_tray)
root.mainloop()
