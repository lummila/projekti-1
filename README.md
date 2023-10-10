# VELKAJAHTI / CHASE THE RAT

Ennen pelausta, tee seuraavat toimenpiteet:

- Asenna velkajahti.sql MariaDB-tietokannan lähdetiedostona.
- Avaa main.py
-- Rivillä 37 on muuttuja 'admin_database_name', oletuksena "velkajahti". VAIHDA TÄMÄ ASENTAMASI TIETOKANNAN NIMEEN!
-- Rivillä 38 on muuttuja 'admin_root_passcode'. VAIHDA TÄMÄ SIIHEN SALASANAAN, JOKA SINULLA ON ROOT-KÄYTTÄJÄLLÄ MARIADB:SSÄ! (Suositeltu.)

HUOM PYCHARMIN KÄYTTÄJÄ:
Pycharm ei automaattisesti simuloi Windowsin terminaalia. Peli käyttää ahkerasti os.system("cls") -komentoa, ja tämä ei automaattisesti toimi Pycharmissa.

Seuraa näitä ohjeita:
- Avaa "Run/Debug configurations" -valikko (yläpalkissa oikealla, "Current file")
- Current file kohdasta valitse alivalikko (kolme pistettä jonossa)
- "Run with parameters"
- "Modify options"
- Valitse Python kohdasta "Emulate terminal in output console".
- Apply & Run
