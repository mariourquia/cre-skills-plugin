"""Regression guard for GitHub issue #56.

`claude plugin install cre-skills@cre-skills` rejected `.claude-plugin/plugin.json`
because the runtime schema (confirmed against Claude Code 2.1.311) requires:

- every `userConfig` option to have a string `title` (and `description` / `type`);
- no unrecognized keys inside a `userConfig` option (`enum` is rejected;
  fixed choices belong in `options`);
- `agents`, when set, to be `.md` files. A directory string such as
  `./src/agents/` fails with `agents: Invalid input` / `must end with ".md"`.

Nested files under `src/agents/<category>/` are orchestrator-internal and are
not part of the user-invocable roster (see scripts/registry-validator.py).
The manifest lists only the flat `src/agents/*.md` personas, excluding
`_index.md`, which is a roster index rather than an agent.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"
AGENTS_DIR = REPO_ROOT / "src" / "agents"

# Strict userConfig object. Unknown keys fail plugin load.
# https://code.claude.com/docs/en/plugins/manifest-reference
USER_CONFIG_KEYS = frozenset({
    "type",
    "title",
    "description",
    "required",
    "default",
    "options",
    "multiple",
    "sensitive",
    "min",
    "max",
})
USER_CONFIG_TYPES = frozenset({"string", "number", "boolean", "directory", "file"})
# Choices that used to live in `enum` (issue #56). Kept here so a regression
# that drops them from `description` or `options` is visible.
ENUMERATED_FIELDS = {
    "default_output_style": (
        "exec-brief",
        "ic-memo",
        "pm-action-list",
        "lender-brief",
        "lp-update",
    ),
    "feedback_mode": (
        "local_only",
        "ask_each_time",
        "anonymous_remote",
        "remote_with_contact",
    ),
    "customization_feedback_mode": (
        "off",
        "metadata_only",
        "metadata_and_summary",
        "metadata_and_diff",
        "metadata_and_content",
    ),
}


def _manifest() -> dict:
    return json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))


def _component_path(value: str) -> Path:
    assert isinstance(value, str), value
    assert value.startswith("./"), f"component path must start with ./ ({value})"
    assert ".." not in Path(value).parts, f"component path escapes the plugin root ({value})"
    resolved = (REPO_ROOT / value[2:]).resolve()
    assert str(resolved).startswith(str(REPO_ROOT.resolve())), value
    assert resolved.exists(), f"component path does not exist: {value}"
    return resolved


def test_user_config_matches_runtime_schema() -> None:
    """The #56 failures: missing title, and unrecognized `enum`."""
    user_config = _manifest()["userConfig"]
    assert user_config, "userConfig must stay declared"
    for key, option in user_config.items():
        assert isinstance(option, dict), key
        unknown = set(option) - USER_CONFIG_KEYS
        assert not unknown, f"userConfig.{key} has unrecognized keys {sorted(unknown)}"
        assert option.get("type") in USER_CONFIG_TYPES, key
        assert isinstance(option.get("title"), str) and option["title"].strip(), (
            f"userConfig.{key}.title must be a non-empty string"
        )
        assert isinstance(option.get("description"), str) and option["description"].strip(), (
            f"userConfig.{key}.description must be a non-empty string"
        )
        assert "enum" not in option, f"userConfig.{key} still uses enum (issue #56)"
        if "options" in option:
            assert option["type"] == "string", key
            assert option.get("multiple") is not True
            assert option.get("sensitive") is not True
            options = option["options"]
            assert isinstance(options, list) and options, key
            assert all(isinstance(item, str) and 1 <= len(item) <= 64 for item in options), key
            if "default" in option:
                assert option["default"] in options, f"userConfig.{key} default not in options"


def test_enumerated_choices_remain_documented() -> None:
    """Replacing `enum` must not drop the choice list the settings UI described."""
    user_config = _manifest()["userConfig"]
    for key, choices in ENUMERATED_FIELDS.items():
        option = user_config[key]
        if "options" in option:
            assert tuple(option["options"]) == choices, key
        else:
            description = option["description"]
            missing = [choice for choice in choices if choice not in description]
            assert not missing, f"userConfig.{key} description dropped {missing}"


def test_agents_are_markdown_files_not_a_directory() -> None:
    """`agents: ./src/agents/` is invalid input. List persona markdown files."""
    agents = _manifest()["agents"]
    assert isinstance(agents, list) and agents, "agents must be a non-empty array of .md paths"
    listed: list[Path] = []
    for entry in agents:
        assert isinstance(entry, str), entry
        assert entry.endswith(".md"), f"agents entry must end with .md ({entry})"
        path = _component_path(entry)
        assert path.is_file(), entry
        assert path.parent == AGENTS_DIR, (
            f"{entry} is nested; the manifest must not point at a directory, "
            "and nested orchestrator agents are not the user-invocable roster"
        )
        assert path.name != "_index.md"
        listed.append(path)
    expected = sorted(
        path for path in AGENTS_DIR.glob("*.md") if path.name != "_index.md"
    )
    assert listed == expected, (
        "plugin.json agents drifted from src/agents/*.md "
        "(excluding _index.md)"
    )


def test_component_paths_exist_inside_the_plugin_root() -> None:
    manifest = _manifest()
    skills = _component_path(manifest["skills"])
    assert skills.is_dir()
    commands = _component_path(manifest["commands"])
    assert commands.is_dir()
    hooks = _component_path(manifest["hooks"])
    assert hooks.is_file()
    mcp = _component_path(manifest["mcpServers"])
    assert mcp.is_file()
    icon = _component_path(manifest["interface"]["composerIcon"])
    assert icon.is_file()
    assert _component_path(manifest["interface"]["logo"]) == icon
