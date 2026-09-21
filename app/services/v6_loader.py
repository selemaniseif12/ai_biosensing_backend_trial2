import importlib

def load_v6():
    module = importlib.import_module("app.services.analyzer_v6_service")
    return getattr(module, "run_analyzer_v6")
