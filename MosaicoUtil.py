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
from util import modif_text, parse_json, modif_balise
import sqlite3
import json

icon = """
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAAAAXNSR0IArs4c6QAAAARnQU1BAACx
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
        self.json_group.pack(fill=tk.X, padx=5, pady=10)

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
        self.webappsstore_file_button.pack(padx=5, pady=5)

        self.frame_json_button = tk.Frame(self.json_group)
        self.frame_json_button.pack(fill=tk.X)
        self.import_json_button = tk.Button(self.frame_json_button, text="import json", command=self.on_import_json_button_clicked)
        self.import_json_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.export_json_button = tk.Button(self.frame_json_button, text="export json", command=self.on_export_json_button_clicked)
        self.export_json_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.modif_json_button = tk.Button(self.frame_json_button, text="modif export.json", command=self.on_modif_json_button_clicked)
        self.modif_json_button.pack(side=tk.LEFT, padx=5, pady=5)


        # interface pour les modif html
        self.html_group = tk.LabelFrame(self, text="Modif HTML")
        self.html_group.pack(fill=tk.X, padx=10, pady=10)

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
        self.master.resizable(width=False, height=False)

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
        with open(json_file, "r") as f:
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
        soup = BeautifulSoup(html, "html.parser")
        texts = soup.find_all(string=True)
        for t in texts:
            if type(t) == NavigableString and t.parent.name != "style":
                t.replace_with(modif_text(t))

        # modification des balises
        html = soup.prettify(formatter=None)
        html = modif_balise(html)

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
