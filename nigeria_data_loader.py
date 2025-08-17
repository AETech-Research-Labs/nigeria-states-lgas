import json
import csv
import sqlite3
from pathlib import Path

class NigeriaDataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.states_and_lgas = self._load_states_and_lgas()

    def _load_states_and_lgas(self):
        file_path = self.data_dir / "nigeria_states_and_lgas.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    def get_states(self):
        """Returns a list of all Nigerian States + FCT."""
        return list(self.states_and_lgas.keys())
    
    def get_lgas(self, state):
        """Returns a list of Local Government Areas (LGAs) for a given state."""
        state = state.title()
        return self.states_and_lgas.get(state, [])
    
    def find_state_by_lga(self, lga_name):
        """Return the state that contains the given LGA."""
        lga_name = lga_name.title()
        for state, lgas in self.states_and_lgas.items():
            if lga_name in [l.title() for l in lgas]:
                return state
        return None
    
    def export_to_csv(self, filename="nigeria_states_and_lgas_export.csv"):
        """Export state & LGA data into a CSV file."""
        filepath = self.data_dir / filename
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["State", "LGA"])
            for state, lgas in self.states_and_lgas.items():
                for lga in lgas:
                    writer.writerow([state, lga])
        return filepath

    def export_to_sqlite(self, db_name="nigeria_states_lgas.db"):
        """Export data into SQLite database for easy queries."""
        db_path = self.data_dir / db_name
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS states_lgas")
        cursor.execute("CREATE TABLE states_lgas (state TEXT, lga TEXT)")
        for state, lgas in self.states_and_lgas.items():
            for lga in lgas:
                cursor.execute("INSERT INTO states_lgas (state, lga) VALUES (?, ?)", (state, lga))
        conn.commit()
        conn.close()
        return db_path