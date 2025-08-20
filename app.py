import os, time, uuid, subprocess, sys
import streamlit as st
from pathlib import Path
from manim_engine.parser import parse_prompt
from manim_engine.runner import build_scene_file, run_manim, guess_video_path

st.set_page_config(page_title="Manim Chat Animator", page_icon="✨", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "quality" not in st.session_state:
    st.session_state.quality = "medium"
if "last_video" not in st.session_state:
    st.session_state.last_video = None

with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state.theme = st.selectbox("Theme", ["Dark", "Light"], index=0)
    st.session_state.quality = st.selectbox("Render quality", ["low", "medium", "high"], index=1)
    st.caption("Low = faster, High = slower but sharper")
    st.markdown("---")
    st.write("Outputs")
    if st.session_state.last_video and Path(st.session_state.last_video).exists():
        st.download_button("Download last video", data=open(st.session_state.last_video, "rb").read(), file_name=Path(st.session_state.last_video).name)

st.title("🎬 Manim Chat Animator")
st.caption("Enter a prompt; the app parses it into a Manim scene and returns an animation.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if m["type"] == "text":
            st.markdown(m["content"])
        elif m["type"] == "video":
            st.video(m["content"])

prompt = st.chat_input("Describe the animation you want...")

def quality_flag(q):
    return {"low":"-ql","medium":"-qm","high":"-qh"}.get(q,"-qm")

outputs_dir = Path("outputs"); outputs_dir.mkdir(exist_ok=True)

if prompt:
    st.session_state.messages.append({"role":"user","type":"text","content":prompt})
    with st.chat_message("assistant"):
        status = st.status("Parsing prompt...", expanded=True)
        try:
            plan = parse_prompt(prompt)
            status.update(label="Building scene...", state="running")
            scene_code, scene_class, scene_slug = build_scene_file(plan)
            scene_file = outputs_dir / f"{scene_slug}.py"
            scene_file.write_text(scene_code, encoding="utf-8")
            status.update(label="Rendering with Manim...", state="running")
            manim_cmd = ["manim", quality_flag(st.session_state.quality), "-o", f"{scene_slug}.mp4", str(scene_file), scene_class]
            run_manim(manim_cmd, status)
            video_path = guess_video_path(scene_slug)
            if video_path and Path(video_path).exists():
                st.session_state.messages.append({"role":"assistant","type":"video","content":video_path})
                st.video(video_path)
                st.session_state.last_video = video_path
                status.update(label="Done ✔️", state="complete")
            else:
                st.session_state.messages.append({"role":"assistant","type":"text","content":"Render completed but video not found."})
                st.markdown("Render completed but video not found.")
                status.update(label="Render finished, but could not locate the MP4.", state="error")
        except Exception as e:
            st.session_state.messages.append({"role":"assistant","type":"text","content":f"Error: {e}"})
            st.error(f"Error: {e}")
            status.update(label="Failed", state="error")
