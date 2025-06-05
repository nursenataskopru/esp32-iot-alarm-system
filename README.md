# IoT-Based Security and Distance Monitoring System

This project creates a real-time alarm system using an ESP32 microcontroller with a PIR motion sensor and an ultrasonic distance sensor. When motion is detected, it measures the distance; if the distance falls below a set threshold, it activates a buzzer alarm and uses an RGB LED to indicate the status.

---

## Project Overview

This ESP32-based IoT system first detects motion via the PIR sensor. When motion is sensed, it uses the ultrasonic sensor to measure the distance. If the measured distance is between 0 and 100 cm:
- The buzzer is activated (alarm).
- The RGB LED turns red (DANGER).

If the distance is equal to or above 100 cm:
- The buzzer remains off (no alarm).
- The RGB LED turns green (SAFE).

When no motion is detected, the system goes into standby mode and the RGB LED glows blue (IDLE/STANDBY).

---

## Hardware Components

- **ESP32 Development Board**  
- **PIR Motion Sensor (HC-SR501 or equivalent)**  
- **Ultrasonic Distance Sensor (HC-SR04 or equivalent)**  
- **Buzzer**  
- **RGB LED (Common Cathode)**  
- **3 × 220 Ω Resistors** (current limiting for RGB LED)  
- **Breadboard & Jumper Wires**

---

## Circuit Diagram & Simulation

- The `diagram.json` file contains the Wokwi circuit simulation layout.  
- To view and run the simulation:  
  1. Open your browser and go to the Wokwi project link:  
     `https://wokwi.com/projects/429416013126438913`  
  2. Click “Open in Editor” in the top-right corner to view the circuit.  
  3. Start the simulation. All pin assignments and connections are defined in `diagram.json`.

---

## Software Setup

1. **Flashing MicroPython to the ESP32**  
   - If MicroPython is not already installed on your ESP32, download the ESP32 firmware from [micropython.org](https://micropython.org/download/esp32/) and follow the instructions to flash it.

2. **Uploading `main.py`**  
   - Use one of the following methods to transfer `main.py` to the ESP32:  
     - **Thonny IDE**: Connect to the ESP32, then use “File → Save as…” and choose “MicroPython device” to save `main.py` directly.  
     - **ampy / rshell / filesystem tools**: Use a command like `ampy put main.py` from your terminal to send the file.  

3. **Reboot the ESP32**  
   - After uploading, reset the board. MicroPython will automatically run `main.py` on startup—no further action is needed.

---

## main.py Explanation

```python
# Required libraries
from machine import Pin         # For controlling GPIO pins
import time                     # For timing and delays

# PIR sensor setup (reads from GPIO16)
pir = Pin(16, Pin.IN)

# Ultrasonic sensor pins
trigger = Pin(17, Pin.OUT)
echo = Pin(18, Pin.IN)

# Buzzer setup (controlled via GPIO14)
buzzer = Pin(14, Pin.OUT)

# RGB LED pins (GPIO19 = Red, GPIO20 = Green, GPIO21 = Blue)
led_red = Pin(19, Pin.OUT)
led_green = Pin(20, Pin.OUT)
led_blue = Pin(21, Pin.OUT)

def measure_distance():
    # Sends a 10 µs pulse to the ultrasonic trigger pin,
    # measures the echo pulse width, and converts it to centimeters.
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()

    while echo.value() == 0:
        start = time.ticks_us()
    while echo.value() == 1:
        end = time.ticks_us()

    duration = time.ticks_diff(end, start)
    distance = (duration / 2) / 29.1  # Convert to cm
    return distance

def set_led_color(r, g, b):
    # Sets the RGB LED color. Each parameter r/g/b is 0 or 1.
    led_red.value(r)
    led_green.value(g)
    led_blue.value(b)

# Main loop
while True:
    if pir.value() == 1:                    # If motion is detected
        distance = measure_distance()       # Measure distance
        print("Distance:", distance, "cm")  # Print to serial console

        if 0 < distance < 100:              # If distance is between 0 and 100 cm
            buzzer.value(1)                 # Turn buzzer ON (alarm)
            set_led_color(1, 0, 0)          # Red LED (DANGER)
        else:
            buzzer.value(0)                 # Turn buzzer OFF
            set_led_color(0, 1, 0)          # Green LED (SAFE)
    else:
        buzzer.value(0)                     # No motion: buzzer OFF
        set_led_color(0, 0, 1)              # Blue LED (IDLE/STANDBY)

    time.sleep(0.5)                         # Pause half a second before next loop
```

- **PIR Sensor** (`pir.value()`): Returns 1 if motion is present, 0 otherwise.  
- **Ultrasonic Sensor** (`measure_distance()`): Calculates distance in centimeters.  
- **Buzzer**: Activated (set to 1) when an object is within 0–100 cm.  
- **RGB LED** (`set_led_color(r, g, b)`):  
  - `(1, 0, 0)` → Red = DANGER  
  - `(0, 1, 0)` → Green = SAFE  
  - `(0, 0, 1)` → Blue = IDLE/STANDBY  

---

## Usage

1. Connect the ESP32 to your computer via USB.  
2. Verify that `main.py` is uploaded correctly and that MicroPython is running.  
3. Open a serial monitor (Thonny, PuTTY, or minicom) to view the printed distance values.  
4. When no motion is detected, the RGB LED will shine **blue** (IDLE).  
5. Upon detecting motion:  
   - The ultrasonic sensor measures distance.  
   - If the measured distance is between 0 and 100 cm:  
     - The buzzer sounds (HIGH).  
     - The RGB LED turns **red** (DANGER).  
   - If the measured distance is ≥ 100 cm:  
     - The buzzer remains off.  
     - The RGB LED turns **green** (SAFE).

---

## File List

- **`main.py`**  
  - MicroPython code for running the ESP32 IoT alarm system.  

- **`diagram.json`**  
  - Wokwi circuit layout for simulating and visualizing the hardware connections.  

- **`wokwi-project.txt`**  
  - Contains the Wokwi simulation URL:  
    ```
    Simulate this project at: https://wokwi.com/projects/429416013126438913
    ```

- **`README.md`**  
  - This file, describing how to set up, run, and understand the project.
