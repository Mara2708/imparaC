1. Avviare MongoDB 
Cmd ammministratore; net start MongoDB

2. Importare il database (da backup_mongo o JSON) (ANCHE SE IN REALTà SE è INSTALLATO MONGODB NON C'è NE BISOGNO PERCHE LO CREA AUTOMATICAMENTE IL DB)
Aprire; MongoDB; Connettersi a mongodb://localhost:27017
Creare un database chiamato imparaC_db;
Creare due collezioni utenti e risultati;
In ciascuna collezione cliccare su Import Data;
Importare utenti.json e risultati.json da questa cartella;

3. Eseguire "python app.py"
Aprire il terminale nella cartella progetto 
cd Desktop, cd imparaC, python app.py

4. Aprire http://127.0.0.1:5000 nel browser
copiare dal terminale e incollare nel browser
