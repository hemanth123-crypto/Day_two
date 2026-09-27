from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up high-res figure
fig, ax = plt.subplots(figsize=(16, 10), dpi=300)
fig.patch.set_facecolor('#090d16')
ax.set_facecolor('#090d16')

# Color palette
C_BG = '#0f172a'
C_BORDER = '#334155'
C_CYAN = '#06b6d4'
C_VIOLET = '#8b5cf6'
C_EMERALD = '#10b981'
C_AMBER = '#f59e0b'
C_TEXT = '#f8fafc'
C_MUTED = '#94a3b8'

# Draw section boxes
def draw_box(x, y, w, h, title, subtitle, color, icon_text=""):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=1.8, edgecolor=color, facecolor=C_BG,
        zorder=2
    )
    ax.add_patch(box)
    
    # Title
    ax.text(x + w/2, y + h - 0.05, title, ha='center', va='top', fontsize=12, fontweight='bold', color=C_TEXT, zorder=3)
    # Subtitle / description
    ax.text(x + w/2, y + 0.04, subtitle, ha='center', va='bottom', fontsize=9, color=C_MUTED, zorder=3)

# Draw arrows
def draw_arrow(x1, y1, x2, y2, label=""):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color=C_CYAN, lw=2, mutation_scale=15),
        zorder=4
    )
    if label:
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.text(mx, my + 0.02, label, ha='center', va='bottom', fontsize=8, color=C_CYAN, fontweight='semibold', zorder=5)

# Layer 1: User & Interface (Top)
draw_box(0.35, 0.84, 0.30, 0.12, "Student / User Interface", "React 18 + Vite + TypeScript + Tailwind CSS\nInteractive Discovery, Gap Studio & Timeline", C_CYAN)

# Layer 2: API Gateway / FastAPI
draw_box(0.35, 0.64, 0.30, 0.12, "FastAPI Microservice Layer", "REST Endpoints: /search, /recommendations,\n/skills/analyze, /learning-path, /feedback", C_VIOLET)
draw_arrow(0.50, 0.84, 0.50, 0.76, "Natural Language Query")
draw_arrow(0.52, 0.76, 0.52, 0.84, "Structured JSON Response")

# Layer 3: Query Understanding & Offline Knowledge Base
draw_box(0.05, 0.44, 0.25, 0.12, "Query Understanding", "Regex & Intent Parser\nExtracts Skills, Career & Difficulty", C_CYAN)
draw_box(0.375, 0.44, 0.25, 0.12, "Knowledge Base", "Skill Taxonomy (60+ Skills)\nCareer Competency Maps", C_VIOLET)
draw_box(0.70, 0.44, 0.25, 0.12, "Course Data Pipeline", "Coursera CSV Preprocessing\nCleaned Metadata & SQLite Sync", C_EMERALD)

draw_arrow(0.40, 0.64, 0.18, 0.56, "Query Text")
draw_arrow(0.50, 0.64, 0.50, 0.56, "Role Lookup")
draw_arrow(0.60, 0.64, 0.80, 0.56, "Data Access")

# Layer 4: Semantic Search & AI Vector Store
draw_box(0.05, 0.24, 0.25, 0.12, "Vector Search (FAISS)", "384-D Sentence-Transformers\nIndexFlatIP Cosine Similarity", C_CYAN)
draw_box(0.375, 0.24, 0.25, 0.12, "Skill Gap Engine", "Target vs Existing Skills\nMissing Skill Course Matcher", C_AMBER)
draw_box(0.70, 0.24, 0.25, 0.12, "Prerequisite Graph", "Curated Dependency Rules\nCycle Detection & Topo Sort", C_EMERALD)

draw_arrow(0.18, 0.44, 0.18, 0.36, "Target Intent Embeddings")
draw_arrow(0.50, 0.44, 0.50, 0.36, "Required Skills")
draw_arrow(0.50, 0.44, 0.80, 0.36, "Dependencies")

# Layer 5: Hybrid Reranking & Learning Path Synthesis (Bottom)
draw_box(0.20, 0.04, 0.28, 0.12, "Hybrid Reranking Engine", "Multi-Signal Weighted Fusion:\nSemantic (0.6) + Skill (0.2) + Diff (0.1) + Rating (0.1)", C_VIOLET)
draw_box(0.52, 0.04, 0.28, 0.12, "Learning Path Generator", "Topological Sequencing\nMaps Real Coursera Courses 1 to 5", C_CYAN)

draw_arrow(0.18, 0.24, 0.30, 0.16, "Candidate Courses")
draw_arrow(0.50, 0.24, 0.38, 0.16, "Skill Scores")
draw_arrow(0.50, 0.24, 0.62, 0.16, "Gaps to Bridge")
draw_arrow(0.80, 0.24, 0.70, 0.16, "Topological Order")

# Final arrow back up to API
draw_arrow(0.34, 0.16, 0.45, 0.64, "Reranked Courses")
draw_arrow(0.66, 0.16, 0.55, 0.64, "Sequenced Curriculum")

# Title & Footer
fig.text(0.50, 0.98, "UNIVERSITY COURSE FINDER — SYSTEM ARCHITECTURE & DATA FLOW", ha='center', va='top', fontsize=18, fontweight='black', color=C_TEXT)
fig.text(0.50, 0.95, "End-to-End Microservice Architecture: From Raw Coursera Data to Personalized Recommendations", ha='center', va='top', fontsize=11, color=C_CYAN)
fig.text(0.50, 0.01, "University Course Finder • Deep Learning & FAISS Retrieval • Non-Docker Windows Execution", ha='center', va='bottom', fontsize=9, color=C_MUTED)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

out_path = Path(__file__).resolve().parent / 'architecture_diagram.png'
plt.tight_layout()
plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
print(f"Architecture diagram generated and saved to {out_path}")
