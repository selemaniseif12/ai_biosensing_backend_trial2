# app/models/analyzer_v6_model.py

class DummyAnalyzerV6Model:
    def predict(self, X):
        # Always return a fixed value for now
        return [42.0]

# Export the model instance
analyzer_v6 = DummyAnalyzerV6Model()
