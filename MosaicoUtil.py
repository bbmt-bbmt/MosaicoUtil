#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
import pathlib
import sys
import traceback
from bs4 import BeautifulSoup
from bs4 import NavigableString
from util import modif_text, parse_json, modif_balise, verif_html
import sqlite3
import json
import os
import fnmatch
from threading import Thread
import time
import configparser

icon = """iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAAXNSR0IArs4c6QAAAARnQU1BAACx
jwv8YQUAAAMAUExURQAAAAUAAAkAAA0AABEAABUAABkAAB0AACEAACQAACoAAC0AADEAADUAADkA
ADwAAEIAAEUAAEgAAE0AAFEAAFUAAFkAAF0AAGEAAGUAAGkAAG0AAHEAAHUAAHkAAH0AAIEAAIUA
AIkAAI0AAJAAAJUAAJkAAJ0AAKAAAKUAAKkAAK0AALEAALUAALkAAL0AAMIAAMUAAMkAAM0AANEA
ANQAANoAAN0AAOEAAOUAAOgAAO0AAPEAAPUAAPkAAP4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOHBI0gAAAAJcEhZcwAADsMA
AA7DAcdvqGQAAAAZdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjAuMTJDBGvsAAAEtUlEQVRYR9VW
13biMBAVppiAwRBMqE5IaJtCMcWUgPX/f7Uzd2RwSDaH3X3KzTlhpBldS9Mkpf8TP5agVw6N9I8E
eZVdi/SJIBy9i7Cfa700MhCZX8JWKZUX3SXB0FKuWDZnWj8uITKeddNIhBERKBlfENyzpgXxdafX
ndn7Rq8OenlYFMJQB9FidWRdnc3SED8QRG1WKMXfXaTtVdbq/aqvM95b2qtbvjfM+OX0I+mOFlux
dEHQxXKlOiT7Tbf/0iGC+9d9bVnX7qFWeXdLoy7pJmyUPmBNkqCH1QQ+Q7cyfuh5vbHXDlbVlQeC
8NZdMnmDjVggJAiGWMx4o9EyWwjtzKuyZqlaXzn69tgcqnF1RTuI0mxkEuFM8Iy1KvNixoL9RlO4
dkfNHtvpA/3pGduVRH8mmMExytma8TeAq4dmEBMsU7IeofkeUZYt92ZkCDY5rC+IZ7/HlC1dMzAE
Rwfr8zEtIZG4BttWLt2lHTbZ9MlMGgJklkqb+mC0U7mpSNFkMuGNvcD3dXOCuBiFYMxTKkXVE4ND
klpBfCGRNHGQZ4hBESoGExzAqUYkvlR9PsbR5okyG2B3wTlJ3Ar/l3JhMIEoPa3XJfotEgOqTTXY
YMvh2QcSpBPOycIEZZ66Oeq+WNW1LmIGIeH6zBzzPJHAjlUAE2BquuHPA69z/MCJ7+w6F45Xlv+K
/SddwATvmOueN5n1+L/0i0cW5fsZqvKDWOFwAiKILs4nSGGXB3gTsAIa70RmfxvwESSLLnAPtXgT
GPC4L/ICSoAJWjLLsGoZEVIoquhGRgSbqyQyG2KdActIbiC/0muRxAOmxBnUYuOMUwUoBSCLD1rh
JLqFyAfm9h+jysPYIzUoBSCAq5XqYQb9yobIWWwAQvRsgg+tAARHPmrWFA++0oZYYBFweBjG4UoE
QQj0MpeqmVb0BhPuivGJGX0eu2YgKWYgBPoYd4IIWYxUjV3OYPa46ccOEhiCEyRpMywazzDY7b9Y
cJHvUueCC4IO6+XIC+myAFUq1qsZCi/RuD4SHM3VxkEzZxEUtxKAklTunwh2kgIEqjaff5vSak6Y
CEGy9SYIJmenpQI4wNon/EiomN5hFgAY7NvDXvOyZxDGpxwVUD0zQRYrDUCQCLhC7xWQJ+S6MOAE
/JrgXE2qxq8XgU1HTRKUuB5rJHwmOC+iOzvONzSQRKuQWwfR+OxEc1SbMzjuIUh4bm7FZ66BgsQO
9fU5lZ942hngZo2kpUjFcTAcHXhuy3wVm0VtGwiBDqer04tuwDa3Iu8pEXIiGrATKDwnGIIPIBsv
vlsXtukNMba8wfPF9CWBnp6fh3RdXTw5Fr5/n3h/fknwN/ixBOFmtxHpHwkWywAXxfUEU4eyvP7m
RPd0xU2aYRhswoBjfS1Bo0vp1xjVowERBQ/z9XwV4El1LUHzbuZ3/W5rfNdqtYcPzWFn3Eavv5Zg
rvybYrmXzjt3o0KjYlvVXB3v/aud2FSNjhpbatjw7J5XvHWyaVzy1xLcTdVd2xpbqZFddXqe4zfW
I7ziriWoV3L2TaaaSjvWTa6cz7ZLbgsP9msJxv3l4KnT6XT9zsOo3+/PH0YDXKBX++BP+PEEWv8G
UN++3JjTpFIAAAAASUVORK5CYII=
"""
throbber_gif = """R0lGODlhFAAUAOZ/ALe3t7i4uKSkpKenp5qampKSkqCgoFVVVaqqqlpaWp6enqioqJaWlqKiooaG
hpiYmJSUlHx8fCsrK4yMjI+Pj4qKin5+foSEhHJycoKCgoiIiJCQkJycnICAgHV1dXh4eHZ2dm5u
bk1NTWxsbHBwcGBgYHp6emhoaGRkZFxcXGZmZkRERGJiYjMzM15eXmpqajs7Ox4eHvHx8fX19fv7
+/Pz8/j4+Pb29t3d3fn5+fr6+vDw8Pz8/PT09Orq6u7u7tra2ujo6NfX1+3t7eTk5OLi4ubm5vf3
9+vr6+/v79LS0rW1teXl5ezs7N/f3/39/f7+/s7Ozs3NzePj4+Dg4NTU1PLy8snJydnZ2d7e3sjI
yLq6usDAwNXV1cvLy8LCwsbGxunp6eHh4dbW1srKysPDw+fn59jY2NHR0dPT09vb27u7u729vby8
vL6+vtzc3LKysqysrK2trcTExNDQ0K6urrOzs6+vr8fHx8/Pz7CwsMzMzLGxscHBwf///////yH/
C05FVFNDQVBFMi4wAwEAAAAh/wtYTVAgRGF0YVhNUDw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0i
VzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6
bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMDY3IDc5LjE1Nzc0NywgMjAxNS8w
My8zMC0yMzo0MDo0MiAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3Lncz
Lm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJv
dXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBN
TT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9u
cy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0i
QWRvYmUgUGhvdG9zaG9wIENDIDIwMTUgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAu
aWlkOjE5MDVDNDUwQ0I2NzExRTY4OTdERDdFODRENjdCMUNCIiB4bXBNTTpEb2N1bWVudElEPSJ4
bXAuZGlkOjE5MDVDNDUxQ0I2NzExRTY4OTdERDdFODRENjdCMUNCIj4gPHhtcE1NOkRlcml2ZWRG
cm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6MTkwNUM0NEVDQjY3MTFFNjg5N0REN0U4NEQ2
N0IxQ0IiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6MTkwNUM0NEZDQjY3MTFFNjg5N0REN0U4
NEQ2N0IxQ0IiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/
eHBhY2tldCBlbmQ9InIiPz4B//79/Pv6+fj39vX08/Lx8O/u7ezr6uno5+bl5OPi4eDf3t3c29rZ
2NfW1dTT0tHQz87NzMvKycjHxsXEw8LBwL++vby7urm4t7a1tLOysbCvrq2sq6qpqKempaSjoqGg
n56dnJuamZiXlpWUk5KRkI+OjYyLiomIh4aFhIOCgYB/fn18e3p5eHd2dXRzcnFwb25tbGtqaWhn
ZmVkY2JhYF9eXVxbWllYV1ZVVFNSUVBPTk1MS0pJSEdGRURDQkFAPz49PDs6OTg3NjU0MzIxMC8u
LSwrKikoJyYlJCMiISAfHh0cGxoZGBcWFRQTEhEQDw4NDAsKCQgHBgUEAwIBAAAh+QQJBAB/ACwA
AAAAFAAUAAAH4IB/goM3Qm5yCEtRMoONgzplBAwFFBMaFx11PY6CPgsGHAwEAgYUGRYRHUCOQwKk
AEU8gjQ4DR8fGG+DNHUIA0KcgloYGCQzglJ1cWrBg1chIwR/OnBwXM2NBScoO0UAS0PYg0QoKGtp
W23ijSElDFJuZOuDDikXdF9R84IRKRFYYK7s+5NAQoYgV8hsWudnSQkjNMhEWcXQj8U/TpRUCYfN
4sU/PKqcwcIomMePf2acweHEh41GUE76cdTDSREmQYZYuWHjyclgPJow8fFDxowcPGLOxEZjRo0a
N5BC4RQIACH5BAkEAH8ALAAAAAAUABQAAAfggH+CgzdCbnIIS1Eyg42DOmUEDAUUExoXHXU9joI+
CwYcDAQCBhQZFhEdQI5DAqQARTyCNDgNHx8Yb4M0dQgDQpyCWhgYJDOCUnVxasGDVyEjBH86cHBc
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
dHCgYYIaYT8YnAiBwcOHCBYyyEGGzQebgQQQgGnCKRAAIfkECQQAfwAsAAAAABQAFAAAB+uAf4KD
MzhVSnlkaD+DjYM5OE1IQUxiOFhVXzKOgkM/NTJNRWNKaUJdaGBdjkk5OTdURDSCOkBfUl54Y4M0
NFA0U5yCV1pgXJt/SH5+YcKDYF9cfH86yzvOjXxsWz5Dy8jYf2oB5D9+OuGNdUsLVn496YMCcAI1
fjPxggZ1BjtRZfn+GEBAQEyLFrvS7RAwgEwTEQdexNvSoAE+BwkSLAkHhICCNoJquChRYo2zMRAe
PDgyiE4JFCcKnGlURA+FAgWKOJIyYkQIDBkYEJjgoMKEAlmEJSHw80MECxkcOOBjJRwSLgM81tEy
hFMgACH5BAkEAH8ALAAAAAAUABQAAAfogH+CgzNOZ0JVeVVJg42DOVQyMkM+RlNOWGAyjoI/NTk3
VmZAQlg4pFJjjjt+fjRERjSCNG9gVUpSQoM0NK1MnIJ7UntgVoJIrT7Ag3haYEt/Oq07y41LZVxI
Q62b1YJvbmxrP67e1ltxMn495oMIAAtqKXXtggJ2Ag4SK/V/AnoKFqQ4gKadDARxvAxJkCJCOzcD
Btz4U6FECQDecBgQwEVQDxQoTrBZdoaAAQNHBqVRMSIEAyyNiCxhQIDAFEdRMGDw8MHBAwUFJmwo
8IAKsCQKeEbocMHBhAlLanhD0gfByTtkfnAKBAAh+QQJBAB/ACwAAAAAFAAUAAAH64B/goM3Ympv
Z2ljO4ONgzpTNzc1O01BRE5XVo6CSTZ+PEdNVGpORVRvSmeOMn6uYUE0gjpZZFiJq4I0NK5mnIJR
VUpem39Nrj6/g2RSewF/Oq6MyoMBV2BNQ64y1INZc2VsP1w63Y0BXHoUMQ7mg3JsciwJJe6CCwEI
DvT2fwhLBu6kcFHFnYw7fKIkKcGig7svcuTc+EMBxYkt3ZwMQFBGUI8TI0JwUQbEgAABNgalCYEB
AwEgUAYxCUDAgAEijvJ8AGEiQgUOBhgUYPBAgZhfOwyYsJDBQYUJGwps6dENSZk4DQQskZKEUyAA
IfkECQQAfwAsAAAAABQAFAAAB+uAf4KDN1NZWW9jZzuDjYM6Rjw8OTMyPz5MUjWOgkk2fn5PMlNO
REFGRUJYjjKgfkhhPII0TlFOOFirszygZpyCdFhnaFaCSKA+v4N7VUptfzqgjMqDbHleTWondjLU
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
ZAHiZIoRH0Nk1LAB9NoRJGaCINkxg8emQAA7"""


class FindThread(Thread):
    def __init__(self, app):#, init_dir, file, result):
        super().__init__()
        self.app = app
        self.stop = False
        # self.init_dir = init_dir
        # self.file = file
        # self.result = result
        return

    def run(self):
        try:
            throbber_thread = ThrobberThread(self.app.throbber_label, throbber_gif)
            throbber_thread.start()
            profile_matches = []
            # on cherche le fichier profiles.ini
            src_dir = os.path.expanduser("~")
            profile_file = "profiles.ini"
            for root, dirnames, filenames in os.walk(src_dir):
                if "firefox" in root.lower():
                    for filename in fnmatch.filter(filenames, profile_file):
                        profile_matches.append(os.path.join(root, filename))
                        print(root, filename)
                if  profile_matches:
                    break
            if profile_matches == []:
                messagebox.showinfo(message="Aucun fichier profiles.ini trouvé", title="Erreur")
                return
            # dans le fichier profiles.ini on tente d'extraire le profile par defaut
            config_ini = configparser.ConfigParser()
            try:
                config_ini.read(profile_matches[0])
            except IndexError:
                messagebox.showinfo(message="Aucun fichier profiles.ini trouvé", title="Erreur")
                return

            dict_ini = config_ini._sections
            path = None
            for section, items in dict_ini.items():
                if "Profile" in section:
                    try:
                        if items["default"] == "1":
                            path = items["path"]
                            break
                    except KeyError:
                        pass
            src_dir = pathlib.Path(profile_matches[0]).parent
            try:
                path = src_dir / path / "webappsstore.sqlite"
            except TypeError:
                messagebox.showinfo(message="Aucun profile par defaut trouvé", title="Erreur")
                return

            if path.is_file():
                self.app.webappsstore_text.delete(0, tk.END)
                self.app.webappsstore_text.insert(0, str(path))
                return
            else:
                messagebox.showinfo(message="impossible d'extraire le profile par défaut \
                                            dans le fichier profiles.ini", title="Erreur")
        finally:
            throbber_thread.stop = True
            throbber_thread.join()
        return

class ThrobberThread(Thread):
    def __init__(self, throbber_label, data_image):
        super().__init__()
        # le label doit contenir le gif
        self.gif = data_image
        self.throbber_label = throbber_label
        self.stop = False
        return

    def run(self):
        self.throbber_label.pack(side=tk.LEFT, padx=5, pady=5)
        while not self.stop:
            try:
                time.sleep(0.04)
                img = tk.PhotoImage(data=self.gif, format="gif - {}".format(self.num))

                self.throbber_label.config(image=img)
                self.throbber_label.image=img
                
                self.num += 1
            except:
                self.num = 0
        self.throbber_label.pack_forget()

class Application(tk.Frame):
    def __init__(self):
        super().__init__()
        # self.bind("<KeyPress-Return>", self.on_file_button_clicked)
        self.createWidgets()
        self.html = None
        return

    def createWidgets(self):
        self.pack(fill=tk.BOTH, expand=1)

        # interface pour la partie json
        self.json_group = tk.LabelFrame(self, text="JSON outils")
        self.json_group.pack(fill=tk.X, padx=20, pady=10)

        self.frame_template_id = tk.Frame(self.json_group)
        self.frame_template_id.pack(fill=tk.X)
        self.label_template_id = tk.Label(self.frame_template_id,text="Template id")
        self.label_template_id.pack(side=tk.LEFT, padx=5, pady=5)
        self.template_id_text = tk.Entry(self.frame_template_id)
        self.template_id_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=0, padx=5, pady=5)

        self.frame_webappsstore = tk.Frame(self.json_group)
        self.frame_webappsstore.pack(fill=tk.X)
        self.label_webappsstore = tk.Label(self.frame_webappsstore,text="File webappsstore")
        self.label_webappsstore.pack(side=tk.LEFT, padx=5, pady=5)
        self.webappsstore_text = tk.Entry(self.frame_webappsstore)
        self.webappsstore_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, padx=5, pady=5)
        self.webappsstore_file_button = tk.Button(self.frame_webappsstore, text="...", command=self.on_webappsstore_file_button_clicked)
        self.webappsstore_file_button.pack(side=tk.LEFT,padx=5, pady=5)
        self.webappsstore_auto_button = tk.Button(self.frame_webappsstore, text="Auto find", command=self.on_webappsstore_auto_button_clicked)
        self.webappsstore_auto_button.pack(side=tk.LEFT, padx=5, pady=5)
        # photo = tk.PhotoImage(data=throbber_gif, format="gif -index 4")
        self.throbber_label = tk.Label(self.frame_webappsstore)
        # self.throbber_label.photo = photo
        self.throbber_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.throbber_label.pack_forget()

        self.frame_json_button = tk.Frame(self.json_group)
        self.frame_json_button.pack(fill=tk.X)
        self.import_json_button = tk.Button(self.frame_json_button, text="Import json", command=self.on_import_json_button_clicked)
        self.import_json_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.export_json_button = tk.Button(self.frame_json_button, text="Export json", command=self.on_export_json_button_clicked)
        self.export_json_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.modif_json_button = tk.Button(self.frame_json_button, text="Modif json", command=self.on_modif_json_button_clicked)
        self.modif_json_button.pack(side=tk.LEFT, padx=5, pady=5)


        # interface pour les modif html
        self.html_group = tk.LabelFrame(self, text="Modif HTML")
        self.html_group.pack(fill=tk.X, padx=20, pady=10)

        self.frame_html_file = tk.Frame(self.html_group)
        self.frame_html_file.pack(fill=tk.X)
        self.label_html_file = tk.Label(self.frame_html_file,text="Nouveau titre")
        self.label_html_file.pack(side=tk.LEFT, padx=10, pady=5)
        self.title_text = tk.Entry(self.frame_html_file)
        self.title_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, padx=10, pady=5)
        self.title_text.bind("<KeyPress-Return>", self.on_file_html_button_clicked)

        self.frame_html_file_button = tk.Frame(self.html_group)
        self.frame_html_file_button.pack(fill=tk.X)
        self.file_html_button = tk.Button(self.frame_html_file_button, text="Choisir le fichier à modifier", command=self.on_file_html_button_clicked)
        self.file_html_button.pack(pady=5)


        # modif du titre et de l'icone de l'interface
        self.master.title('Mosaico Util')
        img = tk.PhotoImage(data=icon)
        self.master.iconphoto(self._w, img)
        # self.master.resizable(width=False, height=False)

        self.centerWindow()
        return

    def centerWindow(self):
        w = 500
        h = 300

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_webappsstore_auto_button_clicked(self):
        # result = None
        # self.throbber_label.pack(side=tk.LEFT, padx=5, pady=5)
        find_thread = FindThread(self)#,os.path.expanduser("~"), "webappsstore.sqlite", result)
        find_thread.start()
        return

    def on_import_json_button_clicked(self):
        file_name = self.webappsstore_text.get()
        if not pathlib.Path(file_name).is_file():
            messagebox.showinfo(message="Le fichier n'existe pas", title="erreur fichier")
            return
        template_id = self.template_id_text.get()
        template_name = "template-" + template_id
        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM webappsstore2 WHERE originKey LIKE "%%ociasom%%" AND key LIKE "%s"' % template_name)
        if cursor.fetchall() == []:
            messagebox.showinfo(message="L'id n'est pas correct", title="erreur d'id")
            return
        json_file = filedialog.askopenfilename(initialdir=".", filetypes=[("json","*.json")])
        with open(json_file, "r", encoding="utf-8") as f:
            json_str = f.read()
        sql = 'UPDATE webappsstore2 SET value=? WHERE originKey LIKE "%%ociasom%%" AND key LIKE ?' #% (json_str, template_name)
        cursor.execute(sql, (json_str, template_name))
        conn.commit()
        messagebox.showinfo(message="Import réussit", title="Import réussit")
        return

    def on_export_json_button_clicked(self):
        file_name = self.webappsstore_text.get()
        if not pathlib.Path(file_name).is_file():
            messagebox.showinfo(message="Le fichier n'existe pas", title="erreur fichier")
            return
        template_id = self.template_id_text.get()
        template_name = "template-" + template_id
        conn = sqlite3.connect(file_name)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM webappsstore2 WHERE originKey LIKE "%%ociasom%%" AND key LIKE "%s"' % template_name)
        result = cursor.fetchall()
        if result == []:
            messagebox.showinfo(message="L'id n'est pas correct", title="erreur d'id")
            return

        json_str = result[0][0]
        with open("export.json", "w", encoding="utf-8") as f:
            f.write(json_str)

        messagebox.showinfo(message="export réussit", title="export réussit")
        return

    def on_modif_json_button_clicked(self):
        file_name = filedialog.askopenfilename(initialdir=".", filetypes=[("json","*.json")])
        try:
            with open(file_name, mode="r", encoding="utf-8") as json_file:
                json_dict = json.load(json_file)
        except FileNotFoundError:
            messagebox.showinfo(message="Le fichier n'existe pas", title="Fichier non trouvé")
            return

        result = parse_json(json_dict)

        # ecriture du nouveau fichier
        path = pathlib.Path(file_name)
        save_file_name = str(path.with_name("json_modif.json"))
        with open(save_file_name, mode="w", encoding="utf-8") as f:
            f.write(result)

        messagebox.showinfo(message="fichier modifié", title="fichier modifié")
        return


    def on_webappsstore_file_button_clicked(self, event=None):
        file_name = filedialog.askopenfilename(initialdir=".", filetypes=[("webappsstore.sqlite","webappsstore.sqlite")])
        self.webappsstore_text.delete(0, tk.END)
        self.webappsstore_text.insert(0, file_name)
        return

    def on_file_html_button_clicked(self, event=None):
        title = self.title_text.get()
        file_name = filedialog.askopenfilename(initialdir=".", filetypes=[("html","*.htm*")])
        try:
            with open(file_name, mode="r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            messagebox.showinfo(message="Le fichier n'existe pas", title="Fichier non trouvé")
            return

        # modification du titre
        html = re.sub("<title>(.|\s)*?</title>", "<title>%s</title>" % title, html)

        # modification du texte: féminisation, ponctuation ...
        soup = BeautifulSoup(html, "lxml")
        texts = soup.find_all(string=True)
        for t in texts:
            if type(t) == NavigableString and t.parent.name != "style":
                t.replace_with(modif_text(t))

        # modification des balises
        html = soup.prettify(formatter=None)
        # html = modif_balise(html)

        # ecriture du nouveau fichier pour internet
        # path = pathlib.Path(file_name)
        # save_file_name = str(path.with_name("fichier_pour_site_internet.html"))
        save_file_name = "fichier_pour_site_internet.html"
        with open(save_file_name, mode="w", encoding="utf-8") as f:
            f.write(html)

        # ecriture du nouveau fichier pour thunderbird
        # integration de la class pour thundirbird
        html = html.replace("<img","<img moz-do-not-send='true'")
        # save_file_name = str(path.with_name("fichier_pour_thunderbird.html"))
        save_file_name = "fichier_pour_thunderbird.html"
        with open(save_file_name, mode="w", encoding="utf-8") as f:
            f.write(html)

        verif_html(html)

        messagebox.showinfo(message="fichier modifié", title="fichier modifié")
        return

def last_error(e_type, e_value, e_tb):
    messagebox.showerror(message=''.join(traceback.format_exception(e_type, e_value, e_tb)))
    return

def main(args):
    sys.excepthook = last_error
    
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main(sys.argv)
