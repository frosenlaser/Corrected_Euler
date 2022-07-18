import matplotlib
import numpy as np
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
import tkinter

matplotlib.use('TkAgg')


def error(y1, y2, x):
    z = []
    for i in range(len(x)):
        a = 0
        a = math.fabs(y1[i] - y2[i])
        z.append(a)
    return z


def f1(m, h, T0, taumax):

    lbl_bg = Label(window, text="", width=112, height=30)
    lbl_bg.config(bg='#ffffff')
    lbl_bg.place(x=200, y=0)

    def f(t, T):
        return -m * T

    if taumax % h != 0:
        lbl_warning = Label(window, text="taumax не кратен шагу")
        lbl_warning.config(bg='#ffaaaa')
        lbl_warning.place(x=205, y=65)
    else:
        n = int(taumax / h + 1)

        time = np.linspace(0, taumax, 1000)
        T_exact = []
        for i in range(len(time)):
            T_exacti = T0 * np.exp(-m * time[i])
            T_exact.append(T_exacti)

        tau = []
        tau.append(0)
        for i in range(1, n):
            taui = tau[i - 1] + h
            tau.append(taui)

        T_exact_tau = []
        for i in range(len(tau)):
            T_exacti_tau = T0 * np.exp(-m * tau[i])
            T_exact_tau.append(T_exacti_tau)

        T = []
        T.append(T0)
        for i in range(1, n):
            a = f(tau[i - 1], T[i - 1])
            Ti = (T[i - 1] + 0.5 * h * (a + f(tau[i], T[i - 1] + h * a)))
            T.append(Ti)

        Err = error(T, T_exact_tau, tau)

        print('       t       T_численное     T_точное       Погрешность')
        for i in range(len(tau)):
            print("%10.3f%15.3f%15.3f%15.3f" % (tau[i], T[i],
                                                T_exact_tau[i], Err[i]))
        print('\n')

        plot_error(tau, Err, window)
        plot_solution(tau, T, time, T_exact, window)

        def save():
            file1 = open('Corrected_Euler.txt', 'w')
            file1.write('dT/dtau = -mT, 0 < tau < taumax\n')
            file1.write(f"m = {m}, h = {h}, T(0) = {T0}, taumax = {taumax}\n")
            file1.write('       t       T_численное     T_точное\
            Погрешность\n')
            for i in range(len(tau)):
                file1.write("%10.3f%15.3f%15.3f%15.3f\n" % (tau[i], T[i],
                                                            T_exact_tau[i],
                                                            Err[i]))
            file1.close()
            print("Data saved!")
            btn2.destroy()
            lbl_saved = Label(window, text="Данные сохранены!")
            lbl_saved.place(x=25, y=195)

        btn2 = Button(window, text="Сохранить решение", command=save)
        btn2.place(x=25, y=195)


def plot_solution(x1, y1, x2, y2, window):
    fig = Figure(figsize=(5, 5))
    a = fig.add_subplot(111)
    a.plot(x1, y1, 'o', x2, y2)
    a.legend(['численное', 'точное'])
    a.set_title("Решение", fontsize=10)
    a.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=200, y=0)
    canvas.draw()


def plot_error(x1, y1, window):
    fig = Figure(figsize=(5, 5))
    a = fig.add_subplot(111)
    a.plot(x1, y1)
    a.set_title("Погрешность", fontsize=10)
    a.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().place(x=700, y=0)
    canvas.draw()


def clicked():
    m = float(txt_m.get())
    h = float(txt_h.get())
    T0 = float(txt_T0.get())
    taumax = int(txt_taumax.get())
    f1(m, h, T0, taumax)


def _quit():
    window.quit()
    window.destroy()


window = Tk()
window.title("Исправленный метод Эйлера")
window.geometry("1200x540+100+100")

lbl = Label(window, text="Введите данные:")
lbl.place(x=20, y=5)

lbl_m = Label(window, text="m")
lbl_m.place(x=25, y=35)
txt_m = Entry(window, width=10)
txt_m.place(x=60, y=35)
txt_m.focus()

lbl_h = Label(window, text="h")
lbl_h.place(x=25, y=65)
txt_h = Entry(window, width=10)
txt_h.place(x=60, y=65)

lbl_T0 = Label(window, text="T(0)")
lbl_T0.place(x=20, y=95)
txt_T0 = Entry(window, width=10)
txt_T0.place(x=60, y=95)

lbl_taumax = Label(window, text="taumax")
lbl_taumax.place(x=5, y=125)
txt_taumax = Entry(window, width=10)
txt_taumax.place(x=60, y=125)

btn = Button(window, text="Решить", command=clicked)
btn.place(x=65, y=165)

lbl_equation = Label(window, text="dT/dtau = -mT,")
lbl_equation.place(x=40, y=230)

lbl_condition = Label(window, text="0 < tau < taumax")
lbl_condition.place(x=35, y=260)

btn1 = Button(window, text="Выйти", command=_quit)
btn1.pack(side=BOTTOM, pady=10)

lbl_bg1 = Label(window, text="", width=109, height=30)
lbl_bg1.config(bg='#cdcdcd')
lbl_bg1.place(x=200, y=0)

window.mainloop()
