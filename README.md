# Orderrapportering

Det här är min individuella uppgift i Fördjupning i Pythonprogrammering.
Jag har refaktorerat ett befintligt program som läser orderdata från
en CSV-fil och skapar rapporter över försäljning och returer.

Målet har varit att förbätttra kodens struktur, felhantering och
testbarhet utan att ändra rapporternas beräkningar.

## Installation

Projektet är utvecklat och testat med Python 3.12.9 på Windows.
Programmet använder pandas och testerna använder pytest.
Paketversionerna och deras beroenden finns i `requirements.txt`.

Klona projektet och gå till projektmappen:

```powershell
git clone https://github.com/SoroushGReza/order-report-project.git
cd order-report-project
```

Skapa en virtuell miljö och installera beroendena:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Kommandona nedan körs från projektets rotmapp. De använder miljöns
Python direkt, så miljön behöver inte aktiveras i PowerShell.

## Kör programmet

```powershell
.\.venv\Scripts\python.exe order_report.py
```

Programmet läser `data/orders.csv` och sparar fyra rapporter i `output`:

| Fil                       | Innehåll                                          |
| ------------------------- | ------------------------------------------------- |
| `overview.csv`            | Total försäljning, antal ordrar och antal returer |
| `sales_by_category.csv`   | Försäljning och returer per produktkategori       |
| `sales_by_region.csv`     | Försäljning och returer per region                |
| `returns_by_category.csv` | Antal returer och returandel per produktkategori  |

Utdatamappen skapas automatiskt om den saknas.
Sökvägarna utgår från startfilens plats.

Körsinformation visas med logging. Varningar visar när saknade eller
ogiltiga värden ersätts. Vid ett hanterat fel avslutas programmet
med avslutningskod 1, annars med 0.

## Data och beräkningar

Datasetet innehåller 80 orderrader. Originalets regler är bevarade:

- Ordervärde beräknas som quantity × unit_price.
- Rabatterat värde beräknas som ordervärde × (1 − discount).
- Försäljningen inkluderar även returnerade ordrar.
- Antalet ordrar räknas som unika order_id.
- Antalet returer räknas som rader där returned är sant.
- Returandelen är antalet returer delat med antalet unika ordrar
  i respektive grupp.

Regioner och productkategorier normaliseras genom att ta bort
omgivande blanksteg och justera stora och små bokstäver.
Saknade värden i dessa kolumner blir `Unknown`.

Saknad eller ogiltig quantity ersätts med 1, unit_price med
medianpriset och discount med 0. Returvärdena `true`, `yes`,
`1` och `ja` räknas som sanna efter normalisering.
Övriga värden, inklusive saknade, räknas som falska.

Programmet stoppar vid bland annat saknade obligatoriska kolumner,
tom data, quantity som är högst 0, negativa priser, rabatter
utanför intervallet 0–1 och oändliga numeriska värden.
Det stoppar också om inget giltigt pris finns för att beräkna medianen.

Resultatet för det medföljande datasetet är:

| Mått                           |  Resultat |
| ------------------------------ | --------: |
| Total försäljning efter rabatt | 138036.05 |
| Antal ordrar                   |        80 |
| Antal returer                  |        15 |

## Kör testerna

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Projektet innehåller 13 testfall. De kontrollerar beräkningar,
datarensning, validering och att de fyra rapporterna motsvarar
de sparade originalrapporterna.

## Projektstruktur

| Fil eller mapp                     | Ansvar                                                   |
| ---------------------------------- | -------------------------------------------------------- |
| `order_report.py`                  | Startpunkt, logging, filinläsning, körflöde och sparande |
| `order_reporting/config.py`        | Dataclass för indatafil och utdatamapp                   |
| `order_reporting/processing.py`    | Datarensning och beräkning av ordervärden                |
| `order_reporting/reporting.py`     | Sammanställning av rapporter                             |
| `order_reporting/validation.py`    | Kontroll av kolumner och datavärden                      |
| `order_reporting/__init__.py`      | Markerar mappen som ett Pythonpaket                      |
| `data/orders.csv`                  | Datasetet från uppgiften                                 |
| `tests/`                           | Automatiska tester                                       |
| `tests/fixtures/original_reports/` | Sparade rapporter från originalprogrammet                |
| `output/`                          | Genererade rapporter                                     |
| `code_review.md`                   | Granskning av originalkoden                              |
| `requirements.txt`                 | Pythonberoenden och versioner                            |

## Reflektion

### 1. Vilka var de viktigaste problemen i originalkoden?

Flera olika ansvar låg direkt i samma fil och hela programmet
startade vidd import. Rapportkoden innehöll också upprepningar,
felmeddelandena var otydliga och automatiska tester saknades.

### 2. Vilka förändringar förbättrade programmet mest?

Jag tycker att uppdelningen i funktioner och moduler gjorde störst
skillnad. Det blev lättare att se vad varje del gör och att testa
bearbetningen utan att behöva läsa och skriva filer. Den gemensamma
funktionen för kategori- och regionrapporter minskade också dupliceringen.

### 3. Varför valde jag den här projektstrukturen?

Jag delade upp bearbetning, rapporter, vallidering och konfigration
eftersom de har olika ansvar. Startfilen håller ihop körningen
och sköter filhanteringen. För ett så här litet program tyckte jag
att det räckte, utan att skapa fler moduler än vad som behövdes.

### 4. Var använde jag OOP/dataclass och varför?

Jag använde dataclass i `ReportConfig` för att samla indatafilen
och utdatamappen i ett objekt. Det gör inställningarna tydliga.
Jag valde `frozen=True` för att de inte ska ändras av misstag
efter att objektet har skapats.

### 5. Vilka beteenden skyddar testerna och vilken nytta ger de?

Testerna kontrollerar ordervärden, rabatter, returvärden och
ersättning av saknade eller inkonsekventa värden. De kontrollerar
också att valideringen upptäcker bland annat saknade kolumner,
tom data och orimliga numeriska värden.

De fyra rapporttesterna jäämför resultatet med originalrapporterna
för datasetet. Om jag ändrar koden i framtiden kan testerna upptäcka
om värden, kolumner eller radordning förändras av misstag.
Testerna täcker inte alla möjliga indata, men de skyddar flera
viktiga beteenden.

### 6. Vad var svårast?

Det svåraste var att följa hur koden flyttades mellan filerna.
När startfilen blev mycket kortare behövde jag förstå att
funktionaliteten fanns kvar i de andra modulerna. Jämförelsen
med originalrapporterna hjälpte mig att kontrollera det.

### 7. Vad hade jag velat förbättra med mer tid?

Jag hade velat lägga till fler tester för filhanteringen,
till exempel när indatafilen saknas eller en rapport inte
går att spara. Jag hade också velat göra det möjligt att
välja indatafil via ett kommandoradsargument.
