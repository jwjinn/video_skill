"""Validate portable package inputs without an installed agent or Node dependencies."""
import ast
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/data-story-video"


def check():
    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    legacy = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    assert manifest["name"] == legacy["name"] == market["plugins"][0]["name"] == "data-story-video"
    assert manifest["version"] == legacy["version"]
    assert (ROOT / market["plugins"][0]["source"]["path"]).resolve() == ROOT
    assert (ROOT / legacy["skills"] / "data-story-video/SKILL.md").is_file()
    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert re.search(r"(?m)^name: data-story-video$", skill_text)
    for relative in re.findall(r"\]\((references/[^)]+)\)", skill_text):
        assert (SKILL / relative).is_file(), relative
    starter = SKILL / "assets/his01-starter"
    episode = json.loads((starter / "episode.json").read_text(encoding="utf-8"))
    assert episode["synthetic"] is True
    assert episode["chapters"][0]["chart"] == "DEMO"
    with (starter / "motion-canvas/data/sample.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 4
    assert sum(int(rows[-1][k]) for k in ("implementation", "tests", "docs")) == 6500
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in {"node_modules", ".git", ".venv", "__pycache__", ".vite-cache", "output", "work", "charts"} for part in relative.parts):
            continue
        assert not path.is_symlink(), f"Non-portable symlink: {relative}"
        if path.is_file() and path.suffix in {".py", ".md", ".json", ".yaml", ".yml", ".ts", ".mjs"}:
            text = path.read_text(encoding="utf-8")
            # Construct the pattern to keep this checker portable and self-scannable.
            private_home = "/" + "Users" + "/"
            assert private_home not in text, f"Personal filesystem path in {relative}"
            assert "fabrix" + "_endpoint" not in text.lower(), f"Private project identifier in {relative}"
            if path.suffix == ".py":
                ast.parse(text, filename=str(relative))
            if path.suffix == ".json":
                json.loads(text)
    print("PASS: plugin identity, marketplace, skill references, synthetic data, Python syntax, portable paths")


if __name__ == "__main__":
    check()
