"""Typed checked-in playbook registry contracts.

These schemas define the registry surfaces introduced for Gates 11-13. The
registry exists to make live playbooks and execution templates explicit
artefacts without duplicating stack-definition or coefficient-set ownership.
"""

from __future__ import annotations

from pathlib import Path
from typing import Self, cast

import yaml  # type: ignore[import-untyped]
from pydantic import BaseModel, ConfigDict, Field, model_validator

from nvda_desk.schemas.cognition import PlaybookAction, PlaybookDecision


class PlaybookDecisionProfile(BaseModel):
    """Registry-backed output contract for one playbook decision state."""

    model_config = ConfigDict(extra="forbid")

    decision: PlaybookDecision
    action_bias: PlaybookAction
    sizing_fraction: float = Field(default=0.0, ge=0.0, le=1.0)
    hedge_overlay: bool = False


class PlaybookSpec(BaseModel):
    """One checked-in live-playbook definition."""

    model_config = ConfigDict(extra="forbid")

    playbook_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    execution_template_id: str = Field(min_length=1)
    priority: int = Field(ge=1)
    active: bool = True
    eligible: PlaybookDecisionProfile
    watch_only: PlaybookDecisionProfile
    ineligible: PlaybookDecisionProfile
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_decision_profiles(self) -> Self:
        if self.eligible.decision is not PlaybookDecision.ELIGIBLE:
            raise ValueError("eligible profile must use PlaybookDecision.ELIGIBLE")
        if self.watch_only.decision is not PlaybookDecision.WATCH_ONLY:
            raise ValueError("watch_only profile must use PlaybookDecision.WATCH_ONLY")
        if self.ineligible.decision is not PlaybookDecision.INELIGIBLE:
            raise ValueError("ineligible profile must use PlaybookDecision.INELIGIBLE")
        return self


class ExecutionTemplateSpec(BaseModel):
    """Execution-shape contract shared by one or more playbooks."""

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1)
    entry_style: str = Field(min_length=1)
    watch_execution_style: str = Field(default="watchlist", min_length=1)
    scaling_step_factors: list[float] = Field(default_factory=list)
    default_inventory_action: str = Field(min_length=1)
    default_fresh_capital_action: str = Field(min_length=1)
    thesis_invalidation_state: str = Field(min_length=1)
    invalidation_reasons: list[str] = Field(default_factory=list)
    exit_reasons: list[str] = Field(default_factory=list)
    hedge_exit_reason: str = Field(default="overlay_hedge_if_gamma_reaccelerates", min_length=1)
    respect_posture_biases: bool = True
    posture_override_actions: list[str] = Field(default_factory=lambda: ["reduce", "trim", "hedge"])
    inventory_pressure_states: list[str] = Field(default_factory=lambda: ["trapped", "full"])
    inventory_pressure_exit_reason: str = Field(default="respect_inventory_pressure", min_length=1)

    @model_validator(mode="after")
    def _validate_scaling_steps(self) -> Self:
        if any(step < 0.0 for step in self.scaling_step_factors):
            raise ValueError("scaling_step_factors must be non-negative")
        return self


class PlaybookRegistryDocument(BaseModel):
    """Checked-in registry containing live playbooks and execution templates."""

    model_config = ConfigDict(extra="forbid")

    schema_version: str = Field(min_length=1)
    registry_version: str = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)
    execution_templates: list[ExecutionTemplateSpec] = Field(default_factory=list)
    playbooks: list[PlaybookSpec] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_cross_references(self) -> Self:
        template_ids = [template.template_id for template in self.execution_templates]
        if len(set(template_ids)) != len(template_ids):
            raise ValueError("execution template ids must be unique")
        playbook_ids = [playbook.playbook_id for playbook in self.playbooks]
        if len(set(playbook_ids)) != len(playbook_ids):
            raise ValueError("playbook ids must be unique")
        priorities = [playbook.priority for playbook in self.playbooks]
        if len(set(priorities)) != len(priorities):
            raise ValueError("playbook priorities must be unique")
        template_id_set = set(template_ids)
        for playbook in self.playbooks:
            if playbook.execution_template_id not in template_id_set:
                raise ValueError(
                    f"unknown execution template for playbook {playbook.playbook_id}: "
                    f"{playbook.execution_template_id}"
                )
        return self

    def ordered_playbooks(self) -> list[PlaybookSpec]:
        """Return active playbooks in deterministic priority order."""

        return sorted((playbook for playbook in self.playbooks if playbook.active), key=lambda item: item.priority)

    def execution_template_index(self) -> dict[str, ExecutionTemplateSpec]:
        """Return deterministic template lookup by id."""

        return {template.template_id: template for template in self.execution_templates}

    @classmethod
    def from_yaml_text(cls, text: str) -> PlaybookRegistryDocument:
        """Parse one checked-in YAML registry string."""

        loaded = yaml.safe_load(text)
        if not isinstance(loaded, dict):
            raise ValueError("playbook registry YAML must decode to a mapping")
        return cls.model_validate(loaded)

    @classmethod
    def from_yaml_path(cls, path: Path | str) -> PlaybookRegistryDocument:
        """Load one checked-in YAML registry file."""

        return cls.from_yaml_text(Path(path).read_text(encoding="utf-8"))

    def to_yaml_text(self) -> str:
        """Serialise the registry to deterministic YAML text."""

        return cast(str, yaml.safe_dump(self.model_dump(mode="json"), sort_keys=False, allow_unicode=False))
