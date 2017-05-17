#!/usr/bin/env python3
from tkinter import *
import tkinter.messagebox as messagebox
import re


def vloz_a_vykresli_vstupni_pole(vstupy):
    for i, j in enumerate(vstupy):
        vstupy[i][0].insert(10, vstupy[i][1])
        vstupy[i][0].grid(row=i, column=1)

def uprava_vstupu(vstup_hodnota, vstup_objekt):
    if re.search("^.*\s.*$", vstup_hodnota):
        vstup_hodnota = vstup_hodnota.replace(" ", "")
        vstup_objekt.delete(0, END)
        vstup_objekt.insert(10, vstup_hodnota)
    if re.match('^\d+[,]\d+$', vstup_hodnota):
        vstup_hodnota = vstup_hodnota.replace(",", ".")
        vstup_objekt.delete(0, END)
        vstup_objekt.insert(10, vstup_hodnota)
    return vstup_hodnota, vstup_objekt

def je_vstup_cislo(vstup_hodnota, vstup_objekt, index):
    zadano_spravne = False
    vstup_hodnota, vstup_objekt = uprava_vstupu(vstup_hodnota, vstup_objekt)
    try:
        n = float(vstup_hodnota)
        if index == 2 and (n == 0):
            vstup_objekt.configure(bg="light salmon")
            hodnota_l.configure(text=" ")
        elif index == 1 and (180.0 < n):
            vstup_objekt.configure(bg="light salmon")
        elif n >= 0:
            zadano_spravne = True
            vstup_objekt.configure(bg="white")
        else:
            vstup_objekt.configure(bg="light salmon")
    except ValueError:
        zadano_spravne = False
        vstup_objekt.configure(bg="light salmon")
    return zadano_spravne


# dosazeni tabulkove hodnoty "x" podle pomeru R/t (z tuple "x_tabulka") - pokud neexistuje tab. hodnota, dosadi se
# aproximovana hodnota
# vypocet "l_0" a vypocet "l" (podle typu profilu)
def spocti_a_vrat_vypocet(*args):
    rkut = float(vstup_R.get()) / float(vstup_t.get())

    x = None
    for first, second in x_tabulka:
        if first == rkut:
            x = second
            break
        else:
            # None
            # shall
            pass

    if x is None:
        x = 9.936985045 * pow(10, -3) * pow(rkut, 3 / 2) - 8.345332984 * pow(10, -2) * rkut + 2.385543455 * pow(10, -1) * pow(rkut, 1 / 2) + 2.514238307 * pow(10, -1)

    l_0 = 3.1415926535 * (180 - float(vstup_alfa.get())) * (float(vstup_R.get()) + float(vstup_t.get()) * x) / 180

    if profil.get() == 1:  # l profil
        l = l_0 + float(vstup_a.get()) + float(vstup_b.get())
        hodnota_l_0.configure(text="L\u2080 = %.2f" % l_0)
    else:  # u profil
        l = 2 * l_0 + float(vstup_a.get()) + float(vstup_b.get()) + float(vstup_c.get())
        hodnota_l_0.configure(text="L\u2080\u2081 = L\u2080\u2082 = %.2f" % l_0)
    hodnota_l.configure(text="L = %.2f" % l)


def spocti_a_vrat(prepnuto_mezi_profily=False):
    szn = 6 * [False]
    szn[0] = je_vstup_cislo(vstup_R.get(), vstup_R, 0)
    szn[1] = je_vstup_cislo(vstup_alfa.get(), vstup_alfa, 1)
    szn[2] = je_vstup_cislo(vstup_t.get(), vstup_t, 2)
    szn[3] = je_vstup_cislo(vstup_a.get(), vstup_a, 3)
    szn[4] = je_vstup_cislo(vstup_b.get(), vstup_b, 4)
    szn[5] = je_vstup_cislo(vstup_c.get(), vstup_c, 5)

    if not isinstance(prepnuto_mezi_profily, bool):
        prepnuto_mezi_profily = False
    # profil=1 -> L,  profil=2-> U
    if (profil.get() == 2 and all(szn)) or (profil.get() == 1 and all(szn[:-1])):
        spocti_a_vrat_vypocet()
    elif profil.get() == 2:
        hodnota_l.configure(text="L =")
        hodnota_l_0.configure(text="L\u2080\u2081 = L\u2080\u2082 = ")
        if prepnuto_mezi_profily is False:
            messagebox.showwarning("Upozornění", "Zadali jste nesprávnou hodnotu/hodnoty!")
    else:
        hodnota_l.configure(text="L =")
        hodnota_l_0.configure(text="L\u2080 =")
        if prepnuto_mezi_profily is False:
            messagebox.showwarning("Upozornění", "Zadali jste nesprávnou hodnotu/hodnoty!")


def l_profil(*args):
    vstup_c.configure(state="disabled")
    delka_c.configure(fg="grey")
    obrazek_label = Label(ramec4, image=obrazekL)
    obrazek_label.place(relx=0.5, rely=0.5, anchor="center")
    spocti_a_vrat(True)


def u_profil(*args):
    vstup_c.configure(state="normal")
    delka_c.configure(fg="black")
    obrazek_label = Label(ramec4, image=obrazekU)
    obrazek_label.place(relx=0.5, rely=0.5, anchor="center")
    spocti_a_vrat(True)


x_tabulka = ((0.1, 0.32), (0.25, 0.35), (0.5, 0.38), (1, 0.42),
             (2, 0.445), (3, 0.47), (4, 0.475), (5, 0.478),
             (6, 0.48), (8, 0.483), (10, 0.486))

master = Tk()
master.wm_title("Bender1.3.7")
master.iconbitmap("icon.ico")
master.geometry("560x320+500+200")
master.resizable(width=False, height=False)

obrazekL = PhotoImage(file="obrL.gif")
obrazekU = PhotoImage(file="obrU.gif")

Grid.rowconfigure(master, 0, weight=1)
Grid.rowconfigure(master, 1, weight=5)
Grid.rowconfigure(master, 2, weight=2)
Grid.columnconfigure(master, 0, weight=1)
Grid.columnconfigure(master, 1, weight=7)


ramec1 = LabelFrame(master, text=" Výběr profilu: ")                # Vyber profilu
ramec1.grid(row=0, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)
ramec2 = LabelFrame(master, text=" Zadání hodnot: ")                # Zadani vstupu a tlacitko "Spocitat"
ramec2.grid(row=1, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)
ramec3 = LabelFrame(master, text=" Výsledky: ")                     # Zobrazeni vysledku
ramec3.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)
ramec4 = LabelFrame(master, text=" Profil: ")                       # obrazek profilu
ramec4.grid(row=0, column=1, rowspan=3, columnspan=1, sticky=W + E + N + S)


Label(ramec2, text="Poloměr R ").grid(row=0, sticky=W, ipadx=4)
Label(ramec2, text="Úhel \u03B1").grid(row=1, sticky=W, ipadx=4)
Label(ramec2, text="Tloušťka t").grid(row=2, sticky=W, ipadx=4)
Label(ramec2, text="Délka a ").grid(row=3, sticky=W, ipadx=4)
Label(ramec2, text="Délka b ").grid(row=4, sticky=W, ipadx=4)
delka_c = Label(ramec2, text="Délka c ")
delka_c.grid(row=5, sticky=W, ipadx=4)


vstup_R = Entry(ramec2)
vstup_alfa = Entry(ramec2)
vstup_t = Entry(ramec2)
vstup_a = Entry(ramec2)
vstup_b = Entry(ramec2)
vstup_c = Entry(ramec2)
vstupy = [[vstup_R, "20"], [vstup_alfa, "90"], [vstup_t, "5"], [vstup_a, "0"], [vstup_b, "0"], [vstup_c, "0"]]
vloz_a_vykresli_vstupni_pole(vstupy)

hodnota_l_0 = Label(ramec3, text="L\u2080 =")
hodnota_l_0.grid(row=0, column=0, columnspan=2, sticky=W, ipadx=8)
hodnota_l = Label(ramec3, text="L =")
hodnota_l.grid(row=1, column=0, columnspan=2, sticky=W, ipadx=8)

profil = IntVar()
vyber_profiluL = Radiobutton(ramec1, text='''Profil "L"''', variable=profil, value=1, command=l_profil)
vyber_profiluU = Radiobutton(ramec1, text='''Profil "U"''', variable=profil, value=2, command=u_profil)
vyber_profiluL.grid(row=0, column=0, ipadx=8, ipady=4, sticky=W + E + N + S)
vyber_profiluU.grid(row=0, column=1, ipadx=4, ipady=4, sticky=W + E + N + S)
vyber_profiluL.invoke()

cudl_pocitaci = Button(ramec2, text="Spočítat", command=spocti_a_vrat)
cudl_pocitaci.grid(row=6, column=1, ipadx=10, sticky=W)

master.bind('<Return>', spocti_a_vrat)

master.mainloop()
