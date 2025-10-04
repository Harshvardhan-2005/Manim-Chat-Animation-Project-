# 🎬 Manim Chat Animation

A fun and interactive project that combines **ChatGPT-style prompts** with **Manim animations**.  
Just type what you want (e.g., "Show me a Lorenz attractor") and get a generated animation right in your browser!

---

## 🚀 Features
- 🖥️ Chat-like interface built with **Streamlit**
- 🎞️ Dynamic animations powered by **Manim**
- ✨ Supports multiple scenes (Lorenz Attractor, Graphs, Equations, etc.)
- 📦 Modular design: easy to add new animations
- 🌐 Runs locally with no extra setup beyond Python

---

## 📂 Project Structure
- `app.py` → Main Streamlit app (ChatGPT-style interface)  
- `manim_engine/runner.py` → Utility to run Manim and return video path  
- `manim_engine/prompts.py` → Maps natural language prompts to animations  
- `manim_engine/lorenz_scene.py` → Example animation (Lorenz attractor)  
- `requirements.txt` → Dependencies  

---

## 🛠️ Installation Guide

```bash
git clone https://github.com/your-username/manim-chat-env.git
cd manim-chat-env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
