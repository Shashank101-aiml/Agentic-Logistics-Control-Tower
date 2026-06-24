#calls gemini as of now no gemini yet, just trying to make it work
class ExplanationAgent:

    def explain(self, route):

        return (
            f"Route changed because "
            f"{route['reason']}"
        )