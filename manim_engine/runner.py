from pathlib import Path
import subprocess, os, sys, textwrap

def build_scene_file(plan):
    slug = "scene_" + str(abs(hash(str(plan))))[:10]
    cls = "AutoScene"
    code = make_scene_code(plan, cls)
    return code, cls, slug

def run_manim(cmd, status=None):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = []
    while True:
        line = p.stdout.readline()
        if not line and p.poll() is not None:
            break
        if line:
            lines.append(line)
            if status: status.write(line.strip())
    if p.returncode != 0:
        raise RuntimeError("Manim failed with return code %d" % p.returncode)
    return "\n".join(lines)

def guess_video_path(slug):
    p = Path("media/videos")
    if not p.exists():
        return str(Path("outputs")/f"{slug}.mp4")
    for sub in p.rglob(f"{slug}.mp4"):
        return str(sub)
    out = Path("outputs")/f"{slug}.mp4"
    if out.exists():
        return str(out)
    return None

def make_scene_code(plan, cls):
    actions = plan.get("actions", [])
    lines = []
    lines.append("from manim import *")
    lines.append("import numpy as np")
    lines.append(f"class {cls}(Scene):")
    lines.append("    def construct(self):")
    indent = "        "
    title_added = False
    for a in actions:
        op = a.get("op")
        if op == "title" and not title_added:
            t = repr(a.get("text","Title"))
            lines.append(indent + f"title = Text({t}).scale(0.9)")
            lines.append(indent + "self.play(Write(title))")
            lines.append(indent + "self.wait(0.5)")
            title_added = True
        elif op == "plot":
            expr = a.get("expr","np.sin(x)")
            x_min = a.get("x_min","-TAU")
            x_max = a.get("x_max","TAU")
            lines.append(indent + "ax = Axes(x_range=["+str(x_min)+","+str(x_max)+",1], y_range=[-1.5,1.5,0.5], tips=False)")
            lines.append(indent + "self.play(Create(ax))")
            lines.append(indent + "g = ax.plot(lambda x: " + expr + ")")
            lines.append(indent + "self.play(Create(g))")
            lines.append(indent + "self.wait(0.5)")
        elif op == "number_line":
            start, end = a.get("start",-5), a.get("end",5)
            lines.append(indent + f"nl = NumberLine(x_range=[{start},{end},1], include_numbers=True)")
            lines.append(indent + "self.play(Create(nl))")
            lines.append(indent + "self.wait(0.3)")
        elif op == "move_dot":
            x = a.get("x",2.0)
            lines.append(indent + "if 'nl' not in locals():")
            lines.append(indent + "    nl = NumberLine(x_range=[-5,5,1], include_numbers=True)")
            lines.append(indent + "    self.play(Create(nl))")
            lines.append(indent + "dot = Dot(nl.n2p(0))")
            lines.append(indent + "self.add(dot)")
            lines.append(indent + f"self.play(dot.animate.move_to(nl.n2p({x})))")
            lines.append(indent + "self.wait(0.3)")
        elif op == "shape":
            s = a.get("shape","circle")
            if s == "triangle":
                lines.append(indent + "m = Triangle().scale(1.2)")
            elif s == "square":
                lines.append(indent + "m = Square().scale(1.2)")
            else:
                lines.append(indent + "m = Circle().scale(1.2)")
            lines.append(indent + "self.play(Create(m))")
            lines.append(indent + "self.wait(0.3)")
        elif op == "rotate":
            deg = a.get("degrees",180)
            lines.append(indent + f"self.play(Rotate(m if 'm' in locals() else Dot(), angle={deg}*DEGREES))")
            lines.append(indent + "self.wait(0.3)")
            
    lines.append(indent + "self.wait(0.7)")
    return "\n".join(lines)
