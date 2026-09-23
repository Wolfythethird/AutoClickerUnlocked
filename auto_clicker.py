import sys
import threading
import time
import click
import customtkinter as ctk
from pynput import keyboard, mouse


# --- Core Engine Shared by CLI and GUI ---
class AutoClickerEngine:

    def __init__(self, cps=10, uncapped=False):
        self.cps = cps
        self.uncapped = uncapped
        self.running = False
        self.mouse_controller = mouse.Controller()
        self.listener = None
        self.click_thread = None
        self._stop_requested = False

    def start_engine(self, on_toggle_callback=None):
        self._stop_requested = False

        # Thread for clicking loop
        self.click_thread = threading.Thread(
            target=self._click_loop, daemon=True
        )
        self.click_thread.start()

        # Keyboard listener for global F6 hotkey
        def on_press(key):
            if key == keyboard.Key.f6:
                self.running = not self.running
                if on_toggle_callback:
                    on_toggle_callback(self.running)

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def stop_engine(self):
        self.running = False
        self._stop_requested = True
        if self.listener:
            self.listener.stop()

    def _click_loop(self):
        while not self._stop_requested:
            if self.running:
                self.mouse_controller.click(mouse.Button.left)
                if self.uncapped:
                    # 1 millisecond sleep prevents the CPU from locking up
                    # so the F6 hotkey can still be detected.
                    time.sleep(0.001)
                else:
                    time.sleep(1.0 / self.cps)
            else:
                time.sleep(0.02)


# --- GUI Implementation ---
def launch_gui(default_cps=10, default_uncapped=False):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Auto Clicker")
    app.geometry("360x340")
    app.resizable(False, False)

    engine = AutoClickerEngine(cps=default_cps, uncapped=default_uncapped)

    title_label = ctk.CTkLabel(
        app, text="Auto Clicker", font=("Arial", 20, "bold")
    )
    title_label.pack(pady=(20, 10))

    status_label = ctk.CTkLabel(
        app, text="Status: OFF", font=("Arial", 14, "bold"), text_color="#FF5555"
    )
    status_label.pack(pady=5)

    cps_label = ctk.CTkLabel(
        app, text=f"Speed: {engine.cps} CPS", font=("Arial", 12)
    )
    cps_label.pack(pady=(10, 5))

    def update_cps(val):
        engine.cps = int(val)
        if not engine.uncapped:
            cps_label.configure(text=f"Speed: {engine.cps} CPS")

    slider = ctk.CTkSlider(
        app, from_=1, to=50, number_of_steps=49, command=update_cps
    )
    slider.set(engine.cps)
    slider.pack(pady=5, padx=30, fill="x")

    # Uncapped Checkbox Logic
    def toggle_uncapped():
        engine.uncapped = uncapped_var.get()
        if engine.uncapped:
            slider.configure(state="disabled")
            cps_label.configure(text="Speed: MAX / UNCAPPED", text_color="#F1FA8C")
        else:
            slider.configure(state="normal")
            cps_label.configure(text=f"Speed: {engine.cps} CPS", text_color="white")

    uncapped_var = ctk.BooleanVar(value=default_uncapped)
    uncapped_checkbox = ctk.CTkCheckBox(
        app, text="Uncapped Speed", variable=uncapped_var, command=toggle_uncapped
    )
    uncapped_checkbox.pack(pady=10)

    if default_uncapped:
        toggle_uncapped()

    def toggle_action():
        engine.running = not engine.running
        on_toggle(engine.running)

    toggle_btn = ctk.CTkButton(
        app,
        text="Toggle (F6)",
        fg_color="#2EA043",
        hover_color="#268337",
        command=toggle_action,
    )
    toggle_btn.pack(pady=(5, 10))

    def on_toggle(is_running):
        if is_running:
            status_label.configure(text="Status: ON", text_color="#50FA7B")
            toggle_btn.configure(
                text="Stop (F6)", fg_color="#E63946", hover_color="#C1292E"
            )
        else:
            status_label.configure(text="Status: OFF", text_color="#FF5555")
            toggle_btn.configure(
                text="Start (F6)", fg_color="#2EA043", hover_color="#268337"
            )

    engine.start_engine(on_toggle_callback=on_toggle)

    def on_close():
        engine.stop_engine()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)
    app.mainloop()


# --- CLI Implementation ---
def run_cli(cps, uncapped):
    engine = AutoClickerEngine(cps=cps, uncapped=uncapped)

    def on_toggle(is_running):
        state = "STARTED" if is_running else "STOPPED"
        print(f"[Auto Clicker] {state}")

    if uncapped:
        print("Auto Clicker running at UNCAPPED speed.")
    else:
        print(f"Auto Clicker running at {cps} CPS.")
        
    print("Press F6 to toggle clicking. Press Ctrl+C in terminal to exit.")

    engine.start_engine(on_toggle_callback=on_toggle)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting Auto Clicker...")
        engine.stop_engine()


# --- CLI Command Parsing with Click ---
@click.command()
@click.option(
    "--cli", is_flag=True, help="Run in terminal mode instead of GUI mode."
)
@click.option(
    "--cps", default=10, type=int, help="Set starting clicks per second."
)
@click.option(
    "--uncapped", is_flag=True, help="Run as fast as possible, ignoring CPS."
)
def main(cli, cps, uncapped):
    """Auto Clicker application with GUI and CLI support."""
    if cli:
        run_cli(cps, uncapped)
    else:
        launch_gui(cps, uncapped)


if __name__ == "__main__":
    main()
