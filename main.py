# import json
# import socket
# import subprocess
# from pynput.mouse import Controller as MouseController , Button
# from pynput.keyboard import Controller as KeyboardController , Key

# print("Serving on http://" + socket.gethostbyname(socket.gethostname()) + ":3000")

# mouse = MouseController()
# keyboard = KeyboardController()

# def handle_mouse(data):
#     step_factor = float(0.3)
#     x = int(int(data[0])*step_factor)
#     y = int(int(data[1])*step_factor)

#     mouse.move(x, -y)

# def handle_keystoke(data):
#     keyboard.tap(data)

# # Start the subprocess
# process = subprocess.Popen(
#     ["bun", "run", r"C:\Users\acer\Documents\Codes\gameCon\webcon\index.ts"],  # Change this to your command
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     text=True,  # Ensures output is treated as text (not bytes)
#     bufsize=1,  # Line buffering
#     universal_newlines=True  # Ensures line-by-line streaming
# )

# try:
#     for line in process.stdout:
#         try:
#             data = json.loads(line)
#             match data["type"]:
#                 case "mouse":
#                     handle_mouse(data["msg"])
#                 case "keystroke":
#                     handle_keystoke(data["msg"])
#         except json.JSONDecodeError:
#             print(line)  # Print immediately without extra newlines

# except KeyboardInterrupt:
#     process.terminate()
#     print("\nProcess terminated.")

# finally:
#     process.stdout.close()
#     process.stderr.close()
#     process.wait()  # Ensure process exits cleanly

import sys
import json
import pynput
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button

# Initialize keyboard and mouse controllers
keyboard = KeyboardController()
mouse = MouseController()

def press_key(key):
    """Press a keyboard key"""
    try:
        if len(key) == 1:  # Regular character
            keyboard.press(key)
        else:  # Special keys (like "ctrl", "shift", "enter")
            keyboard.press(getattr(Key, key))
    except AttributeError:
        print(f"Invalid key: {key}")

def release_key(key):
    """Release a keyboard key"""
    try:
        if len(key) == 1:
            keyboard.release(key)
        else:
            keyboard.release(getattr(Key, key))
    except AttributeError:
        print(f"Invalid key: {key}")

def type_text(text):
    """Type out a string"""
    keyboard.type(text)

def move_mouse(x, y):
    """Move mouse to (x, y)"""
    mouse.position = (x, y)

def click_mouse(button="left"):
    """Click the mouse button (left or right)"""
    btn = Button.left if button == "left" else Button.right
    mouse.click(btn)

def scroll_mouse(dx, dy):
    """Scroll mouse (dx, dy)"""
    mouse.scroll(dx, dy)

def process_command(command):
    """Process JSON command"""
    try:
        data = json.loads(command)
        msg_type = data.get("msg_type")

        match msg_type:
            case "key_press":
                press_key(data["key"])
            case "key_release":
                release_key(data["key"])
            case "type_text":
                type_text(data["text"])
            case "mouse_move":
                move_mouse(data["x"], data["y"])
            case "mouse_click":
                click_mouse(data.get("button", "left"))
            case "mouse_scroll":
                scroll_mouse(data["dx"], data["dy"])
            case "exit":
                print("Exiting...")
                sys.exit(0)    

        # if msg_type == "key_press":
        #     press_key(data["key"])
        # elif msg_type == "key_release":
        #     release_key(data["key"])
        # elif msg_type == "type_text":
        #     type_text(data["text"])
        # elif msg_type == "mouse_move":
        #     move_mouse(data["x"], data["y"])
        # elif msg_type == "mouse_click":
        #     click_mouse(data.get("button", "left"))
        # elif msg_type == "mouse_scroll":
        #     scroll_mouse(data["dx"], data["dy"])
        # elif msg_type == "exit":
        #     print("Exiting...")
        #     sys.exit(0)
        # else:
        #     print(f"Unknown msg_type: {msg_type}")
    except Exception as e:
        print(f"Error processing command: {e}")

def main():
    """Main loop to read JSON commands from stdin"""
    print("Listening for commands...")
    while True:
        try:
            command = sys.stdin.readline().strip()
            if not command:
                continue
            process_command(command)
        except KeyboardInterrupt:
            print("Process interrupted by user")
            break

if __name__ == "__main__":
    main()
