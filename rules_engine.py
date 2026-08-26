"""
Self-Correcting Rules Engine for PawPawDoo.
Parses, enforces, and appends dynamic rules to AGENT_INSTRUCTIONS.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

INSTRUCTIONS_FILE = Path(__file__).parent / "AGENT_INSTRUCTIONS.md"

VALID_CATEGORIES = {
    "BRAND",
    "CRO",
    "CODE",
    "ARCH",
    "TOOL",
    "PROCESS",
    "DATA",
    "UX",
    "FINANCE",
    "PRICING",
    "SUPPLIER",
    "LOGISTICS",
    "OPPORTUNITY",
    "OTHER",
}


class LearnedRule(BaseModel):
    number: int
    category: str
    text: str
    raw_line: str


class RulesEngine:
    def __init__(self, instructions_path: Path = INSTRUCTIONS_FILE):
        self.instructions_path = instructions_path

    def load_rules(self) -> List[LearnedRule]:
        """Reads AGENT_INSTRUCTIONS.md and extracts all numbered rules."""
        if not self.instructions_path.exists():
            return []

        content = self.instructions_path.read_text(encoding="utf-8")
        rules: List[LearnedRule] = []

        # Find the ## Learned Rules section
        learned_section_match = re.search(r"## Learned Rules(.*?)(?:$)", content, re.DOTALL)
        if not learned_section_match:
            return []

        section_text = learned_section_match.group(1)
        # Regex to capture: N. [CATEGORY] Rule content
        rule_pattern = re.compile(r"^(\d+)\.\s*\[([A-Z_]+)\]\s*(.+)$", re.MULTILINE)

        for match in rule_pattern.finditer(section_text):
            num = int(match.group(1))
            cat = match.group(2).upper()
            text = match.group(3).strip()
            rules.append(
                LearnedRule(
                    number=num,
                    category=cat,
                    text=text,
                    raw_line=match.group(0).strip(),
                )
            )

        rules.sort(key=lambda r: r.number)
        return rules

    def get_next_rule_number(self) -> int:
        rules = self.load_rules()
        if not rules:
            return 1
        return max(r.number for r in rules) + 1

    def append_rule(
        self,
        category: str,
        instruction: str,
        reason: Optional[str] = None,
        supersede_rule_no: Optional[int] = None,
    ) -> LearnedRule:
        """
        Appends a newly learned rule to AGENT_INSTRUCTIONS.md adhering to format:
        N. [CATEGORY] Never/Always do X — because Y.
        """
        category_clean = category.upper().strip("[] ")
        if category_clean not in VALID_CATEGORIES:
            category_clean = "OTHER"

        next_num = self.get_next_rule_number()

        # Format rule statement
        statement = instruction.strip()
        if supersede_rule_no:
            statement = f"Supersedes Rule #{supersede_rule_no}: {statement}"

        if reason and "—" not in statement and "because" not in statement.lower():
            rule_body = f"{statement} — because {reason.strip()}."
        else:
            rule_body = statement

        formatted_line = f"{next_num}. [{category_clean}] {rule_body}"

        content = self.instructions_path.read_text(encoding="utf-8")
        
        # Ensure trailing newline
        if not content.endswith("\n"):
            content += "\n"

        updated_content = content + formatted_line + "\n"
        self.instructions_path.write_text(updated_content, encoding="utf-8")

        new_rule = LearnedRule(
            number=next_num,
            category=category_clean,
            text=rule_body,
            raw_line=formatted_line,
        )
        return new_rule

    def format_rules_for_prompt(self) -> str:
        """Returns a clean formatted markdown list of active rules for system prompts."""
        rules = self.load_rules()
        if not rules:
            return "No learned rules yet."
        return "\n".join(r.raw_line for r in rules)


# Global singleton helper
rules_engine = RulesEngine()
