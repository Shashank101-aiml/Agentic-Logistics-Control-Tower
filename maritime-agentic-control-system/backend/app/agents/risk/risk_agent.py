class RiskAgent:
    def calculate_risk(self, event):
        if event["severity"] == "HIGH":
            return 85
        return 20