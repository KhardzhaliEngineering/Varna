import random
import math
import time

class WeatherStation:
    def __init__(self, location: str):
        self.location = location
        self.temperature = 20.0  # Celsius
        self.humidity = 50.0     # Percent
        self.pressure = 1013.25  # hPa
        self.wind_speed = 5.0    # m/s
        self.wind_direction = 0  # Degrees (North)
        self.history = []

    def simulate_step(self):
        # Simulate temperature change
        temp_variation = random.gauss(0, 0.5)
        humidity_variation = random.gauss(0, 1.0)
        pressure_variation = random.gauss(0, 0.2)
        wind_speed_variation = random.gauss(0, 0.3)
        wind_direction_variation = random.gauss(0, 5)

        self.temperature += temp_variation
        self.humidity = max(0, min(100, self.humidity + humidity_variation))
        self.pressure += pressure_variation
        self.wind_speed = max(0, self.wind_speed + wind_speed_variation)
        self.wind_direction = (self.wind_direction + wind_direction_variation) % 360

        self.history.append({
            'temp': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'wind_dir': self.wind_direction
        })

    def report(self):
        return (
            f"Location: {self.location}\n"
            f"Temperature: {self.temperature:.1f}°C\n"
            f"Humidity: {self.humidity:.0f}%\n"
            f"Pressure: {self.pressure:.2f} hPa\n"
            f"Wind: {self.wind_speed:.1f} m/s @ {self.wind_direction:.0f}°\n"
        )

def simulate_weather(station_name, steps, delay=0.5):
    station = WeatherStation(station_name)
    print(f"Weather simulation for {station.location}")
    print("=" * 40)
    for i in range(steps):
        station.simulate_step()
        print(f"Step {i+1}:")
        print(station.report())
        print("-" * 40)
        time.sleep(delay)
    print("Simulation Complete.")

if __name__ == "__main__":
    simulate_weather("London", 10, delay=0.1)
