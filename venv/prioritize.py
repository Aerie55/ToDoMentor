import asyncio
import json
import PySimpleGUI as sg
from config import SERVICE_ID, kernel

async def prioritize_tasks(tasks, window):
    if not tasks:
        sg.popup("Brak zadań do priorytetyzacji!")
        return

    minutes = window["-TIME-"].get() or "60"
    energy = window["-ENERGY-"].get() or "srednia"

    task_list = "\n".join(f"{t['name']} - czas: {t.get('time','?')} min"
                          for t in tasks if not t.get("done", False))

    prompt = f"""
Jesteś inteligentnym asystentem produktywności.
Użytkownik ma {minutes} minut i poziom energii {energy}.
Lista zadań:
{task_list}

Twoim zadaniem jest ocenić każde zadanie pod kątem priorytetu (1-100) i podać krótki komentarz.
Nie przydzielaj czasu – każde zadanie ma zostać wykonane w pełnym czasie podanym przez użytkownika.
Zwróć listę JSON z polami:
- name (dokładna nazwa zadania)
- priorytet
- komentarz
Zwróć **TYLKO JSON**, bez dodatkowych nagłówków ani znaczników.
"""
    try:
        response = await kernel.invoke_prompt(prompt, service_id=SERVICE_ID)
        raw_text = response.result if hasattr(response, "result") else str(response)

        raw_text = raw_text.strip()
        if raw_text.lower().startswith("'''json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("'''"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        data = json.loads(raw_text)

        task_names = [t['name'] for t in tasks]
        for item in data:
            name = item.get("name")
            if name in task_names:
                t = tasks[task_names.index(name)]
                t["priority"] = item["priorytet"]
                t["comment"] = item["komentarz"]

        sorted_tasks = sorted([t for t in tasks if not t.get("done", False)],
                              key=lambda x: x.get("priority", 0), reverse=True)

        remaining = int(minutes)
        for t in sorted_tasks:
            t_time = t.get("time", 0) or 0
            t["fits_today"] = t_time <= remaining
            if t["fits_today"]:
                remaining -= t_time

        table_data = []
        for t in tasks:
            percent = int((t["spent"] / t["time"]) * 100) if t.get("time") else 0
            status = "✅" if t.get("done") else "🕓"
            fits_today = "✅" if t.get("fits_today") else "❌"
            table_data.append([t["id"], t["name"], f"{t['spent']}/{t.get('time','?')}",
                               t.get("energy","?"), f"{percent}%", t.get("priority","?"),
                               t.get("comment",""), fits_today, status])
        window["-TABLE-"].update(values=table_data)

        plan_text = "\n".join([f"{t['name']} → priorytet {t.get('priority','?')} ({t.get('comment','')})"
                               + (" ✅ zmieści się" if t.get("fits_today") else " ❌ nie zmieści się")
                               for t in sorted_tasks])
        sg.popup_scrolled("🎯 Plan priorytetyzacji:\n\n"+plan_text, title="Plan dnia")

    except Exception as e:
        sg.popup(f"❌ Błąd priorytetyzacji:\n{e}\n\nSurowa odpowiedź:\n{response}")
