

import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')                       
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

THIS_FILE    = os.path.abspath(__file__)
PROJE_KOKU   = os.path.dirname(os.path.dirname(THIS_FILE))
CIKTI_KLASOR = os.path.join(PROJE_KOKU, "cikti")
os.makedirs(CIKTI_KLASOR, exist_ok=True)


RENKLER = {
    "Antrenör" : "#534AB7",   
    "Sporcu"   : "#1D9E75",   
    "Öğretmen" : "#D85A30"  
}


data = {
    "Kod"       : ["speaking","professional","listening","motivation","terminology",
                   "daily_life","course_needs","social","referee","anxiety",
                   "vocabulary","education_system","foreign_coach","competition"],
    "Antrenör"  : [4, 4, 1, 3, 3, 1, 2, 2, 1, 0, 0, 2, 1, 2],
    "Sporcu"    : [7, 5, 5, 1, 3, 5, 0, 4, 3, 2, 2, 0, 1, 0],
    "Öğretmen"  : [3, 3, 3, 3, 1, 0, 4, 0, 1, 3, 2, 1, 0, 0]
}

df = pd.DataFrame(data).set_index("Kod")
df["TOTAL"] = df.sum(axis=1)              
df = df.sort_values("TOTAL", ascending=True) 



def chart1_stacked_bar():
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    katilimcilar = ["Antrenör", "Sporcu", "Öğretmen"]
    kodlar       = df.index.tolist()


    y_positions = list(range(len(kodlar)))

    lefts = [0] * len(kodlar)   

    for katilimci in katilimcilar:
        degerler = df[katilimci].tolist()
        ax.barh(y_positions, degerler, left=lefts,
                color=RENKLER[katilimci], label=katilimci,
                edgecolor="white", linewidth=0.5)

        
        for pos, val, left in zip(y_positions, degerler, lefts):
            if val > 0:
                ax.text(left + val / 2, pos, str(val),
                        ha="center", va="center",
                        color="white", fontsize=9, fontweight="bold")

       
        lefts = [l + v for l, v in zip(lefts, degerler)]

   
    for pos, total in zip(y_positions, df["TOTAL"].tolist()):
        ax.text(total + 0.15, pos, f"n={total}",
                va="center", fontsize=9,
                color="#444441")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(kodlar, fontsize=11)
    ax.set_xlabel("Number of coded excerpts", fontsize=11)
    ax.set_title("Code Frequency by Participant Group", fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="lower right", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(0, df["TOTAL"].max() + 2)

    plt.tight_layout()
    yol = os.path.join(CIKTI_KLASOR, "chart1_stacked_bar.png")
    plt.savefig(yol, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: cikti/chart1_stacked_bar.png")



def chart2_heatmap():
    katilimcilar = ["Antrenör", "Sporcu", "Öğretmen"]
    matris = df[katilimcilar]         

    fig, ax = plt.subplots(figsize=(7, 9))
    fig.patch.set_facecolor("white")

  
    im = ax.imshow(matris.values, cmap="Blues", aspect="auto")

    ax.set_xticks(range(len(katilimcilar)))
    ax.set_xticklabels(katilimcilar, fontsize=11)
    ax.set_yticks(range(len(matris)))
    ax.set_yticklabels(matris.index.tolist(), fontsize=10)

   
    for i in range(len(matris)):
        for j in range(len(katilimcilar)):
            val = matris.values[i, j]
            renk = "white" if val >= 4 else "#2C2C2A"
            ax.text(j, i, str(val), ha="center", va="center",
                    fontsize=11, color=renk, fontweight="bold")

    ax.set_title("Heatmap: Code Frequency per Participant Group",
                 fontsize=13, fontweight="bold", pad=12)
    plt.colorbar(im, ax=ax, label="Number of excerpts")
    plt.tight_layout()

    yol = os.path.join(CIKTI_KLASOR, "chart2_heatmap.png")
    plt.savefig(yol, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: cikti/chart2_heatmap.png")



def chart3_themes():
   
    temalar = {
        "Theme 1\nOral Communication" : ["speaking", "listening", "anxiety", "vocabulary"],
        "Theme 2\nDomain-Specific Language" : ["terminology", "referee", "competition"],
        "Theme 3\nReal-World Contexts Abroad" : ["daily_life", "social", "foreign_coach"],
        "Theme 4\nMotivation & Professional Goals" : ["motivation", "professional", "education_system"]
    }

    katilimcilar = ["Antrenör", "Sporcu", "Öğretmen"]

 
    tema_df = pd.DataFrame({
        tema: {k: df.loc[[kod for kod in kodlar if kod in df.index], k].sum()
               for k in katilimcilar}
        for tema, kodlar in temalar.items()
    }).T

    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    x      = np.arange(len(temalar))
    width  = 0.25
    offsets = [-width, 0, width]

    for i, (katilimci, offset) in enumerate(zip(katilimcilar, offsets)):
        degerler = tema_df[katilimci].tolist()
        bars = ax.bar(x + offset, degerler, width,
                      label=katilimci, color=list(RENKLER.values())[i],
                      edgecolor="white")
        for bar, val in zip(bars, degerler):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.15,
                        str(val), ha="center", va="bottom",
                        fontsize=9, color="#444441")

    ax.set_xticks(x)
    ax.set_xticklabels(tema_df.index.tolist(), fontsize=10)
    ax.set_ylabel("Total coded excerpts", fontsize=11)
    ax.set_title("Theme Clusters by Participant Group", fontsize=14,
                 fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    yol = os.path.join(CIKTI_KLASOR, "chart3_themes.png")
    plt.savefig(yol, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: cikti/chart3_themes.png")



def chart4_donut():
    
    tema_totals = {
        "Oral\nCommunication"       : sum(df.loc[k, "TOTAL"] for k in ["speaking","listening","anxiety","vocabulary"] if k in df.index),
        "Motivation &\nProfessional": sum(df.loc[k, "TOTAL"] for k in ["motivation","professional","education_system"] if k in df.index),
        "Real-World\nContexts"      : sum(df.loc[k, "TOTAL"] for k in ["daily_life","social","foreign_coach"] if k in df.index),
        "Domain-Specific\nLanguage" : sum(df.loc[k, "TOTAL"] for k in ["terminology","referee","competition"] if k in df.index),
        "Course\nNeeds"             : df.loc["course_needs", "TOTAL"] if "course_needs" in df.index else 0
    }

    labels  = list(tema_totals.keys())
    values  = list(tema_totals.values())
    colors  = ["#534AB7", "#1D9E75", "#D85A30", "#E9A227", "#888780"]

    fig, ax = plt.subplots(figsize=(8, 7))
    fig.patch.set_facecolor("white")

    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        colors=colors,
        autopct="%1.0f%%",
        startangle=140,
        pctdistance=0.78,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2}
    )

    for at in autotexts:
        at.set_fontsize(11)
        at.set_color("white")
        at.set_fontweight("bold")

   
    legenda = [mpatches.Patch(color=c, label=f"{l.replace(chr(10), ' ')}  (n={v})")
               for l, v, c in zip(labels, values, colors)]
    ax.legend(handles=legenda, loc="lower center",
              bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=10,
              frameon=False)

    ax.set_title("Distribution of Coded Excerpts by Theme",
                 fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()

    yol = os.path.join(CIKTI_KLASOR, "chart4_donut.png")
    plt.savefig(yol, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: cikti/chart4_donut.png")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  SPORTS ENGLISH — VISUALIZATION")
    print("="*60 + "\n")

    chart1_stacked_bar()
    chart2_heatmap()
    chart3_themes()
    chart4_donut()

    print("\n  All charts saved to cikti/ folder.")
    print("  Open the folder to view your visualizations.\n")

    
