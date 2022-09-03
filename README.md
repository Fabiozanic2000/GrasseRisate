# GRASSERISATE
##### Social per ridere un po' di più



## Istruzioni per l'installazione delle dipendenze e l'utilizzo
#### ATTENZIONE: PER L'UTILIZZO DI QUESTO PROGETTO OCCORRE AVERE PYTHON 3.10.5
- Per installare le dipendenze entrare nella cartella e tramite riga di comando eseguire i seguenti comandi:
```
git clone https://github.com/Zanicus2000/GrasseRisate.git
pipenv shell
pipenv install
```
- A questo punto, eseguire il comando:
```
python manage.py runserver
```
- Se e dipendenze erano già state installate in precedenza, allora eseguire soltanto i seguenti comandi (sempre all'interno della cartella):
```
pipenv shell
python manage.py runserver
```

Il sito è accessibile tramite qualsiasi browser all'indirizzo 127.0.0.1:8000

## Test
Se si vogliono eseguire i test (dopo aver installato le dipendenze) lanciare al posto dell'ultimo comando quest'altro comando:
```
pipenv shell
python manage.py test
```

## Admin
Le credenziali per accedere come admin sono
> Username: admin <br />
> Password: admin

