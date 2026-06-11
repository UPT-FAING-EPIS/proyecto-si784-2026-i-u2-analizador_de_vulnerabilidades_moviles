import json
from datetime import datetime, timezone
from io import StringIO

import pandas as pd


class ReportExportService:
    def build_csv(self, findings):
        rows = [self._finding_row(finding) for finding in findings]
        df = pd.DataFrame(rows)
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue().encode("utf-8")

    def build_json(self, scan, findings, artifacts):
        payload = {
            "scan": scan,
            "findings": [self._finding_row(finding) for finding in findings],
            "artifacts": [
                {
                    "type": artifact.get("artifact_type"),
                    "value": artifact.get("artifact_value"),
                    "source_file": artifact.get("source_file"),
                }
                for artifact in artifacts
            ],
            "exported_at": datetime.now(timezone.utc).isoformat(),
        }
        return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")

    def build_filename(self, scan, extension):
        scan_id = str(scan.get("id", "scan"))[:8]
        base_name = scan.get("file_name", "apk_scan").replace(".apk", "")
        safe_name = "".join(
            char if char.isalnum() or char in ("-", "_") else "_"
            for char in base_name
        )
        return f"anzencore_{safe_name}_{scan_id}.{extension}"

    def build_export_log(self, scan, user_id, export_format, file_name):
        return {
            "scan_id": scan["id"],
            "user_id": user_id,
            "export_format": export_format,
            "file_name": file_name,
        }

    def _finding_row(self, finding):
        return {
            "severity": finding.get("severity"),
            "type": finding.get("finding_type"),
            "title": finding.get("title"),
            "description": finding.get("description"),
            "evidence": finding.get("evidence"),
            "recommendation": finding.get("recommendation"),
            "source_file": finding.get("source_file"),
            "cwe": finding.get("cwe"),
            "owasp_mobile": finding.get("owasp_mobile"),
        }
