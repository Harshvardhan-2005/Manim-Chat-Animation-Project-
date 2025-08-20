# 🎥 Manim Chat Animation

**Manim Chat Animation** is an interactive project where you can chat like **ChatGPT**, but instead of text-only responses, you get **beautiful mathematical & scientific animations** generated with [Manim](https://www.manim.community/).

✨ Think of it as **ChatGPT + Manim = Animated Explanations**.

---

## 🚀 Features
- 💬 Chat interface powered by **Streamlit**
- 🎨 Dynamic **Manim animations** generated from text prompts
- 📊 Supports mathematical functions, geometry, and even **Lorenz attractor**
- ⚡ Real-time video rendering & display
- 🎥 Export animations as `.mp4` for reuse

---

## 📸 Demo

![Demo Animation](assets/demo.gif)

---

## 📂 Project Structure
- `app.py` → Main Streamlit app (ChatGPT-style interface)  
- `manim_engine/runner.py` → Utility to run Manim and return video path  
- `manim_engine/prompts.py` → Maps natural language prompts to animations  
- `manim_engine/lorenz_scene.py` → Example animation (Lorenz attractor)  
- `requirements.txt` → Dependencies  


---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/manim-chat-env.git
cd manim-chat-env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
