from supabase import create_client
import streamlit as st


class AnzenModel:
    def __init__(self):
        self.supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

    def authenticate(self, user, pw):
        return self.supabase.table("usuarios").select("*").eq("username", user).eq("password", pw).execute()

    def user_exists(self, user):
        return self.supabase.table("usuarios").select("id").eq("username", user).limit(1).execute()

    def register(self, user, pw):
        return self.supabase.table("usuarios").insert({"username": user, "password": pw}).execute()

    def update_ping(self, user_id):
        return self.supabase.table("usuarios").update({"last_ping": "now()"}).eq("id", user_id).execute()

    def get_online_users(self, time_limit):
        return self.supabase.table("usuarios").select("username").gt("last_ping", time_limit).execute()

    def get_vulnerabilities(self):
        return self.supabase.table("vulnerabilidades").select("*").order("fecha", desc=True).execute()

    def generate_scan_results(self, target=None):
        import platform
        import random
        import socket
        import os
        from datetime import datetime

        def scan_local_device():
            vulnerabilities = []
            system = platform.system()
            machine = platform.machine()
            hostname = socket.gethostname()

            common_ports = [21, 22, 23, 80, 443, 3306, 3389]
            open_ports = []
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.3)
                    result = sock.connect_ex(('127.0.0.1', port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass

            if len(open_ports) > 0:
                vulnerabilities.append({
                    "vulnerabilidad": f"Open Ports ({', '.join(map(str, open_ports))})",
                    "nivel": "Alto",
                    "descripcion": f"Se detectaron {len(open_ports)} puertos expuestos localmente"
                })

            if system == "Windows":
                try:
                    import subprocess
                    uac_result = subprocess.run(['reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System', '/v', 'EnableLUA'], capture_output=True, text=True)
                    if '0x0' in uac_result.stdout or uac_result.returncode != 0:
                        vulnerabilities.append({
                            "vulnerabilidad": "UAC Disabled",
                            "nivel": "Alto",
                            "descripcion": "Control de cuentas de usuario deshabilitado"
                        })
                except:
                    vulnerabilities.append({
                        "vulnerabilidad": "UAC Status Unknown",
                        "nivel": "Medio",
                        "descripcion": "No se pudo verificar el estado de UAC"
                    })

                vulnerabilities.append({
                    "vulnerabilidad": "Windows Update Status Unknown",
                    "nivel": "Alto",
                    "descripcion": "Verificar si hay actualizaciones pendientes"
                })

                try:
                    win_ver = platform.version()
                    if win_ver.startswith("10.") or win_ver.startswith("11."):
                        vulnerabilities.append({
                            "vulnerabilidad": "Windows Telemetry Enabled",
                            "nivel": "Medio",
                            "descripcion": "Telemetria de Windows puede exponer datos"
                        })
                except:
                    pass

                try:
                    if os.path.exists("C:\\Windows\\Temp"):
                        perm = os.stat("C:\\Windows\\Temp")
                        vulnerabilities.append({
                            "vulnerabilidad": "Temp Directory Permissions",
                            "nivel": "Medio",
                            "descripcion": "Permisos del directorio Temp deben revisarse"
                        })
                except:
                    pass

            elif system in ["Linux", "Darwin"]:
                if os.path.exists("/tmp") and os.access("/tmp", os.W_OK):
                    vulnerabilities.append({
                        "vulnerabilidad": "Writable Temporary Directory",
                        "nivel": "Medio",
                        "descripcion": "Directorio /tmp accesible sin restricciones"
                    })

                if os.path.exists("/.ssh") and os.access("/.ssh", os.R_OK):
                    vulnerabilities.append({
                        "vulnerabilidad": "SSH Keys Directory Accessible",
                        "nivel": "Alto",
                        "descripcion": "Directorio .ssh con permisos inseguros"
                    })

                try:
                    import subprocess
                    fw_result = subprocess.run(['ufw', 'status'], capture_output=True, text=True)
                    if 'inactive' in fw_result.stdout.lower():
                        vulnerabilities.append({
                            "vulnerabilidad": "Firewall Disabled",
                            "nivel": "Alto",
                            "descripcion": "Firewall del sistema no esta activo"
                        })
                except:
                    vulnerabilities.append({
                        "vulnerabilidad": "Firewall Status Unknown",
                        "nivel": "Medio",
                        "descripcion": "No se pudo verificar el estado del firewall"
                    })

                try:
                    passwd_stat = os.stat('/etc/passwd')
                    if passwd_stat.st_mode & 0o077:
                        vulnerabilities.append({
                            "vulnerabilidad": "Insecure Password File Permissions",
                            "nivel": "Alto",
                            "descripcion": "El archivo /etc/passwd tiene permisos inseguros"
                        })
                except:
                    pass

            try:
                if hasattr(os, 'cpu_count'):
                    cpu_count = os.cpu_count()
                    if cpu_count and cpu_count > 4:
                        vulnerabilities.append({
                            "vulnerabilidad": "Resource Exhaustion Risk",
                            "nivel": "Bajo",
                            "descripcion": "Sistema con alta capacidad de CPU, riesgo de ataques DoS"
                        })
            except:
                pass

            try:
                import subprocess
                proc_result = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], capture_output=True, text=True) if system == "Windows" else subprocess.run(['sysctl', 'hw.memsize'], capture_output=True, text=True)
                mem_kb = 0
                if system == "Windows":
                    for line in proc_result.stdout.split('\n'):
                        if line.strip().isdigit():
                            mem_kb = int(line.strip())
                else:
                    for line in proc_result.stdout.split('\n'):
                        if 'hw.memsize' in line:
                            mem_kb = int(line.split()[1]) // 1024
                if mem_kb > 8000000:
                    vulnerabilities.append({
                        "vulnerabilidad": "High Memory System",
                        "nivel": "Bajo",
                        "descripcion": "Sistema con memoria elevada, vulnerable a ataques de memoria"
                    })
            except:
                pass

            try:
                if os.path.exists('/etc/shadow') and os.access('/etc/shadow', os.R_OK):
                    vulnerabilities.append({
                        "vulnerabilidad": "Shadow File Readable",
                        "nivel": "Crítico",
                        "descripcion": "Archivo /etc/shadow accesible sin privilegios root"
                    })
            except:
                pass

            return vulnerabilities, f"{system} {machine} ({hostname})"

        base_vulnerabilities = [
            {"vulnerabilidad": "SSL/TLS Misconfiguration", "nivel": "Crítico", "descripcion": "Certificado expirado o débil en comunicaciones"},
            {"vulnerabilidad": "Open Ports Detected", "nivel": "Alto", "descripcion": "Puertos 22, 80 abiertos sin protección"},
            {"vulnerabilidad": "Weak Password Policy", "nivel": "Medio", "descripcion": "Política de contraseñas inadecuada"},
            {"vulnerabilidad": "Outdated Dependencies", "nivel": "Alto", "descripcion": "Bibliotecas con CVEs conocidos"},
            {"vulnerabilidad": "Debug Mode Enabled", "nivel": "Bajo", "descripcion": "Modo debug activo en producción"},
            {"vulnerabilidad": "Missing Security Headers", "nivel": "Alto", "descripcion": "Cabeceras de seguridad HTTP no configuradas"},
            {"vulnerabilidad": "SQL Injection Vulnerability", "nivel": "Crítico", "descripcion": "Posible inyección SQL en formularios"},
            {"vulnerabilidad": "XSS Vulnerability", "nivel": "Alto", "descripcion": "Cross-Site Scripting posible en inputs"},
            {"vulnerabilidad": "CSRF Protection Missing", "nivel": "Medio", "descripcion": "Falta protección contra CSRF"},
            {"vulnerabilidad": "Insecure File Permissions", "nivel": "Alto", "descripcion": "Permisos de archivos inseguros detectados"},
            {"vulnerabilidad": "Default Credentials", "nivel": "Crítico", "descripcion": "Credenciales por defecto sin cambiar"},
            {"vulnerabilidad": "Unpatched Kernel", "nivel": "Alto", "descripcion": "Kernel con vulnerabilidades conocidas"},
            {"vulnerabilidad": "Insecure SSH Config", "nivel": "Alto", "descripcion": "SSH permite autenticación por contraseña"},
        ]

        results = []
        if target:
            for vuln in random.sample(base_vulnerabilities, k=random.randint(1, 3)):
                results.append({
                    "dispositivo": target,
                    "vulnerabilidad": vuln["vulnerabilidad"],
                    "nivel": vuln["nivel"],
                    "descripcion": vuln["descripcion"],
                    "fecha": datetime.now().isoformat()
                })
        else:
            local_vulns, device_info = scan_local_device()
            for vuln in local_vulns:
                results.append({
                    "dispositivo": device_info,
                    "vulnerabilidad": vuln["vulnerabilidad"],
                    "nivel": vuln["nivel"],
                    "descripcion": vuln["descripcion"],
                    "fecha": datetime.now().isoformat()
                })
        return results
