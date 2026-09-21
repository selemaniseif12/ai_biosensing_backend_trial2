import asyncio
import importlib
from datetime import datetime
from typing import Dict, List, Optional

from app.schemas.analyze_schema import AnalyzeRequest, AnalyzeResponse, AnalyzerResult

# Safe imports
from app.services.analyzer_v2_service import analyze_v2
from app.services.analyzer_v4_service import run_analyzer_v4


DEVICE_ANALYZER_MAP: Dict[str, List[str]] = {
    "QCM": ["v2", "v4", "v6"],
}


def _get_device_family(device_id: str) -> Optional[str]:
    if device_id.startswith("QCM"):
        return "QCM"
    return None


async def _run_analyzer_v2(req: AnalyzeRequest) -> AnalyzerResult:
    try:
        result = analyze_v2(req.payload)
        return AnalyzerResult(
            analyzer_version="v2",
            success=True,
            data=result if isinstance(result, dict) else {"result": result},
        )
    except Exception as e:
        return AnalyzerResult(analyzer_version="v2", success=False, error=str(e))


async def _run_analyzer_v4(req: AnalyzeRequest) -> AnalyzerResult:
    try:
        sensor_data = req.payload.get("data") or req.payload.get("values") or []
        result = run_analyzer_v4(sensor_data)
        return AnalyzerResult(
            analyzer_version="v4",
            success=True,
            data=result,
        )
    except Exception as e:
        return AnalyzerResult(analyzer_version="v4", success=False, error=str(e))


async def _run_analyzer_v6(req: AnalyzeRequest) -> AnalyzerResult:
    try:
        # Dynamic import to avoid circular import
        module = importlib.import_module("app.services.analyzer_v6_service")
        run_analyzer_v6 = getattr(module, "run_analyzer_v6")

        device_id = int(req.payload.get("device_id"))
        virus_id = int(req.payload.get("virus_id"))
        deposition_rate = float(req.payload.get("deposition_rate"))
        temperature = req.payload.get("temperature")
        humidity = req.payload.get("humidity")
        flow_rate = req.payload.get("flow_rate")

        result = run_analyzer_v6(
            device_id=device_id,
            virus_id=virus_id,
            deposition_rate=deposition_rate,
            temperature=temperature,
            humidity=humidity,
            flow_rate=flow_rate,
        )

        return AnalyzerResult(
            analyzer_version="v6",
            success=True,
            data=result,
        )

    except Exception as e:
        return AnalyzerResult(analyzer_version="v6", success=False, error=str(e))


ANALYZER_RUNNERS = {
    "v2": _run_analyzer_v2,
    "v4": _run_analyzer_v4,
    "v6": _run_analyzer_v6,
}


async def orchestrate_analysis(req: AnalyzeRequest) -> AnalyzeResponse:
    device_family = _get_device_family(req.device_id)

    if not device_family:
        return AnalyzeResponse(
            device_id=req.device_id,
            analyzers_used=[],
            primary_analyzer=None,
            ml_prediction=None,
            ml_confidence=None,
            results={},
            timestamp=datetime.utcnow().isoformat(),
        )

    compatible = DEVICE_ANALYZER_MAP.get(device_family, [])

    tasks = [ANALYZER_RUNNERS[v](req) for v in compatible if v in ANALYZER_RUNNERS]
    results_list = await asyncio.gather(*tasks)

    results_map = {r.analyzer_version: r for r in results_list}

    primary = None
    ml_pred = None
    ml_conf = None

    v6 = results_map.get("v6")
    if v6 and v6.success and v6.data:
        primary = "v6"
        ml_pred = v6.data.get("final_prediction_label")
        ml_conf = v6.data.get("final_prediction_confidence")
    else:
        for fallback in ["v4", "v2"]:
            r = results_map.get(fallback)
            if r and r.success:
                primary = fallback
                break

    return AnalyzeResponse(
        device_id=req.device_id,
        analyzers_used=list(results_map.keys()),
        primary_analyzer=primary,
        ml_prediction=ml_pred,
        ml_confidence=ml_conf,
        results=results_map,
        timestamp=datetime.utcnow().isoformat(),
    )
