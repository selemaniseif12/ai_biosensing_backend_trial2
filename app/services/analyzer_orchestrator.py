# app/services/analyzer_orchestrator.py

import logging
import asyncio
from typing import Dict, Any, List

from app.services.analyzer_v1_service import run_analyzer_v1
from app.services.analyzer_v2_service import analyze_v2
from app.services.analyzer_v3_service import run_analyzer_v3
from app.services.analyzer_v4_service import run_analyzer_v4
from app.services.analyzer_v5_service import run_analyzer_v5
from app.services.analyzer_v6_service import run_analyzer_v6

logger = logging.getLogger("analyzers")


# ---------------------------------------------------------
# Helper: run sync analyzers asynchronously
# ---------------------------------------------------------
async def _run_async(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


# ---------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------
async def orchestrate_analysis(payload) -> Dict[str, Any]:
    """
    Runs all compatible analyzers in parallel and merges results.
    """

    logger.info(f"[Orchestrator] Starting orchestration with payload: {payload.dict()}")

    tasks = []

    # -----------------------------------------------------
    # SENSOR-BASED ANALYZERS (v1–v4)
    # -----------------------------------------------------
    if payload.sensor_data:
        tasks.append(_run_async(run_analyzer_v1, payload.sensor_data))
        tasks.append(_run_async(analyze_v2, payload))
        tasks.append(_run_async(run_analyzer_v3, payload.sensor_data))
        tasks.append(_run_async(run_analyzer_v4, payload.sensor_data))

    # -----------------------------------------------------
    # DEVICE/PHYSICS ANALYZERS (v5–v6)
    # -----------------------------------------------------
    if payload.device_id and payload.virus_id:
        tasks.append(_run_async(run_analyzer_v5, payload.device_id, payload.virus_id))

        if payload.deposition_rate:
            tasks.append(
                _run_async(
                    run_analyzer_v6,
                    payload.device_id,
                    payload.virus_id,
                    payload.deposition_rate,
                    payload.temperature,
                    payload.humidity,
                    payload.flow_rate,
                )
            )

    if not tasks:
        raise ValueError("No analyzers can run with the provided input.")

    # -----------------------------------------------------
    # Run all analyzers in parallel
    # -----------------------------------------------------
    results = await asyncio.gather(*tasks, return_exceptions=True)

    merged: List[Dict[str, Any]] = []

    for result in results:
        if isinstance(result, Exception):
            logger.error(f"[Orchestrator] Analyzer error: {result}")
            continue
        merged.append(result)

    if not merged:
        raise ValueError("All analyzers failed.")

    # -----------------------------------------------------
    # Best-result selection logic
    # -----------------------------------------------------
    best = None
    best_conf = -1

    for r in merged:
        if "confidence" in r:
            conf = r["confidence"]
        elif "final_prediction_confidence" in r:
            conf = r["final_prediction_confidence"]
        else:
            conf = 0.0

        if conf > best_conf:
            best_conf = conf
            best = r

    logger.info("[Orchestrator] Completed successfully")

    return {
        "analyzers_run": len(merged),
        "best_result": best,
        "all_results": merged,
    }
