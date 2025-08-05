import random
import math
import time
import csv
import matplotlib.pyplot as plt
from typing import List, Dict

class WeatherStation:
    def __init__(self, location: str):
        self.location = location
        self.temperature = 20.0  # Celsius
        self.humidity = 50.0     # Percent
        self.pressure = 1013.25  # hPa
        self.wind_speed = 5.0    # m/s
        self.wind_direction = 0  # Degrees (North)
        self.history: List[Dict] = []

    def simulate_step(self):
        # Extreme events
        event = None
        if random.random() < 0.05:
            event = random.choice(['storm', 'heatwave', 'cold_snap'])
            if event == 'storm':
                self.wind_speed += random.uniform(5, 15)
                self.pressure -= random.uniform(10, 20)
                self.humidity += random.uniform(10, 30)
            elif event == 'heatwave':
                self.temperature += random.uniform(3, 7)
                self.humidity -= random.uniform(5, 15)
            elif event == 'cold_snap':
                self.temperature -= random.uniform(3, 7)
                self.humidity += random.uniform(5, 15)

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
            'wind_dir': self.wind_direction,
            'event': event or ""
        })

    def report(self):
        last = self.history[-1] if self.history else {}
        event_str = f"Event: {last.get('event', '')}\n" if last.get('event', '') else ""
        return (
            f"Location: {self.location}\n"
            f"Temperature: {self.temperature:.1f}°C\n"
            f"Humidity: {self.humidity:.0f}%\n"
            f"Pressure: {self.pressure:.2f} hPa\n"
            f"Wind: {self.wind_speed:.1f} m/s @ {self.wind_direction:.0f}°\n"
            f"{event_str}"
        )

    def export_csv(self, filename="weather_history.csv"):
        keys = ['temp', 'humidity', 'pressure', 'wind_speed', 'wind_dir', 'event']
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.history)

    def plot_history(self):
        if not self.history:
            print("No data to plot.")
            return
        steps = range(1, len(self.history)+1)
        temps = [h['temp'] for h in self.history]
        hums = [h['humidity'] for h in self.history]
        press = [h['pressure'] for h in self.history]
        plt.figure(figsize=(12,6))
        plt.subplot(3,1,1)
        plt.plot(steps, temps, label='Temperature (°C)', color='red')
        plt.legend()
        plt.subplot(3,1,2)
        plt.plot(steps, hums, label='Humidity (%)', color='blue')
        plt.legend()
        plt.subplot(3,1,3)
        plt.plot(steps, press, label='Pressure (hPa)', color='green')
        plt.legend()
        plt.tight_layout()
        plt.savefig("weather_simulation_plot.png")
        plt.close()

    def forecast(self):
        # Linear regression (simple)
        def linreg(y):
            n = len(y)
            x = list(range(n))
            if n < 2:
                return y[-1] if y else 0
            x_mean = sum(x)/n
            y_mean = sum(y)/n
            num = sum((xi-x_mean)*(yi-y_mean) for xi,yi in zip(x,y))
            den = sum((xi-x_mean)**2 for xi in x)
            slope = num/den if den else 0
            intercept = y_mean - slope*x_mean
            return slope*n + intercept

        temps = [h['temp'] for h in self.history[-10:]]
        hums = [h['humidity'] for h in self.history[-10:]]
        forecast_temp = linreg(temps)
        forecast_hum = linreg(hums)
        return f"Forecast -- Next temp: {forecast_temp:.1f}°C, Next humidity: {forecast_hum:.0f}%"


def simulate_weather():
    print("Welcome to Varna's Smart Weather Simulator!")
    location = input("Enter location name: ")
    try:
        steps = int(input("How many steps? (e.g., 20): "))
    except:
        steps = 20
    try:
        delay = float(input("Delay between steps in seconds (e.g., 0.2): "))
    except:
        delay = 0.2
    station = WeatherStation(location)
    print(f"\nWeather simulation for {station.location}")
    print("=" * 40)
    for i in range(steps):
        station.simulate_step()
        print(f"Step {i+1}:")
        print(station.report())
        print(station.forecast())
        print("-" * 40)
        time.sleep(delay)
    print("Simulation Complete.\nExporting data and generating plot...")
    station.export_csv()
    station.plot_history()
    print("CSV saved as weather_history.csv and plot as weather_simulation_plot.png.")

if __name__ == "__main__":
    simulate_weather()