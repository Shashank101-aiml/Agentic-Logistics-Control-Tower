import os
from typing import Any, Dict, Optional, Sequence

from openai import OpenAI

from app.agents.explanation.prompt_builder import PromptBuilder


class ExplanationAgent:
    """
    Generates human-readable explanations for route decisions.

    Uses OpenAI when an API key is configured.
    Falls back to a deterministic explanation when no API key is available.
    """

    def __init__(
        self,
        model: str = "gpt-4.1",
        api_key: Optional[str] = None,
    ) -> None:

        self.model = model

        self.api_key = (
            api_key
            or os.getenv("OPENAI_API_KEY")
        )

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key
            )

    def explain(
        self,
        route: Dict[str, Any],
        event: Optional[Dict[str, Any]] = None,
        risk: Optional[Dict[str, Any]] = None,
        recommendations: Optional[
            Sequence[Dict[str, Any]]
        ] = None,
    ) -> str:

        prompt = (
            PromptBuilder
            .build_route_explanation_prompt(
                route=route,
                risk=risk,
                recommendations=recommendations,
            )
        )

        if self.client:
            try:
                return self._generate_explanation(
                    prompt
                )
            except Exception:
                return self._fallback_explanation(
                    route=route,
                    event=event,
                    risk=risk,
                )

        return self._fallback_explanation(
            route=route,
            event=event,
            risk=risk,
        )

    def _generate_explanation(
        self,
        prompt: str,
    ) -> str:

        response = (
            self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI maritime logistics "
                            "decision explanation agent. Explain "
                            "route decisions clearly using the "
                            "provided risk, cost, delay, distance "
                            "and route information."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.3,
            )
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    def _fallback_explanation(
        self,
        route: Dict[str, Any],
        event: Optional[Dict[str, Any]],
        risk: Optional[Dict[str, Any]],
    ) -> str:

        event_type = (
            event.get("event_type", "operational event")
            if event
            else "operational event"
        )

        risk_score = (
            risk.get("score", risk.get("risk_score", "unknown"))
            if risk
            else "unknown"
        )

        selected_route = (
            route.get("route")
            or route.get("name")
            or "recommended route"
        )

        decision = route.get(
            "decision",
            {}
        )

        decision_score = (
            decision.get("decision_score")
            or route.get("decision_score")
            or "N/A"
        )

        return (
            f"The system detected a {event_type} event with "
            f"an assessed risk score of {risk_score}. "
            f"The selected recommendation is "
            f"'{selected_route}'. "
            f"This decision was produced by evaluating "
            f"route risk, estimated cost, operational delay, "
            f"and total distance. "
            f"The final decision score is {decision_score}. "
            f"The recommendation is therefore based on "
            f"multi-criteria route optimization rather than "
            f"a fixed or hardcoded route selection."
        )