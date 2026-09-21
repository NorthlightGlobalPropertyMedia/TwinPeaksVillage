"""Interactive Phase One site plan.
The base image is the engineer's own drawing: Horizons Engineering, Echo Lake Subdivision Phase I, Utilities Plan
(sheet 3 of 9), rendered from the PDF in documents/plans/site-plans and toned to the brand palette. Nothing on it is redrawn.
The lot shapes below are hit areas traced over that drawing's boundary lines (frame 3876 x 3086 px) so each lot can be
selected. Lot areas are the figures printed on the plan."""
import html
e = html.escape
W, H = 3876, 3086

def arc(pts, n=6):
    """Catmull-Rom through pts, so traced road curves read as curves. Returns the smoothed run including both ends."""
    p = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        for k in range(n):
            t = k / n
            out.append(tuple(round(0.5 * ((2*p1[j]) + (-p0[j]+p2[j])*t + (2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t*t + (-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t**3), 1) for j in (0, 1)))
    return out + [pts[-1]]

C2 = arc([(1807,1177),(1810,1300),(1845,1400),(1900,1475),(1990,1545),(2110,1585)])          # Lot 2 road frontage, north to east
C7 = arc([(1737,1501),(1784,1560),(1844,1620),(1935,1683)])                                   # Lot 7 frontage
C6 = arc([(1935,1683),(2030,1722),(2123,1740)])                                               # Lot 6 frontage

LOTS = [
 # n, kind, title, address, sqft, status key, status text, price, link, chip, pin xy, polygon
 (1,"model","The Hunter model home","1 Solar Spring Circle",58310,"model","Model home under construction","Pricing to be announced","hunter.html","The Hunter",(2330,760),
  [(1889,428),(2786,520),(2756,795),(3205,838),(3198,893),(3179,1040),(2510,968),(1842,893)]),
 (2,"lot","Single-family homesite","Lot 2",45452,"avail","Available","$115,000","contact.html","$115,000",(2230,1160),
  [(1842,893),(2510,968),(2421,1621)] + C2[::-1]),
 (3,"lot","Single-family homesite","Lot 3",46467,"avail","Available","$115,000","contact.html","$115,000",(2760,1230),
  [(2510,968),(3179,1040),(3109,1546),(2937,1528),(2926,1630),(2876,1671),(2421,1621)]),
 (4,"lot","Single-family homesite","Lot 4",43605,"avail","Available","$115,000","contact.html","$115,000",(2700,2560),
  [(2676,1800),(2848,1820),(2900,1870),(2888,1975),(3048,1992),(3038,2073),(2903,2880),(2503,2837)]),
 (5,"duplex","The Dormer House","281 Solar Spring Circle",43679,"avail","Available","$950,000","residences/281-solar-spring-circle.html","281 · $950,000",(2420,2020),
  [(2302,1760),(2676,1800),(2503,2837),(2130,2796)]),
 (6,"duplex","The third duplex","295 Solar Spring Circle",43942,"soon","Coming soon","Pricing to be announced","residences/295-solar-spring-circle.html","295 · Coming soon",(2010,2380),
  C6 + [(2302,1760),(2130,2796),(1757,2755)]),
 (7,"duplex","The Colonial at the Gate","37 Solar Spring Circle",48695,"avail","Available","$950,000","residences/37-solar-spring-circle.html","37 · $950,000",(1560,2330),
  [(1572,1582)] + C7 + [(1757,2755),(1384,2715)]),
 (8,"lot","Single-family homesite","Lot 8",46483,"avail","Available","$115,000","contact.html","$115,000",(1230,1330),
  [(1095,808),(1691,878),(1657,1162),(1674,1364),(1026,1515),(1040,1132)]),
 (9,"lot","Single-family homesite","Lot 9",51935,"avail","Available","$115,000","contact.html","$115,000",(620,1500),
  [(256,1025),(1040,1132),(1026,1515),(892,1580),(960,1720),(183,1615)]),
]

def pts(p): return " ".join(f"{x:g},{y:g}" for x, y in p)

def overlay(pre=""):
    g = []
    for (n,kind,title,addr,sf,sk,st,price,link,chip,(px,py),poly) in LOTS:
        ac = sf / 43560
        label = f"Lot {n}. {title}. {addr}. {st}. {price}. {sf:,} square feet, about {ac:.2f} acres."
        xs = [x for x,_ in poly]; ys = [y for _,y in poly]
        cw = 30 + len(chip) * 21
        g.append(f'<g class="lot s-{sk}" tabindex="0" role="button" aria-label="{e(label)}" data-n="{n}" data-title="{e(title)}" data-addr="{e(addr)}" data-status="{e(st)}" data-sk="{sk}" data-price="{e(price)}" data-sf="{sf:,}" data-ac="{ac:.2f}" data-link="{pre}{link}" data-kind="{kind}" data-box="{min(xs):g} {min(ys):g} {max(xs):g} {max(ys):g}">'
                 f'<polygon class="shape" points="{pts(poly)}"/>'
                 f'<g class="mark" transform="translate({px},{py})"><g class="mk"><circle class="pin" r="46"/><text class="num" y="16" text-anchor="middle">{n}</text>'
                 f'<g class="chip" transform="translate(0,66)"><rect x="{-cw/2:g}" y="0" width="{cw:g}" height="58" rx="29"/><text y="40" text-anchor="middle">{e(chip)}</text></g></g></g></g>')
    return f'<svg class="sp-over" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" role="group" aria-label="Phase One lots. Select a lot for details.">{"".join(g)}</svg>'

def block(pre=""):
    rows = "".join(f'<tr><th scope="row">Lot {n}</th><td>{e(addr) if kind!="lot" else "Single-family homesite"}</td><td>{e(st)}</td><td class="num">{sf:,} sq ft</td><td class="num">{e(price)}</td></tr>'
                   for (n,kind,title,addr,sf,sk,st,price,link,chip,pin,poly) in LOTS)
    return f'''<div class="sp" id="sp" data-w="{W}" data-h="{H}">
<div class="sp-view" id="sp-view"><div class="sp-stage" id="sp-stage">
<img src="{pre}assets/img/site/phase-one-site-plan.webp" width="{W}" height="{H}" alt="Engineered utilities plan of Echo Lake Subdivision Phase I, now Twin Peaks Village, by Horizons Engineering: nine numbered lots along Solar Spring Circle and Geodessy Way, south of US Route 3." loading="lazy" decoding="async" draggable="false">
{overlay(pre)}</div>
<div class="sp-tools" role="group" aria-label="Plan view"><button type="button" id="sp-in" aria-label="Zoom in">+</button><button type="button" id="sp-out" aria-label="Zoom out">&minus;</button><button type="button" id="sp-reset" class="txt">Reset</button></div>
<div class="sp-legend"><span><i class="k avail"></i>Available</span><span><i class="k soon"></i>Coming soon</span><span><i class="k model"></i>Model home</span></div>

</div>
<aside class="sp-card" id="sp-card" aria-live="polite"><p class="kicker" id="sp-k">Phase One</p><h3 id="sp-t">Select a lot</h3><p id="sp-a" class="sp-addr">Choose any numbered lot. Drag to move the plan, and use the buttons to zoom.</p>
<dl id="sp-d" hidden><div><dt>Status</dt><dd id="sp-s"></dd></div><div><dt>Price</dt><dd id="sp-p"></dd></div><div><dt>Lot size</dt><dd id="sp-z"></dd></div></dl>
<a class="btn dark" id="sp-l" href="{pre}contact.html" hidden>View details</a></aside>
<p class="sp-credit">Base drawing: Horizons Engineering, Echo Lake Subdivision Phase I, Utilities Plan, sheet 3 of 9. Linework unaltered, toned for the screen, with lot status added. <a href="{pre}docs/echo-lake-subdivision-phase-1-site-plan.pdf">Download the full engineered plan set (PDF, 12.7 MB)</a></p>
</div>
<details class="sp-table"><summary>Lot list</summary><div class="scroll"><table class="spec"><tbody>{rows}</tbody></table></div></details>
<p class="note" style="margin-top:14px">The engineer&rsquo;s plan set is titled Echo Lake Subdivision, Phase I. Per the engineer&rsquo;s general notes, the building footprints and driveways drawn on each lot are representative only and do not show the homes as built. Lot areas are the figures printed on the plan. For boundaries, easements and dimensions, rely on the recorded plan and the offering documents.</p>'''
