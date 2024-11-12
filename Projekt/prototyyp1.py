import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Andmete struktuur kulude salvestamiseks
kulutused = []

# Funktsioon kulude lisamiseks
def lisa_kulu():
    summa = summa_var.get()
    kategooria = kategooria_var.get()
    kirjeldus = kirjeldus_var.get()
    
    if summa and kategooria:
        try:
            summa = float(summa)
            kulutused.append({"kuupäev": datetime.now(), "summa": summa, "kategooria": kategooria, "kirjeldus": kirjeldus})
            messagebox.showinfo("Lisatud", "Kulu on edukalt lisatud!")
            summa_var.set("")
            kategooria_var.set("")
            kirjeldus_var.set("")
        except ValueError:
            messagebox.showerror("Viga", "Sisesta kehtiv summa!")
    else:
        messagebox.showerror("Viga", "Summa ja kategooria on kohustuslikud väljad!")

# Funktsioon kulutuste vaatamiseks
def vaata_kulusid():
    kategooriad = defaultdict(float)
    for kulu in kulutused:
        kategooriad[kulu["kategooria"]] += kulu["summa"]

    if kategooriad:
        kategooriad_list = "\n".join([f"{kat}: €{summa:.2f}" for kat, summa in kategooriad.items()])
        messagebox.showinfo("Kulude kokkuvõte", kategooriad_list)
    else:
        messagebox.showinfo("Kulude kokkuvõte", "Ei leitud kulutusi.")

def kuva_graafik():
    kategooriad = defaultdict(float)
    for kulu in kulutused:
        kategooriad[kulu["kategooria"]] += kulu["summa"]

    if kategooriad:
        kategooriad_nimed = list(kategooriad.keys())
        kategooriad_summa = list(kategooriad.values())

        plt.figure(figsize=(8, 5))
        plt.pie(kategooriad_summa, labels=kategooriad_nimed, autopct='%1.1f%%', startangle=140)
        plt.title("Kulude jaotus kategooriate lõikes")
        
        # Salvesta graafik pildifailina
        plt.savefig("kulude_graafik.png")
        messagebox.showinfo("Graafik", "Graafik salvestati faili 'kulude_graafik.png'")
    else:
        messagebox.showinfo("Graafik", "Ei leitud kulutusi.")

# Lihtne soovitus funktsioon
def kuva_soovitus():
    kogukulu = sum(kulu["summa"] for kulu in kulutused)
    if kogukulu > 500:
        soovitus = "Teie kulud on üsna kõrged! Kaaluge vähendamist!"
    elif kogukulu > 200:
        soovitus = "Hästi hoitud, kuid jälgige oma kulutusi!"
    else:
        soovitus = "Suurepärane! Teie kulud on madalad."

    messagebox.showinfo("Soovitus", soovitus)

# Rakenduse kasutajaliides Tkinteriga
app = tk.Tk()
app.title("Eelarve Jälgimise Rakendus")

# Sisestusväljad ja nupud
summa_var = tk.StringVar()
kategooria_var = tk.StringVar()
kirjeldus_var = tk.StringVar()

tk.Label(app, text="Summa (€):").grid(row=0, column=0)
tk.Entry(app, textvariable=summa_var).grid(row=0, column=1)

tk.Label(app, text="Kategooria:").grid(row=1, column=0)
tk.Entry(app, textvariable=kategooria_var).grid(row=1, column=1)

tk.Label(app, text="Kirjeldus:").grid(row=2, column=0)
tk.Entry(app, textvariable=kirjeldus_var).grid(row=2, column=1)

tk.Button(app, text="Lisa kulu", command=lisa_kulu).grid(row=3, column=0, pady=10)
tk.Button(app, text="Vaata kulusid", command=vaata_kulusid).grid(row=3, column=1, pady=10)
tk.Button(app, text="Kuva graafik", command=kuva_graafik).grid(row=4, column=0, pady=10)
tk.Button(app, text="Kuva soovitus", command=kuva_soovitus).grid(row=4, column=1, pady=10)

app.mainloop()

