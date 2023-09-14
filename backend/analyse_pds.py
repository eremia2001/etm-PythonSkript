import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV-Datei laden
df = pd.read_csv('structured_datensatz.csv', delimiter=';')

def overall_rts_counts(df):
    rts_counts = {"0": 0, "1": 0, "3": 0, "4": 0 , "9": 0}

    # Summe für jeden RTS-Typ berechnen
    for i in range(1, 11):  # Für jede AUSPRAEGUNG
        for j in ["0", "1", "3","4", "9"]:  # Für jeden RTS_Typ
            col_name = f"RTS_{i}.{j}"
            if col_name in df.columns:
                rts_counts[j] += df[col_name].sum()
    print(rts_counts)
    return rts_counts

def plot_rts_counts(rts_counts):
    labels = ["Keine Leistung erhalten", "unter 2/3 erfüllt", "mind 2/3 erfüllt", "voll erfüllt" ,"trifft nicht zu"]
    counts = list(rts_counts.values())
    
    # Balkendiagramm erstellen
    plt.figure(figsize=(10, 6))
    sns.barplot(x=labels, y=counts, palette="viridis")
    plt.xlabel("RTS Typ")
    plt.ylabel("Anzahl")
    plt.title("Gesamtzahl für jeden RTS-Typ über alle PDS")
    plt.tight_layout()
    plt.show()

rts_counts = overall_rts_counts(df)
plot_rts_counts(rts_counts)
