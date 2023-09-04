# Module importieren, um mit CSV und JSON zu arbeiten
import csv
import json

# Definition einer Funktion, um eine strukturierte CSV-Datei aus einer JSON-Datei zu erstellen
def create_structured_csv(input_json_path, output_csv_path):
    # JSON-Datei öffnen und laden
    with open(input_json_path, 'r', encoding='utf-8-sig') as jsonfile:
        data_list = json.load(jsonfile)

    # Starten mit den Basis-Feldnamen für die CSV-Datei
    fieldnames = ["PDS", "ANZ_S"]

    # Durchlaufe alle JSON-Einträge, um die Feldnamen (Spalten) für die CSV zu sammeln
    # Durchlaufe alle 10 AUSPRAEGUNGEN
    for auspr_num in range(1, 11):
        # Durchlaufe die 5 verschiedenen RTS_Typen
        for rts_typ in [0, 1, 3, 4, 9]:
            col_name = f"RTS_{auspr_num}.{rts_typ}"
            fieldnames.append(col_name)

    # Öffne (oder erstelle) die CSV-Datei zum Schreiben
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_outfile:
        # CSV-Writer erstellen, wobei die gesammelten Feldnamen als Spaltenüberschriften verwendet werden
        writer = csv.DictWriter(csv_outfile, fieldnames=fieldnames, delimiter=';')
        # Schreibe die Spaltenüberschriften in die CSV-Datei
        writer.writeheader()

        # Durchlaufe jeden Eintrag in der JSON-Datei
          # Erste Schleife : verschiede PDS --> Reha Institute 
          # Zweite Schleife : verschiedene AUSPRAEGUNGEN -> Reha-Therapien 10 davon ! 
                # -> diese ist ein Objekt mit den Nummern 
          # Dritte Schleife die jeweiligen Daten zu den AUSPRAEGUNGEN 
        for pds_data in data_list:
            # Basiswerte für die aktuelle Zeile der CSV-Datei
            row = {"PDS": pds_data["PDS"], "ANZ_S": pds_data['ANZ_S']}

            counter = 1
            # Durchlaufe die 'AUSPRAEGUNG'-Daten
            for auspr_name, auspr_list in pds_data['AUSPRAEGUNG'].items():
                # Durchlaufe die Daten für die jeweilige AUSPRAEGUNG
                # Nur Zeilen berücksichtigen, bei denen 'RTS_TYP1' nicht leer ist und 'ANZ_UG' nicht gleich 'ANZ_S' ist
                for auspr_data in auspr_list:

                        rts = auspr_data["RTS_TYP1"]
                        # Erstelle den Spaltennamen
                        col_name = f"RTS_{counter}.{rts}"
                        #print(counter)
                        # Setze den 'ANZ_UG'-Wert für diese Spalte in der aktuellen Zeile
                        row[col_name] = auspr_data["ANZ_UG"]
                counter +=1

            # Schreibe die zusammengestellte Zeile in die CSV-Datei
            writer.writerow(row)

# Wenn dieses Skript direkt ausgeführt wird (anstatt importiert)
if __name__ == "__main__":
    # Pfade für die Eingabe-JSON- und Ausgabe-CSV-Datei festlegen
    input_json_path = "./datensatz_etm.json"
    output_csv_path = "./structured_datensatz.csv"
    # Die Hauptfunktion aufrufen
    create_structured_csv(input_json_path, output_csv_path)
