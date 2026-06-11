import socket
from datetime import datetime, timedelta, timezone

from app.dashboard.services.apk_scan_service import ApkScanService
from app.dashboard.services.report_export_service import ReportExportService
from app.dashboard.services.vulnerability_scanner import VulnerabilityScanner


class DashboardController:
    def __init__(self, model):
        self.model = model
        self.vulnerability_scanner = VulnerabilityScanner()
        self.apk_scan_service = ApkScanService()
        self.report_export_service = ReportExportService()

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

    def update_user_ping(self, user_id):
        return self.model.update_ping(user_id)

    def fetch_online_list(self):
        threshold = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
        res = self.model.get_online_users(threshold)
        return res.data

    def fetch_all_reports(self):
        res = self.model.get_vulnerabilities()
        return res.data

    def scan_vulnerabilities(self, target=None):
        return self.vulnerability_scanner.scan(target)

    def fetch_apk_scans(self):
        res = self.model.get_apk_scans()
        return res.data

    def fetch_apk_findings(self, scan_id):
        res = self.model.get_apk_findings(scan_id)
        return res.data

    def fetch_apk_artifacts(self, scan_id):
        res = self.model.get_apk_artifacts(scan_id)
        return res.data

    def build_report_export(self, scan, findings, artifacts, export_format, user_id):
        if export_format == "csv":
            data = self.report_export_service.build_csv(findings)
        elif export_format == "json":
            data = self.report_export_service.build_json(scan, findings, artifacts)
        else:
            raise ValueError("Formato de exportacion no soportado.")

        file_name = self.report_export_service.build_filename(scan, export_format)
        return file_name, data

    def create_apk_scan(self, user_id, uploaded_file):
        is_valid, message = self.apk_scan_service.validate_apk_file(uploaded_file)
        if not is_valid:
            return False, message

        try:
            payload, file_bytes = self.apk_scan_service.build_scan_payload(
                user_id,
                uploaded_file,
            )
            created = self.model.create_apk_scan(payload)
            if not created.data:
                return False, "No se pudo registrar el escaneo del APK."

            scan_id = created.data[0]["id"]
            self.model.update_apk_scan(
                scan_id,
                {
                    "status": "processing",
                    "started_at": datetime.now(timezone.utc).isoformat(),
                },
            )

            analysis = self.apk_scan_service.analyze(file_bytes)
            self.model.update_apk_scan(
                scan_id,
                self.apk_scan_service.build_scan_update_payload(analysis),
            )

            finding_payloads = self.apk_scan_service.build_finding_payloads(
                scan_id,
                analysis.findings,
            )
            artifact_payloads = self.apk_scan_service.build_artifact_payloads(
                scan_id,
                analysis.artifacts,
            )
            self.model.create_apk_findings(finding_payloads)
            self.model.create_apk_artifacts(artifact_payloads)

            if analysis.status == "failed":
                return False, analysis.summary
            return True, analysis.summary
        except Exception as exc:
            message = str(exc)
            if "row-level security" in message.lower():
                return (
                    False,
                    "Supabase bloqueo el registro por RLS. Revisa las politicas de permisos en el SQL Editor de Supabase.",
                )
            return False, f"No se pudo analizar el APK: {exc}"
