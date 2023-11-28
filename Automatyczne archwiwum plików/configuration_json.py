import json
import os

class Configuration:

    def __init__(self, default_config, config_path: str = "config.json", ):
        self.config_path = config_path
        self.default_config = default_config
        self.ensure_config_exists()

    def create_default_config(self):
        """Tworzy domyślny plik konfiguracyjny."""
        with open(self.config_path, 'w') as file:
            json.dump(self.default_config, file, indent=4)

    def load_config(self):
        """Wczytuje konfigurację z pliku."""
        with open(self.config_path, 'r', encoding="utf-8") as file:
            return json.load(file)

    def update_config(self, new_config: dict):
        """Aktualizuje plik konfiguracyjny."""
        with open(self.config_path, 'w',  encoding="utf-8") as file:
            json.dump(new_config, file, indent=4)

    def ensure_config_exists(self):
        """Upewnia się, że plik istnieje. Jeśli nie, zgłasza błąd."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Plik konfiguracyjny '{self.config_path}' nie został znaleziony!")