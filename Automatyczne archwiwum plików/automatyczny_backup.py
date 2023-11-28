import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from configuration_json import Configuration
import sys

DEFAULT_CONFIG_ARCHIVE = {
    "source_directory": os.getcwd(),
    "archive_directory": os.path.join(os.getcwd(), "Archiwum"),
    "file_exclusions": [],
    "folder_exclusions": []
    }

def display_messagebox(title, message, mode="info"):
    """
    Wyświetla okno dialogowe na podstawie podanych argumentów.
    
    Args:
    - title (str): Tytuł okna dialogowego.
    - message (str): Treść komunikatu.
    - mode (str): Rodzaj messageboxa ("info", "error", "yesno"). Domyślnie "info".
    
    Returns:
    - bool: True/False dla trybu "yesno". None dla pozostałych trybów.
    """
    root = tk.Tk()
    root.withdraw()  # Ukrywa główne okno tkinter
    
    if mode == "info":
        messagebox.showinfo(title, message)
    elif mode == "error":
        messagebox.showerror(title, message)
    elif mode == "yesno":
        result = messagebox.askyesno(title, message)
        root.destroy()
        return result
    else:
        raise ValueError("Nieobsługiwany tryb messageboxa.")
    
    root.destroy()

class DirectoryArchiver:

    def __init__(self, config: dict):
        # Pobieranie wartości z konfiguracji
        self.directory_path = config.get("source_directory", "")
        self.archive_directory_path = config.get("archive_directory", "")
        self.exclusions = config.get("file_exclusions", []) + config.get("folder_exclusions", [])
        
        # Dodajemy skrypt i folder Archiwum jako domyślne wyjątki
        self.exclusions.append("Archiwum")
        self.exclusions.append(os.path.basename(__file__))
        self._verify_source_directory_exists()
        self._verify_archive_directory()

    def _verify_source_directory_exists(self):
        """Sprawdza czy katalog źródłowy istnieje."""
        if not os.path.exists(self.directory_path) or not os.path.isdir(self.directory_path):
            raise ValueError(f"Podany katalog źródłowy '{self.directory_path}' nie istnieje lub nie jest katalogiem.")
        
    def _verify_archive_directory(self):
        """Sprawdza czy katalog źródłowy istnieje."""
        if not os.path.exists(self.archive_directory_path) or not os.path.isdir(self.archive_directory_path):
            raise ValueError(f"Podany katalog źródłowy '{self.archive_directory_path}' nie istnieje lub nie jest katalogiem.")
                
    def _create_archive_directory(self) -> str:
        """Tworzy katalog Archiwum jeśli jeszcze nie istnieje oraz podfolder z dzisiejszą datą i godziną."""

        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        sub_dir = os.path.join(self.archive_directory_path, current_time)

        os.makedirs(sub_dir)

        return sub_dir

    def archive_directory(self):
        """Kopiuje całą zawartość wskazanego katalogu (oprócz folderu Archiwum) do odpowiedniego podkatalogu w Archiwum."""
        destination_dir = self._create_archive_directory()
        
        for item in os.listdir(self.directory_path):
            source_item = os.path.join(self.directory_path, item)
            
            # Pomija foldery i pliki, których nazwy są na liście wyjątków
            if item in self.exclusions:  # Zmiana z source_item na item
                continue
            
            if os.path.isfile(source_item):
                shutil.copy2(source_item, destination_dir)
            elif os.path.isdir(source_item):
                shutil.copytree(source_item, os.path.join(destination_dir, item))

if __name__ == "__main__":
    
    #config_path = os.path.join(os.path.dirname(sys.argv[0]), "config.json")
    #config_manager = Configuration(config_path) 
    config_data = {
    "source_directory": "//polkomtel/pliki/PakVolt/Dzial_Energii/BAZA_DANYCH_ACCESS",
    "archive_directory": "//polkomtel/pliki/PakVolt/Dzial_Energii/BAZA_DANYCH_ACCESS/Archiwum",
    "file_exclusions": [],
    "folder_exclusions": []
}
    archiver = DirectoryArchiver(config_data)
    
    # Wyświetlanie okna dialogowego do potwierdzenia
    excluded_items = "\n- ".join(archiver.exclusions)
    message = (f"Czy chcesz utworzyć archiwum katalogu {archiver.directory_path} "
            f"w docelowym katalogu z archiwum z pominięciem folderów i plików, które mają w nazwie:\n"
            f"- {excluded_items}?")

    if display_messagebox("Potwierdzenie", message, mode="yesno"):
        try:
            archiver.archive_directory()
            display_messagebox("Sukces", "Zawartość folderu została zarchiwizowana pomyślnie.")
        except Exception as e:
            display_messagebox("Błąd", f"Wystąpił błąd: {e}", mode="error")
