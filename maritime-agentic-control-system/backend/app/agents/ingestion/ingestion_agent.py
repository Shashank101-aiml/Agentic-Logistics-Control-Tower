from typing import Any, Dict, Optional


class IngestionAgent:
    def collect_data(self, source_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if source_payload is None:
            return {
                "event_type": "Storm",
                "location": "Arabian Sea",
                "severity": "critical",
            }

        return self._normalize_event(source_payload)

    def _normalize_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "event_type": str(payload.get("event_type", "unknown")).strip(),
            "severity": self._normalize_severity(payload.get("severity")),
            "source": self._normalize_source(payload),
            "description": payload.get("description"),
            "location": payload.get("location"),
            "timestamp": payload.get("timestamp"),
        }

    def _normalize_severity(self, severity: Any) -> str:
        if severity is None:
            return "info"
        severity_value = str(severity).strip().lower()
        if severity_value in {"high", "critical", "urgent"}:
            return "critical"
        if severity_value in {"medium", "moderate"}:
            return "warning"
        if severity_value in {"low", "minor"}:
            return "info"
        return severity_value

    def _normalize_source(self, payload: Dict[str, Any]) -> Optional[str]:
        return (
            payload.get("source")
            or payload.get("location")
            or payload.get("source_system")
            or None
        )