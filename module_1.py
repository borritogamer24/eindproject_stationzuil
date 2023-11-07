import datetime
import random
import csv

tijd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def module_1():

    with open('qHAWzQ8V.htm', 'r') as station_file:
        stations = station_file.readlines()
        random_station = random.choice(stations).strip()


    naam = input("Voer uw naam in (laat leeg voor anoniem): ")

    if len(naam) == 0:
        naam = "Anoniem"
        print("hallo anoniem")
        print(tijd)
    else:
        print("hallo " + naam)
        print(tijd)
    bericht = input("Voer uw bericht in (maximaal 140 tekens): ")

    if len(bericht) <= 140:
        print(bericht)
        print(tijd)
    else:
        print("Foutmelding: Uw bericht is te lang (maximaal 140 tekens).")
        print(tijd)
        return



    with open('gegevens_module_1.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([naam, tijd, random_station, bericht])

    print(f"Uw bericht is opgeslagen in gegegevens_module_1.csv.")
module_1()