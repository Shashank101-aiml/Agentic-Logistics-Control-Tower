from typing import Any, Dict, Optional, Sequence

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None

from app.agents.explanation.prompt_builder import PromptBuilder


class ExplanationAgent:
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4.1",
        api_key: Optional[str] = None,
    ) -> None:
        self.provider = provider
        self.model = model

        if self.provider == "openai":
            if openai is None:
                raise ImportError(
                    "openai package is required for OpenAI explanation generation."
                )
            if api_key:
                openai.api_key = api_key

    def explain(
        self,
        route: Dict[str, Any],
        event: Optional[Dict[str, Any]] = None,
        risk: Optional[Dict[str, Any]] = None,
        recommendations: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> str:
        prompt = PromptBuilder.build_route_explanation_prompt(
            route=route,
            risk=risk,
            recommendations=recommendations,
        )
        return self._generate_explanation(prompt)

    def _generate_explanation(self, prompt: str) -> str:
        if self.provider == "openai" and openai:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an explanation agent for a maritime control system."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return response.choices[0].message["content"].strip()

        return self._fallback_explanation(prompt)

    def _fallback_explanation(self, prompt: str) -> str:
        return (
            "Route explanation generated from current system state.\n\n"
            f"{prompt}"
        )