"""載入資料頁面 — 純 UI，不含任何被其他模組 import 的函式。"""
import streamlit as st
from app_pages.data_loader import load_default_data

# ── 頁面 UI ──────────────────────────────────────────────────────────────────
st.title("📂 資料載入狀態")
st.caption("系統會自動從最新的 W* 資料夾讀取資料，以下為目前載入狀況。")

rubric = st.session_state.get("rubric")
wf1    = st.session_state.get("wf1")
wf2    = st.session_state.get("wf2")
csv_df = st.session_state.get("csv_df")
config = st.session_state.get("viz_config")

def status(ok):
    return "✅ 已載入" if ok else "❌ 未載入"

st.markdown("### 自動載入結果")
col1, col2 = st.columns(2)
with col1:
    st.write(f"{status(rubric)}　**rubric.json**")
    st.write(f"{status(wf1)}　**wf1_results.json**")
with col2:
    st.write(f"{status(wf2)}　**wf2_report.json**")
    st.write(f"{status(csv_df is not None)}　**CSV 原始資料**")
    st.write(f"{status(config)}　**config.json**")

all_loaded = all([rubric, wf1, wf2, csv_df is not None, config])

if all_loaded:
    st.success("✅ 所有資料已成功載入，可前往分析頁面。")
else:
    st.warning("部分資料未載入，請確認 W13/ 資料夾內的檔案是否齊全，且 config.json 放在 W13/ 內而非根目錄。")
    if st.button("🔄 重新載入"):
        result = load_default_data()
        if result is not None:
            rubric, wf1, wf2, csv_df, tag_display, config = result
            if rubric:
                st.session_state.rubric = rubric
                st.session_state.tag_display = tag_display
            if wf1:
                st.session_state.wf1 = wf1
                st.session_state.wf1_by_index = {r["student_index"]: r for r in wf1}
            if wf2:
                st.session_state.wf2 = wf2
            if csv_df is not None:
                st.session_state.csv_df = csv_df
            if config:
                st.session_state.viz_config = config
            st.rerun()
