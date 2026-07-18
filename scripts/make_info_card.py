import os

def generate_info_card(output_path="info-card.svg"):
    # SVG Dimensions - Designed to sit flush alongside the 370px wide ASCII portrait
    width = 490
    height = 350
    
    username = "andrew"
    hostname = "github"
    
    # Key-value pairs for the neofetch display
    stats = [
        ("OS", "Windows, WSL2 Linux, MacOS"),
        ("Uptime", "Senior Year (Expected Grad: Dec 2026)"),
        ("Shell", "bash / zsh / Git Bash / Command Prompt"),
        ("Major", "Computer Science (Math Minor)"),
        ("Stack", "Python, JavaScript, Node.js, Express, SQL, C++"),
        ("Current", "Backend Lead and Solutions Engineering Co-Op"),
        ("Focus", "Full Stack Web Development, AI Tooling, Data Science")
    ]
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>',
        '    <style>',
        '      @import url("https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&amp;display=swap");',
        '      .terminal { font-family: "Fira Code", monospace; font-size: 13px; }',
        '      .prompt { font-weight: 600; fill: #58a6ff; }',
        '      .host { font-weight: 600; fill: #39d353; }',
        '      .key { font-weight: 600; fill: #ff7b72; }',
        '      .val { fill: #c9d1d9; }',
        '      .separator { fill: #8b949e; }',
        '    </style>',
        '  </defs>',
        f'  <rect width="100%" height="100%" fill="#0d1117" rx="6" />' # Matching dark window canvas
    ]
    
    # 1. Add the fake shell prompt at the very top line
    # e.g., andrew@github ~ $ neofetch
    start_y = 35
    line_spacing = 24
    
    svg_lines.append(f'  <text x="25" y="{start_y}" class="terminal" opacity="0">')
    svg_lines.append(f'    <tspan class="prompt">{username}</tspan>')
    svg_lines.append(f'    <tspan class="separator">@</tspan>')
    svg_lines.append(f'    <tspan class="host">{hostname}</tspan>')
    svg_lines.append(f'    <tspan class="val"> ~ $ neofetch</tspan>')
    svg_lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.15s" begin="0.1s" fill="freeze" />')
    svg_lines.append('  </text>')
    
    # 2. Add the clean underline divider block
    # andrew----------------github
    divider_y = start_y + 16
    divider_text = "-" * (len(username) + len(hostname) + 1)
    svg_lines.append(f'  <text x="25" y="{divider_y}" class="terminal" fill="#8b949e" opacity="0">')
    svg_lines.append(f'    {divider_text}')
    svg_lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.1s" begin="0.25s" fill="freeze" />')
    svg_lines.append('  </text>')
    
    # 3. Loop through your stats arrays and stagger their animations down the screen
    content_start_y = divider_y + 24
    
    for idx, (key, value) in enumerate(stats):
        current_y = content_start_y + (idx * line_spacing)
        # Stagger line-by-line animations right after the header elements settle
        delay = 0.35 + (idx * 0.08)
        
        svg_lines.append(f'  <text x="25" y="{current_y}" class="terminal" opacity="0">')
        svg_lines.append(f'    <tspan class="key">{key}</tspan>')
        svg_lines.append(f'    <tspan class="separator">Layout: </tspan>') # Replicates the standard neofetch spaces
        svg_lines.append(f'    <tspan class="val">{value}</tspan>')
        
        # Staggered slide and fade-in animations via CSS-SMIL properties
        svg_lines.append(f'    <animate attributeName="opacity" from="0" to="1" dur="0.2s" begin="{delay:.2f}s" fill="freeze" />')
        svg_lines.append(f'    <animate attributeName="y" from="{current_y + 5}" to="{current_y}" dur="0.2s" begin="{delay:.2f}s" fill="freeze" />')
        svg_lines.append('  </text>')
        
    # 4. Add a tiny classic color block strip at the absolute bottom
    color_blocks_y = content_start_y + (len(stats) * line_spacing) + 12
    colors = ["#161b22", "#ff7b72", "#39d353", "#d29922", "#58a6ff", "#bc8cff", "#3080f4", "#c9d1d9"]
    
    svg_lines.append(f'  <g transform="translate(25, {color_blocks_y})">')
    for idx, color in enumerate(colors):
        x_offset = idx * 20
        block_delay = 0.4 + (len(stats) * 0.08) + (idx * 0.03)
        svg_lines.append(f'    <rect x="{x_offset}" width="18" height="12" fill="{color}" opacity="0">')
        svg_lines.append(f'      <animate attributeName="opacity" from="0" to="1" dur="0.15s" begin="{block_delay:.2f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
    svg_lines.append('  </g>')

    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Success! Neofetch info card compiled to: {output_path}")

if __name__ == "__main__":
    generate_info_card()
