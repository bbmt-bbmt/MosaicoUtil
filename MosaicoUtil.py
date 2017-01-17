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
from util import modif_text, parse_json, modif_balise, verif_html, firefox_running, firefox_path
import sqlite3
import json
import os
import fnmatch
from threading import Thread
import time
import configparser
import urllib
import subprocess
import ttk
from ressource import *

# todo
# les try except sont inutiles dans les bouton json,
# des que le fichier change la connection est verifie dans on_webappstore_change
# à enlever 




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
                self.app.webappsstore_text.config(state=tk.NORMAL)
                self.app.webappsstore_text.delete(0, tk.END)
                self.app.webappsstore_text.insert(0, str(path))
                self.app.webappsstore_text.config(state=tk.DISABLED)
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

        # parametre commun
        self.param_commun = tk.LabelFrame(self, text="Commun")
        self.param_commun.pack(fill=tk.X, padx=20, pady=10)
        self.frame_img_path = tk.Frame(self.param_commun)
        self.frame_img_path.pack(fill=tk.X)
        self.label_img_path = tk.Label(self.frame_img_path,text="Path des images")
        self.label_img_path.pack(side=tk.LEFT, padx=10, pady=5)
        self.img_path = tk.Entry(self.frame_img_path)
        self.img_path.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, padx=10, pady=5)

        # interface pour la partie json
        self.json_group = tk.LabelFrame(self, text="JSON outils")
        self.json_group.pack(fill=tk.X, padx=20, pady=10)

        self.frame_webappsstore = tk.Frame(self.json_group)
        self.frame_webappsstore.pack(fill=tk.X)
        self.label_webappsstore = tk.Label(self.frame_webappsstore,text="File webappsstore")
        self.label_webappsstore.pack(side=tk.LEFT, padx=5, pady=5)
        # poru tracer le changement de texte
        self.str_webappstore = tk.StringVar()
        self.str_webappstore.trace("w", self.on_webappstore_change)
        self.webappsstore_text = tk.Entry(self.frame_webappsstore, textvariable=self.str_webappstore, state=tk.DISABLED, disabledbackground="white")
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

        self.frame_template_id = tk.Frame(self.json_group)
        self.frame_template_id.pack(fill=tk.X)
        self.label_template_id = tk.Label(self.frame_template_id,text="Template id")
        self.label_template_id.pack(side=tk.LEFT, padx=5, pady=5)
        self.combo_box_template_id = ttk.Combobox(self.frame_template_id, state=tk.DISABLED)
        # self.combo_box_template_id.insert(2, "salut2")
        self.combo_box_template_id.pack(fill=tk.BOTH, side=tk.LEFT, expand=0, padx=5, pady=5)
        # self.template_id_text = tk.Entry(self.frame_template_id)
        # self.template_id_text.pack(fill=tk.BOTH, side=tk.LEFT, expand=0, padx=5, pady=5)

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

        self.frame_title = tk.Frame(self.html_group)
        self.frame_title.pack(fill=tk.X)
        self.label_title = tk.Label(self.frame_title,text="Nouveau titre")
        self.label_title.pack(side=tk.LEFT, padx=10, pady=5)
        self.title_text = tk.Entry(self.frame_title)
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

    def on_webappstore_change(self, *args):
        path = pathlib.Path(self.webappsstore_text.get())
        if not path.is_file():
            return
        try:
            conn = sqlite3.connect(str(path))
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM webappsstore2 WHERE originKey LIKE "%%ociasom%%" AND key LIKE "edits"')
            result = cursor.fetchall()
        except sqlite3.DatabaseError:
            messagebox.showinfo(message="Impossible a d'ouvrir le fichier")
            self.combo_box_template_id.config(state="DISABLED")
            self.webappsstore_text.delete(0, tk.END)
            self.combo_box_template_id.config(state="NORMAL")
            self.combo_box_template_id['values'] = ()
            self.combo_box_template_id.config(state="DISABLED")
            return
        finally:
            conn.close()
        # on récupere le str de la base de doonnée
        # print(result)
        
        base_string = result[0][0][1:-1]
        # on split pour juste avoir l'id dans une list
        list_base_string = base_string.split(",")
        len_list = len(list_base_string)
        ids_list = list((list_base_string[i].strip('"') for i in range(len_list)))
        

        self.combo_box_template_id.config(state="NORMAL")
        self.combo_box_template_id['values'] = ids_list
        self.combo_box_template_id.current(newindex=0)
        # if result == []:
        #     messagebox.showinfo(message="L'id n'est pas correct", title="erreur d'id")
        #     return
        return

    def centerWindow(self):
        w = 500
        h = 350

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_webappsstore_auto_button_clicked(self):
        find_thread = FindThread(self)
        find_thread.start()
        return

    def on_import_json_button_clicked(self):
        file_name = self.webappsstore_text.get()
        if not pathlib.Path(file_name).is_file():
            messagebox.showinfo(message="Le fichier n'existe pas", title="erreur fichier")
            return
        template_id = self.combo_box_template_id.get()
        template_name = "template-" + template_id
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM webappsstore2 WHERE originKey LIKE "%%ociasom%%" AND key LIKE "%s"' % template_name)
            result = cursor.fetchall()
        except sqlite3.DatabaseError:
            messagebox.showinfo(message="Impossible d'ouvrir le fichier")
            conn.close()
            return

        if result == []:
            messagebox.showinfo(message="L'id n'est pas correct", title="erreur d'id")
            return
        json_file = filedialog.askopenfilename(initialdir=".", filetypes=[("json","*.json")])
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                json_str = f.read()
            sql = 'UPDATE webappsstore2 SET value=? WHERE originKey LIKE "%%ociasom%%" AND key LIKE ?' #% (json_str, template_name)
            cursor.execute(sql, (json_str, template_name))
        except FileNotFoundError:
            return
        finally:
            conn.commit()
            conn.close()

        final_message = "Import réussit"
        if firefox_running():
            final_message += ("\nVous devez fermer et re-ouvrir firefox\n"
                              "voici l'adresse à utiliser: https://mosaico.io/editor.html#%s" % template_id)
        else:
            final_message += "\nfirefox va être lancé avec l'identifiant json %s" % template_id

        messagebox.showinfo(message=final_message, title="Import réussit")

        if not firefox_running():
            try:
                subprocess.Popen([firefox_path(), "https://mosaico.io/editor.html#%s" % template_id])
            # on prend tout pour ne pas crasher le programme
            except Exception as e:
                messagebox.showinfo(message="Impossible de lancer firefox, vous devez le faire vous même :-)")
        return

    def on_export_json_button_clicked(self):
        file_name = self.webappsstore_text.get()
        if not pathlib.Path(file_name).is_file():
            messagebox.showinfo(message="Le fichier n'existe pas", title="erreur fichier")
            return
        template_id = self.combo_box_template_id.get()
        template_name = "template-" + template_id
        try:
            conn = sqlite3.connect(file_name)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM webappsstore2 WHERE originKey LIKE "%%ociasom%%" AND key LIKE "%s"' % template_name)
            result = cursor.fetchall()
        except sqlite3.DatabaseError:
            messagebox.showinfo(message="Impossible d'ouvrir le fichier")
            conn.close()
            return

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

        result = parse_json(json_dict, self.img_path.get())

        # ecriture du nouveau fichier
        path = pathlib.Path(file_name)
        save_file_name = str(path.with_name("json_modif.json"))
        with open(save_file_name, mode="w", encoding="utf-8") as f:
            f.write(result)

        messagebox.showinfo(message="fichier modifié", title="fichier modifié")
        return


    def on_webappsstore_file_button_clicked(self, event=None):
        file_name = filedialog.askopenfilename(initialdir=".", filetypes=[("webappsstore.sqlite","webappsstore.sqlite")])
        self.webappsstore_text.config(state=tk.NORMAL)
        self.webappsstore_text.delete(0, tk.END)
        self.webappsstore_text.insert(0, file_name)
        self.webappsstore_text.config(state=tk.DISABLED)
        return

    def on_file_html_button_clicked(self, event=None):
        title = self.title_text.get()
        img_path = self.img_path.get()
        file_name = filedialog.askopenfilename(initialdir=".", filetypes=[("html","*.htm*")])
        try:
            with open(file_name, mode="r", encoding="utf-8") as f:
                html = f.read()
        except FileNotFoundError:
            if file_name != "":
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

        # modification du src des img
        if img_path != "":
            if img_path[-1:] != "/":
                img_path = img_path + "/"
            imgs = soup.find_all("img")
            for img in imgs:
                # faut le faire 2 fois à cause du cas %2520
                src = urllib.parse.unquote(img["src"])
                src = urllib.parse.unquote(src)
                reg_img_name = re.search("/.*/(.*\.[\w]{3})",src)
                try: 
                    img_name = reg_img_name.group(1)
                    img["src"] = img_path + urllib.parse.quote(img_name)
                except AttributeError:
                    pass



        # modification des balises
        html = soup.prettify(formatter=None)
        html = modif_balise(html)


        # ecriture du nouveau fichier pour internet
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
