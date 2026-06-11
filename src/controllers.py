import socket
from datetime import datetime, timedelta

class AnzenController:
    def __init__(self, model):
        self.model = model

    def login(self, username, password):
        res = self.model.authenticate(username, password)
        return res.data[0] if res.data else None

    def signup(self, username, password):
        username = username.strip()
        if not username or not password:
            return False, "Completa usuario y contrasena."

        try:
            existing = self.model.user_exists(username)
            if existing.data:
                return False, "El usuario ya existe."
            self.model.register(username, password)
            return True, "Registrado. Ingresa ahora."
        except socket.gaierror:
            return False, "No se pudo conectar con Supabase: revisa internet, DNS o la URL del proyecto."
        except Exception as exc:
            if "getaddrinfo failed" in str(exc):
                return False, "No se pudo conectar con Supabase: revisa internet, DNS o la URL del proyecto."
            return False, f"No se pudo crear el usuario: {exc}"

    def fetch_online_list(self):
        # Umbral de 30 segundos para considerar online
        umbral = (datetime.now() - timedelta(seconds=30)).isoformat()
        res = self.model.get_online_users(umbral)
        return res.data

    def fetch_all_reports(self):
        res = self.model.get_vulnerabilities()
        return res.data

    def scan_vulnerabilities(self, target=None):
        return self.model.generate_scan_results(target)
