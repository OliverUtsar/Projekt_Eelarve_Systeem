import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Globaalsed muutujad sissetuleku ja kuu jaoks
sissetulek = 0
kuu_nimi = ""

# Andmete struktuur kulude salvestamiseks
kulutused = []
failinimi = "kulutused.txt"

# Esimene aken sissetuleku ja kuu valikuks
def ava_sissetuleku_aken():
    sissetuleku_aken = tk.Tk()
    sissetuleku_aken.title("Sisesta kuu sissetulek")

    tk.Label(sissetuleku_aken, text="Sisesta sissetulek (€):").grid(row=0, column=0)
    sissetulek_var = tk.StringVar()
    tk.Entry(sissetuleku_aken, textvariable=sissetulek_var).grid(row=0, column=1)

    tk.Label(sissetuleku_aken, text="Vali kuu:").grid(row=1, column=0)
    kuu_var = tk.StringVar()
    kuu_valikud = ["Jaanuar", "Veebruar", "Märts", "Aprill", "Mai", "Juuni", 
                   "Juuli", "August", "September", "Oktoober", "November", "Detsember"]
    kuu_dropdown = tk.OptionMenu(sissetuleku_aken, kuu_var, *kuu_valikud)
    kuu_dropdown.grid(row=1, column=1)

    def kinnita_sissetulek():
        global sissetulek, kuu_nimi
        try:
            sissetulek = float(sissetulek_var.get())
            kuu_nimi = kuu_var.get()
            if kuu_nimi == "":
                messagebox.showerror("Viga", "Palun vali kuu.")
            else:
                sissetuleku_aken.destroy()
                ava_kulude_aken()
        except ValueError:
            messagebox.showerror("Viga", "Palun sisesta kehtiv sissetulek.")
    def ava_eelistused():
        sissetuleku_aken.destroy()
        ava_eelistused_aken()

    tk.Button(sissetuleku_aken, text="Kinnita", command=kinnita_sissetulek).grid(row=0, column=2, columnspan=2, pady=10)
# TODO funktsionaalsus
    tk.Button(sissetuleku_aken, text="Mine edasi", command=kinnita_sissetulek).grid(row=1, column=2, columnspan=2, pady=10)
# TODO  funktsionaalsus
    tk.Button(sissetuleku_aken, text="Eelistused", command=ava_eelistused).grid(row=4, column=0, columnspan=2, pady=10)
    
    sissetuleku_aken.mainloop()
    
    
def ava_eelistused_aken():
    eelistus_protsent = ""
    eelistus_kategooria =""
# TODO nupu töö  ei saa protsenti??
    def kinnita_eelisus():
        try:
            eelistus_kategooria = kulutuste_var.get()
            eelistus_protsent = protsent_var.get()
            print(eelistus_protsent)
            
            print(eelistus_kategooria, eelistus_protsent)
        except ValueError:
            messagebox.showerror("Viga")            

        
# TODO nupu töö
    def tagasi():
        print(eelistus_kategooria, eelistus_protsent)

        
        
    eelistused_aken = tk.Tk()
    eelistused_aken.title(f"Eelistused - {kuu_nimi}")
    tk.Label(eelistused_aken, text=f"Määra {kuu_nimi} kulutuste jaotus").grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(eelistused_aken, text="Määra  kulutuste kategooria").grid(row=2, column=0, columnspan=2, pady=5)
    
    kulutuste_var = tk.StringVar()
    eelistuste_valikud = ["kat1", "kat2"]
    kuu_dropdown = tk.OptionMenu(eelistused_aken, kulutuste_var, *eelistuste_valikud)
    kuu_dropdown.grid(row=2, column=2)
    
    tk.Label(eelistused_aken, text="Määra protsent kogu kulust").grid(row=3,column=0, columnspan=1, pady=5)
    protsent_var = tk.StringVar()
    tk.Entry(eelistused_aken, textvariable=protsent_var).grid(row=3, column=1)
    
#     kinnita
    tk.Button(eelistused_aken, text="Kinnita", command=kinnita_eelisus).grid(row=4, column=0, columnspan = 1, pady=5)
    
# tagasi
    tk.Button(eelistused_aken, text="Tagasi", command=tagasi).grid(row=4, column=2, columnspan = 1, pady=5)

    eelistused_aken.mainloop()
    
    


    

# Põhiaken kulude haldamiseks
def ava_kulude_aken():
    app = tk.Tk()
    app.title(f"Eelarve Jälgimine - {kuu_nimi}")

    tk.Label(app, text=f"Kuu sissetulek: €{sissetulek:.2f}").grid(row=0, column=0, columnspan=2, pady=5)

    # Sisestusväljad ja nupud kulude lisamiseks
    summa_var = tk.StringVar()
    kategooria_var = tk.StringVar()

    tk.Label(app, text="Summa (€):").grid(row=1, column=0)
    tk.Entry(app, textvariable=summa_var).grid(row=1, column=1)

    tk.Label(app, text="Kategooria:").grid(row=2, column=0)
    tk.Entry(app, textvariable=kategooria_var).grid(row=2, column=1)

     # Funktsioon kulude lisamiseks
    def lisa_kulu():
        summa = summa_var.get()
        kategooria = kategooria_var.get()
        
        if summa and kategooria:
            try:
                summa = float(summa)
                kulu = {"kuupäev": datetime.now(), "summa": summa, "kategooria": kategooria}
                kulutused.append(kulu)
                
                # Salvesta uus kulu tekstifaili
                with open(failinimi, "a") as file:
                    file.write(f"{kulu['kuupäev']}, {kulu['summa']}, {kulu['kategooria']}\n")
                
                messagebox.showinfo("Lisatud", "Kulu on edukalt lisatud ja salvestatud faili!")
                summa_var.set("")
                kategooria_var.set("")
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

    # Funktsioon kulutuste graafiku näitamiseks
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
            plt.savefig("kulude_graafik.png")
            messagebox.showinfo("Graafik", "Graafik salvestati faili 'kulude_graafik.png'")
        else:
            messagebox.showinfo("Graafik", "Ei leitud kulutusi.")

    # Lihtne soovitus funktsioon
    def kuva_soovitus():
        kogukulu = sum(kulu["summa"] for kulu in kulutused)
        if kogukulu > sissetulek * 0.8:
            soovitus = "Teie kulud on üsna kõrged! Kaaluge vähendamist!"
        elif kogukulu > sissetulek * 0.5:
            soovitus = "Hästi hoitud, kuid jälgige oma kulutusi!"
        else:
            soovitus = "Suurepärane! Teie kulud on madalad."

        messagebox.showinfo("Soovitus", soovitus)

    # Nupud kulude lisamiseks ja vaatamiseks
    tk.Button(app, text="Lisa kulu", command=lisa_kulu).grid(row=4, column=0, pady=10)
    tk.Button(app, text="Vaata kulusid", command=vaata_kulusid).grid(row=4, column=1, pady=10)
    tk.Button(app, text="Kuva graafik", command=kuva_graafik).grid(row=5, column=0, pady=10)
    tk.Button(app, text="Kuva soovitus", command=kuva_soovitus).grid(row=5, column=1, pady=10)

    app.mainloop()

# Käivita sissetuleku aken
ava_sissetuleku_aken()

