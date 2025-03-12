# AutoTask - Hotkey-Controlled Action Recorder

**Record and Replay Mouse and Keyboard Actions**

AutoTask is a simple Python application that allows you to record your mouse and keyboard actions and replay them later using hotkeys. It's useful for automating repetitive tasks on your computer.

## Features

- **Record Mouse and Keyboard Actions:** Captures mouse movements, clicks (left and right), scrolls, and keyboard presses/releases.
- **Hotkey Control:**
  - **F9:** Start and Stop Recording.
  - **F10:** Replay and Stop Replay.
- **Save Recordings:** Save recorded actions to `.rec` files for later use.
  - Prompts you to choose the save location and filename.
- **Load Recordings:** Load saved `.rec` files to replay previously recorded actions.
- **GUI Interface:** Simple Tkinter-based graphical user interface for status updates and control buttons.
- **Status Indicator:** Displays the current status (Idle, Recording, Replaying) in the GUI.
- **Save Button:** A button in the GUI to manually trigger the saving of the current recording.
- **Load Button:** A button in the GUI to load a previously saved recording file.

## How to Use

1.  **Requirements:**

    - Python 3.x
    - Required Python Libraries (install using `pip`):
      ```bash
      pip install pynput keyboard tkinter
      ```
      - `pynput`: For controlling and monitoring input devices (mouse and keyboard).
      - `keyboard`: For registering and detecting global hotkeys.
      - `tkinter`: For the graphical user interface.

2.  **Running the Application:**

    - Save the Python code as a `.py` file (e.g., `autotask.py`).
    - Open a terminal or command prompt.
    - Navigate to the directory where you saved the file.
    - Run the script using: `python autotask.py`

3.  **Using the Hotkeys:**

    - **Start/Stop Recording:** Press the **F9** key.
      - The status in the GUI will change to "Recording started..." when recording begins.
      - Press **F9** again to stop recording. The status will change to "Recording stopped."
    - **Replay/Stop Replay:** Press the **F10** key.
      - The status in the GUI will change to "Replaying actions..." when replay begins.
      - Press **F10** again to stop replaying. The status will change to "Replay stopped."

4.  **Saving Recordings:**

    - After stopping a recording (by pressing F9), click the **"Save Recording"** button in the GUI.
    - A "Save As" dialog will appear.
    - Choose a location on your computer to save the recording.
    - Enter a filename for the recording (e.g., `my_macro.rec`). The `.rec` extension is recommended.
    - Click "Save".
    - The GUI status will update to indicate where the recording was saved.

5.  **Loading Recordings:**

    - Click the **"Load Recording"** button in the GUI.
    - A file selection dialog will appear.
    - Navigate to the folder where you saved your `.rec` files.
    - Select the `.rec` file you want to load.
    - Click "Open".
    - The GUI status will update to indicate from where the recording was loaded.
    - Press **F10** to replay the loaded actions.

6.  **Exiting the Application:**
    - Click the **"Exit"** button in the GUI window to close the application.

## Notes

- **Accuracy of Replay:** The accuracy of replay depends on various factors like system load and application behavior. Minor deviations might occur, especially for mouse movements.
<!-- - **Special Keys:** Special keys like `F1-F12`, `Shift`, `Ctrl`, `Alt`, `Tab`, etc., are generally recorded and replayed correctly. -->
- **Error Handling:** Basic error handling is included for saving and loading files. Check the terminal/command prompt output and GUI status for any error messages.

---

**Enjoy automating your tasks with AutoTask!**
