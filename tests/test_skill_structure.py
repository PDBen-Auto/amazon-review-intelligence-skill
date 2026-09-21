import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\n"), "SKILL.md must start with YAML frontmatter"
    frontmatter = skill.split("---", 2)[1]
    assert re.search(r"^name:\s*amazon-review-scraper\s*$", frontmatter, re.MULTILINE)
    assert re.search(r"^description:\s*\S", frontmatter, re.MULTILINE)

    markdown_files = [ROOT / "SKILL.md", ROOT / "README.md", ROOT / "README.zh-CN.md"]
    link_pattern = re.compile(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)")
    missing = []
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            target_path = target.split("#", 1)[0]
            if target_path and not (markdown_file.parent / target_path).exists():
                missing.append(f"{markdown_file.name}: {target}")
    assert not missing, "Missing local Markdown targets: " + ", ".join(missing)
    print("skill structure and local links: OK")


if __name__ == "__main__":
    main()
