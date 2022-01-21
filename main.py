#!/usr/bin/env python
import tkinter as tk
from tkinter.font import BOLD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import read_csv, DataFrame
from requests import get
from datetime import datetime
from webbrowser import open_new
import os

class App(object):
    def __init__(self, window):
        self.window = window
        window.title("COVID-19 info Poland")
        window.resizable(0,0)
#       window.iconbitmap('files/pics/icon.ico')

        self.wojewodztwo = {'': ['Cały kraj','dol.śląsk','kuj.-pom.','lubel.','lubus.','łódz.','małopol.','mazowiec.','opolsk.','podkarp.','podlask.','pomor.','śląsk.','świętokrz.','warm.-maz.','wielkopol.','zach.pom.']}


        self.bg = tk.PhotoImage(file='files/pics/background.gif')
        self.buttonPic = tk.PhotoImage(file='files/pics/button.gif')
        self.buttonPic2 = tk.PhotoImage(file='files/pics/button2.gif')
        self.buttonPic3 = tk.PhotoImage(file='files/pics/button3.gif')

        self.my_label = tk.Label(window, image=self.bg)

        self.my_canvas = tk.Canvas(window, width = 485, height = 300)
        self.my_canvas.pack(fill='both', expand=True)

        self.my_canvas.create_image(0,0, image=self.bg, anchor=('nw'))
        self.my_canvas.create_text(90, 70, text='Aktualna liczba zarażeń: ', font=("Helvetica", 10), fill='black')
        self.my_canvas.create_text(88, 100, text='Aktualna liczba zgonów: ', font=("Helvetica", 10), fill='black')
        self.my_canvas.create_text(109, 130, text='Aktualna liczba ozdrowieńców: ', font=("Helvetica", 10), fill='black')


        self.button1 = tk.Button(window, text='sprawdź', image=self.buttonPic, command=self.zarazenia)
        self.button2 = tk.Button(window, text='sprawdź', image=self.buttonPic, command=self.zgony)
        self.button3 = tk.Button(window, text='sprawdź', image=self.buttonPic, command=self.ozdrowiency)
        self.button4 = tk.Button(window, text='sprawdź', image=self.buttonPic2, command=self.download)
        self.button5 = tk.Button(window, text='sprawdź', image=self.buttonPic3, command=self.callback)

        self.button1_window = self.my_canvas.create_window(205,58,anchor='nw', window=self.button1)
        self.button2_window = self.my_canvas.create_window(205,88,anchor='nw', window=self.button2)
        self.button3_window = self.my_canvas.create_window(205,118,anchor='nw', window=self.button3)
        self.button4_window = self.my_canvas.create_window(310,282, window=self.button4)
        self.button5_window = self.my_canvas.create_window(205,220,anchor='nw', window=self.button5)

        self.my_canvas.create_text(135, 293, text='Ostatnia aktualizacja: ' + self.tryOpenDate()[0], font=("Helvetica", 10, BOLD), fill=self.tryOpenDate()[1])

        self.my_canvas.create_text(380, 70, text='Nowe przypadki: ' + str(self.casesTotal()), font=("Georgia", 10, BOLD), fill='#B41202')
        self.my_canvas.create_text(120, 220, text='Najnowsze zasady i obostrzenia\n\n można sprawdzić klikając ', font=('Helvetica', 10, BOLD), fill='black')

    def datesave(self):
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        with open('files/data/date.txt', 'w') as file:
            file.write(dt_string)
        return dt_string

    def download(self):
        req = get('https://www.arcgis.com/sharing/rest/content/items/153a138859bb4c418156642b5b74925b/data')
        with open('files/data/cases.csv', 'wb') as csv_file:
            csv_file.write(req.content)
        self.redraw()
        return 0

    def getData(self, case, legend):
        data = read_csv('files/data/cases.csv', sep=';', encoding='latin1')
        woj = DataFrame(self.wojewodztwo)
        df = DataFrame(data,columns=[case])
        df[''] = woj
        plotdata = df[['',case]].groupby('').sum().tail(16)
        plotdata = DataFrame.rename(plotdata, columns={case : legend})
        return plotdata

    def casesDate(self):
        if os.path.exists('files/data/cases.csv'):
            data = read_csv('files/data/cases.csv', sep=';', encoding='latin1')
            date = DataFrame(data, columns=['stan_rekordu_na', 'liczba_przypadkow'])
            d = date.iloc[0]['stan_rekordu_na']
            return d
        else:
            return 'error'

    def casesTotal(self):
        if os.path.exists('files/data/cases.csv'):
            data = read_csv('files/data/cases.csv', sep=';', encoding='latin1')
            date = DataFrame(data, columns=['stan_rekordu_na', 'liczba_przypadkow'])
            total = date.iloc[0]['liczba_przypadkow']
            return total
        else:
            return 'error'

    def barplot(self, case, title, legend):
        win = self.new_window()
        if os.path.exists('files/data/cases.csv'):
            figure = plt.Figure(figsize=(5,5), dpi=90)
            ax = figure.add_subplot(111)
            figure.autofmt_xdate()
            self.getData(case, legend).plot(kind='bar', legend=True, ax=ax, color=(0.7, 0.6, 0.55, 0.5),  edgecolor='red')
            bar = FigureCanvasTkAgg(figure, win)
            bar.get_tk_widget().pack()
            ax.set_title(title)
            return 0
        else:
            tk.Label(win, text="Najpierw wygeneruj dane przyciskiem 'zaktualizuj'.", bg='#8de3fe', fg='red', font='none 12 bold').pack()
            return 0

    def new_window(self):
        win1 = tk.Toplevel(self.window)
        win1.resizable(0,0)
        win = tk.Canvas(win1, bg='white')
        win.pack(expand=tk.YES, fill=tk.BOTH)
        return win

    def zarazenia(self):
        return self.barplot('liczba_przypadkow', 'Zarażenia w poszczególnych województwach\n' + 'Statystyki z dnia: ' + self.casesDate(), 'liczba przypadków')
    def zgony(self):
        return self.barplot('zgony', 'Zgony w poszczególnych województwach\n' + 'Statystyki z dnia: ' + self.casesDate(), 'liczba zgonów')
    def ozdrowiency(self):
        return self.barplot('liczba_ozdrowiencow', 'Liczba osób, które wyzdrowiały\n' + 'Statystyki z dnia: ' + self.casesDate(), 'liczba ozdrowieńców')


    def redraw(self):
        self.my_canvas.create_image(0,0, image=self.bg, anchor=('nw'))
        self.my_canvas.create_text(90, 70, text='Aktualna liczba zarażeń: ', font=("Helvetica", 10), fill='black')
        self.my_canvas.create_text(88, 100, text='Aktualna liczba zgonów: ', font=("Helvetica", 10), fill='black')
        self.my_canvas.create_text(109, 130, text='Aktualna liczba ozdrowieńców: ', font=("Helvetica", 10), fill='black')
        self.my_canvas.create_text(380, 70, text='Nowe przypadki: ' + str(self.casesTotal()), font=("Georgia", 10, BOLD), fill='#B41202')
        self.my_canvas.create_text(135, 293, text='Ostatnia aktualizacja: ' + self.datesave(), font=("Helvetica", 10, BOLD), fill='#005511')
        self.my_canvas.create_text(120, 220, text='Najnowsze zasady i obostrzenia\n\n można sprawdzić klikając ', font=('Helvetica', 10, BOLD), fill='black')

    def tryOpenDate(self):
        if os.path.exists('files/data/date.txt'):
            file = open('files/data/date.txt', 'r')
            return file.read(), '#005511'
        else:
            return 'BRAK', 'red'

    def callback(self):
        open_new('https://www.gov.pl/web/koronawirus/aktualne-zasady-i-ograniczenia')


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

