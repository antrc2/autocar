import keyboard

def on_key_event(event):
    print(f"Bạn vừa nhấn phím: {event.name}")

keyboard.on_press(on_key_event)

print("Nhấn phím bất kỳ để kiểm tra. Nhấn ESC để thoát.")

keyboard.wait('esc')
