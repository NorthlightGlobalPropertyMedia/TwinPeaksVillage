"""Interactive illustrated Phase One site plan.
Lot lines, roads and building positions are traced by eye from Horizons Engineering, Echo Lake Subdivision Phase I,
Utilities Plan (sheet 3 of 9). Illustrative only: not a survey. Lot areas are the figures printed on that plan."""
import random, html
e = html.escape

LOTS = [
 # id, kind, title, address, sqft, status key, status text, price, link, polygon
 (1,"model","The Hunter model home","1 Solar Spring Circle",58310,"model","Model home under construction","Pricing to be announced","hunter.html",
  [(1130,160),(1672,218),(1655,395),(1930,425),(1916,545),(1505,500),(1098,455)]),
 (2,"lot","Single-family homesite","Lot 2",45452,"avail","Available","$115,000","contact.html",
  [(1098,455),(1505,500),(1455,880),(1250,862),(1160,830),(1100,760),(1075,630)]),
 (3,"lot","Single-family homesite","Lot 3",46467,"avail","Available","$115,000","contact.html",
  [(1505,500),(1916,545),(1872,905),(1760,912),(1455,880)]),
 (4,"lot","Single-family homesite","Lot 4",43605,"avail","Available","$115,000","contact.html",
  [(1608,1010),(1720,1027),(1745,1055),(1738,1118),(1837,1128),(1829,1178),(1746,1672),(1502,1646)]),
 (5,"duplex","The Dormer House","281 Solar Spring Circle",43679,"avail","Available","$950,000","residences/281-solar-spring-circle.html",
  [(1378,987),(1608,1010),(1502,1646),(1273,1621)]),
 (6,"duplex","The third duplex","295 Solar Spring Circle",43942,"soon","Coming soon","Pricing to be announced","residences/295-solar-spring-circle.html",
  [(1153,938),(1378,987),(1273,1621),(1045,1596)]),
 (7,"duplex","The Colonial at the Gate","37 Solar Spring Circle",48695,"avail","Available","$950,000","residences/37-solar-spring-circle.html",
  [(930,880),(1000,868),(1060,880),(1110,905),(1153,938),(1045,1596),(815,1572)]),
 (8,"lot","Single-family homesite","Lot 8",46483,"avail","Available","$115,000","contact.html",
  [(640,403),(1003,446),(985,640),(965,720),(597,835),(605,600)]),
 (9,"lot","Single-family homesite","Lot 9",51935,"avail","Available","$115,000","contact.html",
  [(125,535),(605,600),(597,835),(515,858),(553,950),(80,890)]),
]
BUILDINGS = {  # existing buildings and the model home, as positioned on the plan
 7:[(1022,1003),(1066,1010),(1033,1200),(990,1192)],
 6:[(1180,1275),(1225,1282),(1192,1475),(1147,1468)],
 5:[(1375,1327),(1420,1334),(1390,1525),(1345,1518)],
 1:[(1205,258),(1330,272),(1326,312),(1201,298)],
}

def centroid(p):
    a=cx=cy=0
    for i in range(len(p)):
        x0,y0=p[i]; x1,y1=p[(i+1)%len(p)]; c=x0*y1-x1*y0; a+=c; cx+=(x0+x1)*c; cy+=(y0+y1)*c
    a*=0.5; return cx/(6*a), cy/(6*a)

def inside(pt,poly):
    x,y=pt; c=False
    for i in range(len(poly)):
        x0,y0=poly[i]; x1,y1=poly[(i+1)%len(poly)]
        if (y0>y)!=(y1>y) and x < (x1-x0)*(y-y0)/(y1-y0)+x0: c=not c
    return c

def pts(p): return " ".join(f"{x},{y}" for x,y in p)

def trees():
    """Deterministic scatter of evergreen dots outside the roads, thinned inside lots."""
    rnd=random.Random(7); out=[]
    road=[(1070,130),(1050,450),(1030,640),(1060,760),(1130,850),(1250,895),(1455,915),(1790,950)]
    stub=[(1010,770),(540,905)]
    def near(p,line,d):
        for i in range(len(line)-1):
            (x0,y0),(x1,y1)=line[i],line[i+1]; dx,dy=x1-x0,y1-y0; L=dx*dx+dy*dy
            t=max(0,min(1,((p[0]-x0)*dx+(p[1]-y0)*dy)/L)); qx,qy=x0+t*dx,y0+t*dy
            if (p[0]-qx)**2+(p[1]-qy)**2<d*d: return True
        return False
    polys=[l[9] for l in LOTS]; blds=list(BUILDINGS.values())
    while len(out)<560:
        p=(rnd.uniform(-20,2020),rnd.uniform(-10,1750))
        if abs(p[1]-(0.111*p[0]-40)) < 70: continue            # Route 3 corridor and beyond
        if near(p,road,62) or near(p,stub,55): continue
        if any(inside(p,b) for b in blds): continue
        if any(near(p,[b[0],b[2]],75) for b in blds): continue
        inlot=any(inside(p,q) for q in polys)
        if inlot and rnd.random()<0.55: continue
        if 330<p[0]<780 and 990<p[1]<1250 and rnd.random()<0.8: continue   # open field on the plan
        out.append((round(p[0]),round(p[1]),rnd.choice([9,11,13,15]),rnd.choice(["#4f6048","#5d6d52","#727D62","#64745a"])))
    out.sort(key=lambda t:t[1])
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".78"/>' for x,y,r,c in out)

def svg(pre=""):
    g=[]
    for (n,kind,title,addr,sf,sk,st,price,link,poly) in LOTS:
        cx,cy=centroid(poly)
        if n==1: cx,cy=1400,400
        if n==4: cx,cy=1640,1400
        ac=sf/43560
        label=f"Lot {n}. {title}. {addr}. {st}. {price}. {sf:,} square feet, about {ac:.2f} acres."
        b=f'<polygon class="bld" points="{pts(BUILDINGS[n])}"/>' if n in BUILDINGS else ""
        g.append(f'<g class="lot s-{sk}" tabindex="0" role="button" aria-label="{e(label)}" data-n="{n}" data-title="{e(title)}" data-addr="{e(addr)}" data-status="{e(st)}" data-sk="{sk}" data-price="{e(price)}" data-sf="{sf:,}" data-ac="{ac:.2f}" data-link="{pre}{link}" data-kind="{kind}">'
                 f'<polygon class="shape" points="{pts(poly)}"/>{b}'
                 f'<circle class="pin" cx="{cx:.0f}" cy="{cy:.0f}" r="30"/><text class="num" x="{cx:.0f}" y="{cy+11:.0f}" text-anchor="middle">{n}</text></g>')
    return f'''<svg class="siteplan" viewBox="0 0 2000 1760" role="group" aria-label="Illustrated site plan of Twin Peaks Village, Phase One. Nine lots; select a lot for details.">
<rect x="0" y="0" width="2000" height="1760" fill="#E9E6D3"/>
<path d="M-40,1240 C200,1180 420,1210 640,1170 C800,1150 860,1290 980,1390 C1100,1470 1300,1440 1480,1500 C1640,1560 1800,1600 2040,1640 L2040,1800 L-40,1800 Z" fill="#cfd8d6" opacity=".75"/>
<g>{trees()}</g>
<text x="300" y="1520" class="soft">wetland and woods</text>
<text x="250" y="1130" class="soft">Lot 10 &#183; remaining land, future phase</text>
<path d="M-60,-47 L2060,189" stroke="#B4BBB8" stroke-width="96" fill="none"/><path d="M-60,-47 L2060,189" stroke="#F6F1E4" stroke-width="3" stroke-dasharray="26 22" fill="none"/>
<text x="300" y="4" class="road" transform="rotate(6.3 300 4)">US ROUTE 3</text>
<path d="M1088,90 L1050,450 L1030,640 C1025,760 1110,880 1250,895 L1455,915 L1790,950" stroke="#c9c5b4" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M1010,770 L540,905" stroke="#c9c5b4" stroke-width="56" fill="none" stroke-linecap="round"/>
<path d="M1790,900 L1800,1060" stroke="#c9c5b4" stroke-width="46" fill="none" stroke-linecap="round"/>
<text class="road" x="1042" y="600" transform="rotate(-84 1042 600)">SOLAR SPRING CIRCLE</text>
<text class="road" x="1330" y="915" transform="rotate(6 1330 915)">SOLAR SPRING CIRCLE</text>
{"".join(g)}
<g transform="translate(150,1620) rotate(12)"><path d="M0,-70 L18,10 L0,-4 L-18,10 Z" fill="#2A372A"/><text x="0" y="40" text-anchor="middle" class="road" style="font-size:26px">N</text></g>
<g transform="translate(1560,1720)"><path d="M0,0 H180" stroke="#2A372A" stroke-width="4"/><path d="M0,-9 V9 M90,-6 V6 M180,-9 V9" stroke="#2A372A" stroke-width="3"/><text x="90" y="-16" text-anchor="middle" class="road" style="font-size:22px">about 100 ft</text></g>
</svg>'''

def block(pre=""):
    rows="".join(f'<tr><th scope="row">Lot {n}</th><td>{e(addr) if kind!="lot" else "Single-family homesite"}</td><td>{e(st)}</td><td class="num">{sf:,} sq ft</td><td class="num">{e(price)}</td></tr>' for (n,kind,title,addr,sf,sk,st,price,link,poly) in LOTS)
    return f'''<div class="sp-wrap"><div class="sp-map">{svg(pre)}</div>
<aside class="sp-panel" aria-live="polite"><div class="sp-legend"><span><i class="k avail"></i>Available</span><span><i class="k soon"></i>Coming soon</span><span><i class="k model"></i>Model home</span></div>
<div class="sp-card" id="sp-card"><p class="kicker" id="sp-k">Phase One</p><h3 id="sp-t">Select a lot</h3><p id="sp-a" class="sp-addr">Hover, tap or tab to any numbered lot on the plan.</p>
<dl id="sp-d" hidden><div><dt>Status</dt><dd id="sp-s"></dd></div><div><dt>Price</dt><dd id="sp-p"></dd></div><div><dt>Lot size</dt><dd id="sp-z"></dd></div></dl>
<a class="btn dark" id="sp-l" href="{pre}contact.html" hidden>View details</a></div></aside></div>
<details class="sp-table"><summary>Lot list</summary><div class="scroll"><table class="spec"><tbody>{rows}</tbody></table></div></details>
<p class="note" style="margin-top:14px">Illustrative plan traced from the Horizons Engineering Phase I utilities plan. It is not a survey. Lot lines, roads, tree cover and building positions are approximate, and the building shown on Lot 1 is the engineer&rsquo;s representative footprint. Lot areas are the figures printed on that plan. The scale bar is approximate.</p>'''
