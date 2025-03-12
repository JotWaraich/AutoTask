import time
import keyboard as kb
from pynput import mouse, keyboard
from pynput.mouse import Controller, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Controller as KeyboardController, Key
import threading
import tkinter as tk
import pickle  # Import pickle for saving
from tkinter import filedialog # Import filedialog for save dialog

recorded_actions = []
is_recording = False
replaying = False
recording_listeners = []

mouse_controller = Controller()
keyboard_controller = KeyboardController()

# Keyboard listener
def on_press(key):
    try:
        recorded_actions.append(('keyboard', 'press', key.char, time.time()))
    except AttributeError:
        recorded_actions.append(('keyboard', 'press', str(key), time.time()))

def on_release(key):
    try:
        recorded_actions.append(('keyboard', 'release', key.char, time.time()))
    except AttributeError:
        recorded_actions.append(('keyboard', 'release', str(key), time.time()))

# Mouse listener
def on_move(x, y):
    recorded_actions.append(('mouse', 'move', x, y, time.time()))

def on_click(x, y, button, pressed):
    action_type = 'press' if pressed else 'release'
    recorded_actions.append(('mouse', action_type, button.name, x, y, time.time()))

def on_scroll(x, y, dx, dy):
    recorded_actions.append(('mouse', 'scroll', dx, dy, x, y, time.time()))

# Recording control function
def start_recording():
    global is_recording, recording_listeners
    if is_recording:
        # If already recording, do nothing.
        return
    recorded_actions.clear()  # Clear previous actions
    is_recording = True
    print("Recording started...")
    update_status("Recording started...")
    # Create listeners (non-blocking)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    recording_listeners = [mouse_listener, keyboard_listener]
    mouse_listener.start()
    keyboard_listener.start()

def save_recording():
    global recorded_actions
    if not recorded_actions:
        print("No actions recorded to save.")
        update_status("No actions recorded to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".rec",  # default extension for recording files
        filetypes=[("Recording files", "*.rec"), ("All files", "*.*")],
        title="Save Recording As"
    )

    if file_path:
        try:
            with open(file_path, 'wb') as file: # binary write mode for pickle
                pickle.dump(recorded_actions, file)
            print(f"Recording saved to: {file_path}")
            update_status(f"Recording saved to: {file_path}")
        except Exception as e:
            print(f"Error saving recording: {e}")
            update_status(f"Error saving recording: {e}")

def load_recording():
    global recorded_actions
    file_path = filedialog.askopenfilename(
        defaultextension=".rec",
        filetypes=[("Recording files", "*.rec"), ("All files", "*.*")],
        title="Load Recording"
    )
    if file_path:
        try:
            with open(file_path, 'rb') as file: # binary read mode for pickle
                loaded_actions = pickle.load(file)
                recorded_actions = loaded_actions # Update current actions with loaded actions
            print(f"Recording loaded from: {file_path}")
            update_status(f"Recording loaded from: {file_path}")
        except Exception as e:
            print(f"Error loading recording: {e}")
            update_status(f"Error loading recording: {e}")

def stop_recording():
    global is_recording, recording_listeners
    if not is_recording:
        return
    is_recording = False
    # Stop all listeners
    for listener in recording_listeners:
        listener.stop()
    recording_listeners = []
    print("Recording stopped.")
    update_status("Recording stopped.")
    # save_recording() # REMOVED save_recording() call from here


# Replaying function
def replay_actions():
    global replaying
    if replaying:
        print("Replay already in progress.")
        update_status("Replay already in progress.")
        return

    replaying = True
    print("Replaying actions...")
    update_status("Replaying actions...")
    last_time = time.time()

    for action in recorded_actions:
        if not replaying:  # If replay is stopped during replay
            break
        action_type = action[0]
        if action_type == 'keyboard':
            event_type, key, timestamp = action[1], action[2], action[3]
            time_diff = timestamp - last_time
            if time_diff > 0:
                time.sleep(time_diff)  # Only sleep if time difference is positive

            # Handle special keys properly
            if key.startswith('Key.'):  # If it's a special key (e.g., F9, F10)
                key = getattr(Key, key[4:])  # Convert to pynput's Key enumeration (e.g., Key.f9)

            if event_type == 'press':
                keyboard_controller.press(key)
            else:
                keyboard_controller.release(key)

        elif action_type == 'mouse':
            if action[1] == 'move':
                _, _, x, y, timestamp = action
                time_diff = timestamp - last_time
                if time_diff > 0:
                    time.sleep(time_diff)  # Only sleep if time difference is positive
                mouse_controller.position = (x, y)
            elif action[1] == 'press' or action[1] == 'release':
                _, _, button, x, y, timestamp = action
                time_diff = timestamp - last_time
                if time_diff > 0:
                    time.sleep(time_diff)  # Only sleep if time difference is positive
                mouse_button = mouse.Button.left if button == 'left' else mouse.Button.right
                if action[1] == 'press':
                    mouse_controller.press(mouse_button)
                else:
                    mouse_controller.release(mouse_button)
            elif action[1] == 'scroll':
                _, _, dx, dy, x, y, timestamp = action
                time_diff = timestamp - last_time
                if time_diff > 0:
                    time.sleep(time_diff)  # Only sleep if time difference is positive
                mouse_controller.scroll(dx, dy)
        last_time = timestamp
    replaying = False  # Mark replay as finished

# Stop replaying when F10 is pressed
def stop_replay():
    global replaying
    replaying = False
    print("Replay stopped.")
    update_status("Replay stopped.")


def hotkey_listener():
    # Register hotkeys using the keyboard module (aliased as kb)
    kb.add_hotkey('F9', lambda: stop_recording() if is_recording else threading.Thread(target=start_recording).start())
    kb.add_hotkey('F10', lambda: stop_replay() if replaying else threading.Thread(target=replay_actions).start())
    kb.wait()  # Block this thread and keep listening for hotkeys

# Start the hotkey listener in a background thread
listener_thread = threading.Thread(target=hotkey_listener, daemon=True)
listener_thread.start()

# Setup the Tkinter GUI
root = tk.Tk()
root.title("AtuoTask")
root.minsize(250, 230)

status_var = tk.StringVar()
status_var.set("Idle")

def update_status(text):
    status_var.set(text)
    status_label.update()

# Create labels to display hotkey instructions
header_label = tk.Label(root, text="Hotkey Controls", font=("Arial", 16, "bold"))
header_label.pack(pady=10)

label_f9 = tk.Label(root, text="F9: Start/Stop Recording", font=("Arial", 12))
label_f9.pack(pady=5)

label_f10 = tk.Label(root, text="F10: Replay/Stop Replay", font=("Arial", 12))
label_f10.pack(pady=5)

status_label = tk.Label(root, textvariable=status_var)
status_label.pack(pady=10)

# Save Button
save_button = tk.Button(root, text="Save Recording", command=save_recording) # Button to call save_recording
save_button.pack(pady=10)

# Load Button
load_button = tk.Button(root, text="Load Recording", command=load_recording) # Button to call load_recording
load_button.pack(pady=10)

# Optional exit button to close the GUI
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()