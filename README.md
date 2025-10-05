# 🧠 Smart ToDo Mentor

Smart ToDo Mentor to aplikacja desktopowa w Pythonie, która pomaga w zarządzaniu zadaniami i priorytetyzacji przy użyciu LLM (OpenAI) oraz Semantic Kernel. Umożliwia dodawanie zadań, oznaczanie ich jako wykonane, aktualizowanie czasu poświęconego na zadania oraz automatyczne ustalanie priorytetów zadań w oparciu o dostępny czas i energię użytkownika.

---

## Funkcjonalności

- Dodawanie nowych zadań z określeniem czasu trwania i poziomu energii
- Aktualizowanie czasu poświęconego na zadania
- Oznaczanie zadań jako wykonane
- Usuwanie zadań
- Priorytetyzacja zadań przy pomocy OpenAI (LLM)
- Wyświetlanie planu dnia w oparciu o priorytet zadań
- Łatwe zapisywanie i wczytywanie listy zadań

---

## Wymagania

- Python 3.12 lub nowszy
- Klucz API OpenAI (`OPENAI_API_KEY`) w pliku `.env`
- Model OpenAI (`OPENAI_MODEL_ID`), domyślnie `gpt-4o-mini`

---

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone https://github.com/twoje-repo/llm-smart-todo.git
cd llm-smart-todo
```

2. Zainstaluj zależności:
```bash
python -m pip install --upgrade pip
python -m pip install python-dotenv semantic-kernel openai asyncio
python -m pip install python-dotenv
```

3. Instalacja PySimpleGUI z prywatnego repozytorium::

```bash
python -m pip install --upgrade --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
```

# Konfiguracja

4. Otwórz plik .env w katalogu głównym projektu i podaj swój OPENAI_API_KEY
   
## Struktura projektu
```bash
llm-smart-todo/
│
├─ main.py            # Główny plik uruchamiający GUI
├─ config.py          # Konfiguracja Kernel, SERVICE_ID itp.
├─ tasks.py           # Funkcje do wczytywania, zapisywania i aktualizacji zadań
├─ prioritize.py      # Funkcja priorytetyzacji zadań przy użyciu OpenAI
├─ tasks.json         # Automatycznie generowany plik przechowujący zadania
└─ .env               # Plik z kluczem API OpenAI
```
## Autor
Aerie55
