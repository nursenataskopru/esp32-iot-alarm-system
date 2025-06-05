# Gerekli kütüphaneler
from machine import Pin  # Pinleri kontrol etmek için kullanılır
import time  # Zaman fonksiyonlarını kullanmak için

# PIR sensör tanımlama
pir = Pin(16, Pin.IN)

# Ultrasonik sensör pinleri tanımlama
trigger = Pin(17, Pin.OUT)
echo = Pin(18, Pin.IN)

# Buzzer tanımlama
buzzer = Pin(14, Pin.OUT)

# RGB LED'in kırmızı, yeşil ve mavi pinleri tanımlama
led_red = Pin(19, Pin.OUT)
led_green = Pin(20, Pin.OUT)
led_blue = Pin(21, Pin.OUT)

def measure_distance():
    """Ultrasonik sensör ile mesafe ölçen fonksiyon"""
    trigger.low()  # Önce trigger sıfırlanır
    time.sleep_us(2)  # 2 mikrosaniye beklenir
    trigger.high()  # Trigger sinyali gönderilir
    time.sleep_us(10)  # 10 mikrosaniye boyunca
    trigger.low()  # Trigger kapatılır

    # Echo pininde cevap beklenir (sinyal gidip gelme süresi ölçülür)
    while echo.value() == 0:
        start = time.ticks_us()
    while echo.value() == 1:
        end = time.ticks_us()

    # Süre hesaplanır ve mesafeye çevrilir
    duration = time.ticks_diff(end, start)
    distance = (duration / 2) / 29.1  # Sesin havadaki hızına göre
    return distance

def led_color(r, g, b):
    """RGB LED'in rengini ayarlayan fonksiyon"""
    led_red.value(r)
    led_green.value(g)
    led_blue.value(b)

# Ana döngü
while True:
    if pir.value() == 1:  # Hareket algılandıysa
        distance = measure_distance()  # Mesafe ölç
        print("Mesafe:", distance)
        if 0 < distance < 100:  # Eğer mesafe 0-100 cm arasındaysa
            buzzer.value(1)  # Buzzer çalsın (alarm)
            led_color(1, 0, 0)  # RGB LED kırmızı yansın (tehlike)
        else:
            buzzer.value(0)  # Buzzer sessiz
            led_color(0, 1, 0)  # RGB LED yeşil yansın (güvenli)
    else:
        buzzer.value(0)  # Buzzer sessiz
        led_color(0, 0, 1)  # RGB LED mavi yansın (bekleme)

    time.sleep(0.5)  # Döngüyü biraz yavaşlatmak için 0.5 saniye bekle