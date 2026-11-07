"""Shared-secret tokens for the two Switch participants that call the API.

The agent token can read and draft proposals. The gate token is the only credential that
can write dispositions and movements. An unset token refuses every request.
"""

import hmac

from fastapi import Header, HTTPException, status

from app.config import settings


def _check(provided: str | None, expected: str, who: str) -> None:
    if not expected or not provided or not hmac.compare_digest(provided, expected):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"{who} token required")


def require_agent_token(x_api_token: str | None = Header(default=None)) -> None:
    _check(x_api_token, settings.QC_AGENT_TOKEN, "qc-agent")


def require_gate_token(x_api_token: str | None = Header(default=None)) -> None:
    _check(x_api_token, settings.QC_GATE_TOKEN, "qc-gate")
