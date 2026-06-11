import json
import pytest

from app.dashboard.services.report_export_service import ReportExportService


def test_report_export_service_builds_json():
    service = ReportExportService()
    payload = service.build_json(
        scan={"id": "scan-1", "file_name": "demo.apk"},
        findings=[{"severity": "Alto", "title": "HTTP inseguro"}],
        artifacts=[{"artifact_type": "url", "artifact_value": "http://x.test"}],
    )

    data = json.loads(payload.decode("utf-8"))

    assert data["scan"]["file_name"] == "demo.apk"
    assert data["findings"][0]["severity"] == "Alto"
    assert data["artifacts"][0]["type"] == "url"


def test_report_export_service_builds_csv():
    service = ReportExportService()
    payload = service.build_csv(
        [{"severity": "Medio", "title": "Libreria nativa"}]
    )

    text = payload.decode("utf-8")

    assert "severity" in text
    assert "Libreria nativa" in text

def test_report_export_service_build_filename():
    service = ReportExportService()
    scan = {"id": "12345678-abcd", "file_name": "My App! @v1.apk"}
    
    filename = service.build_filename(scan, "csv")
    
    assert filename.startswith("anzencore_My_App___v1_")
    assert filename.endswith(".csv")
    assert "12345678" in filename

def test_report_export_service_build_export_log():
    service = ReportExportService()
    scan = {"id": 101}
    
    log = service.build_export_log(scan, "user-1", "json", "report.json")
    
    assert log["scan_id"] == 101
    assert log["user_id"] == "user-1"
    assert log["export_format"] == "json"
    assert log["file_name"] == "report.json"
