from machine import Pin, PWM
import time

red_pin = Pin(15, Pin.OUT)
green_pin = Pin(14, Pin.OUT)
blue_pin = Pin(13, Pin.OUT)

red_pwm = PWM(red_pin)
green_pwm = PWM(green_pin)
blue_pwm = PWM(blue_pin)

def set_color(red, green, blue):
    red_pwm.duty_u16(int(red * 65535 / 255))
    green_pwm.duty_u16(int(green * 65535 / 255))
    blue_pwm.duty_u16(int(blue * 65535 / 255))

moods = {
    "calm": (0, 0, 255),
    "happy": (255, 255, 0),
    "energetic": (255, 0, 0),
    "custom": None
}

def main():
    print("Choose a mood: calm, happy, energetic, or custom")
    mood = input("Enter your mood: ").strip().lower()

    if mood in moods and mood != "custom":
        color = moods[mood]
        set_color(*color)
        print(f"Mood set to {mood} with color {color}")
    elif mood == "custom":
        red = int(input("Enter red value (0-255): "))
        green = int(input("Enter green value (0-255): "))
        blue = int(input("Enter blue value (0-255): "))
        set_color(red, green, blue)
        print(f"Custom color set to ({red}, {green}, {blue})")
    else:
        print("Invalid mood selected.")

    time.sleep(10)

if __name__ == "__main__":
    main()
