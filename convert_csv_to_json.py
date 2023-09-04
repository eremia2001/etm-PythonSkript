# Module importieren, um mit CSV und JSON zu arbeiten
import csv
import json

# Definition einer Funktion, um eine CSV-Datei in eine JSON-Datei zu konvertieren
def convert_csv_to_json(input_csv_path, output_json_path):
    # Leere Liste erstellen, um die konvertierten Daten zu speichern
    data = []

    # CSV-Datei öffnen und lesen
    with open(input_csv_path, mode='r', encoding='utf-8-sig') as csvfile:
        # CSV-Reader erstellen und das Semikolon als Trennzeichen festlegen
        reader = csv.DictReader(csvfile, delimiter=';')

        # Zeilenweise durch die CSV-Datei gehen
        for row in reader:
            # Wichtige Spaltenwerte aus der aktuellen Zeile extrahieren
            pds = row['PDS']
            auspr = row['AUSPRAEGUNG']
            rts_typ1 = row['RTS_TYP1']
            anz_ug = row['ANZ_UG']
            anz_s = row['ANZ_S']

            # Wenn RTS_TYP1 leer ist und ANZ_UG gleich ANZ_S, überspringe die Zeile
            if not rts_typ1 and anz_ug == anz_s:
                continue

            # Prüfen, ob der aktuelle PDS-Wert bereits in der Liste 'data' existiert
            pds_entry = next((item for item in data if item['PDS'] == pds), None)

            # Wenn der PDS-Wert nicht gefunden wurde, erstelle ein neues PDS-Element
            if not pds_entry:
                pds_entry = {
                    "PDS": pds,
                    "ANZ_S": anz_s,
                    "AUSPRAEGUNG": {}
                }
                data.append(pds_entry)

            # Wenn die aktuelle 'AUSPRAEGUNG' nicht im PDS-Element existiert, füge sie hinzu
            if auspr not in pds_entry['AUSPRAEGUNG']:
                pds_entry['AUSPRAEGUNG'][auspr] = []

            # Erstelle ein neues Eintrag-Element mit den entsprechenden Werten
            entry = {
                "KRIT_NR": row['KRIT_NR'],
                "LL_UG_NR": row['LL_UG_NR'],
                "AUSPR2": row['AUSPR2'],
                "RTS_TYP1": rts_typ1,
                "ANZ_UG": anz_ug
            }
            # Füge das Eintrag-Element zum entsprechenden 'AUSPRAEGUNG'-Abschnitt hinzu
            pds_entry['AUSPRAEGUNG'][auspr].append(entry)

    # Speichere die konvertierten Daten in einer JSON-Datei
    with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

# Wenn dieses Skript direkt ausgeführt wird (anstatt importiert)
if __name__ == "__main__":
    # Pfade für die Eingabe-CSV- und Ausgabe-JSON-Datei festlegen
    input_csv_path = "./datensatz_etm.CSV"   # Hier den Pfad anpassen, falls benötigt
    output_json_path = "./datensatz_etm.json"    # Hier den Pfad anpassen, falls benötigt
    
    # Die Konvertierungsfunktion aufrufen
    convert_csv_to_json(input_csv_path, output_json_path)
