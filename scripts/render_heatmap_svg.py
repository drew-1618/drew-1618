import os
import json

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run fetch_contributions.py first.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_past_year", 0)
    username = data.get("username", "user")

    # GitHub-inspired neon/dark green theme color ramp
    PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

    # Layout dimensions to line up perfectly at 860px wide
    svg_width = 860
    svg_height = 175
    box_size = 11
    box_gap = 3
    padding_left = 35
    padding_top = 25

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">',
        '  <defs>',
        '    <style>',
        '      @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&amp;display=swap");',
        '      .meta-text { font-family: "Fira Code", monospace; font-size: 11px; fill: #8b949e; }',
        '      .day-label { font-family: "Fira Code", monospace; font-size: 9px; fill: #8b949e; }',
        '      .heatmap-box { fill-opacity: 0; animation: revealBox 0.4s ease forwards; }',
        '      @keyframes revealBox {',
        '        to { fill-opacity: 1; }',
        '      }',
        '    </style>',
        '  </defs>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="6" />'
    ]

    # Add Day Labels (Mon, Wed, Fri)
    day_labels = {1: "Mon", 3: "Wed", 5: "Fri"}
    for day_idx, label in day_labels.items():
        y_pos = padding_top + (day_idx * (box_size + box_gap)) + 9
        svg_lines.append(f'  <text x="10" y="{y_pos}" class="day-label">{label}</text>')

    # Render the 53-week grid boxes
    for idx, day in enumerate(days):
        week = idx // 7
        day_of_week = idx % 7

        x = padding_left + (week * (box_size + box_gap))
        y = padding_top + (day_of_week * (box_size + box_gap))
        
        level = day.get("level", 0)
        color = PALETTE[min(level, len(PALETTE) - 1)]

        # Beautiful diagonal cascade wave effect[cite: 1]
        delay = (week + day_of_week) * 0.015

        svg_lines.append(
            f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" class="heatmap-box" fill="{color}" style="animation-delay: {delay:.3f}s;">'
        )
        svg_lines.append(f'    <title>{day.get("count", 0)} contributions on {day.get("date", "")}</title>')
        svg_lines.append('  </rect>')

    # Less -> More Legend at bottom right
    legend_start_x = svg_width - 130
    legend_y = padding_top + (7 * (box_size + box_gap)) + 12
    svg_lines.append(f'  <text x="{legend_start_x - 35}" y="{legend_y + 9}" class="meta-text">Less</text>')
    
    for idx, color in enumerate(PALETTE[:5]):
        lx = legend_start_x + (idx * (box_size + box_gap))
        svg_lines.append(f'  <rect x="{lx}" y="{legend_y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" />')
        
    svg_lines.append(f'  <text x="{legend_start_x + (5 * (box_size + box_gap)) + 5}" y="{legend_y + 9}" class="meta-text">More</text>')

    # Summary Statistics Footer text
    footer_text = f"{total_contribs:,} contributions in the last year"
    svg_lines.append(f'  <text x="{padding_left}" y="{legend_y + 9}" class="meta-text" font-weight="500">{footer_text}</text>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Map compiled to: {output_path}[cite: 1]")

if __name__ == "__main__":
    render_heatmap()