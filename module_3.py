import tkinter as tk
import psycopg2
import requests
from PIL import Image, ImageTk

def create_station_screen(station_name):
    root = tk.Tk()
    root.title(f"Stationshal {station_name}")

    root.configure(bg='yellow')

    ns_logo = Image.open("ns_logo.png")
    ns_logo = ImageTk.PhotoImage(ns_logo)
    logo_label = tk.Label(root, image=ns_logo, bg='yellow')
    logo_label.photo = ns_logo
    logo_label.pack()

    weather_label = tk.Label(root, text=get_station_weather(station_name), bg='yellow')
    weather_label.pack()

    # Voeg faciliteiten toe
    facilities_label = tk.Label(root, text=get_facilities(station_name), bg='yellow')
    facilities_label.pack()

    # Voeg berichten toe
    messages_label = tk.Label(root, text=get_latest_messages(station_name), bg='yellow')
    messages_label.pack()

    root.mainloop()

def get_station_weather(station_name):
    api_key = "9347f62ba95dae7199fc792dec1a3226"
    coördinaten = {
        "Amsterdam Centraal": {"lat": 52.379189, "lon": 4.899431},
        "Utrecht Centraal": {"lat": 52.088166, "lon": 5.110702},
        "Rotterdam Centraal": {"lat": 51.9225, "lon": 4.481111},
        "Den Haag Centraal": {"lat": 52.078663, "lon": 4.323825},
        "Eindhoven Centraal": {"lat": 51.443231, "lon": 5.469722}
    }

    if station_name in coördinaten:
        lat = coördinaten[station_name]["lat"]
        lon = coördinaten[station_name]["lon"]
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            weer_beschrijving = data["weather"][0]["description"]
            temperatuur = data["main"]["temp"]
            return f"Weer in {station_name}: {weer_beschrijving}, Temperatuur: {temperatuur}°C"
        else:
            return f"Weergegevens voor {station_name} niet beschikbaar."
    else:
        return "Station niet gevonden."

def get_facilities(station_name):
    db_config = {
        "database": "stationzuil",
        "user": "postgres",
        "password": "aap",
        "host": "172.187.187.51"
    }

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT facilities FROM stations WHERE station_name = %s", (station_name,))
    facilities = cursor.fetchone()

    conn.close()

    if facilities:
        return facilities[0]
    else:
        return "Faciliteiten niet beschikbaar"

def get_latest_messages(station_name):
    db_config = {
        "database": "stationzuil",
        "user": "postgres",
        "password": "aap",
        "host": "172.187.187.51"
    }

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT bericht, datum_tijd, reiziger_naam FROM Gemodereerde_Berichten WHERE station = %s ORDER BY datum_tijd DESC LIMIT 5", (station_name,))
    messages = cursor.fetchall()

    conn.close()

    if messages:
        message_str = "\n".join([f"{row[2]} ({row[1]}): {row[0]}" for row in messages])
        return message_str
    else:
        return "Geen recente berichten beschikbaar."

if __name__ == "__main__":
    station_choice = input("Kies een station (Amsterdam Centraal, Utrecht Centraal, Rotterdam Centraal, Den Haag Centraal, Eindhoven Centraal): ")
    create_station_screen(station_choice)
