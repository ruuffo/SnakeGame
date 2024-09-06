import csv
from datetime import datetime
import os


class PerformanceTracker:

    def __init__(self):
        self.start_time = datetime.now()
        self.lapins_manges = 0
        self.movements = 0
        self.score = 0

    def increment_lapins_manges(self):
        self.lapins_manges += 1
        self.update_score()

    def increment_movements(self):
        self.movements += 1

    def update_score(self):
        # Exemple de calcul du score
        self.score = self.lapins_manges * 10 - self.movements

    def get_performance_data(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            "start_time": self.start_time.isoformat(),
            "duration": duration,
            "lapins_manges": self.lapins_manges,
            "movements": self.movements,
            "score": self.score,
        }

    def save_performance(self, filename="performances.csv"):
        fieldnames = [
            "start_time", "duration", "lapins_manges", "movements", "score"
        ]
        performance_data = self.get_performance_data()

        # Vérifiez si le fichier existe
        file_exists = os.path.isfile(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Écrire l'en-tête uniquement si le fichier n'existe pas encore
            if not file_exists:
                writer.writeheader()

            # Écrire les données de performance
            writer.writerow(performance_data)

        print("Performance enregistrée dans le fichier CSV.")

    def reset(self):
        self.__init__()
