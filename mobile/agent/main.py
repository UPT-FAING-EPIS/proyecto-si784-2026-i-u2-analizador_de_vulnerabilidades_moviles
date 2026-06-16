import platform

import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


SUPABASE_URL = "https://hnwradnsykylksjvrmpb.supabase.co"
SUPABASE_KEY = "sb_publishable_Sh4c3OF_PXYUnZcUAF6uTQ_qI3Oga8T"


class AnzenAgent(App):
    def build(self):
        self.view = BoxLayout(orientation="vertical", padding=40, spacing=20)
        self.view.add_widget(Label(text="AnzenCore Agent", font_size=30))
        self.uid = TextInput(
            hint_text="ID de usuario del dashboard",
            multiline=False,
            size_hint_y=None,
            height=100,
        )
        self.view.add_widget(self.uid)

        button = Button(
            text="ESCANEAR AHORA",
            size_hint_y=None,
            height=120,
            background_color=(0, 0.7, 1, 1),
        )
        button.bind(on_press=self.scan)
        self.view.add_widget(button)

        self.log = Label(text="Listo para analizar")
        self.view.add_widget(self.log)
        return self.view

    def scan(self, instance):
        user_id = self.uid.text.strip()
        if not user_id:
            self.log.text = "Falta el ID de usuario"
            return

        self.log.text = "Analizando..."
        results = [
            {
                "v": "Root Check",
                "n": "Critico",
                "d": "Binarios SU detectados en /system/bin",
            },
            {
                "v": "USB Debugging",
                "n": "Medio",
                "d": "Modo desarrollador activo",
            },
        ]

        try:
            sent = 0
            for item in results:
                payload = {
                    "user_id": user_id,
                    "dispositivo": f"{platform.system()} {platform.machine()}",
                    "vulnerabilidad": item["v"],
                    "nivel": item["n"],
                    "descripcion": item["d"],
                }
                response = requests.post(
                    f"{SUPABASE_URL}/rest/v1/vulnerabilidades",
                    json=payload,
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation",
                    },
                    timeout=15,
                )
                if not 200 <= response.status_code < 300:
                    detail = response.text[:180] if response.text else response.reason
                    raise RuntimeError(f"Supabase {response.status_code}: {detail}")
                sent += 1

            self.log.text = f"Reporte enviado al Dashboard ({sent})"
        except Exception as exc:
            self.log.text = f"Error enviando reporte: {exc}"


if __name__ == "__main__":
    AnzenAgent().run()
