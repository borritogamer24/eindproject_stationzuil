import datetime
import random
import csv
import psycopg2

def moderate_messages(naam, bericht, station_naam):
    tijd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    scheldwoorden_lijst = ["kanker", "tyfus", "nazi", "mogool", "homo", "loser", "belg", "limburger"]
    status = 'j'  # Standaardwaarde 'j' (goedgekeurd)

    for woord in scheldwoorden_lijst:
        if woord in bericht:
            status = 'n'  # Status wordt 'n' (afgekeurd)
            break

    if status == 'j':
        # Voeg het goedgekeurde bericht toe aan de Gemodereerde_Berichten tabel
        insert_moderated_message(naam, bericht, station_naam, tijd)

    # Verwijder het oorspronkelijke bericht, ongeacht de status
    delete_original_message(naam, bericht, station_naam, tijd)

def insert_moderated_message(naam, bericht, station_naam, datum_tijd):
    db_config = {
        "database": "stationzuil",
        "user": "postgres",
        "password": "aap",
        "host": "172.187.187.51"
    }

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Gemodereerde_Berichten (bericht, datum_tijd, reiziger_naam, station) VALUES (%s, %s, %s, %s)",
        (bericht, datum_tijd, naam, station_naam)
    )

    conn.commit()
    conn.close()

def delete_original_message(naam, bericht, station_naam, datum_tijd):
    db_config = {
        "database": "stationzuil",
        "user": "postgres",
        "password": "aap",
        "host": "172.187.187.51"
    }

    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM Berichten WHERE bericht = %s AND datum_tijd = %s AND reiziger_naam = %s AND station = %s",
        (bericht, datum_tijd, naam, station_naam)
    )

    conn.commit()
    conn.close()

def main():
    with open('gegevens_module_1.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        for row in csv_reader:
            datum_tijd, naam, station, bericht = row
            moderate_messages(naam, bericht, station)

if __name__ == "__main__":
    main()
