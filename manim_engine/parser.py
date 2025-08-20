import re, math

def parse_prompt(p):
    s = p.lower()
    plan = {"title": None, "actions": []}
    m = re.search(r"['\"]([^'\"]+)['\"]", p)
    if "title" in s or "write" in s:
        if m:
            plan["actions"].append({"op":"title", "text":m.group(1)})
        else:
            plan["actions"].append({"op":"title", "text":p.strip()[:48]})
    if "sine" in s or "sin(" in s:
        plan["actions"].append({"op":"plot", "expr":"np.sin(x)", "x_min":"-TAU", "x_max":"TAU"})
    if "cos" in s and "plot" in s:
        plan["actions"].append({"op":"plot", "expr":"np.cos(x)", "x_min":"-TAU", "x_max":"TAU"})
    if "number line" in s:
        rng = re.search(r"(-?\d+)\s*to\s*(-?\d+)", s)
        a,b = (-5,5)
        if rng: a,b = int(rng.group(1)), int(rng.group(2))
        plan["actions"].append({"op":"number_line","start":a,"end":b})
    if "dot" in s and ("move" in s or "to" in s):
        pos = re.search(r"to\s*(-?\d+(?:\.\d+)?)", s)
        x = float(pos.group(1)) if pos else 2.0
        plan["actions"].append({"op":"move_dot","x":x})
    if "triangle" in s or "square" in s or "circle" in s:
        shape = "triangle" if "triangle" in s else "square" if "square" in s else "circle"
        plan["actions"].append({"op":"shape","shape":shape})
    if "rotate" in s:
        deg = re.search(r"(\d+)\s*deg|degrees", s)
        ang = int(deg.group(1)) if deg else 180
        plan["actions"].append({"op":"rotate","degrees":ang})
    if not plan["actions"]:
        plan["actions"].append({"op":"title","text":p.strip()[:48]})
        if "lorenz" in s or "lorentz" in s:
         plan["actions"].append({"op":"lorenz","steps":12000,"dt":0.005})
    return plan

    