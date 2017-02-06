#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import NavigableString
import json
import re
import sys
from tkinter import messagebox
import urllib
import psutil
import os

def modif_text(text):
    # à mettre avant le traitement des espaces sinon le -e : peut devenir -e&nbsp:
    # obliger d'utiliser le code utf8 sinon le str(soup) va proteger les &
    # Modification de la féminisation
    result = re.sub("-e-s|-e", lambda m: "\u2011e" if m.group(0) == "-e" else "\u2011e\u2011s ", text)
    # Suppression des espaces multiple
    result = re.sub("( |\u00a0|&nbsp;)+", " ", result)
    # Modification de la ponctuation
    result = re.sub("[\u00a0 ]?([:!\?])[\u00a0 ]?", "\u00a0\\1 ", result)
    # modification des guillements
    result = re.sub('"[\u00a0 ]?((.|\s)*?)[\u00a0 ]?"', "\u00ab\u00a0\\1\u00a0\u00bb", result)
    return result


def parse_json(json_dict, img_path):
    # json_file = open("14112016.json", "r", encoding="utf-8")
    # json_dict = json.load(json_file)
    # result = parse_json(json_dict)
    json_str = json.dumps(json_dict, indent=True)
    json_list = json_str.split("\n")
    i=0
    for ligne in json_list:
        try:
            key, value = ligne.split(":", maxsplit=1)
        except ValueError:
            i=i+1
            continue
        # le -1 c'est à cause du point virgule de fin de ligne"
        if value[-1] == ",":
            value = value[:-1]
        value = value.strip('" ')
        value = value.replace('\\"','"')
        if "text" in key[-5:].lower():
            soup = BeautifulSoup(value, "lxml")

            final_value = soup.decode(formatter=None)
            final_value = final_value.replace('"','\\"')
            texts = soup.find_all(string=True)
            for t in texts:
                if type(t) == NavigableString and t.parent.name != "style": 
                    final_value = final_value.replace(t.strip(), modif_text(t).strip())
                    # le strip est important 
                    # json_list[i]=json_list[i].replace(t.encode(formatter=None).strip(), modif_text(t).strip())
                    json_list[i]= key + ': "' + final_value +'"'
                    if "}" not in json_list[i+1]:
                        json_list[i] = json_list[i] +','
        if '"src"' in key and img_path != "":
            if img_path[-1:] != "/":
                img_path = img_path + "/"
            # on unquote 2 fois à cause de %2520
            src = urllib.parse.unquote(value)
            src = urllib.parse.unquote(src)
            reg_img_name = re.search("/.*/(.*\.[\w]{3})",src)
            try: 
                img_name = reg_img_name.group(1)
            except AttributeError:
                pass
            else:
                # si mosaico est dans le nom du fichier, ce n'est pas une image que l'on traite
                if "mosaico" not in img_name.lower():
                    json_list[i] = key + ': "' + img_path + urllib.parse.quote(img_name) +'"'
                    if "}" not in json_list[i+1]:
                        json_list[i] = json_list[i] +','
        i=i+1
    return "\n".join(json_list)

def modif_balise(html):
    # suppression des data-mce qui serve à rien
    html = re.sub(" data-mce-.*?=[\"'].*?[\"']","",html)
    # la fermeture des balises est faite automatiquement grace au parser lxml
    # modification des <br> en <br/>
    # html = html.replace("<br>", "<br/>")
    # modification des <img ...> en <img ... />
    # html = re.sub("(<img.*?)>", r"\1/>", html)
    # modification des meta
    # html = re.sub("(<meta.*?)>", r"\1/>", html)
    # modification des hr
    # html = re.sub("(<hr.*?)>", r"\1/>", html)
    # suppression du footer
    html = re.sub("<!-- footerBlock -->(.|\s)*?<!-- /footerBlock -->", "", html)
    return html

def verif_html(html):
    soup = BeautifulSoup(html, "lxml")
    imgs = soup.find_all("img")
    alt_text = 0
    href_img = 0
    for img in imgs:
        try:
            if img["alt"] == "":
                alt_text = alt_text + 1
        except KeyError:
            alt_text = alt_text + 1

        if img.parent.name != "a":
            href_img = href_img + 1

    message = "Attention il y a:\n"
    if alt_text != 0:
        message = message + "%s image(s) qui n'ont pas de texte alternatif" % alt_text
    if href_img != 0:
        message = message + "%s image(s) qui n'ont pas de lien" % href_img
    if alt_text != 0 or href_img != 0:
        messagebox.showinfo(message="Attention il y a:\n %s image(s) qui n'ont pas de texte alternatif.\n %s image(s) qui n'ont pas de lien"
                                    % (alt_text, href_img), title="Avertissement" )
    return

def firefox_running():
    firefox_on = False
    for pid in psutil.process_iter():
        if "firefox" in pid.name():
            firefox_on = True
            break
    return firefox_on

def firefox_path():
    if "nt" in os.name:
        return win_firefox_path()
    elif "posix" in os.name:
        return "firefox"
    else:
        raise Warning("impossible de determiner l'os")


def win_firefox_path():
    
    win32_firefox_path = "C:\\Program Files (x86)" + "\\Mozilla Firefox\\firefox.exe"
    if not os.path.isfile(win32_firefox_path):
        win32_firefox_path = ""
    
    win64_firefox_path = "C:\\Program Files" + "\\Mozilla Firefox\\firefox.exe"
    if not os.path.isfile(win64_firefox_path):
        win64_firefox_path = ""

    if win64_firefox_path != "" and win32_firefox_path != "":
        raise Warning("aucun path valide")
    firefox_path = win32_firefox_path or win64_firefox_path
    return firefox_path

def main(args):
    pass

if __name__ == "__main__":
    main(sys.argv)
