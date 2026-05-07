from pathlib import Path


def load_skill(skill_name: str) -> str:
    """
    Load a local skill's SKILL.md content.
    """

    project_root = Path(__file__).resolve().parents[1]
    skill_path = project_root / "skills" / skill_name / "SKILL.md"

    if not skill_path.exists():
        raise FileNotFoundError(f"Skill file not found: {skill_path}")

    return skill_path.read_text(encoding="utf-8")