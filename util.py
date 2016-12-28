#!/usr/bin/python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import NavigableString
import json
import re
import sys
from tkinter import messagebox

def modif_text(text):
    # à mettre avant le traitement des espaces sinon le -e : peut devenir -e&nbsp:
    # Modification de la féminisation
    result = re.sub("-e-s|-e", lambda m: "&#8209;e" if m.group(0) == "-e" else "&#8209;e&#8209;s ", text)
    # Suppression des espaces multiple
    result = re.sub("( |&nbsp;)+", " ", result)
    # Modification de la ponctuation
    result = re.sub(" ?([:!\?]) ?", r"&nbsp;\1 ", result)
    # modification des guillements
    result = re.sub('" ?((.|\s)*?) ?"', r"&laquo;&nbsp;\1&nbsp;&raquo;", result)
    return result


def parse_json(json_dict):
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
        value = value[:-1].strip('" ')
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
                    if json_list[i+1].strip() != "}":
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
def main(args):
    pass

if __name__ == "__main__":
    main(sys.argv)
