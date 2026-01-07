# BESA LK2020 Pflege-Rapport Template

## Übersicht

Dieses Template basiert auf dem **BESA Leistungskatalog 2020** (LK2020) und dient der täglichen Dokumentation von Pflegeleistungen in der stationären Alterspflege. Es entspricht den Anforderungen gemäss KLV Art. 8b Absatz 2.

## Datei

- **Dateiname:** `besa_lk2020_pflege_rapport.json`
- **Version:** 2.0.0
- **Sprachen:** Deutsch (de), Englisch (default)

## Struktur

### Objekteigenschaften

Das Template definiert folgende Objekteigenschaften für Bewohner:

| Eigenschaft | Typ | Beschreibung |
|-------------|-----|--------------|
| `bewohner_name` | Text | Name des Bewohners/der Bewohnerin |
| `zimmer` | Text | Zimmernummer |
| `station` | Dropdown | Station/Abteilung (A, B, C) |

---

## Kategorien und Aktivitäten

### 1. Morgenpflege (MP 3.2.1)
*Farbe: Orange (#f59e0b)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Wecke Bewohner/in | Stimmung beim Aufwachen |
| Führe Teilkörper-Morgentoilette durch | Unterstützungsgrad, Bereiche, Hautkontrolle |
| Führe Ganzkörper-Morgentoilette durch | Unterstützungsgrad, Durchgeführte Tätigkeiten |
| Führe Mundpflege durch | Unterstützungsgrad, Art (Zähne/Prothese/etc.) |
| Rasiere Bewohner/in | Methode |
| Kleide Bewohner/in an | Unterstützungsgrad, Spezielle Hilfsmittel |

---

### 2. Baden/Duschen (MP 3.2.1)
*Farbe: Blau (#3b82f6)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Dusche Bewohner/in | Unterstützungsgrad, Inkl. Tätigkeiten, Hilfsmittel |
| Bade Bewohner/in | Unterstützungsgrad, Badeart |
| Wasche Haare separat | Methode |

---

### 3. Hand- und Fusspflege (MP 3.2.1)
*Farbe: Violett (#8b5cf6)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Führe Handpflege durch | Tätigkeiten (Nägel, Eincremen) |
| Führe Fusspflege durch | Tätigkeiten, Diabetiker-Fusspflege |

---

### 4. Mobilisation (MP 2.2.1)
*Farbe: Grün (#10b981)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Lagere im Bett um | Position, Hilfsmittel, Dekubitusprophylaxe |
| Lagere im Sessel/Stuhl um | Unterstützungsgrad |
| Transferiere von/zu Bett | Richtung, Hilfsmittel, Anzahl Pflegende |
| Setze Patientenheber ein | Transferart |
| Begleite zur Toilette | Unterstützungsgrad, Hilfsmittel |
| Begleite zum Essen | Mahlzeit, Hilfsmittel |
| Begleite bei der Fortbewegung | Hilfsmittel, Ziel |
| Führe Bewegungsübungen durch | Art, Ort |
| Führe Geh-/Krafttraining durch | Art |
| Mobilisiere mit Standing/Stehbrett | Dauer |
| Bringe Orthese/Prothese an oder entferne sie | Aktion, Art |
| Ziehe Kompressionsstrümpfe an/aus | Aktion, Art |

---

### 5. Essen und Trinken (MP 4.2.1)
*Farbe: Orange (#f97316)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Bereite Mahlzeit vor | Tätigkeiten |
| Fordere zum Essen/Trinken auf | Art |
| Unterstütze beim Essen | Unterstützungsgrad, Mahlzeit, Gegessene Menge |
| Unterstütze beim Trinken | Unterstützungsgrad, Menge (ml) |
| Verabreiche Nährlösung via PEG-Sonde | Menge, Art |
| Führe Schlucktraining durch | Dauer |
| Übe Benutzung von Esshilfen | Hilfsmittel |
| Führe Zimmerservice durch | Mahlzeit, Grund |

---

### 6. Kontinenzversorgung (MP 3.2.2)
*Farbe: Cyan (#06b6d4)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Reinige nach Darmentleerung/Toilettengang | Unterstützungsgrad |
| Wechsle Inkontinenz-Einlage | Produktart, Grund |
| Reiche Bettschüssel/Urinflasche | Art |
| Lege Katheter ein/wechsle ihn | Aktion, Art |
| Pflege Urinalsystem | Tätigkeiten |
| Versorge Stoma | Tätigkeit, Stoma-Art |
| Verabreiche Einlauf/Klistier | Art |
| Führe digitales Ausräumen durch | - |
| Führe Toilettentraining durch | Art |

---

### 7. Abendpflege (MP 3.2.1)
*Farbe: Indigo (#6366f1)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Führe Abendtoilette durch | Umfang, Unterstützungsgrad |
| Kleide Bewohner/in aus | Unterstützungsgrad, Entfernte Hilfsmittel |
| Ziehe Nachtwäsche an | Unterstützungsgrad |
| Bringe ins Bett | Schlafposition, Hilfsmittel, Transfermethode |
| Richte Bett her | Tätigkeiten |

---

### 8. Medikation (MP 5.2.1)
*Farbe: Rot (#ef4444)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Verabreiche orale Medikation | Zeitpunkt, Verabreichung |
| Appliziere transdermales Pflaster | Aktion |
| Verabreiche Augen-/Ohren-/Nasentropfen | Art |
| Trage rezeptpflichtige Salbe auf | Körperbereich |
| Verabreiche Injektion | Applikationsart, Art |
| Bereite Infusion vor und überwache sie | Tätigkeit |
| Erfasse Schmerzen | Schmerzskala (0-10) |
| Messe Vitalzeichen | Messungen |
| Bringe Wickel/Kompresse an | Art (warm/kalt) |
| Führe Bluttest durch | Art |
| Führe Urintest durch | Art |

---

### 9. Wundversorgung (MP 5.2.2)
*Farbe: Dunkelrot (#dc2626)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Versorge Wunde (bis 10 Min.) | Wundart, Durchgeführte Aktionen |
| Versorge Wunde (10-30 Min.) | Wundart |
| Versorge Wunde (30-60 Min.) | Wundart |
| Führe Haut-/Schleimhautkontrolle durch | Kontrollierte Bereiche, Befund |

---

### 10. Atmung und Sauerstoff (MP 5.2.3)
*Farbe: Hellblau (#0ea5e9)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Verabreiche und überwache Inhalation | Gerät |
| Unterstütze beim Abhusten | Effektivität |
| Sauge Sekrete ab | Weg |
| Pflege Trachealkanüle | Tätigkeiten |
| Verabreiche Sauerstoff | Gerät, Flussrate |
| Übe Benutzung von Inhalationsgeräten | - |

---

### 11. Psychogeriatrische Pflege (MP 1.2.1 - 1.2.3)
*Farbe: Lila (#a855f7)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Gebe Orientierungshilfe | Art (zeitlich, örtlich, Person, situativ) |
| Begleite wegen Desorientierung | Ziel |
| Führe Gedächtnistraining durch | Art |
| Leiste emotionalen Beistand | Grund, Intervention |
| Plane individuelle Tagesstruktur | - |
| Verhindere Selbstgefährdung | Massnahmen |
| Bringe Fixierung an/entferne sie | Aktion, Art |
| Unterstütze bei sozialen Kontakten | Tätigkeiten |
| Kontrolliere Stimmungslage | Stimmung |

---

### 12. Nachtkontrollen
*Farbe: Dunkelblau (#1e3a8a)*

| Aktivität | Eigenschaften |
|-----------|---------------|
| Führe Nachtkontrolle durch | Schlafstatus, Durchgeführte Versorgung |
| Unterstütze bei nächtlichem Toilettengang | Methode |

---

## Eigenschaftstypen

Das Template verwendet folgende Eigenschaftstypen:

| Typ | Beschreibung | Beispiel |
|-----|--------------|----------|
| `radio` | Einzelauswahl | Unterstützungsgrad |
| `checkbox` | Mehrfachauswahl | Durchgeführte Tätigkeiten |
| `number` | Zahlenwert mit Einheit | Menge (ml), Dauer (min) |

---

## BESA Massnahmenpakete (MP)

Das Template deckt folgende BESA Massnahmenpakete ab:

| MP | Bezeichnung | Pflegethema |
|----|-------------|-------------|
| 1.2.1 | Gedächtnis und Orientierung | Psychogeriatrische Leistungen |
| 1.2.2 | Affektregulierung und Impulskontrolle | Psychogeriatrische Leistungen |
| 1.2.3 | Sozialverhalten und Integration | Psychogeriatrische Leistungen |
| 2.2.1 | Mobilität, Motorik, Sensorik | Mobilität, Motorik und Sensorik |
| 3.2.1 | Kompensation der Selbstpflegefähigkeit | Körperpflege |
| 3.2.2 | Kontinenz und Kompensation der Inkontinenz | Körperpflege |
| 4.2.1 | Nahrungs- und Flüssigkeitsaufnahme | Essen und Trinken |
| 5.2.1 | Medikation und Schmerzmanagement | Medizinische Pflege |
| 5.2.2 | Wund- und Hautversorgung | Medizinische Pflege |
| 5.2.3 | Atmung und Sauerstoffversorgung | Medizinische Pflege |

---

## Import

1. Öffnen Sie die Anwendung
2. Navigieren Sie zu **Settings > Templates**
3. Wählen Sie **Import Template**
4. Laden Sie die Datei `besa_lk2020_pflege_rapport.json`

---

## Lizenz & Quelle

- **Basiert auf:** BESA Leistungskatalog 2020 (Version 1 | 2020)
- **Herausgeber:** BESA Care / BESAQSys
- **Rechtliche Grundlage:** KLV Art. 8b Absatz 2

---

## Changelog

### Version 1.0.0 (2025-01-07)
- Initiale Version
- 12 Kategorien mit 77 Aktivitäten
- Vollständige Abdeckung der BESA MP 1.2.1 bis 5.2.3
- Zweisprachig (DE/EN)