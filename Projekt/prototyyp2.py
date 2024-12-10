import tkinter as tk
import csv
from tkinter import *
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Globaalsed muutujad sissetuleku, kuu ja kategooriate jaoks
sissetulek = 0
kuu_nimi = ""
kategooriad = ["Majapidamine", "Kommunaalid/Üür", "Toit","Kütus","Hobid","Muu"]



# Andmete struktuur kulude salvestamiseks
kulutused = []
failinimi = "kulutused.csv"
eelistused = []
failinimetus = "eelistused.csv"

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
            
    # Sulgeb sisstetulekute akna ja avab eelistuste akna        
    def ava_eelistused():
        sissetuleku_aken.destroy()
        ava_eelistused_aken()
        
    
    # Sulgeb sisstetulekute akna ja avab kulude akna
    def mine_edasi():
        sissetuleku_aken.destroy()
        ava_kulude_aken()


    tk.Button(sissetuleku_aken, text="Kinnita", command=kinnita_sissetulek).grid(row=0, column=2, columnspan=2, pady=10)
    tk.Button(sissetuleku_aken, text="Mine edasi", command=mine_edasi).grid(row=1, column=2, columnspan=2, pady=10)
    tk.Button(sissetuleku_aken, text="Eelistused", command=ava_eelistused).grid(row=4, column=0, columnspan=2, pady=10)
    
    sissetuleku_aken.mainloop()
    
    
def ava_eelistused_aken():
    
    eelistus_protsent = ""
    eelistus_kategooria =""
    
    def kinnita_eelisus():
        
        try:
            eelistus_kategooria = kulutuste_var.get()
            eelistus_protsent = protsent_var.get()        
            print(eelistus_kategooria, eelistus_protsent)
        except ValueError:
            messagebox.showerror("Viga")
                                            
        eelistus = {"kategooria": eelistus_kategooria, "Protsent kogu kulust": eelistus_protsent}
        eelistused.append(eelistus)
        with open(failinimetus, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["kategooria","Protsent kogu kulust"])
            # Kui fail on tühi, kirjuta pealkirjaread
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(eelistus)
        file.close()
        
    # Sulgeb eelistuste akna ja avab sissetuleku akna    
    def tagasi_sissetuleku_aken():
        eelistused_aken.destroy()
        ava_sissetuleku_aken()       
            
    eelistused_aken = tk.Tk()
    eelistused_aken.title(f"Eelistused - {kuu_nimi}")
    tk.Label(eelistused_aken, text=f"Määra {kuu_nimi} kulutuste jaotus").grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(eelistused_aken, text="Määra  kulutuste kategooria").grid(row=2, column=0, columnspan=2, pady=5)
    
    kulutuste_var = tk.StringVar()
    kuu_dropdown = tk.OptionMenu(eelistused_aken, kulutuste_var, *kategooriad)
    kuu_dropdown.grid(row=2, column=2)
    
    tk.Label(eelistused_aken, text="Määra protsent kogu kulust").grid(row=3,column=0, columnspan=1, pady=5)
    protsent_var = tk.StringVar()
    tk.Entry(eelistused_aken, textvariable=protsent_var).grid(row=3, column=1)
    tk.Button(eelistused_aken, text="Kinnita", command=kinnita_eelisus).grid(row=4, column=0, columnspan = 1, pady=5)
    tk.Button(eelistused_aken, text="Tagasi", command=tagasi_sissetuleku_aken).grid(row=4, column=2, columnspan = 1, pady=5)
    eelistused_aken.mainloop()
    
    

# Põhiaken kulude haldamiseks
def ava_kulude_aken():
    kulude_aken = tk.Tk()
    kulude_aken.title(f"Eelarve Jälgimine - {kuu_nimi}")
    tk.Label(kulude_aken, text=f"Kuu sissetulek: €{sissetulek:.2f}").grid(row=0, column=0, columnspan=2, pady=5)

    # Sisestusväljad ja nupud kulude lisamiseks
    summa_var = tk.StringVar()
    tk.Label(kulude_aken, text="Summa (€):").grid(row=1, column=0)
    tk.Entry(kulude_aken, textvariable=summa_var).grid(row=1, column=1)
    tk.Label(kulude_aken, text="Kategooria:").grid(row=2, column=0)    
    kategooria_var = tk.StringVar()
    kulutuste_dropdown = tk.OptionMenu(kulude_aken, kategooria_var, *kategooriad)
    kulutuste_dropdown.grid(row=2, column=1)
    
        
    # Sulgeb kulude akna ja avab eelistuste akna 
    def ava_eelistused():
        kulude_aken.destroy()
        ava_eelistused_aken()
     
    #Toplevel mis näitab edukat salvestamist
    def lisatud():
        kestvus = 1500
        top = Toplevel()
        top.title('Lisatud')
        Message(top, text="Kulu on edukalt lisatud ja salvestatud faili!", padx=20, pady=20).pack()
        top.after(kestvus, top.destroy)

     # Funktsioon kulude lisamiseks     
    def lisa_kulu():
        summa = summa_var.get()
        kategooria = kategooria_var.get()
        
        if summa and kategooria:
            try:
                # Avab Toplevel-i, mis näitab edukat salvestamist
                lisatud()                
                summa = float(summa)
                kulu = {"kuupäev": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "summa": summa, "kategooria": kategooria, "Kuu nimi": kuu_nimi}
                kulutused.append(kulu)
                
                # Salvesta uus kulu CSV-faili
                with open(failinimi, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Kuu nimi","kuupäev", "summa", "kategooria"])
                    # Kui fail on tühi, kirjuta pealkirjaread
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow(kulu)
                
                summa_var.set("")
                kategooria_var.set("")
            except ValueError:
                messagebox.showerror("Viga", "Sisesta kehtiv summa!")
        else:
            messagebox.showerror("Viga", "Summa ja kategooria on kohustuslikud väljad!")

    # Loeb kulud CSV failist. Retunring dictionary kuludest
    def kulud_csvst():        
        kategooriad = defaultdict(float)
        with open(failinimi, mode = "r", newline = "", encoding = "utf-8") as fail:
            reader = csv.DictReader(fail)
            for rida in reader:
                kategooria = rida.get("kategooria", "summa")
                summa = float(rida.get("summa", 0))
                kategooriad[kategooria] += summa
        return kategooriad
    
    
    # Funktsioon kulutuste vaatamiseks
    def vaata_kulusid():
        kategooriad = kulud_csvst()
        if kategooriad:
            kategooriate_kokkuvõte = "\n".join(
                [f"{kat}: €{summa:.2f}" for kat, summa in kategooriad.items()])
            messagebox.showinfo("Kulude kokkuvõte", kategooriate_kokkuvõte)
        else:
            messagebox.showinfo("Kulude kokkuvõte", "Ei leitud kulutusi.")

    # Funktsioon kulutuste graafiku näitamiseks
    def kuva_graafik():
        kategooriad = kulud_csvst()
        if kategooriad:
            kategooriad_nimed = list(kategooriad.keys())
            kategooriad_summa = list(kategooriad.values())
            plt.figure(figsize=(8, 5))
            plt.pie(kategooriad_summa, labels=kategooriad_nimed, autopct='%1.1f%%', startangle=140)
            plt.title("Kulude jaotus kategooriate lõikes")
            plt.savefig("kulude_graafik.png")
            
            #Kuvab graafiku
            plt.show()            
            messagebox.showinfo("Graafik", "Graafik salvestati faili 'kulude_graafik.png'")
        else:
            messagebox.showinfo("Graafik", "Ei leitud kulutusi.")

    # Lihtne soovitus funktsioon
#     TODO mingi algo siia taha, mis arvestab eelistusi CSV/st
    def kuva_soovitus():        
# Võtab kulud CSV-st ja liidab kõik kokku
        kogukulu = sum(kulud_csvst().values())
                
        if kogukulu > sissetulek * 0.8:
            soovitus = "Teie kulud on üsna kõrged! Kaaluge vähendamist!"
        elif kogukulu > sissetulek * 0.5:
            soovitus = "Hästi hoitud, kuid jälgige oma kulutusi!"
        else:
            soovitus = "Suurepärane! Teie kulud on madalad."

        messagebox.showinfo("Soovitus", soovitus)

    # Nupud kulude lisamiseks ja vaatamiseks
    tk.Button(kulude_aken, text="Lisa kulu", command=lisa_kulu).grid(row=4, column=0, pady=10)
    tk.Button(kulude_aken, text="Vaata kulusid", command=vaata_kulusid).grid(row=4, column=1, pady=10)
    tk.Button(kulude_aken, text="Kuva graafik", command=kuva_graafik).grid(row=5, column=0, pady=10)
    tk.Button(kulude_aken, text="Kuva soovitus", command=kuva_soovitus).grid(row=5, column=1, pady=10)
    
    # Nupp eelistuste lehe avamiseks
    tk.Button(kulude_aken,text="Ava eelistused", command=ava_eelistused).grid(row=6, column=0, padx=10, pady=10)
    
    kulude_aken.mainloop()

# Käivita sissetuleku aken
ava_sissetuleku_aken()

