# Recenzje gier API

---

# Instrukcja uruchomienia projektu w środowisku wirtualnym

## 1. Utworzenie i aktywacja środowiska wirtualnego

System Windows (PowerShell):

python -m venv .venv
.venv\Scripts\Activate.ps1

---

System macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

## 2. Instalacja zależności

pip install --upgrade pip
pip install -r requirements.txt

## 3. Wykonanie migracji bazy danych

python manage.py migrate

## 4. Utworzenie konta administratora (Superuser)

python manage.py createsuperuser

(Wprowadź nazwę użytkownika, adres e-mail oraz hasło)

## 5. Uruchomienie serwera deweloperskiego

python manage.py runserver

Serwer zostanie uruchomiony pod adresem: http://127.0.0.1:8000/

Panel administracyjny Django: http://127.0.0.1:8000/admin/
