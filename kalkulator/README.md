# Kalkulator

Der Kalkulator erlaubt es, mathematische Ausdrücke zu fomulieren.
Er unterstützt im Augenblick nur die vier Grundrechenarten, 
erlaubt aber die Eingabe in der gewohnten Python-Syntax, also z. B.
Benutzung von Variablen und Klammersetzung.

Er rechnet grundsätzlich mit Vektoren, Berechnungen mit einfachen Zahlen
sind trotzdem möglich, diese Zahlen werden automatisch als eindimensionale
Vektoren dargestellt.

Der Kalkulator berechnet nicht nur das Ergebnis eines mathematischen
Ausdrucks sondern dokumentiert auch den Rechenweg, in der Ausgabedate
in einem JSON-Format und als grafische Darstellung der mathematischen
Ausdrücke im Unterverzeichnis `data`.

Hinweis: Der Kalkulator ist ein Anwendungsbeispiel einer internen DSL.

## Vorbereitung

Alle Anweisungen hier sind als Kommandos in einer Unix-Shell-Umgebung
anzuwenden, also z. B. in einem Terminal unter Linux oder MacOS oder
in einer Git bash unter Windows.

### Voraussetzungen

- Python 3 ist installiert (https://www.python.org/downloads/)
- Git-Client ist installiert (https://git-scm.com/downloads)
- GitHub-Account ist angelegt und SSH-Key ist bei GitHub hinterlegt (https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

### Clonen des Repositories

```shell
git clone git@github.com:igeldo/MPKurs.git
```

Es ist ein neues Verzeichnis mit dem Namen `MPKurs` entstanden.

Wechsel in das Verzeichnis und Abfrage des Status mit
```shell
cd MPKurs/kalkulator
git status
```
sollte ungefähr folgende Ausgabe ergeben:
```shell
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### Einrichten des virtual environment 

Einmalig wird die virtuelle Umgebung für das Projekt eingerichtet:
```shell
python3 -m venv kalk_venv
source kalk_venv/bin/activate
python -m pip install -r requirements.txt
```

## Starten des Programms

### Wechsel in virtual environment

Für jede neu geöffnete Shell muss einmalig in die virtuelle Umgebung geechselt werden:
```shell
cd <pfad_zu_MPKurs>/kalkulator
source kalk_venv/bin/activate
```

### Ausführen des Programms

```shell
python main.py data/input.json data/output.json
```




