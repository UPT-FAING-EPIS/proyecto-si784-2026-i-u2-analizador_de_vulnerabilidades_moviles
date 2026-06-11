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
    secret_patterns = [
        re.compile(r"(?i)(api[_-]?key|apikey|secret|token|bearer)\s*[:=]\s*['\"]?([A-Za-z0-9_\-\.]{16,})"),
        re.compile(r"sb_publishable_[A-Za-z0-9_\-]+"),
        re.compile(r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),
    ]
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

                text_samples = self._read_text_samples(apk_zip, file_names)
                result.artifacts.extend(self._extract_url_artifacts(text_samples))
                result.findings.extend(self._detect_insecure_http(text_samples))
                result.findings.extend(self._detect_possible_secrets(text_samples))

            result.findings = self._deduplicate_findings(result.findings)
            result.artifacts = self._deduplicate_artifacts(result.artifacts)
            result.severity_max = self._max_severity(result.findings)
            result.summary = (
                f"Analisis completado: {len(result.findings)} hallazgos y "
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
        elif len(dex_files) > 1:
            findings.append(
                ApkFinding(
                    finding_type="dex",
                    title="MultiDex detectado",
                    severity="Info",
                    description=f"Se detectaron {len(dex_files)} archivos DEX.",
                    evidence=", ".join(dex_files[:10]),
                    recommendation="Revisar clases decompiladas durante el analisis profundo.",
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
        return findings

    def _read_text_samples(self, apk_zip, file_names):
        samples = []
        readable_names = [
            name
            for name in file_names
            if name.endswith(self.text_file_extensions) or name.endswith(".dex")
        ]
        for name in readable_names[:250]:
            try:
                data = apk_zip.read(name)
            except Exception:
                continue
            if len(data) > 1_000_000:
                data = data[:1_000_000]
            text = data.decode("utf-8", errors="ignore")
            if text:
                samples.append((name, text))
        return samples

    def _extract_url_artifacts(self, text_samples):
        artifacts = []
        for source_file, text in text_samples:
            for url in self.url_pattern.findall(text):
                artifacts.append(ApkArtifact("url", url, source_file))
        return artifacts[:200]

    def _detect_insecure_http(self, text_samples):
        insecure_evidence = []
        for source_file, text in text_samples:
            insecure_urls = [
                url
                for url in self.url_pattern.findall(text)
                if url.lower().startswith("http://")
                and not url.lower().startswith(self.ignored_http_prefixes)
            ]
            if insecure_urls:
                for url in insecure_urls:
                    insecure_evidence.append((url, source_file))
        unique_urls = sorted({url for url, _ in insecure_evidence})
        if not unique_urls:
            return []
        sources = sorted({source for _, source in insecure_evidence})[:5]
        return [
            ApkFinding(
                finding_type="insecure_communication",
                title="Uso de HTTP no cifrado",
                severity="Alto",
                description="Se detectaron endpoints HTTP sin cifrado dentro del APK.",
                evidence=", ".join(unique_urls[:5]),
                recommendation="Usar HTTPS y validar certificados correctamente.",
                source_file=", ".join(sources),
                cwe="CWE-319",
                owasp_mobile="M5",
            )
        ]

    def _detect_possible_secrets(self, text_samples):
        findings = []
        for source_file, text in text_samples:
            for pattern in self.secret_patterns:
                matches = pattern.findall(text)
                if matches:
                    findings.append(
                        ApkFinding(
                            finding_type="hardcoded_secret",
                            title="Posible secreto hardcodeado",
                            severity="Critico",
                            description="Se detectaron patrones compatibles con tokens, secrets o API keys embebidas.",
                            evidence=self._mask_secret(str(matches[0])),
                            recommendation="Eliminar secretos del APK y moverlos a un backend seguro.",
                            source_file=source_file,
                            cwe="CWE-798",
                            owasp_mobile="M9",
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
