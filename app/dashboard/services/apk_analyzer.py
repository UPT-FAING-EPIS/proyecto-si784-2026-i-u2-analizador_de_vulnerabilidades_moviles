import re
import zipfile
from dataclasses import dataclass, field
from io import BytesIO


SEVERITY_ORDER = {
    "Info": 0,
    "Bajo": 1,
    "Medio": 2,
    "Alto": 3,
    "Critico": 4,
}


@dataclass
class ApkFinding:
    finding_type: str
    title: str
    severity: str
    description: str
    evidence: str | None = None
    recommendation: str | None = None
    source_file: str | None = None
    cwe: str | None = None
    owasp_mobile: str | None = None


@dataclass
class ApkArtifact:
    artifact_type: str
    artifact_value: str
    source_file: str | None = None


@dataclass
class ApkAnalysisResult:
    status: str = "completed"
    summary: str = ""
    severity_max: str | None = None
    findings: list[ApkFinding] = field(default_factory=list)
    artifacts: list[ApkArtifact] = field(default_factory=list)
    error_message: str | None = None


class ApkAnalyzer:
    text_file_extensions = (
        ".xml",
        ".json",
        ".txt",
        ".html",
        ".js",
        ".properties",
        ".MF",
        ".RSA",
        ".SF",
    )

    url_pattern = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
    secret_patterns = [  # nosonar - these regexes detect secrets in APK files, not store credentials
        re.compile(r"(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})"),  # nosonar
        re.compile(r"sb_publishable_[A-Za-z0-9_\-]+"),  # nosonar
        re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),  # nosonar
    ]
    
    crypto_patterns = [
        re.compile(r"MessageDigest\.getInstance\(\s*[\"'](MD5|SHA-1)[\"']\s*\)", re.IGNORECASE),
        re.compile(r"Cipher\.getInstance\(\s*[\"'](DES|DESede|AES/ECB/PKCS5Padding)[\"']\s*\)", re.IGNORECASE)
    ]
    
    webview_patterns = [
        re.compile(r"setJavaScriptEnabled\(\s*true\s*\)")
    ]
    
    random_patterns = [
        re.compile(r"new\s+java\.util\.Random\(\s*\)")
    ]
    
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

    ignored_http_prefixes = (
        "http://www.apache.org/licenses/",
        "http://schemas.android.com/",
        "http://ns.adobe.com/",
        "http://www.w3.org/",
    )

    def analyze(self, file_bytes):
        result = ApkAnalysisResult()
        try:
            with zipfile.ZipFile(BytesIO(file_bytes)) as apk_zip:
                file_names = apk_zip.namelist()
                result.artifacts.extend(self._build_structure_artifacts(file_names))
                result.findings.extend(self._analyze_structure(file_names))

                # Extraer classes.dex para nuestro motor algoritmico Custom
                dex_files = [n for n in file_names if n.endswith(".dex")]
                all_strings = []
                is_packed = False
                
                # Usar nuestro parser custom 100% Python en los archivos DEX
                for dex_name in dex_files:
                    try:
                        dex_data = apk_zip.read(dex_name)
                        from app.dashboard.services.dex_parser import CustomDexParser
                        parser = CustomDexParser(dex_data)
                        
                        all_strings.extend(parser.get_strings())
                        
                        if parser.is_packed():
                            is_packed = True
                            result.artifacts.append(ApkArtifact("heuristic", f"Entropia Alta ({parser.entropy:.2f}) en {dex_name}"))
                    except Exception as e:
                        print(f"Error parseando {dex_name}: {e}")

                if is_packed:
                    result.findings.append(
                        ApkFinding(
                            finding_type="packer_detected",
                            title="Alto Ofuscamiento Detectado (Código Cifrado)",
                            severity="Alto",
                            description="El algoritmo matemático de Entropía detectó que el código Dalvik es pseudoaleatorio. La aplicación probablemente usa un Packer comercial o está cifrada.",
                            recommendation="Se requiere Análisis Dinámico en memoria para evadir la protección.",
                            owasp_mobile="M9"
                        )
                    )

                # Si no hay cadenas extraidas del bytecode, leemos los XML/TXT como respaldo
                if not all_strings:
                    text_samples = self._read_text_samples(apk_zip, file_names)
                    all_strings = [text for _, text in text_samples]

                # Ejecutar nuestras reglas algorítmicas sobre el String Pool
                result.artifacts.extend(self._extract_url_artifacts(all_strings))
                result.findings.extend(self._detect_insecure_http(all_strings))
                result.findings.extend(self._detect_possible_secrets(all_strings))
                result.findings.extend(self._detect_weak_crypto(all_strings))

            result.findings = self._deduplicate_findings(result.findings)
            result.artifacts = self._deduplicate_artifacts(result.artifacts)
            result.severity_max = self._max_severity(result.findings)
            result.summary = (
                f"Analisis completado (Motor Heuristico): {len(result.findings)} hallazgos y "
                f"{len(result.artifacts)} artefactos extraidos."
            )
        except zipfile.BadZipFile:
            result.status = "failed"
            result.error_message = "El archivo no es un APK valido o esta corrupto."
            result.summary = result.error_message
        except Exception as exc:
            result.status = "failed"
            result.error_message = f"Error analizando APK: {exc}"
            result.summary = result.error_message
        return result

    def _build_structure_artifacts(self, file_names):
        artifacts = []
        dex_count = len([name for name in file_names if name.endswith(".dex")])
        native_libs = [name for name in file_names if name.startswith("lib/") and name.endswith(".so")]

        artifacts.append(ApkArtifact("dex_count", str(dex_count)))
        artifacts.append(ApkArtifact("file_count", str(len(file_names))))
        for lib in native_libs[:50]:
            artifacts.append(ApkArtifact("native_library", lib, lib))
        return artifacts

    def _analyze_structure(self, file_names):
        findings = []
        if "AndroidManifest.xml" not in file_names:
            findings.append(
                ApkFinding(
                    finding_type="manifest",
                    title="AndroidManifest.xml no encontrado",
                    severity="Alto",
                    description="No se encontro el manifiesto principal del APK.",
                    recommendation="Verificar que el archivo APK no este corrupto o manipulado.",
                    owasp_mobile="M8",
                )
            )

        dex_files = [name for name in file_names if name.endswith(".dex")]
        if not dex_files:
            findings.append(
                ApkFinding(
                    finding_type="dex",
                    title="Archivo DEX no encontrado",
                    severity="Alto",
                    description="No se encontraron clases DEX dentro del APK.",
                    recommendation="Validar integridad del APK.",
                )
            )

        if any(name.startswith("lib/") and name.endswith(".so") for name in file_names):
            findings.append(
                ApkFinding(
                    finding_type="native_code",
                    title="Librerias nativas detectadas",
                    severity="Medio",
                    description="El APK incluye codigo nativo, lo que puede ocultar logica sensible o controles de seguridad.",
                    recommendation="Analizar las librerias nativas con herramientas especializadas.",
                    owasp_mobile="M7",
                )
            )
            
        db_files = [name for name in file_names if name.endswith((".db", ".sqlite", ".sqlite3"))]
        if db_files:
            findings.append(
                ApkFinding(
                    finding_type="internal_database",
                    title="Bases de datos locales empaquetadas",
                    severity="Medio",
                    description="Se detectaron archivos de base de datos dentro del APK.",
                    evidence="Archivos encontrados:\n" + "\n".join(db_files[:5]),
                    recommendation="Asegurarse de no empaquetar bases de datos pre-pobladas en producción.",
                    owasp_mobile="M1",
                )
            )
            
        return findings

    def _read_text_samples(self, apk_zip, file_names):
        samples = []
        readable_names = [n for n in file_names if n.endswith(self.text_file_extensions)]
        for name in readable_names[:100]:
            try:
                data = apk_zip.read(name)
                if len(data) > 500_000: data = data[:500_000]
                text = data.decode("utf-8", errors="ignore").replace("\x00", "")
                if text: samples.append((name, text))
            except Exception:
                continue
        return samples

    def _extract_url_artifacts(self, strings_pool):
        artifacts = []
        for text in strings_pool:
            if isinstance(text, str):
                for url in self.url_pattern.findall(text):
                    artifacts.append(ApkArtifact("url", url, "classes.dex (String Pool)"))
        return artifacts[:100]

    def _detect_insecure_http(self, strings_pool):
        findings = []
        from app.dashboard.services.dalvik_heuristics import DalvikHeuristics
        
        for text in strings_pool:
            if isinstance(text, str) and text.lower().startswith("http://") and not text.lower().startswith(self.ignored_http_prefixes):
                if len(text) < 150:
                    evidence = DalvikHeuristics.generate_pseudo_code("insecure_communication", text)
                    recommendation = DalvikHeuristics.get_recommendation("insecure_communication")
                    
                    findings.append(
                        ApkFinding(
                            finding_type="insecure_communication",
                            title="Uso de HTTP no cifrado",
                            severity="Alto",
                            description="Se detectó una llamada a un endpoint HTTP sin cifrado a nivel de bytecode.",
                            evidence=f"```java\n{evidence}\n```",
                            recommendation=f"```java\n{recommendation}\n```",
                            source_file="classes.dex (Bytecode)",
                            cwe="CWE-319",
                            owasp_mobile="M5",
                        )
                    )
        return findings[:5]

    def _detect_possible_secrets(self, strings_pool):
        findings = []
        from app.dashboard.services.dalvik_heuristics import DalvikHeuristics
        
        for text in strings_pool:
            if not isinstance(text, str): continue
            
            for pattern in self.secret_patterns:
                matches = pattern.findall(text)
                if matches:
                    match_obj = pattern.search(text)
                    if match_obj:
                        full_match = match_obj.group(0)
                        safe_match = self._mask_secret(full_match)
                        
                        evidence = DalvikHeuristics.generate_pseudo_code("hardcoded_secret", safe_match)
                        recommendation = DalvikHeuristics.get_recommendation("hardcoded_secret")
                        
                        findings.append(
                            ApkFinding(
                                finding_type="hardcoded_secret",
                                title="Secreto Hardcodeado (Motor Heurístico)",
                                severity="Critico",
                                description="El algoritmo encontró una API Key estática en la tabla de memoria de Dalvik.",
                                evidence=f"```java\n{evidence}\n```",
                                recommendation=f"```java\n{recommendation}\n```",
                                source_file="classes.dex (Bytecode)",
                                cwe="CWE-798",
                                owasp_mobile="M9",
                            )
                        )
        return findings[:5]

    def _detect_weak_crypto(self, strings_pool):
        findings = []
        from app.dashboard.services.dalvik_heuristics import DalvikHeuristics
        
        weak_algos = ["MD5", "SHA-1", "DES", "AES/ECB/PKCS5Padding"]
        
        for text in strings_pool:
            if isinstance(text, str) and any(algo == text for algo in weak_algos):
                evidence = DalvikHeuristics.generate_pseudo_code("weak_crypto", text)
                recommendation = DalvikHeuristics.get_recommendation("weak_crypto")
                
                findings.append(
                    ApkFinding(
                        finding_type="weak_crypto",
                        title="Criptografía Débil o Insegura",
                        severity="Alto",
                        description=f"El algoritmo encontró invocaciones en bytecode a un algoritmo roto ({text}).",
                        evidence=f"```java\n{evidence}\n```",
                        recommendation=f"```java\n{recommendation}\n```",
                        source_file="classes.dex (Bytecode)",
                        cwe="CWE-327",
                        owasp_mobile="M5",
                    )
                )
        return findings


    def _mask_secret(self, value):
        clean = value.replace("\\n", " ")
        if len(clean) <= 24:
            return clean[:4] + "***"
        return clean[:12] + "***" + clean[-6:]

    def _deduplicate_findings(self, findings):
        seen = set()
        unique = []
        for finding in findings:
            key = (finding.finding_type, finding.title, finding.source_file, finding.evidence)
            if key in seen:
                continue
            seen.add(key)
            unique.append(finding)
        return unique

    def _deduplicate_artifacts(self, artifacts):
        seen = set()
        unique = []
        for artifact in artifacts:
            key = (artifact.artifact_type, artifact.artifact_value)
            if key in seen:
                continue
            seen.add(key)
            unique.append(artifact)
        return unique

    def _max_severity(self, findings):
        if not findings:
            return "Info"
        return max(findings, key=lambda item: SEVERITY_ORDER[item.severity]).severity
