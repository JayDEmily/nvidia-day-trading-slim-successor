"""Checked-in playbook registry loading and lookup helpers."""

from __future__ import annotations

from pathlib import Path

from nvda_desk.config import Settings
from nvda_desk.schemas.playbook_registry import (
    ExecutionTemplateSpec,
    PlaybookRegistryDocument,
    PlaybookSpec,
)


class PlaybookRegistryService:
    """Load and expose the checked-in playbook registry deterministically.

    Purpose:
        Make live playbook and execution-template lookup come from the checked-in registry.
    Inputs:
        Optional registry path override; otherwise uses `Settings.playbook_registry_path`.
    Outputs:
        Typed playbook ordering, playbook specs, and execution-template specs.
    Determinism:
        Loads one checked-in YAML file with no live calls or hidden fallbacks.
    """

    def __init__(self, registry_path: Path | str | None = None):
        if registry_path is None:
            registry_path = Settings().playbook_registry_path
        self._registry_path = Path(registry_path)
        self._document: PlaybookRegistryDocument | None = None

    def document(self) -> PlaybookRegistryDocument:
        """Return the cached typed registry document."""

        if self._document is None:
            self._document = PlaybookRegistryDocument.from_yaml_path(self._registry_path)
        return self._document

    def ordered_playbooks(self) -> list[PlaybookSpec]:
        """Return active playbooks in deterministic registry priority order."""

        return self.document().ordered_playbooks()

    def active_playbook_ids(self) -> list[str]:
        """Return active playbook ids in deterministic priority order."""

        return [playbook.playbook_id for playbook in self.ordered_playbooks()]

    def playbook_index(self) -> dict[str, PlaybookSpec]:
        """Return deterministic playbook lookup by id."""

        return {playbook.playbook_id: playbook for playbook in self.document().playbooks}

    def template_index(self) -> dict[str, ExecutionTemplateSpec]:
        """Return deterministic execution-template lookup by id."""

        return self.document().execution_template_index()

    def playbook(self, playbook_id: str) -> PlaybookSpec:
        """Return one playbook spec by id."""

        return self.playbook_index()[playbook_id]

    def template(self, template_id: str) -> ExecutionTemplateSpec:
        """Return one execution-template spec by id."""

        return self.template_index()[template_id]

    def template_for_playbook(self, playbook_id: str) -> ExecutionTemplateSpec:
        """Return the execution template linked to one playbook id."""

        return self.template(self.playbook(playbook_id).execution_template_id)
