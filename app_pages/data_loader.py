"""Pure data-loading utilities — no Streamlit UI code here.
Imported by both streamlit_app.py and load_data.py without side effects.
"""
import json
import io
import pathlib
import pandas as pd
import streamlit as st

REPO_ROOT = pathlib.Path(__file__).parent.parent  # app_pages/ → project root


def build_tag_display(rubric: dict) -> dict:
    """Flatten tag_display from rubric into {tag: Chinese_name}."""
    result = {}
    for question_tags in rubric.get("tag_display", {}).values():
        if isinstance(question_tags, dict):
            result.update(question_tags)
    return result


@st.cache_data
def parse_csv(content: bytes) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(content))


def load_default_data():
    """自動找 repo 根目錄下最新的 W* 資料夾並載入所有資料。"""
    candidates = sorted(REPO_ROOT.glob("W*/"))
    if not candidates:
        return None, None, None, None, {}, None
    base_path = candidates[-1]

    rubric_path = base_path / "rubric.json"
    wf1_path    = base_path / "wf1_results.json"
    wf2_path    = base_path / "wf2_report.json"
    config_path = base_path / "config.json"
    csv_candidates = list(base_path.glob("*.csv"))
    csv_path = csv_candidates[0] if csv_candidates else None

    rubric = wf1 = wf2 = csv_df = config = None
    tag_display = {}

    if rubric_path.exists():
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        tag_display = build_tag_display(rubric)
    if wf1_path.exists():
        wf1 = json.loads(wf1_path.read_text(encoding="utf-8"))
    if wf2_path.exists():
        wf2 = json.loads(wf2_path.read_text(encoding="utf-8"))
    if csv_path and csv_path.exists():
        csv_df = parse_csv(csv_path.read_bytes())
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))

    return rubric, wf1, wf2, csv_df, tag_display, config
