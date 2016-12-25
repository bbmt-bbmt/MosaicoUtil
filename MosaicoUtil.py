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
import os
import fnmatch
from threading import Thread
import time

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
throbber_gif = """R0lGODlhFAAUAPcAACsrKy8vLzg4OEVFRUZGRktLS05OTk5OTllZWV1dXV1dXWFhYWFhYWFhYWVl
ZWhoaHR0dHZ2dnp6enx8fIODg4qKioyMjJ+fn6CgoKKioqOjo6qqqqurq6+vr7Ozs7Ozs7S0tLe3
t7q6ury8vLy8vL+/v8HBwcHBwcPDw8XFxcfHx8vLy8vLy83NzdLS0tPT09TU1NTU1NfX19jY2Nra
2tzc3N3d3d3d3d3d3d/f39/f3+Dg4ODg4OLi4uLi4uPj4+Tk5OXl5eXl5ebm5unp6enp6enp6erq
6urq6uvr6+vr6+zs7Ozs7O3t7e7u7u/v7+/v7/Dw8PDw8PLy8vPz8/Pz8/Pz8/Pz8/T09PX19fb2
9vb29vb29vf39/f39/f39/f39/j4+Pj4+Pj4+Pn5+fr6+vr6+vr6+vv7+/v7+/z8/Pz8/Pz8/Pz8
/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v//
/////////////////////////////////////////////////////wAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAgHAAAAIf8LTkVUU0NB
UEUyLjADAQAAACwAAAAAFAAUAAAI1AAbCRxIsKDBglOe8DnIsBGPBwhSBGpoEEQAABOkLKIoEIyJ
DQsMYDACiGOjEgIGhGhhgwtBMi7EGFxBoAAJK2wGEfQiAskdgnZofBhx48zBNmH2EMRxgEEOM4YO
dlGxhWCQBg5epGF4hcOPOgMJDUGhY07DMlTkEOyhoMKXg0ROoGnEiKCPBBGA9DG440KSPAX9CIGh
wYObgVGOJNJSRY/BQ2MoQCgyg0WjDhayCCrUEIqMJRkkNHESg8kfioje0MFSQwmeNWoUmRQIJ07d
2bhzEwwIACH5BAgHAAAALAAAAAAUABQAhykpKSoqKioqKjAwMEpKSktLS05OTlBQUF9fX2hoaGlp
aWxsbG9vb3V1dXV1dXZ2doaGhoeHh4yMjI2NjZOTk5SUlJiYmJubm6CgoKOjo6Wlpaampqmpqays
rK2trbGxsbGxsbKysrW1tba2tra2tra2tra2trq6ur+/v8LCwsLCwsLCwsPDw8nJycrKysrKysvL
y8/Pz9TU1NbW1tbW1tnZ2dra2tra2tvb29zc3Nzc3N3d3d7e3uDg4ODg4OHh4ePj4+Tk5OTk5OXl
5eXl5ebm5ubm5ufn5+jo6Ojo6Ojo6O3t7e3t7e7u7u7u7vDw8PPz8/Pz8/T09PT09PT09PX19fX1
9fX19fb29vb29vf39/f39/f39/j4+Pj4+Pj4+Pj4+Pj4+Pn5+fn5+fn5+fv7+/v7+/v7+/v7+/z8
/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+
/v7+/v7+/v7+/v7+/v7+/v///////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjMABEJ
HEiwoEGDdlJQoHHwYBglPgwIUCClIcE8FwhMQDAgAZFDFgWiaQBgwQoLJZAECqljw4gIHYYkMfIl
JCIJASoI6YGFj55CNmE8AAFFziCDWpoY5HHiRpeGO0jQIQiGQYEcFtkwyUKwDQYHNfA0rPLETcEo
LlSQacjCxMEPB3AYfONnChAuBoNosGHFzMA/HF4g2pLG4J0lRSCEQNRiBqIYMtY0NLRHjQgUYjJ4
mHPGSRmbW454ofLjCqI+hGwCgiOozpg4NmPLthkQACH5BAgHAAAALAAAAAAUABQAhyoqKioqKi4u
Li4uLjo6OkpKSlNTU1ZWVl9fX2FhYWhoaGpqam1tbXBwcHh4eHx8fH19fYKCgoiIiIuLi5OTk5OT
k5eXl5iYmJiYmJmZmZubm52dnaSkpKenp6ysrK2trbS0tLS0tLe3t7e3t7i4uLq6ur6+vsDAwMHB
wcPDw8fHx8jIyMnJyczMzM3Nzc/Pz9DQ0NPT09PT09PT09TU1NfX19fX19/f39/f3+Dg4OHh4eHh
4eLi4uLi4uPj4+fn5+fn5+fn5+jo6Onp6evr6+zs7Ozs7Ozs7O3t7e3t7e7u7u/v7+/v7+/v7/Dw
8PDw8PDw8PHx8fHx8fHx8fLy8vLy8vPz8/Pz8/X19fX19fX19fb29vb29vb29vb29vf39/j4+Pn5
+fn5+fn5+fr6+vr6+vr6+vr6+vr6+vv7+/v7+/v7+/v7+/v7+/z8/Pz8/Pz8/P39/f39/f39/f39
/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+/v7+/v//////////////////////
/////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAjPABkJHEiwoEGDSGh0sWGBBaCDBcM8IJCBQQADQyAK5IFBxYIB
ERoIOPBDIyMOACCYqNAixQQQWUy+cCDiiI8oTXQYkQPxzQcKMYjQ2XNI0Jw/Gq8gKLCjkMmCYEZ4
sPK0YB0XJ8pAVJRGT8FAEhRggcgnRI+Cd1aUGAMRT44pBftICTJDi8E2SryoOXgjgQxGiRgRgsMI
iIYtEJ+gSFKjg5siF5ZwwWEG4hkobGBsEOOEBJU4X+xAXCSwipA1ZJigqSowj5tBhvwgYk27dsGA
ACH5BAgHAAAALAAAAAAUABQAh19fX2BgYGZmZmZmZmpqam5ubnV1dXd3d3p6eoGBgYyMjJCQkJKS
kpWVlZmZmZqamp+fn6KioqOjo6ioqKqqqqurq6ysrKysrK2trbS0tLm5uby8vL29vb+/v8DAwMHB
wcHBwcbGxsjIyMvLy8zMzM3Nzc7Ozs/Pz9DQ0NLS0tLS0tPT09PT09PT09TU1NbW1tbW1tfX19jY
2NnZ2dnZ2dvb29vb29zc3Nzc3N3d3d3d3eHh4eHh4eLi4uLi4uLi4uPj4+Xl5ebm5ubm5ubm5ubm
5ufn5+fn5+fn5+jo6Onp6evr6+vr6+zs7O7u7u7u7vHx8fHx8fLy8vLy8vX19fX19fX19fX19fX1
9fb29vb29vf39/f39/n5+fn5+fr6+vr6+vr6+vr6+vv7+/v7+/v7+/z8/Pz8/Pz8/Pz8/Pz8/Pz8
/Pz8/P39/f39/f39/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+
/v7+/v7+/v///////////////////////////////////////////////////wAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjOABsJHEiwoMGC
gcoIMqODSKGDBmEwYJGiQIIfJWzYgcgGDQYAFzoMQABBgIEdB6lEqBBiQo4XFEA8CEBAxkEgBxT4
MNIlShAlHxZYsGJwEBIOM+roUWQIEJkhMZbkMcjHg4YtBt+AuXNQSwMJdCBCnILiiFiIZ4oIIXT2
4AYHYdoWFLPCxZ6DjHhIMZjmyRUVNQyuMcHkYKIxGUQ0ukGiURIcX6DAgZilR5U/LUY0onFikRxD
EPF4maOmCZY4TrjIFXjIjR9Ebfqsnk27YEAAIfkECAcAAAAsAAAAABQAFACHXl5eaGhoaWlpbGxs
bGxsbW1tdXV1enp6e3t7fn5+g4ODhYWFhoaGiYmJjIyMkZGRkZGRmpqanZ2doaGhpqamq6urq6ur
sbGxt7e3uLi4urq6vLy8wMDAwcHBxcXFxcXFx8fHx8fHycnJysrKzc3Nzs7Ozs7O0dHR0dHR1NTU
1NTU1dXV1tbW1tbW1tbW2NjY2NjY2NjY2dnZ2tra2tra2tra3Nzc3t7e39/f39/f4eHh4uLi4uLi
4+Pj5OTk5OTk5eXl5ubm5+fn5+fn6enp6urq6+vr6+vr6+vr7e3t7+/v8PDw8PDw8PDw8/Pz8/Pz
9PT09PT09fX19fX19fX19fX19fX19fX19vb29vb29vb29vb29vb29/f39/f39/f3+Pj4+Pj4+Pj4
+Pj4+Pj4+fn5+fn5+vr6+vr6+vr6+vr6+vr6+/v7+/v7+/v7+/v7+/v7/Pz8/Pz8/Pz8/Pz8/f39
/f39/f39/f39/f39/f39/f39/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+
/v7+////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAACM8AHQkcSLCgwYOKnoQ5eLDOECs/GEwwU4SIIIYCYRig4KHAgxgJEOzA
OOaDAgwpOuTgIIBAiBpXDC7RQOJGmSpUopiocGFBAAuBCMoZcaAFn0YC8ygJAmIAAAhwCGp5IeON
QTEoIjhQUVCNiyYH9RyZIcQOwUJAGqxgCGiOn4JucLAgg/HgoC5OkPypa9DQCQlf+BbMYsNHIihY
CPYhxJDOFjxxMohwdAeRohI86i5iokPKmQ1GuPSYUpcRGzR7ktAA0yaNYIGHvKx5Tbs2w4AAIfkE
CAcAAAAsAAAAABQAFACHKCgoKysrMDAwOjo6TU1NTk5OUVFRVFRUVVVVXV1dYGBgY2NjZGRkcnJy
d3d3goKCg4ODhISEiYmJiYmJi4uLjY2NkJCQlZWVmJiYm5ubn5+fqKioq6urr6+vsrKys7Ozs7Oz
tbW1tra2t7e3urq6u7u7vb29wcHBwsLCxsbGx8fHyMjIycnJzMzMzMzMzc3Nzs7O0dHR0tLS0tLS
1NTU1tbW1tbW1tbW1tbW19fX2dnZ3d3d4ODg4eHh4eHh4uLi4uLi5eXl5eXl5ubm5ubm5ubm6enp
6urq6+vr6+vr7Ozs7Ozs7e3t7u7u7u7u7+/v7+/v8PDw8PDw8PDw8fHx8fHx8fHx8vLy8/Pz9PT0
9fX19fX19fX19vb29/f39/f39/f3+Pj4+Pj4+Pj4+Pj4+fn5+vr6+vr6+vr6+vr6+/v7+/v7/Pz8
/Pz8/f39/f39/f39/f39/f39/f39/f39/f39/f39/f39/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+
/v7+/v7+////////////////////////////////////////////////////////AAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNMAHwkcSLCgwYNhzBxc
KBCJAwtfSGzYwvDRnRc0XBBocKPAgBqPGB1EdGTBAx0neuCYcGEGhRF0DMYBYoIHGC9vlPh4IgEA
AigF7Xj4wAXQQD1ujGQwEEFInoGFmlTgcPCKDRAKDqwY6IdJETQH92DRICAABoJLRGRZSCVEAgY5
BtaRASHJQjE7YATpM/DMkCiKFhpSUwYPQUFsEqlIUfFglxIsGhvUIsXRjxiPBlVJ05hQoDUtUDwi
04GI5Edjpsz5Y8UJnNOH+DRa1EbO6du4DwYEACH5BAgHAAAALAAAAAAUABQAh2BgYGFhYWRkZGpq
am5ubnJycnJycnJycoCAgISEhIiIiIyMjIyMjI6OjpaWlpiYmJqampycnJ2dnZ2dnZ6enqGhoaKi
oqSkpKysrK6urri4uL6+vr+/v8DAwMHBwcHBwcLCwsPDw8vLy8zMzM/Pz9DQ0NDQ0NPT09PT09TU
1NTU1NXV1dbW1tbW1tbW1tfX19jY2NnZ2dra2tra2tvb29vb29/f39/f39/f39/f3+Dg4OPj4+Pj
4+Pj4+Tk5OXl5eXl5eXl5efn5+fn5+jo6Onp6enp6enp6evr6+vr6+zs7O3t7e/v7+/v7+/v7/Dw
8PDw8PDw8PHx8fHx8fHx8fHx8fLy8vLy8vLy8vT09PT09PT09Pb29vb29vb29vf39/f39/j4+Pj4
+Pn5+fr6+vr6+vr6+vr6+vr6+vr6+vv7+/v7+/v7+/v7+/z8/Pz8/Pz8/Pz8/Pz8/Pz8/P39/f39
/f39/f39/f39/f39/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+
/v///////////////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAjVACUJHEiwoMGCkQrReYSHi5+DBQdd+WBBiIcEJCAKJBQGiY0MEFRc
KBCCCIwzBhM92bAgiJY0UnjgaKFgAAqDjJrIYMFGYCNIXUw8YOCjYJ4sJaoY1BOlyI0OMRYN3PIi
wo+Dc3pMAIAAy8AyVMAcOtiGRgUDEsQMdHTHyZeDhpaIoADizUA1RjCkOBhHhwMBBGYMlAOFCZmD
Y040CHAgB0FEdo5YMVhnyAgNLvoQdKOEQ42DfMwIMgjIC5pAcIAk0Xhwz5QVO1gbVLTmj+zbuHPr
PhgQACH5BAgHAAAALAAAAAAUABQAhy0tLS4uLi8vLzIyMjo6OklJSU9PT1FRUV1dXWhoaGlpaWlp
aWtra21tbXNzc3x8fHx8fHx8fIKCgoeHh4qKipWVlZeXl5qampqamp6enqKioqSkpKWlpaenp6en
p6enp6qqqra2tre3t7m5uby8vL29vb29vb+/v8DAwMHBwcTExMXFxcbGxsnJycrKysrKytHR0dLS
0tXV1dfX19fX19jY2Nra2tra2tzc3N3d3d3d3d3d3d7e3uDg4OPj4+Pj4+Pj4+Pj4+Tk5OXl5ebm
5ufn5+jo6Ojo6Orq6urq6urq6uvr6+vr6+zs7Ozs7O7u7vHx8fHx8fHx8fHx8fHx8fLy8vPz8/Pz
8/T09PT09PT09PT09PX19fX19fj4+Pj4+Pj4+Pj4+Pn5+fn5+fn5+fr6+vr6+vv7+/v7+/v7+/v7
+/z8/Pz8/Pz8/Pz8/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+
/v7+/v7+/v7+/v7+/v//////////////////////////////////////////////////////////
/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjVACEJHEiw
oEGCfvZAokPGS5+DBQNBcXGBx4gGMsxMQXNwUB5AT0pIwJECQgsRCDoc/AJEQ407a/DIaaMERAEM
B8H4yECj4BkpM2KQQEIw0R9EihoZVJPjQQALBMUcCZHkYJ0iHxioIBhGCIchBwlxCfJiCcFCeg5B
TKNjAgEHXQbCuWIjy8ExNyIMUKBlYBkjG34YdNPEBIUKPQgKmvOGz6KCVFAcEJDAisE4VVgQIRjl
hAEAC7YYtIMFBhOCbJys8LDj4CNGjgwaQgSxtu3buHPrrh0QACH5BAgHAAAALAAAAAAUABQAhysr
Ky0tLTQ0NDo6OlFRUVRUVFZWVlpaWlxcXFxcXFxcXF9fX2BgYGBgYGRkZGZmZmxsbHd3d3t7e39/
f4mJiYmJiZCQkJWVlZeXl52dnaioqKqqqq+vr7CwsLKysrW1tbW1tba2trm5ub+/v8HBwcHBwcHB
wcLCwsPDw8TExMfHx9HR0dHR0dLS0tPT09XV1dXV1dbW1tfX19fX19jY2Nvb29vb29zc3Nzc3N3d
3d7e3t/f39/f3+Li4uLi4uPj4+Pj4+Tk5OTk5OXl5eXl5efn5+jo6Ojo6Onp6erq6urq6uvr6+vr
6+zs7Ozs7Ozs7O3t7e3t7e3t7e7u7u7u7vDw8PLy8vPz8/Pz8/Pz8/T09PT09PT09PT09PX19ff3
9/f39/j4+Pj4+Pn5+fn5+fn5+fn5+fn5+fn5+fr6+vr6+vv7+/v7+/v7+/v7+/z8/Pz8/Pz8/Pz8
/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v//////////////////////
/////////////////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjWAB8JHEiwoEGDbrSI4XOI0UGCbLy0ybJiQgoqS9I8
FGilBQUeTDKoIKFAxMNAfu448fBE4BogF04EKYKnIBgjNdAYLAMjAoEZBcPcqIDEIB0kFhzsIFgH
zh4ueg6eERKjCSGBhrDIKBH1YBUTDRgMEcjoTQ8UeR5+YbHAgA+CihAlOjjmCA4XRPoQJBPFhpqC
gJJ8OJCARsE4UkB0IWhmig4NAwSMKOioUaFFA+384PAAAoYOWzYOlJNDAoAAG0QTFHQlRAEEL1QT
HDRHCZQ/snPr3q06IAAh+QQIBwAAACwAAAAAFAAUAIdeXl5fX19lZWVlZWVxcXFzc3N0dHR4eHh7
e3uEhISGhoaLi4uOjo6Ojo6QkJCRkZGcnJydnZ2ioqKjo6OkpKSkpKSnp6eurq6zs7O1tbW2tra7
u7u7u7u+vr7BwcHCwsLDw8PDw8PDw8PHx8fJycnKysrNzc3Nzc3Pz8/S0tLS0tLT09PU1NTU1NTV
1dXV1dXV1dXW1tbW1tbY2NjY2NjY2NjZ2dnd3d3f39/f39/g4ODh4eHi4uLi4uLl5eXm5ubm5ubo
6Ojo6Ojo6Ojp6enq6urt7e3t7e3t7e3t7e3u7u7v7+/w8PDw8PDw8PDx8fHx8fHx8fHx8fHx8fHy
8vLz8/P09PT19fX19fX29vb29vb29vb29vb39/f39/f39/f39/f4+Pj4+Pj5+fn5+fn6+vr6+vr7
+/v7+/v7+/v7+/v7+/v8/Pz8/Pz8/Pz8/Pz8/Pz9/f39/f39/f39/f39/f39/f39/f39/f39/f39
/f39/f39/f3+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7/////////////////////
//////////////////////////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAI1gAnCRxIsKDBgn7AtFkkh89BgpIOTSLDI0MLIitsCHo4CU+TIlKsgKCR5AKELIwMOiqUhwmH
EAIjDeKyA8UGIwXfOBmC5UsXgo+iiEDAouAcKh1uHCQURseTOwUbqaHzUMsLChaqDPwzRg9HMTUS
GPAxcI0SEkgemoHSIwecgYjYBPFycM+PDxNScCwICA2QCgAepNmbSFEcISpKzNAgY6+dIzhijFAg
QEKdvZOumGhAwMGCARHcYN5y4kCAAi5gLME8KdAUDwwwlGE9EJKhM31o695tMCAAIfkECAcAAAAs
AAAAABQAFACHKysrKysrNjY2Ozs7PDw8Pz8/SEhIUVFRUlJSWVlZXV1dampqc3NzdnZ2fn5+hYWF
hoaGh4eHiIiIjY2Nj4+PlpaWl5eXm5ubnZ2dnZ2doaGhpqampqamqKiora2tsbGxsrKytbW1tbW1
urq6v7+/wsLCw8PDw8PDxMTExcXFxsbGyMjIyMjIy8vLz8/Pz8/P0dHR0tLS09PT1NTU1dXV1tbW
2NjY2dnZ2tra2tra2tra29vb29vb3Nzc3d3d3t7e39/f4eHh5OTk5OTk5OTk5eXl5ubm5+fn6Ojo
6urq7Ozs7e3t7e3t7+/v8PDw8fHx8vLy8vLy8vLy8vLy8vLy8/Pz9PT09PT09fX19fX19fX19vb2
9vb29vb29vb29/f39/f39/f39/f3+fn5+fn5+fn5+fn5+fn5+vr6+vr6+vr6+vr6+/v7+/v7+/v7
+/v7+/v7/Pz8/f39/f39/f39/f39/f39/f39/f39/v7+/v7+/v7+/v7+/v7+/v7+/v7+////////
////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACMQADwkcSLCgwYJy3BCCY2UMn4MD
86zZUyVHiCU3ItA4NAhiGiQihAzpEGXKCB5BYnQ5iCcMCyYFqZRQMKOgoTl1IOrRUiNLwUBXfsCA
+EUHBxQEC8Uh4gJimR4LJNyBePAPmiRQqB4kA4SEiTNaC3p5kaCAjbACAYl5ogSEBScH6XABY+cN
mzY+MjSQAVFQkxYUJqz4cCEFAwAYIPo5okHAAAcIAkDA4cEIVSwnDhCo8MDABrR91OxQIWVLETNo
U6tenTogACH5BAgHAAAALAAAAAAUABQAh2JiYmZmZmhoaG1tbXR0dHZ2dnd3d3p6ent7e35+foSE
hIiIiImJiYyMjI6OjpSUlJaWlpaWlpeXl5mZmZ6enqioqKqqqq+vr7Kysrm5ubq6ury8vL+/v8HB
wcHBwcLCwsLCwsPDw8PDw8nJycnJycrKyszMzM3Nzc7OztTU1NXV1djY2NjY2NjY2Nra2tra2tra
2t3d3d7e3t/f39/f3+Dg4ODg4ODg4ODg4OHh4eLi4uLi4uLi4uPj4+Pj4+Xl5eXl5efn5+fn5+fn
5+jo6Onp6enp6erq6urq6uvr6+3t7e/v7/Dw8PHx8fHx8fHx8fLy8vLy8vPz8/T09PT09PX19fX1
9fX19fb29vb29vb29vb29vf39/f39/j4+Pj4+Pj4+Pn5+fn5+fn5+fn5+fr6+vr6+vr6+vv7+/v7
+/v7+/v7+/v7+/z8/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+
/v7+/v7+/v7+/v7+/v///////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjGAA8J
HEiwoEGCc7aggRNmz8GDZo5smLEjQ5IubAYdNFSHDqA1QqZEKVEkhgUaBwlVASKjoJsmHH48bIPk
xcEwQ2pQefhQSwsGHnge5APmBhOhBtMY4bEEacEvKxpIOONUoKE7WVCYyFNQjZQrcQqKCYLDiUE9
RD5AqKDkT6E4dp6IQODASkE5NigAGHABhIocJ0iweDABS0FBUDoYSBBBQAENCgKMKOPloB8yPlyE
IHAgBYYFMJwGGqOjB543XPpUXc269cOAACH5BAgHAAAALAAAAAAUABQAhywsLDg4ODk5OTw8PD8/
P0JCQklJSVxcXF1dXV1dXV9fX2VlZWhoaGlpaW5ubnFxcXV1dXV1dXl5eX5+foGBgYODg5CQkJqa
mp2dnaioqKqqqq2tra6urrGxsbKysrS0tLe3t7i4uLm5ubm5uby8vL29vcbGxsbGxsbGxsrKyszM
zM3Nzc3Nzc7Ozs/Pz8/Pz9HR0dLS0tPT09fX19vb29vb293d3d/f3+Dg4ODg4OHh4eLi4uLi4uLi
4uLi4uPj4+Xl5ebm5ubm5ufn5+fn5+jo6Onp6erq6urq6urq6urq6urq6uvr6+3t7e3t7e3t7e3t
7e7u7u7u7u/v7/Dw8PLy8vLy8vPz8/Pz8/Pz8/Pz8/T09PT09PX19fX19fb29vb29vb29vb29vb2
9vb29vj4+Pr6+vr6+vr6+vv7+/v7+/v7+/z8/Pz8/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f7+
/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v//////////////////////////////////////////////
/////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAjRABcJHCjwjhtBBBMm/LNnUZkjT+LQUZhQ0ZgrcObgwECkyBiKAxWpWXFi
ERsqYDhoCGQIpEAsUwgyuTGkCiCXFM2wmGAEJ0UpJLj4VGglBxI8BBEVOuTyi4cGSgYS8pJkyyCK
feoAERFmYBoaGSqgSKSwiw4neQiikXEAgIImBPnYyTJiQQuCfqBAGPCgBI83bexE+aGlhoQYCoN0
uGAAgYoZQmxYiNBDjh6Ka0IEKLDBQQIYFASYwCnmA4gdDAi8WJKCzFCBPlyceU27tm2cAQEAIfkE
CAcAAAAsAAAAABQAFACHKioqLy8vMDAwQ0NDSUlJTExMUlJSWlpaW1tbXFxcX19fYmJiZGRkaGho
d3d3fHx8fHx8fHx8hISEhYWFiYmJiYmJjo6OkZGRkZGRnZ2dn5+foaGhoaGhqKioqamprKysra2t
sLCwtra2t7e3urq6v7+/v7+/wcHBwcHBwcHBxMTExcXFxsbGycnJzs7Oz8/Pz8/P0tLS0tLS09PT
09PT09PT19fX19fX2dnZ29vb3d3d3d3d3d3d4ODg4eHh4eHh5OTk5eXl5eXl5eXl5ubm5+fn5+fn
6Ojo6urq6urq6+vr7Ozs7Ozs7e3t7u7u7+/v7+/v8PDw8PDw8vLy9PT09PT09PT09fX19fX19vb2
9vb29/f39/f39/f39/f39/f3+Pj4+Pj4+fn5+fn5+fn5+fn5+fn5+/v7+/v7+/v7/Pz8/Pz8/Pz8
/Pz8/Pz8/f39/f39/f39/f39/f39/f39/f39/f39/f39/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+
/v7+////////////////////////////////////////////////////////////////AAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACNMAIQkcCImRoUaQHD0i
yJBhGip2BGUR07AiJDZDSJiZkiKHxYZedLwh5ILGmI8W/zwZIQNlw0J4SrxgOEgOnUUfuSwpQ1BL
DxxOFFm8ouJCFYGAjIRQ0IDHxx8gtggM1MRCAAEfKvqBwqQNwTssEjCAUXFPEg0Z4hAEs4KCgxkE
Eak5k0fEBjcE0dQwAKAClj5z1tQpEgOIHj4MD1nBcICDBxNBbhBBImFBFItkjpwYQAAFBAQ7WnQI
8zGRkgcRhEwoYMPlwC9dIEnxAce17du4bQcEACH5BAgHAAAALAAAAAAUABQAh19fX2NjY2ZmZmtr
a3V1dXZ2dnl5eX19fX5+foCAgIGBgYuLi5OTk5eXl5eXl5mZmZycnJycnKCgoKGhoaGhoaKioqmp
qampqaqqqqurq6+vr6+vr6+vr7GxsbOzs7i4uLm5ubq6urq6ur29vb29vcLCwsvLy8zMzMzMzM3N
zdTU1NfX19fX19jY2NnZ2dra2tra2tvb29zc3N3d3d3d3d/f3+Dg4OHh4eHh4eHh4eHh4eLi4uLi
4uPj4+Tk5OTk5OXl5ebm5ubm5ufn5+rq6uvr6+vr6+zs7Ozs7O7u7u7u7u7u7u/v7/Dw8PDw8PHx
8fLy8vLy8vLy8vPz8/Pz8/Pz8/Pz8/Pz8/T09PX19fb29vb29vf39/f39/j4+Pr6+vr6+vr6+vr6
+vr6+vr6+vr6+vr6+vv7+/v7+/z8/Pz8/Pz8/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f39
/f39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v//////////////////////////////
/////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAjSABkJHEgQEaBDBBMqFKgGy52FEAXOATKkUBg9ChP9GaSwxws3RbQk
XLQliJE1EGeUAERQjg0QG3xAhCLDDME9KxAEiJBmIZocOwwR1GFAAAMyEFl0iEPwSAYHMCDycfKE
oJ8fFRScgHjmBo8+BJEkACChjkJBgVw0uELQTogFIpokVDSFiBUcbRKWUfGAg5Qsedh4wZOEBA2I
MQYQMIFiiZIWUcZA+ACxi4cRKQ5cYEJBA50qXCISYlSjwAQwGCy8iUgQjhAqjL6IYU27tu3bCwMC
ACH5BAgHAAAALAAAAAAUABQAh2FhYWFhYWJiYmdnZ2hoaHJycnZ2dnt7e3x8fIaGhoiIiIiIiIiI
iJWVlZaWlpiYmJqampqampycnJ6enqOjo6ampqioqKmpqaqqqqysrLCwsLKysrS0tLW1tbe3t7m5
ubm5ub29vcjIyMvLy8/Pz9DQ0NHR0dLS0tLS0tPT09PT09TU1NTU1NXV1dXV1dfX19jY2NjY2NnZ
2dvb29zc3N3d3d3d3d7e3t/f3+Dg4ODg4OHh4eTk5OTk5OTk5Obm5ufn5+fn5+jo6Onp6enp6erq
6urq6urq6uzs7Ozs7O3t7e7u7u/v7/Dw8PHx8fHx8fHx8fHx8fLy8vPz8/T09PT09PX19fX19fX1
9fX19fb29vb29vf39/f39/f39/f39/f39/j4+Pn5+fn5+fr6+vr6+vr6+vr6+vv7+/v7+/z8/Pz8
/Pz8/Pz8/Pz8/P39/f39/f39/f39/f39/f39/f7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v//
/////////////////////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAjPABMJHEiwoMGB
hgQdLHToYKI3TpCAIURwjxcyDp+I6EBDDsFBQoo4/KGAgIQxBWvI0LMmUMEbBgIw+FKQjx8sTOYQ
rFJigoMVDpWEEENwSAMEIxwmohIjDcEeBQBwUAoliBuCYTQ8wKEUiIUsBOG8uMAij0FEaJroaFPQ
gwAIWq4S/JMkhxqDJhJsUGEET5w+dracsRFBisE6XFos+HDFh5UyM3hEOWHGIYkBFI5kgHEHQwU6
ShN1SbGEyAEQiVygABR6IJsdU1rLnk27NsGAADs=
"""


class FindThread(Thread):
    def __init__(self, app, init_dir, file):
        super().__init__()
        self.app = app
        self.stop = False
        self.init_dir = init_dir
        self.file = file
        # self.result = result
        return

    def run(self):
        throbber_thread = ThrobberThread(self.app.throbber_label, throbber_gif)
        throbber_thread.start()
        matches = []
        for root, dirnames, filenames in os.walk(self.init_dir):
            # print(root, filenames)
            for filename in fnmatch.filter(filenames, self.file):
                if "firefox" in root.lower():
                    matches.append(os.path.join(root, filename))
    
        throbber_thread.stop = True
        throbber_thread.join()
        if len(matches) != 1:
            info = "%s fichiers trouvé(s)\n" % len(matches)
            for f in matches:
                info = info + f + "\n"
            messagebox.showinfo(message=info)
        else:
            self.app.webappsstore_text.delete(0, tk.END)
            self.app.webappsstore_text.insert(0, matches[0])
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
        self.webappsstore_auto_button = tk.Button(self.frame_webappsstore, text="find auto", command=self.on_webappsstore_auto_button_clicked)
        self.webappsstore_auto_button.pack(side=tk.LEFT, padx=5, pady=5)
        # photo = tk.PhotoImage(data=throbber_gif, format="gif -index 4")
        self.throbber_label = tk.Label(self.frame_webappsstore)
        # self.throbber_label.photo = photo
        self.throbber_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.throbber_label.pack_forget()

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
        find_thread = FindThread(self,os.path.expanduser("~"), "webappsstore.sqlite")
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
