class RouteAgent:

    def suggest_route(self, risk_score):

        if risk_score > 80:

            return {
                "route": "Cape of Good Hope",
                "reason": "High Storm Risk"
            }

        return {
            "route": "Suez Canal",
            "reason": "Safe"
        }