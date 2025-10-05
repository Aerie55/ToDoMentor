import PySimpleGUI as sg

def create_layout(tasks):
    table_data = [[t["id"], t["name"], f"{t['spent']}/{t.get('time','?')}", t.get("energy","?"),
                   f"{int((t['spent']/t.get('time',1))*100) if t.get('time') else 0}%",
                   t.get("priority","?"), t.get("comment",""), "", "✅" if t.get("done") else "🕓"]
                  for t in tasks]

    sg.theme("DarkBlue14")
    layout = [
        [sg.Text("🧠 Smart ToDo Mentor", font=("Helvetica", 18, "bold"))],
        [sg.Button("➕ Dodaj zadanie"), sg.Button("✅ Oznacz wykonane"),
         sg.Button("🕓 Aktualizuj czas"), sg.Button("🗑️ Usuń"),
         sg.Button("🎯 Priorytetyzacja OpenAI"), sg.Button("💾 Zapisz i wyjdź", button_color=("white","#2C7A7B"))],
        [sg.Table(values=table_data,
                  headings=["ID","Zadanie","Czas","Energia","Postęp","Priorytet","Komentarz","Starczy czasu?","Status"],
                  auto_size_columns=False, col_widths=[4,25,10,10,10,8,25,12,8],
                  justification="center", key="-TABLE-", enable_events=True,
                  expand_x=True, expand_y=True, num_rows=10, alternating_row_color="#1E3A8A")],
        [sg.Text("Czas całkowity (min):"), sg.Input(key="-TIME-", size=(10,1)), 
         sg.Text("Energia:"), sg.Combo(["niska","srednia","wysoka"], key="-ENERGY-", default_value="srednia")]
    ]
    return layout

def refresh_table(window, tasks):
    table_data = []
    for t in tasks:
        percent = int((t["spent"] / t["time"]) * 100) if t.get("time") else 0
        status = "✅" if t.get("done") else "🕓"
        priority = t.get("priority", "?")
        comment = t.get("comment", "")
        fits_today = "✅" if t.get("fits_today") else "❌"
        table_data.append([
            t["id"], t["name"], f"{t['spent']}/{t.get('time','?')}", t.get("energy","?"),
            f"{percent}%", priority, comment, fits_today, status
        ])
    window["-TABLE-"].update(values=table_data)
