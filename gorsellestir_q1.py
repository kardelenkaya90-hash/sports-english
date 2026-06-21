import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np


THIS_FILE    = os.path.abspath(__file__)
PROJE_KOKU   = os.path.dirname(os.path.dirname(THIS_FILE))
OUTPUT_DIR   = os.path.join(PROJE_KOKU, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


data = {
    "Code"    : ["speaking","professional","listening","motivation","terminology",
                 "daily_life","course_needs","social","referee","anxiety",
                 "vocabulary","education_system","foreign_coach","competition"],
    "Coach"   : [4, 4, 1, 3, 3, 1, 2, 2, 1, 0, 0, 2, 1, 2],
    "Athlete" : [7, 5, 5, 1, 3, 5, 0, 4, 3, 2, 2, 0, 1, 0],
    "Teacher" : [3, 3, 3, 3, 1, 0, 4, 0, 1, 3, 2, 1, 0, 0]
}
df = pd.DataFrame(data).set_index("Code")
df["Total"] = df.sum(axis=1)

THEMES = {
    "Theme 1\nOral Communication\nNeeds":
        {"codes": ["speaking","listening","anxiety","vocabulary"],
         "color": "#2C2C2A", "light": "#D3D1C7"},
    "Theme 2\nDomain-Specific\nLanguage":
        {"codes": ["terminology","referee","competition"],
         "color": "#5F5E5A", "light": "#E8E6DE"},
    "Theme 3\nReal-World\nContexts Abroad":
        {"codes": ["daily_life","social","foreign_coach"],
         "color": "#888780", "light": "#F1EFE8"},
    "Theme 4\nMotivation &\nProfessional Goals":
        {"codes": ["motivation","professional","education_system"],
         "color": "#B4B2A9", "light": "#F8F7F3"},
}


def chart_thematic_map():
    fig, ax = plt.subplots(figsize=(18, 11))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 11)
    ax.axis("off")

 
    rq = FancyBboxPatch((0.5, 9.3), 17, 1.3,
                        boxstyle="round,pad=0.15",
                        facecolor="#2C2C2A", edgecolor="none")
    ax.add_patch(rq)
    ax.text(9, 9.95,
            "RQ: What are the specific English language needs of Turkish national athletes\n"
            "who attend the Sports English course?",
            ha="center", va="center", fontsize=9.5,
            color="white", fontweight="bold", linespacing=1.6)

 
    xs = [2.25, 6.75, 11.25, 15.75]
    ax.plot([9, 9],   [9.3, 8.75], color="#888780", lw=1.5)           
    ax.plot([xs[0], xs[-1]], [8.75, 8.75], color="#888780", lw=1.5)   
    for x in xs:
        ax.annotate("", xy=(x, 8.25), xytext=(x, 8.75),
                    arrowprops=dict(arrowstyle="->",
                                   color="#888780", lw=1.5))

 
    theme_items = list(THEMES.items())   

    for i, (title, info) in enumerate(theme_items):
        x      = xs[i]
        color  = info["color"]
        light  = info["light"]
        codes  = info["codes"]

      
        theme_box = FancyBboxPatch((x - 1.7, 7.05), 3.4, 1.15,
                                   boxstyle="round,pad=0.1",
                                   facecolor=color, edgecolor="none")
        ax.add_patch(theme_box)
        ax.text(x, 7.625, title,
                ha="center", va="center", fontsize=8.5,
                color="white", fontweight="bold", linespacing=1.4)

        
        ax.annotate("", xy=(x, 6.72), xytext=(x, 7.05),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2))

        
        for j, code in enumerate(codes):
            total = df.loc[code, "Total"] if code in df.index else 0
            cy    = 6.4 - j * 1.15

            code_box = FancyBboxPatch((x - 1.55, cy - 0.3), 3.1, 0.6,
                                      boxstyle="round,pad=0.06",
                                      facecolor=light, edgecolor=color,
                                      linewidth=0.8)
            ax.add_patch(code_box)
            ax.text(x, cy, f"{code}  (n={total})",
                    ha="center", va="center", fontsize=8.5, color="#2C2C2A")

            
            if j < len(codes) - 1:
                ax.annotate("", xy=(x, cy - 0.3 - 0.25), xytext=(x, cy - 0.3),
                            arrowprops=dict(arrowstyle="->",
                                           color=color, lw=0.8))

    ax.text(0.01, 0.99, "Figure 1. Thematic map of English language needs",
            transform=ax.transAxes, fontsize=10, va="top",
            style="italic", color="#444441")

    path = os.path.join(OUTPUT_DIR, "figure1_thematic_map.png")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: output/figure1_thematic_map.png")



def chart_summary_table():

    table_df = df[["Coach", "Athlete", "Teacher", "Total"]].sort_values(
        "Total", ascending=False
    )

    code_to_theme = {}
    for theme_name, info in THEMES.items():
        short = theme_name.replace("\n", " ").strip()
        for c in info["codes"]:
            code_to_theme[c] = short.split("  ")[0]   


    theme_labels = {
        list(THEMES.keys())[0]: "T1",
        list(THEMES.keys())[1]: "T2",
        list(THEMES.keys())[2]: "T3",
        list(THEMES.keys())[3]: "T4",
    }
    code_to_short = {}
    for theme_name, info in THEMES.items():
        for c in info["codes"]:
            code_to_short[c] = theme_labels[theme_name]
    if "course_needs" not in code_to_short:
        code_to_short["course_needs"] = "—"

    table_df.insert(0, "Theme", [code_to_short.get(c, "—") for c in table_df.index])

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    col_labels  = ["Theme", "Code", "Coach", "Athlete", "Teacher", "Total"]
    rows        = [[row["Theme"], code] + [str(row[c]) for c in ["Coach","Athlete","Teacher","Total"]]
                   for code, row in table_df.iterrows()]

    col_widths  = [0.08, 0.20, 0.12, 0.12, 0.12, 0.10]


    header_y = 0.96
    header_x = [0.03, 0.11, 0.31, 0.43, 0.55, 0.67]
    for j, (label, x) in enumerate(zip(col_labels, header_x)):
        ax.text(x, header_y, label,
                transform=ax.transAxes, fontsize=10,
                fontweight="bold", va="top",
                ha="left" if j < 2 else "center")

 
    ax.plot([0.03, 0.78], [0.93, 0.93],
             color="#2C2C2A", lw=1.0, transform=ax.transAxes)

 
    row_height = 0.053
    for i, row in enumerate(rows):
        y     = 0.90 - i * row_height
        shade = "#F8F7F3" if i % 2 == 0 else "white"
        rect  = mpatches.FancyBboxPatch(
            (0.03, y - 0.012), 0.75, row_height - 0.004,
            boxstyle="square,pad=0", transform=ax.transAxes,
            facecolor=shade, edgecolor="none", zorder=0
        )
        ax.add_patch(rect)
        for j, (val, x) in enumerate(zip(row, header_x)):
            ax.text(x, y + 0.018, val,
                    transform=ax.transAxes, fontsize=9,
                    va="center", ha="left" if j < 2 else "center",
                    color="#2C2C2A")

   
    bottom_y = 0.90 - len(rows) * row_height + 0.01
    ax.plot([0.03, 0.78], [bottom_y, bottom_y],
             color="#2C2C2A", lw=0.8, transform=ax.transAxes)

   
    ax.text(0.03, bottom_y - 0.04,
            "Table 1. Frequency of codes across participant groups\n"
            "Note. T1=Oral Communication; T2=Domain-Specific Language; "
            "T3=Real-World Contexts; T4=Motivation & Professional Goals.",
            transform=ax.transAxes, fontsize=8.5,
            color="#5F5E5A", va="top", style="italic")

    path = os.path.join(OUTPUT_DIR, "table1_frequency_summary.png")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: output/table1_frequency_summary.png")



def chart_academic_grouped_bar():
    groups     = ["Coach", "Athlete", "Teacher"]
    grays      = ["#2C2C2A", "#888780", "#D3D1C7"]   
    hatches    = ["///", "...", ""]                  

    theme_names = ["Theme 1\nOral Comm.", "Theme 2\nDomain-Specific",
                   "Theme 3\nReal-World", "Theme 4\nMotivation &\nProfessional"]

    theme_codes = [
        ["speaking","listening","anxiety","vocabulary"],
        ["terminology","referee","competition"],
        ["daily_life","social","foreign_coach"],
        ["motivation","professional","education_system"]
    ]


    theme_totals = {
        g: [sum(df.loc[c, g] for c in codes if c in df.index)
            for codes in theme_codes]
        for g in groups
    }                  

    x      = np.arange(len(theme_names))
    width  = 0.22
    offsets = [-width, 0, width]

    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for i, (group, offset) in enumerate(zip(groups, offsets)):
        vals = theme_totals[group]
        bars = ax.bar(x + offset, vals, width,
                      label=group,
                      color=grays[i],
                      hatch=hatches[i],
                      edgecolor="white" if i == 0 else grays[i],
                      linewidth=0.5)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.2,
                        str(val),
                        ha="center", va="bottom",
                        fontsize=9, color="#2C2C2A")

    ax.set_xticks(x)
    ax.set_xticklabels(theme_names, fontsize=10)
    ax.set_ylabel("Number of coded excerpts", fontsize=10)
    ax.set_ylim(0, max(max(v) for v in theme_totals.values()) + 3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#888780")
    ax.tick_params(colors="#444441")
    ax.yaxis.grid(True, linestyle="--", alpha=0.4, color="#D3D1C7")
    ax.set_axisbelow(True)

    legend = ax.legend(title="Participant group",
                       fontsize=9, title_fontsize=9,
                       frameon=True, framealpha=0.9,
                       edgecolor="#D3D1C7")

    ax.text(0, -0.18,
            "Figure 2. Coded excerpts per theme by participant group.",
            transform=ax.transAxes, fontsize=9,
            style="italic", color="#5F5E5A", va="top")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "figure2_grouped_bar.png")
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  Saved: output/figure2_grouped_bar.png")



if __name__ == "__main__":
    print("\n" + "="*60)
    print("  SPORTS ENGLISH — Q1 JOURNAL VISUALIZATIONS")
    print("="*60 + "\n")

    chart_thematic_map()
    chart_summary_table()
    chart_academic_grouped_bar()
    

    print("\n  3 publication-ready files saved to output/")
    print("  figure1_thematic_map.png")
    print("  table1_frequency_summary.png")
    print("  figure2_grouped_bar.png\n")
