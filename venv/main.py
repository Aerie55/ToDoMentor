import PySimpleGUI as sg
import asyncio
from tasks import load_tasks, save_tasks, update_ids
from gui import create_layout, refresh_table
from prioritize import prioritize_tasks

def handle_events(window, tasks, event, values):
    """Obsługa zdarzeń GUI"""
    if event == "➕ Dodaj zadanie":
        name = sg.popup_get_text("Podaj nazwę zadania:")
        if not name: return
        try:
            time = sg.popup_get_text("Ile minut zajmuje (ENTER = nie wiem):")
            time = int(time) if time else None
        except:
            time = None
        energy = sg.popup_get_text("Energia (niska/srednia/wysoka lub ENTER):")
        energy = energy.lower() if energy and energy.lower() in ["niska","srednia","wysoka"] else None
        tasks.append({
            "id": len(tasks)+1,
            "name": name,
            "time": time,
            "spent": 0,
            "energy": energy,
            "done": False
        })
        refresh_table(window, tasks)

    elif event == "✅ Oznacz wykonane":
        selected = values["-TABLE-"]
        if not selected:
            sg.popup("Wybierz zadanie!")
            return
        task = tasks[selected[0]]
        task["done"] = True
        refresh_table(window, tasks)

    elif event == "🕓 Aktualizuj czas":
        selected = values["-TABLE-"]
        if not selected:
            sg.popup("Wybierz zadanie!")
            return
        task = tasks[selected[0]]
        add_time = sg.popup_get_text(f"Ile minut poświęciłaś na '{task['name']}'?")
        if not add_time: return
        try:
            add_time = int(add_time)
        except:
            sg.popup("Podaj liczbę!")
            return
        task["spent"] += add_time
        if task.get("time") and task["spent"] >= task["time"]:
            task["done"] = True
        refresh_table(window, tasks)

    elif event == "🗑️ Usuń":
        selected = values["-TABLE-"]
        if not selected:
            sg.popup("Wybierz zadanie do usunięcia!")
            return
        task = tasks[selected[0]]
        if sg.popup_yes_no(f"Czy na pewno chcesz usunąć '{task['name']}'?") == "Yes":
            tasks.remove(task)
            update_ids(tasks)
        refresh_table(window, tasks)

    elif event == "🎯 Priorytetyzacja OpenAI":
        asyncio.run(prioritize_tasks(tasks, window))

def main():
    """Główna funkcja programu"""
    tasks = load_tasks()
    update_ids(tasks)
    window = sg.Window("Smart ToDo Mentor (GUI)", create_layout(tasks), size=(950,500), resizable=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "💾 Zapisz i wyjdź"):
            save_tasks(tasks)
            break
        handle_events(window, tasks, event, values)

    window.close()

if __name__ == "__main__":
    main()
