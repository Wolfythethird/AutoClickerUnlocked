# AutoClickerUnlocked

A feature-rich, high-performance Python auto clicker featuring custom CPS rates, an uncapped speed mode, a dark-mode GUI, and command-line support.

## Features

- **GUI & CLI Support:** Run a dark-themed GUI built with `customtkinter` or execute commands directly in the terminal.
- **Customizable Speed:** Set a target Clicks Per Second (CPS) rate between 1 and 50.
- **Uncapped Speed Mode:** Remove rate limits to process clicks as fast as possible.
- **Global Hotkey:** Toggle clicking on or off at any time using the **F6** key.

---

## Prerequisites & Installation

### Requirements
- Python 3.x
- `pynput`
- `customtkinter`
- `click`

### Dependencies Setup
Install the necessary Python packages with `pip`:

```bash
pip install customtkinter pynput click
```

---

## Usage Guide

### GUI Mode
Launch the application window by running the script without flags:

```bash
python auto_clicker.py
```

- Adjust the **Speed Slider** to select your desired CPS.
- Toggle the **Uncapped Speed** checkbox to ignore CPS limits.
- Press the **Start/Stop** button or press **F6** to control the clicker.

### CLI Mode
Run the tool directly inside your terminal using the `--cli` flag:

```bash
# Start CLI mode at default 10 CPS
python auto_clicker.py --cli

# Start CLI mode with a custom CPS rate
python auto_clicker.py --cli --cps 20

# Start CLI mode with uncapped speed
python auto_clicker.py --cli --uncapped
```

To exit CLI mode, press `Ctrl + C` in your terminal window.

---

## Safety Controls

- **Hotkeys:** Press **F6** anywhere to toggle clicking on or off.
- **System Stability:** Uncapped mode applies a micro-delay ($1\text{ ms}$) to keep the global keyboard listener responsive and prevent UI lockups.
