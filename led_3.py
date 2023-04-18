import threading

# Définir la fonction à exécuter dans un processus séparé
def my_function():
    # Insérer le code à exécuter après une demi-seconde
    pass

# Lancer la fonction dans un processus séparé
thread = threading.Timer(0.5, my_function)
thread.start()

# Exécuter le reste du code ici
