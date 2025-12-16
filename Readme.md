# Alterspflege Report Templates für Liten

Dieses Paket enthält umfassende Report-Templates für die stationäre Alterspflege, strukturiert nach dem Liten-Template-Format.

## Struktur

Das Template-System ist in **9 Hauptkategorien** mit insgesamt **46 Aktionen** organisiert:

### 1. Morgenroutine (8 Aktionen)
- Bewohner wecken
- Beim Aufstehen unterstützen
- Körperpflege durchführen
- Beim Anziehen helfen
- Kämmen und Frisieren
- Mund- und Zahnhygiene
- Rasieren
- Zum Frühstück bringen

### 2. Mahlzeiten (7 Aktionen)
- Frühstück herrichten
- Beim Essen unterstützen
- Nahrungsaufnahme dokumentieren
- Mittagessen vorbereiten
- Zwischenmahlzeiten anbieten
- Abendessen servieren
- Diäten berücksichtigen

### 3. Medizinische Versorgung (6 Aktionen)
- Medikamente verabreichen
- Vitalzeichen messen
- Wundversorgung durchführen
- Inkontinenzversorgung
- Lagerung durchführen
- Physiotherapeutische Übungen

### 4. Mobilisation und Aktivierung (5 Aktionen)
- Mobilisieren
- Zu Aktivitäten begleiten
- Spaziergang durchführen
- Beschäftigungsangebote
- Soziale Kontakte fördern

### 5. Hygiene und Hauswirtschaft (5 Aktionen)
- Betten machen
- Zimmer aufräumen
- Wäsche verteilen
- Desinfektion durchführen
- Lüften

### 6. Dokumentation und Organisation (3 Aktionen)
- Pflegedokumentation aktualisieren
- Übergabebericht schreiben
- Zustandsänderung melden

### 7. Abendroutine (5 Aktionen)
- Ausziehen und Nachtkleidung anziehen
- Abendpflege durchführen
- Zu Bett bringen
- Nachtlagerung
- Verabschiedung

### 8. Nachtdienst (4 Aktionen)
- Kontrollrundgang
- Nächtlicher Toilettengang
- Schlafstörung behandeln
- Besondere Vorkommnisse dokumentieren

### 9. Kommunikation (3 Aktionen)
- Mit Bewohnern kommunizieren
- Angehörigenkontakt
- Koordination mit Ärzten

## Features

- **Mehrsprachig**: Alle Templates unterstützen Deutsch (de), Englisch (en) und Norwegisch Bokmål (nb)
- **Strukturierte Properties**: Jede Aktion enthält relevante Eingabefelder wie:
  - Select/Multiselect für vordefinierte Optionen
  - Number-Felder für Messwerte
  - Time/Datetime für Zeitangaben
  - Textarea für Freitexteingaben
  - Media-Felder für Fotos (z.B. Wundfotos)
  - Checkbox für Ja/Nein-Angaben
  - Slider für Bewertungen

- **Praxisnah**: Basierend auf realen Pflegeabläufen in der stationären Alterspflege
- **BESA-kompatibel**: Orientiert am BESA LK2020 Leistungskatalog
- **Flexibel**: Einfach anpassbar und erweiterbar

## Verwendung

1. Kategorien befinden sich als JSON-Dateien im `report/`-Ordner
2. Aktionen befinden sich in Unterordnern nach Kategorien organisiert
3. Jede Datei kann direkt in das Liten-System importiert werden

## Dateistruktur

```
report/
├── morgenroutine.json
├── morgenroutine/
│   ├── wecken.json
│   ├── aufstehen.json
│   └── ...
├── mahlzeiten.json
├── mahlzeiten/
│   ├── fruehstueck-herrichten.json
│   └── ...
└── ...
```

## Anpassung

Die Templates können einfach angepasst werden:
- Neue Properties hinzufügen
- Optionen erweitern
- Sprachen ergänzen
- Kategorien/Aktionen hinzufügen

## Version

Version 1.0 - Erstellt am 16. Dezember 2024

## Lizenz

Für die Verwendung mit Liten
