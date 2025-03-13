import pyautogui
import time
from PIL import ImageGrab
import tkinter as tk
import threading
import keyboard

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

        # Definindo o cursor como "seta" para toda a janela
        self.root.config(cursor="arrow")

        self.status_text = tk.Text(self.root, wrap=tk.WORD, width=60, height=15, bg="#06122b", fg=self.status_color, font=("Comic Sans M", 12, "bold"), bd=0, padx=10)
        self.status_text.pack(pady=10)
        self.status_text.insert(tk.END, "Status: Aceitando automaticamente...\n")
        self.status_text.config(state=tk.DISABLED)

        # Definindo o cursor como "seta" para o widget de texto também
        self.status_text.config(cursor="arrow")

        self.button_frame = tk.Frame(self.root, bg="#06122b")
        self.button_frame.pack(pady=10)

        self.toggle_button = tk.Button(self.button_frame, text="Desativar", command=self.toggle_searching, height=2, width=10, bg=self.button_color, fg="white", font=("Comic Sans M", 12, "bold"))
        self.toggle_button.pack(side=tk.LEFT, padx=10)

        self.close_button = tk.Button(self.button_frame, text="Fechar", command=self.close_program, height=2, width=10, bg=self.button_color, fg="white", font=("Comic Sans M", 12, "bold"))
        self.close_button.pack(side=tk.LEFT, padx=10)

        # Botão de Engrenagem (sem borda e fundo)
        self.gear_button = tk.Button(self.root, text="⚙️", command=self.gear_button_action, height=1, width=3, bg=self.root.cget("bg"), fg="white", font=("Comic Sans M", 12, "bold"), bd=0,
                                     highlightthickness=0, highlightbackground=self.root.cget("bg"), relief="flat")
        # Ajustando a posição 'y' para alinhar com a base dos botões
        self.gear_button.place(x=5, y=345)  # Posição no canto inferior esquerdo, subindo um pouco

        # Menu de Tema
        self.theme_menu = tk.Menu(self.root, tearoff=0)
        self.theme_menu.add_command(label="Claro", command=self.set_light_theme)
        self.theme_menu.add_command(label="Dark", command=self.set_dark_theme)

        # Bind do hover nos botões
        self.toggle_button.bind("<Enter>", self.on_button_hover)
        self.toggle_button.bind("<Leave>", self.on_button_leave)

        self.close_button.bind("<Enter>", self.on_button_hover)
        self.close_button.bind("<Leave>", self.on_button_leave)

        # Bind do hover no botão de engrenagem
        self.gear_button.bind("<Enter>", self.on_gear_button_hover)
        self.gear_button.bind("<Leave>", self.on_gear_button_leave)

        self.run_thread = threading.Thread(target=self.click_accept_button)
        self.run_thread.daemon = True  
        self.run_thread.start()

        self.monitor_key_thread = threading.Thread(target=self.monitor_keys)
        self.monitor_key_thread.daemon = True  
        self.monitor_key_thread.start()

    def toggle_searching(self):
        self.searching = not self.searching
        if self.searching:
            self.toggle_button.config(text="Desativar")
            self.update_status("Status: Ativado, aceitando automaticamente...\n")
        else:
            self.toggle_button.config(text="Ativar")
            self.update_status("Status: Desativado.\n")

    def update_status(self, status_text):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, status_text)  
        self.status_text.config(state=tk.DISABLED)
        self.status_text.see(tk.END)

    def click_accept_button(self):
        while True:
            if self.searching:
                try:
                    screenshot = ImageGrab.grab(all_screens=True)  
                    accept_button_location = pyautogui.locate("aceitar.png", screenshot, confidence=0.7)

                    if accept_button_location:
                        self.update_status("Partida aceita!\n")
                        accept_button_center = pyautogui.center(accept_button_location)
                        pyautogui.mouseDown(x=accept_button_center[0], y=accept_button_center[1])
                        pyautogui.mouseUp(x=accept_button_center[0], y=accept_button_center[1])

                        self.update_status("Reiniciando busca...\n")
                        time.sleep(1)  

                except Exception:
                    pass

            time.sleep(0.5)  

    def close_program(self):
        self.root.quit()  

    def monitor_keys(self):
        while True:
            if self.root.focus_get() is not None and keyboard.is_pressed('ctrl+w'):
                self.close_program()  
                break
            time.sleep(0.1)

    def gear_button_action(self):
        # Exibe o menu de temas quando o botão de engrenagem é clicado
        self.theme_menu.post(self.gear_button.winfo_rootx(), self.gear_button.winfo_rooty())

    def set_light_theme(self):
        # Mudar para o tema claro
        self.root.configure(bg="white")
        self.status_text.config(bg="white", fg="black")
        self.button_color = "#f0f0f0"
        self.button_hover_color = "#d1d1d1"
        self.toggle_button.config(bg=self.button_color, fg="black")
        self.close_button.config(bg=self.button_color, fg="black")
        self.gear_button.config(bg="white", fg="black")  # Definir o fundo do botão de engrenagem para branco
        self.button_frame.config(bg="white")  # Definir o fundo do quadro de botões como branco
        self.update_status("Tema claro ativado.\n")

    def set_dark_theme(self):
        # Mudar para o tema dark
        self.root.configure(bg="#06122b")
        self.status_text.config(bg="#06122b", fg="white")
        self.button_color = "#0a1b40"
        self.button_hover_color = "#0e317d"
        self.toggle_button.config(bg=self.button_color, fg="white")
        self.close_button.config(bg=self.button_color, fg="white")
        self.gear_button.config(bg="#06122b", fg="white")  # Definir o fundo do botão de engrenagem para o fundo escuro
        self.button_frame.config(bg="#06122b")  # Definir o fundo do quadro de botões como escuro
        self.update_status("Tema dark ativado.\n")

    def on_button_hover(self, event):
        event.widget.config(bg=self.button_hover_color)
        event.widget.config(cursor="hand2")  # Mudando o cursor para "hand2" (mãozinha) quando o mouse passa sobre os botões

    def on_button_leave(self, event):
        event.widget.config(bg=self.button_color)
        event.widget.config(cursor="arrow")  # Voltando o cursor para "arrow" (seta) quando sai dos botões

    def on_gear_button_hover(self, event):
        event.widget.config(cursor="hand2")  # Mudando o cursor para "hand2" (mãozinha) quando o mouse passa sobre o botão de engrenagem

    def on_gear_button_leave(self, event):
        event.widget.config(cursor="arrow")  # Voltando o cursor para "arrow" (seta) quando sai do botão de engrenagem


root = tk.Tk()
app = AutoAcceptApp(root)
root.mainloop()
