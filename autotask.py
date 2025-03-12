import time
import keyboard as kb
from pynput import mouse, keyboard
from pynput.mouse import Controller, Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Controller as KeyboardController, Key
import threading
import tkinter as tk

recorded_actions = []
is_recording = False
replaying = False
recording_listeners = []
current_action = ""

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
    current_action = "Recording started..."
    # Create listeners (non-blocking)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    recording_listeners = [mouse_listener, keyboard_listener]
    mouse_listener.start()
    keyboard_listener.start()

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
    current_action = "Recording stopped."

# Replaying function
def replay_actions():
    global replaying
    if replaying:
        print("Replay already in progress.")
        current_action = "Replay already in progress."
        return

    replaying = True
    print("Replaying actions...")
    current_action = "Replaying actions..."
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
    current_action = "Replay stopped."


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
root.title("Hotkey Controller GUI")

# Create labels to display hotkey instructions
header_label = tk.Label(root, text="Hotkey Controls", font=("Arial", 16, "bold"))
header_label.pack(pady=10)

label_f9 = tk.Label(root, text="F9: Start/Stop Recording", font=("Arial", 12))
label_f9.pack(pady=5)

label_f10 = tk.Label(root, text="F10: Replay/Stop Replay", font=("Arial", 12))
label_f10.pack(pady=5)

# Optional exit button to close the GUI
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()