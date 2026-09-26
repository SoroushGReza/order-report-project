# Kodgranskning

Jag har kört originalprogrammet med den medföljande filen
`orders.csv` och gått igenom koden i `order_report.py`.
Programmet läste in 80 rader och skapade fyra rapporter.
Sammanfattningen visade en försäljning på 138036.05,
80 ordrar och 15 returer.

Här beskriver jag de förbättringsområden som jag hittade.

## 1. Flera olika ansvar i samma fil

**Observation:** Hela programmet ligger i `order_report.py`.
Koden läser in filen, kontrollerar kolumner, bearbetar data,
beräknar resultat och sparar rapporter.

**Konsekvens:** Det blir svårt att få en överblick och att
testa en dell av programmet separat. Exempelvis går det inte
att enkelt testa beräkningarn utan att även köra filhanteringen.

**Förslag:** Jag vill dela upp koden i funktioner och moduler
med tydliga ansvar för inläsning, validering, bearbetning och
rapportering.

## 2. Programmet startar direkt vid import

**Observation:** Koden ligger direkt i filen och saknar en
main()-funktion och en kontroll med `if __name__ == "__main__":`.

**Konsekvens:** Om jag importerar filen för att använda eller
testa en del av koden körs hela programmet. Då läses data in
och rapporter sparas även om det inte var avsikten.

**Förslag:** Jag vill lägga programmets körflöde i en
main()-funktion och använda `if __name__ == "__main__":`
för att styra när programmet ska starta.

## 3. Samma rapportlogik uppprepas

**Observation:** Koden för försääljning per produktkategori
och per region är nästan likadan. Båda delarna räknar ordrar,
summerar försäljning och returer samt beräknar returandel.

**Konsekvens:** Om beräkningarna behöver ändras måste samma
ändring göras på flera ställen. Det finns risk att bara en
av rapporterna kommer uppdateras.

**Förslag:** Jag vill använda en gemensam funktion där
grupperingskollumnen skickas in som argument.

## 4. Några variabelnamn är otydliga

**Observation:** Variablerna `result1` och `result2` används
för rapporterna per produktkategori och region.

**Konsekvens:** Namnen förklarar inte vad variablerna innehåller.
Jag behöver läsa koden runt dem för att förstå vilken rapport
det handlar om.

**Förslag:** Jag vill byta till tydligare namn, till exempel
`sales_by_category` och `sales_by_region`.

## 5. Print används för körinformation

**Observation:** Programmet använder print() för att visa
att körningen startar, hur många rader som lästs in, vilka
filer som sparats och om något gått fel.

**Konsekvens:** Vanlig körinformation, varningar och fel
saknar tydliga loggnivåer. Det är också svårt att styra
hur mycket information programmet ska visa.

**Förslag:** Jag vill ersätta dessa utskrifter med logging.
Konfigurationen ska ligga centralt och varje modul ska
använda `logging.getLogger(__name__)`.

## 6. Felhantering och validering behöver bli tydligare

**Observation:** Nästan hela programmet ligger i ett brett
try/except som fångar Exception. Om obligatoriska kolumner
saknas visas bara meddelandet "Fel data".

Saknade och ogiltiga värden ersätts utan någon
varning. Till exempel blir rabatten `unknown` i datasetet
ersatt med 0. Det saknas kontroller för tom data, negativa
priser och rabatter utanför intervallet 0–1.

**Konsekvens:** Det blir svårt att förstå vad som är fel
och vilka värden som har ersatts. Orimliga värden kan också
påverka rapporterna utan att användaren märker det.

**Förslag:** Jag vill ge tydliga felmeddellanden som beskriver
problemet, exempelvis vilka kolumner som saknas. Jag vill
också kontrollera tom data och orimliga numeriska värden.
Originalets ersättningsregler för den medföljande datan ska
bevaras, men programmet ska logga när värden ersätts.
Felhanteringen ska fånga förväntade fel utan att dölja
andra problem.

## 7. Automatiska tester saknas

**Observation:** Originalprojektet har inga automatiska tester
för beräkningar, rapporter eller validering.

**Konsekvens:** När jag ändrar koden är det svårt att veta
om resultaten fortfarande stämmer utan att kontrollera
allt manuellt.

**Förslag:** Jag vill lägga till tester med pytest för bland
annat ordervärde, rabatt, returer och sammanställningar.
Jag vill också testa felscenarier, exempelvis saknade
obligatoriska kolumner och tom data. De sparade
originalrapporterna kan användas för att kontrollera att
refaktoreringen ger samma resultat för datasetet.

## Fokus för refaktoreringen

Jag vill göra programmet tydligare och lättare att testa
utan att ändra rapporternas beräkningar eller betydelse.
Till exempel inkluderar originalets försäljningssumma även
returnerade ordrar, medan antalet returer redovisas separat.
Det beteendet ska finnas kvar efter refaktoreringen.