#!/usr/bin/env python3
"""Twin Peaks Village static site builder. Run: python3 src/build.py  -> writes dist/*.html
Content facts trace to documents in /documents or to Keegan Rice's written confirmations of Sept 18-19, 2026.
Anything wrapped in tbd() is a visible placeholder."""
import os, html, shutil
from data import G281, G37, GSITE
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DIST=os.path.join(ROOT,"dist")
e=html.escape
def tbd(t): return f'<span class="tbd">To confirm: {e(t)}</span>'
def tbdblock(t,sub=""): return f'<div class="tbd-block">{e(t)}<small>{e(sub)}</small></div>'

NAV=[("village.html","The Village"),("residences.html","Residences"),("hunter.html","The Hunter"),("location.html","Location"),("documents.html","Documents")]
def page(fn,title,desc,body,hero=None,pre=""):
    nav="".join(f'<a href="{pre}{h}"{" aria-current=page" if h==fn or (fn.startswith("residences/") and h=="residences.html") else ""}>{t}</a>' for h,t in NAV)
    head_cls="site-head" if hero else "site-head solid"
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Twin Peaks Village</title><meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{pre}assets/brand/04_icon_mark_hires.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Montserrat:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{pre}assets/site.css"></head><body>
<div class="ribbon">Preview draft for Echo Lake Investments and counsel &middot; not for public distribution</div>
<header class="{head_cls}"><div class="wrap in">
<a class="brand" href="{pre}index.html"><img src="{pre}assets/brand/05_horizontal_reversed.svg" alt="Twin Peaks Village, Twin Mountain, New Hampshire" width="230" height="46"></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="cta" href="{pre}contact.html">Inquire</a></nav>
</div></header>
<main>{hero or ""}{body}</main>
<footer><div class="wrap"><div class="cols">
<div><img class="logo" src="{pre}assets/brand/01_primary_reversed.svg" alt="Twin Peaks Village" width="190" height="108"><p>A new community of single-family homes and duplex residences on Solar Spring Circle in Twin Mountain, a village of Carroll, New Hampshire.</p></div>
<div><h5>Explore</h5>{"".join(f'<a href="{pre}{h}">{t}</a>' for h,t in NAV)}<a href="{pre}contact.html">Inquire</a><a href="{pre}legal.html">Legal and disclosures</a></div>
<div><h5>Listing agents</h5><a href="tel:+16033487261">Keegan Rice &middot; 603-348-7261</a><a href="mailto:KeeganR@BadgerPeabodySmith.com">KeeganR@BadgerPeabodySmith.com</a><a href="tel:+16037145148" style="margin-top:12px">Matthew Penner &middot; 603-714-5148</a><a href="mailto:MatthewP@BadgerPeabodySmith.com">MatthewP@BadgerPeabodySmith.com</a></div>
<div><h5>Exclusively listed by</h5><img class="bps" src="{pre}assets/brand/bps_logo_rev.png" alt="Badger Peabody &amp; Smith Realty" width="96" height="107"><p style="margin-top:12px">Badger Peabody &amp; Smith Realty<br>Bretton Woods office &middot; 603-259-0210</p></div>
</div>
<div class="fine">
<p><strong>Draft language for counsel review.</strong> Information on this site is drawn from the documents and sources named on each page and is believed accurate but is not guaranteed. Prices, plans, specifications, dimensions and availability may change without notice. Square footage and room dimensions are approximate. Images marked "virtually staged" show digital furnishings; images marked "twilight" have a digitally enhanced sky; the image of The Hunter is an artist's rendering, and its landscaping, driveway and background are illustrative. References to resorts, trails and public lands are geographic only and imply no affiliation. Buyers should verify all information, including town and association rules, independently.</p>
<p>{tbd("RSA 356-A registration statement and any required disclosure wording, from Attorney Andy Sullivan")} &middot; Equal Housing Opportunity &middot; &copy; 2026 Badger Peabody &amp; Smith Realty</p>
</div></div></footer>
<script src="{pre}assets/site.js"></script></body></html>'''

def hero(img,eyebrow,h1,lead,credit="",short=False,btns="",pre=""):
    return f'''<section class="hero{" short" if short else ""}" style="padding:0"><img src="{pre}{img}" alt="" fetchpriority="high">
<div class="wrap in"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>{btns}</div>
{f'<div class="credit">{credit}</div>' if credit else ""}</section>'''

TAGTXT={"S":"Virtually staged","T":"Twilight sky digitally enhanced"}
def gallery(items,folder,cats,pre=""):
    fb='<button type="button" data-f="all" aria-pressed="true">All</button>'+"".join(f'<button type="button" data-f="{k}" aria-pressed="false">{v}</button>' for k,v in cats)
    cells=[]
    for i,(stem,cap,cat,tag) in enumerate(items):
        full=f"{pre}assets/img/{folder}/{stem}_2000.jpg"; th=f"{pre}assets/img/{folder}/{stem}_900.jpg"
        fullcap=cap+(f". {TAGTXT[tag]}." if tag else "")
        cells.append(f'<button type="button" class="{"wide" if i==0 else ""}" data-cat="{cat}" data-full="{full}" data-cap="{e(fullcap)}"><img src="{th}" alt="{e(fullcap)}" loading="lazy" width="900" height="600">{f"<span class=tagline>{TAGTXT[tag]}</span>" if tag else ""}</button>')
    filt=f'<div class="filters" role="group" aria-label="Filter photos">{fb}</div>' if cats else ""
    return f'<div class="gal-wrap">{filt}<div class="gallery" data-gallery>{"".join(cells)}</div></div>'

def spec(rows):
    return '<table class="spec"><tbody>'+"".join(f'<tr><th scope="row">{k}</th><td>{v}{f"<span class=src>Source: {s}</span>" if s else ""}</td></tr>' for k,v,s in rows)+'</tbody></table>'

def cta(pre=""):
    return f'''<section class="band-forest"><div class="wrap split">
<div><p class="kicker">Visit</p><h2>See it in person</h2><div class="hair"></div><p class="lede">Showings are by appointment with the listing agents. Tell us which residence or homesite interests you and we will arrange a time.</p><div class="btns"><a class="btn fill" href="{pre}contact.html">Request a showing</a><a class="btn" href="{pre}documents.html">Offering documents</a></div></div>
<div class="people"><div class="person"><b>Keegan Rice</b><span>REALTOR&reg;, NH Lic. #072031</span><a href="tel:+16033487261">603-348-7261</a><a href="mailto:KeeganR@BadgerPeabodySmith.com">KeeganR@BadgerPeabodySmith.com</a></div>
<div class="person"><b>Matthew Penner</b><span>Badger Peabody &amp; Smith Realty</span><a href="tel:+16037145148">603-714-5148</a><a href="mailto:MatthewP@BadgerPeabodySmith.com">MatthewP@BadgerPeabodySmith.com</a></div></div>
</div></section>'''

def card(href,img,status,addr,name,meta,price,gold=False,empty=False):
    ph=f'<div class="ph empty"><img src="assets/brand/04_icon_mark_hires.png" alt=""><span class="status{" gold" if gold else ""}">{status}</span></div>' if empty else f'<div class="ph"><img src="{img}" alt="" loading="lazy"><span class="status{" gold" if gold else ""}">{status}</span></div>'
    return f'<a class="card" href="{href}">{ph}<div class="tx"><span class="addr">{addr}</span><h3>{name}</h3><span class="meta">{meta}</span><span class="price">{price}</span></div></a>'

CARDS="".join([
 card("residences/281-solar-spring-circle.html","assets/img/281/LSD01734twilight_900.jpg","Available","281 Solar Spring Circle","The Dormer House","Duplex &middot; two residences, each 4 bedrooms, 3 baths, two-car garage","$950,000"),
 card("residences/37-solar-spring-circle.html","assets/img/37/LSD01943twilight_900.jpg","Available","37 Solar Spring Circle","The Colonial at the Gate","Duplex &middot; two residences, each 4 bedrooms, 2 baths, designed with accessibility in mind","$950,000"),
 card("residences/295-solar-spring-circle.html","","Coming soon","295 Solar Spring Circle","The third duplex","Details, photography and floor plans to follow","Pricing to be announced",empty=True),
 card("hunter.html","assets/img/model/hunter-rendering_900.jpg","Model home under construction","1 Solar Spring Circle","The Hunter","Single-level &middot; 3 bedrooms, 2 baths, two-car garage &middot; artist's rendering","Pricing to be announced",gold=True),
])

def write(fn,s):
    p=os.path.join(DIST,fn); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,"w").write(s)

# ---------------- HOME
home_body=f'''
<section><div class="wrap split">
<div><p class="kicker">Welcome</p><h2>Twenty-seven homesites at the center of the White Mountains</h2><div class="hair"></div>
<p class="lede">Twin Peaks Village is a new planned community on Solar Spring Circle, just off Route 3 in Twin Mountain. Single-family homes and duplex residences sit on level lots of about an acre, served by public water and underground utilities, with private roads cared for by a homeowners' association.</p>
<p>The first three duplex buildings are complete and have never been occupied. The model home, The Hunter, was set on its foundation on September 16, 2026 and will be finished this fall.</p>
<div class="btns"><a class="btn dark" href="village.html">About the village</a></div></div>
<div><img src="assets/img/site/DJI_0619_2000.jpg" alt="Aerial view of Twin Peaks Village from above Route 3 with mountains beyond" loading="lazy"></div>
</div>
<div class="wrap"><div class="facts"><div><b>27</b><span>Homesites planned</span></div><div><b>8</b><span>In Phase One</span></div><div><b>3</b><span>Duplex buildings</span></div><div><b>5</b><span>Single-family sites, Phase One</span></div><div><b>1+ acre</b><span>Phase One lot sizes</span></div></div></div>
</section>
<section class="band-paper"><div class="wrap"><p class="kicker">Residences</p><h2>Available now, and what comes next</h2><div class="hair"></div><div class="cards">{CARDS}</div></div></section>
<section class="band-forest"><div class="wrap split top">
<div><p class="kicker">Why here</p><h2>A basecamp for every season</h2><div class="hair"></div>
<p class="lede">Twin Mountain sits where Routes 3 and 302 meet, between Franconia Notch and Crawford Notch, with the Presidential Range on the horizon.</p>
<div class="btns"><a class="btn" href="location.html">Explore the location</a></div></div>
<div><h4>Winter</h4><p>Alpine and Nordic skiing at Bretton Woods and Cannon Mountain, and the regional snowmobile corridor network.</p>
<h4>Spring and summer</h4><p>Hiking in the Presidential Range and Crawford Notch, fishing and paddling on the Ammonoosuc River, golf, and the Mount Washington Cog Railway.</p>
<h4>Fall</h4><p>Foliage on Route 302 through Crawford Notch and on the rail trails.</p></div>
</div></section>
<section><div class="wrap split rev">
<div><p class="kicker">Progress</p><h2>Where things stand</h2><div class="hair"></div>
<div class="tl">
<div><b>Complete</b>Three duplex buildings finished, with gravel roads and utilities in place to serve them.</div>
<div><b>September 16, 2026</b>The Hunter model home set on its foundation at 1 Solar Spring Circle.</div>
<div><b>September 2026</b>Subdivision plan approved by the New Hampshire Attorney General's office. {tbd("approval date and registration wording from counsel")}</div>
<div class="open"><b>Fall 2026</b>Paving of the road, driveways and walkways, and final landscaping. {tbd("paving date")}</div>
<div class="open"><b>Fall 2026</b>Model home construction and final fit-up.</div>
<div class="open"><b>In process</b>Association declaration, bylaws and budget. {tbd("delivery date from Attorney Sullivan")}</div>
</div></div>
<div><img src="assets/img/site/DJI_0618_2000.jpg" alt="Aerial view of the three completed duplex buildings" loading="lazy"></div>
</div></section>
{cta()}'''
write("index.html",page("index.html","A new village in the White Mountains","Twin Peaks Village: single-family homes and duplex residences in Twin Mountain, New Hampshire.",home_body,
 hero("assets/img/37/DJI_0626twilight_2000.jpg","Twin Mountain &middot; New Hampshire","A new village in the White Mountains","Single-family homes and duplex residences on acre lots, minutes from the slopes, the trails and the river. Two new duplex residences are available now.",
 credit="37 Solar Spring Circle. Twilight sky digitally enhanced.",btns='<div class="btns"><a class="btn fill" href="residences.html">View residences</a><a class="btn" href="contact.html">Request a showing</a></div>')))

# ---------------- VILLAGE
village_body=f'''
<section><div class="wrap split top">
<div><p class="kicker">The plan</p><h2>Two phases, twenty-seven homesites</h2><div class="hair"></div>
<p class="lede">Phase One has eight lots: three duplex buildings, now complete, and five single-family homesites. Phase Two adds nineteen more.</p>
<p>Lots in Phase One range from about 1.0 to 1.3 acres on level ground. Every home in the village belongs to the same homeowners' association.</p></div>
<div>{spec([
 ("Developer","Echo Lake Investments, LLC",""),
 ("Phase One","8 lots: 3 duplex buildings and 5 single-family homesites","Keegan Rice, Sept 19, 2026"),
 ("Phase Two","19 lots "+tbd("mix of single-family and duplex"),"Keegan Rice, Sept 19, 2026"),
 ("Phase One lot sizes","43,605 to 58,310 sq ft","Horizons Engineering site plan, sheet 1"),
 ("Single-family homesites",tbd("public lot pricing and which lots are released"),""),
 ("Roads","Private. Maintained by the homeowners' association","Site plan general note 2; Keegan Rice"),
 ("Stormwater","Maintained by the homeowners' association","Keegan Rice, Sept 19, 2026"),
 ("Water","Public water","MLS sheets; site plan"),
 ("Wastewater","Private septic on each lot, State-approved designs","NHDES approvals on file"),
 ("Utilities","Underground electric. Cable, phone and high-speed internet available","MLS sheets"),
])}</div></div></section>
<section class="band-paper"><div class="wrap"><p class="kicker">Site map</p><h2>The lay of the land</h2><div class="hair"></div>
{tbdblock("Illustrated site map in production","Traced from the Horizons Engineering plan in the brand palette, with every lot numbered and its status shown. Needs the current approved plan set and the Phase Two layout.")}
<div style="height:28px"></div>{gallery(GSITE,"site",[])}
<p class="note" style="margin-top:14px">Aerial photography August 31, 2026.</p></div></section>
<section><div class="wrap split top">
<div><p class="kicker">The association</p><h2>Shared standards, shared care</h2><div class="hair"></div>
<p>A homeowners' association will own and maintain the private roads and the stormwater system and keep the architecture consistent from one home to the next.</p>
<p>The association documents as drafted place no restriction on short-term rentals. {tbd("against the final recorded documents")} Town of Carroll rules also apply, and buyers should confirm current requirements with the town.</p></div>
<div>{spec([
 ("Declaration and bylaws",tbd("from Attorney Andy Sullivan"),""),
 ("Annual budget",tbd("from Attorney Andy Sullivan"),""),
 ("Dues",tbd("amount and frequency"),""),
 ("Architectural review",tbd("process and standards"),""),
 ("Pets, parking, exterior changes",tbd("from final documents"),""),
])}</div></div></section>
<section class="band-forest"><div class="wrap"><p class="kicker">Who is building it</p><h2>The team</h2><div class="hair"></div>
<div class="people">
<div class="person"><b>Westchester Modular Homes</b><span>Manufacturer of the duplex residences and The Hunter. Homes are built indoors to New Hampshire snow loads, then set and finished on site.</span></div>
<div class="person"><b>Construction Management &amp; Estimating</b><span>Charles Allen, construction manager for the model home and all future developer builds. Madison, New Hampshire.</span></div>
<div class="person"><b>Horizons Engineering</b><span>Civil engineering, survey and septic design for the subdivision.</span></div>
<div class="person"><b>Badger Peabody &amp; Smith Realty</b><span>Exclusive listing and marketing firm. Keegan Rice and Matthew Penner, listing agents.</span></div>
</div></div></section>
{cta()}'''
write("village.html",page("village.html","The Village","The plan, the association and the team behind Twin Peaks Village.",village_body,
 hero("assets/img/site/DJI_0624_2000.jpg","The Village","Planned with care, built to last","Private roads, public water, underground utilities and a homeowners' association to look after all of it.",short=True)))

# ---------------- RESIDENCES INDEX
write("residences.html",page("residences.html","Residences","Duplex residences and single-family homes at Twin Peaks Village.",
 f'<section><div class="wrap"><p class="kicker">Phase One</p><h2>Residences</h2><div class="hair"></div><p class="lede">Each duplex is sold as one building to one owner: two complete homes side by side, each with its own entrance, garage, basement, meters and heating system.</p><div style="height:20px"></div><div class="cards">{CARDS}</div></div></section>{cta()}',
 hero("assets/img/site/DJI_0618_2000.jpg","Residences","Two homes under one roof","Live in one and keep the other for the people you want close, or hold the whole building as your White Mountains base.",short=True)))

# ---------------- BUILDING PAGES
def building(fn,addr,name,heroimg,herocredit,lead,facts,intro_html,items,folder,cats,video,plans,specrows,docs):
    pre="../"
    body=f'''
<section><div class="wrap"><div class="split top"><div><p class="kicker">{addr}</p><h2>{name}</h2><div class="hair"></div>{intro_html}</div>
<div><div class="facts" style="margin-top:0">{"".join(f"<div><b>{a}</b><span>{b}</span></div>" for a,b in facts)}</div>
<div class="btns"><a class="btn fill" style="color:var(--forest-deep)" href="{pre}contact.html">Request a showing</a><a class="btn dark" href="#plans">Floor plans</a></div></div></div></div></section>
<section class="band-paper tight"><div class="wrap"><p class="kicker">Gallery</p><h2>Photographs</h2><div class="hair"></div>{gallery(items,folder,cats,pre)}
<p class="note" style="margin-top:14px">Photographed September 1, 2026. Images marked "virtually staged" show digital furnishings in the actual room; the unfurnished photo of the same room appears beside it. Twilight images have a digitally enhanced sky.</p></div></section>
<section><div class="wrap split top"><div><p class="kicker">Walk through</p><h2>Film</h2><div class="hair"></div><p>A continuous walk-through of both residences, recorded from the 3D scan of August 31, 2026.</p><p class="note">{tbd("edited 60 to 90 second film")}</p></div>
<div><video controls preload="none" poster="{pre}assets/video/{video}-walkthrough-poster.jpg"><source src="{pre}assets/video/{video}-walkthrough-720p.mp4" type="video/mp4"></video></div></div></section>
<section class="band-paper" id="plans"><div class="wrap"><p class="kicker">Floor plans</p><h2>Level by level</h2><div class="hair"></div>
<div class="plans">{"".join(f'<figure><figcaption>{c}</figcaption><img src="{pre}assets/img/plans/{f}" alt="{c} floor plan with room dimensions" loading="lazy"></figure>' for c,f in plans)}</div>
<p class="note" style="margin-top:14px">Plans generated by CubiCasa from an on-site scan. Dimensions are approximate. {tbd("branded plan sheets to replace these")}</p></div></section>
<section><div class="wrap"><p class="kicker">Details</p><h2>Facts and specifications</h2><div class="hair"></div>{spec(specrows)}</div></section>
<section class="band-paper tight"><div class="wrap"><p class="kicker">Downloads</p><h2>Documents for this residence</h2><div class="hair"></div><div class="doclist">{docs}</div></div></section>
{cta(pre)}'''
    write(fn,page(fn,f"{addr}",f"{addr}, Twin Peaks Village, Twin Mountain NH.",body,hero(heroimg,addr+" &middot; $950,000",name,lead,credit=herocredit,short=False,pre=pre),pre=pre))

def doc(title,desc,href=None):
    return f'<div class="doc"><div><b>{title}</b><span>{desc}</span></div>{f"<a href={href}>Download PDF</a>" if href else "<em class=tbd>Coming</em>"}</div>'

COMMON_SRC="MLS sheet"
building("residences/281-solar-spring-circle.html","281 Solar Spring Circle","The Dormer House","assets/img/281/LSD01734twilight_2000.jpg","Twilight sky digitally enhanced.",
 "Two complete four-bedroom homes beneath one dormered roofline, each with a two-car garage, set among mature spruce and birch.",
 [("4 + 4","Bedrooms"),("3 + 3","Full baths"),("3,584","Sq ft finished"),("4","Garage bays"),("1.00","Acre")],
 '''<p class="lede">Two real houses, not two apartments. Each side has a first-floor bedroom and full bath, a 20-foot primary suite with a walk-in closet and private bath, a second-floor laundry room, and its own meters and heating zones.</p>
<p>A rustic wood beam frames the open living and dining rooms. The kitchen pairs warm wood cabinetry and crown molding with granite counters, tile floors and stainless appliances. Oak stair treads with iron balusters lead upstairs, where two more bedrooms share a hall bath. Out back, each home has its own stamped concrete patio.</p>
<p>New construction, never occupied. Sold as one building to one owner.</p>''',
 G281,"281",[("exterior","Exterior"),("living","Living and dining"),("kitchen","Kitchen"),("beds","Bedrooms and baths"),("utility","Garage and basement")],"281",
 [("Main level","281-main-level.jpg"),("Upper level","281-upper-level.jpg"),("Basement","281-basement.jpg")],
 [("Price","$950,000","Listing agreement; MLS"),
  ("Address","281 Solar Spring Circle, Carroll (Twin Mountain), NH "+tbd("ZIP code: documents show 03595 and 03598"),"Tax card per Keegan Rice"),
  ("Tax map","Map 206, Lot 58.4","Listing agreement; septic plan"),
  ("Lot","1.00 acre, level, surveyed, 125 ft of frontage","MLS sheet"),
  ("Residences","Two, side by side. Each 4 bedrooms, 3 full baths, approx. 1,792 sq ft (3,584 sq ft total)","Assessor via MLS sheet"),
  ("Garage","Attached two-car garage for each residence, four bays in all, with openers","Photos; floor plan; Keegan Rice"),
  ("Basement","Full, unfinished, insulated ceiling, bulkhead access. Approx. 1,792 sq ft total","Assessor via MLS sheet"),
  ("Built","2023. New construction, never occupied","MLS sheet; Keegan Rice"),
  ("Construction","Modular, by Westchester Modular Homes. Wood frame, vinyl siding, asphalt shingle roof. R-21 walls with 1-inch rigid foam, Andersen 200 Series windows, 91 psf design snow load, one-hour fire separation and 56 STC sound-rated wall between residences","Westchester plan set, serial 23130; applicability confirmed by Keegan Rice"),
  ("Heat and hot water","Propane hot water baseboard, multiple zones per residence. On-demand water heater. No central cooling","MLS sheet; photos"),
  ("Electric","200-amp service, underground. Separate electric and propane meters for each residence","MLS sheet"),
  ("Water and septic","Public water. Private septic shared by the two residences: 8-bedroom Enviro-Septic design, 2,500-gallon tank, NHDES approval eCA2021112215 dated November 22, 2021","Horizons Engineering septic plan, Lot 5"),
  ("Finishes","Granite counters, wood cabinetry with crown molding, tile in kitchens and baths, plank flooring, oak stair treads, recessed lighting","Keegan Rice; photos"),
  ("Appliances","Stainless refrigerator, electric range and dishwasher in each kitchen. Laundry hookups on the second floor "+tbd("microwaves"),"Photos; MLS sheet"),
  ("Outdoors","Covered entry porches. Stamped concrete patio for each residence, about 24 by 9 ft","CubiCasa scan; aerial photos"),
  ("Road and drive","Private association road. Paving of the road, driveways and walkways by the seller "+tbd("paving date"),"Listing agreement, section 9"),
  ("Taxes","$6,727 (2025)","MLS sheet"),
  ("Association dues",tbd("from HOA budget"),""),
  ("Warranty",tbd("builder and manufacturer warranty terms"),"")],
 doc("Floor plans with dimensions","All three levels, CubiCasa, PDF","../docs/281-solar-spring-circle-floor-plans.pdf")+doc("State-approved septic plan","Horizons Engineering, Lot 5, NHDES eCA2021112215","../docs/281-solar-spring-circle-septic-plan.pdf")+doc("Property brochure","Eight pages, in production")+doc("Seller's property disclosure","From the seller"))

building("residences/37-solar-spring-circle.html","37 Solar Spring Circle","The Colonial at the Gate","assets/img/37/LSD01943twilight_2000.jpg","Twilight sky digitally enhanced.",
 "A gray colonial on the largest of the duplex lots, the first building you reach from Route 3, and the one designed around ease of movement.",
 [("4 + 4","Bedrooms"),("2 + 2","Full baths"),("2","Attached garages"),("1.12","Acres"),("151 ft","Frontage")],
 f'''<p class="lede">A mountain home that works for everyone who visits. In both residences, a ramp with handrails leads from the garage to the kitchen door, and the main level has a bedroom beside a full bath with a large roll-in shower, two shower heads and a wall-mounted sink.</p>
<p>The living room runs more than 20 feet, with an oak staircase at its center. The white shaker-style kitchen has stainless appliances and tile floors. Upstairs are three more bedrooms and a full bath with a tub; the smallest bedroom makes a natural office. Out back, each home has a stamped concrete patio and a lawn edged in young pine and birch.</p>
<p>New construction, never occupied. Sold as one building to one owner. The front entries have steps; the step-free route into each home is through its garage.</p>''',
 G37,"37",[("exterior","Exterior"),("access","Accessible features"),("living","Living and dining"),("kitchen","Kitchen"),("beds","Bedrooms and baths"),("utility","Basement")],"37",
 [("Main level","37-main-level.jpg"),("Upper level","37-upper-level.jpg"),("Basement","37-basement.jpg")],
 [("Price","$950,000","Listing agreement; MLS"),
  ("Address","37 Solar Spring Circle, Carroll (Twin Mountain), NH "+tbd("ZIP code"),"Tax card per Keegan Rice"),
  ("Tax map","Map 206, Lot 58.6","Listing agreement; septic plan"),
  ("Lot","1.12 acres (48,787 sq ft), level, surveyed, 151 ft of frontage","MLS sheet"),
  ("Residences","Two, side by side. Each 4 bedrooms and 2 full baths","Floor plan; confirmed by Keegan Rice"),
  ("Living area","Approx. 1,400 sq ft per residence, 2,803 sq ft total, as measured by 3D scan "+tbd("assessor or builder figure"),"CubiCasa scan, Aug 31, 2026"),
  ("Accessible features","In both residences: garage ramp with handrails to the kitchen entry, first-floor bedroom, main-level bath with roll-in shower, two shower heads and wall-mounted sink, lever door handles "+tbd("design standard, clear door and hall widths"),"Photos; floor plan; Keegan Rice"),
  ("Garage","Attached garage for each residence, about 20 by 23 ft, with opener","CubiCasa scan; photos"),
  ("Basement","Full, unfinished, insulated ceiling, bulkhead access","MLS sheet; photos"),
  ("Built","2023. New construction, never occupied","MLS sheet; Keegan Rice"),
  ("Construction","Modular, by Westchester Modular Homes. Wood frame, vinyl siding, asphalt shingle roof. R-21 walls with 1-inch rigid foam, Andersen 200 Series windows, one-hour fire separation and 56 STC sound-rated wall between residences","Westchester duplex specification; applicability confirmed by Keegan Rice"),
  ("Heat and hot water","Propane hot water baseboard, multiple zones per residence. On-demand water heater. No central cooling","MLS sheet; photos"),
  ("Electric","200-amp service. Separate electric and propane meters for each residence","MLS sheet"),
  ("Water and septic","Public water. Private septic shared by the two residences: 8-bedroom Enviro-Septic design, 2,500-gallon tank, NHDES approval eCA2023082407 dated August 24, 2023","Horizons Engineering septic plan, Lot 7"),
  ("Finishes","Formica kitchen counters, granite bath vanity tops, white shaker-style cabinetry, tile in kitchens, plank flooring, oak staircase","Keegan Rice; photos"),
  ("Appliances","Stainless refrigerator, electric range and dishwasher in each kitchen. Laundry hookups "+tbd("microwaves; laundry location"),"Photos; MLS sheet"),
  ("Outdoors","Gabled entry porches. Stamped concrete patio for each residence, about 20 by 8 ft","CubiCasa scan; photos"),
  ("Road and drive","Private association road. Paving of the road, driveways and walkways by the seller "+tbd("paving date"),"Listing agreement, section 9"),
  ("Taxes",tbd("current assessment is land only"),"MLS sheet"),
  ("Association dues",tbd("from HOA budget"),""),
  ("Warranty",tbd("builder and manufacturer warranty terms"),"")],
 doc("Floor plans with dimensions","All three levels, CubiCasa, PDF","../docs/37-solar-spring-circle-floor-plans.pdf")+doc("State-approved septic plan","Horizons Engineering, Lot 7, NHDES eCA2023082407","../docs/37-solar-spring-circle-septic-plan.pdf")+doc("Accessibility feature sheet","Measured clearances and features, in production")+doc("Property brochure","Eight pages, in production")+doc("Seller's property disclosure","From the seller"))

# 295 placeholder
write("residences/295-solar-spring-circle.html",page("residences/295-solar-spring-circle.html","295 Solar Spring Circle","The third duplex at Twin Peaks Village.",
 f'''<section><div class="wrap narrow"><p class="kicker">295 Solar Spring Circle &middot; Map 206, Lot 58.5</p><h2>The third duplex</h2><div class="hair"></div>
<p class="lede">The third completed duplex stands between 281 and 37 Solar Spring Circle. It shares the dormered design of 281.</p>
{tbdblock("Photography, floor plans, film and specifications to come","Needs a shoot date and the same scan package as the other two buildings. Pricing and release timing to be confirmed.")}
<div style="height:28px"></div>{spec([("Septic","8-bedroom Enviro-Septic design, 2,500-gallon tank, NHDES approval eCA2023090625 dated September 6, 2023","Horizons Engineering septic plan, Lot 6"),("Lot","43,942 sq ft","Horizons Engineering site plan"),("Bedrooms, baths, square footage",tbd("from scan and assessor"),""),("Price",tbd("public price and release date"),"")])}</div></section>
<section class="band-paper tight"><div class="wrap">{gallery([g for g in GSITE if g[0] in ("DJI_0647","DJI_0618")],"site",[],"../")}</div></section>{cta("../")}''',pre="../"))

# ---------------- HUNTER
HUNTER_SPEC=spec([("Plan","Westchester Modular Homes “Hunter,” 60 by 27 ft, single level","Westchester plan set, serial 26129, July 1, 2026"),
("Rooms","Living room 18′10″ x 12′9″, primary bedroom 13′2″ x 16′4″, bedrooms 10′6″ x 12′9″, dining 10′9″ x 12′9″, kitchen with pantry","Plan set, sheet 3A"),
("Garage","Attached, 24 by 24 ft, two overhead doors","Plan set"),("Basement","Full","Plan set, sheet 2"),
("Envelope","R-21 walls with 1-inch rigid foam, R-49 roof, Andersen 200 Series windows, 90 psf design snow load","Plan set"),
("Exterior","Siding, shake-style gables, stone accents and PVC trim "+tbd("final colors and materials as built"),"Plan set; rendering"),
("Price",tbd("model home price and base price for future builds"),""),("Completion","Fall 2026 "+tbd("open house date"),"Keegan Rice, Sept 19, 2026")])
hunter_body=f'''
<section><div class="wrap split top"><div><p class="kicker">1 Solar Spring Circle &middot; Model home</p><h2>Everything on one level</h2><div class="hair"></div>
<p class="lede">The Hunter is a single-level home by Westchester Modular Homes, and the model for the single-family homesites at Twin Peaks Village.</p>
<p>A covered porch with tapered columns leads into an open living room, dining room and kitchen with a pantry. The primary suite sits at one end of the house, with two more bedrooms and a second full bath at the other. A sliding door opens from the dining room to the back, and the two-car garage is attached.</p>
<p>The home was set on its foundation on September 16, 2026. Construction and final fit-up continue through the fall.</p></div>
<div><div class="facts" style="margin-top:0"><div><b>3</b><span>Bedrooms</span></div><div><b>2</b><span>Full baths</span></div><div><b>1,630</b><span>Approx. sq ft, from plans</span></div><div><b>2-car</b><span>Attached garage</span></div></div>
{HUNTER_SPEC}</div></div></section>
<section class="band-paper"><div class="wrap"><p class="kicker">Progress</p><h2>Watch it rise</h2><div class="hair"></div>
{tbdblock("Set day and construction photographs","Photos or video from September 16 and weekly progress through fit-up.")}</div></section>
<section><div class="wrap split top"><div><p class="kicker">Build with us</p><h2>Your home, on your lot</h2><div class="hair"></div>
<p>Five single-family homesites are part of Phase One, with nineteen more lots in Phase Two. Future homes are built under the developer's construction manager, who works with each buyer from plan selection through final fit-up.</p>
<p>{tbd("standard features, options list and lot pricing")}</p></div>
<div class="people"><div class="person"><b>Charles Allen</b><span>Construction manager, Construction Management &amp; Estimating<br>PO Box 71, Madison, NH 03849</span><a href="tel:+16033878917">603-387-8917</a><a href="mailto:constructionmanager6426@aol.com">constructionmanager6426@aol.com</a></div></div></div></section>
{cta()}'''
write("hunter.html",page("hunter.html","The Hunter model home","The Hunter, a single-level model home at Twin Peaks Village.",hunter_body,
 hero("assets/img/model/hunter-rendering_1536.jpg","The model home","The Hunter","Three bedrooms, two baths and a two-car garage on one level. Set September 16, 2026 and finishing this fall.",credit="Artist's rendering. Landscaping, driveway and background are illustrative.")))

# ---------------- LOCATION
def place(n,d): return f'<tr><th scope="row">{n}</th><td>{d}<span class="src">{tbd("measured drive time")}</span></td></tr>'
location_body=f'''
<section><div class="wrap split top"><div><p class="kicker">Getting here</p><h2>Just south of the junction</h2><div class="hair"></div>
<p class="lede">From the intersection of US Route 3 and US Route 302 in Twin Mountain, head south on Route 3. Solar Spring Circle is about three tenths of a mile on the left.</p>
<p class="note">Directions from the Horizons Engineering plans on file.</p>
{tbdblock("Location map","Branded map showing the village, Routes 3 and 302, and the destinations below.")}</div>
<div><img src="assets/img/site/DJI_0623_2000.jpg" alt="Aerial view across Route 3 and the valley from above Twin Peaks Village" loading="lazy"></div></div></section>
<section class="band-paper"><div class="wrap"><p class="kicker">Nearby</p><h2>What is close at hand</h2><div class="hair"></div>
<table class="spec"><tbody>
{place("Bretton Woods","Alpine and Nordic skiing, golf and four-season resort activities")}
{place("Cannon Mountain and Franconia Notch State Park","Skiing, the aerial tramway, Echo Lake and the notch trail network")}
{place("Crawford Notch State Park","Hiking, waterfalls and Route 302 through the notch")}
{place("Mount Washington Cog Railway","The mountain-climbing railway to the summit of Mount Washington")}
{place("Presidential Range trailheads","Mount Washington, Mount Jefferson, Mount Adams and the surrounding peaks")}
{place("Ammonoosuc River","Fishing and paddling")}
{place("Snowmobile corridor trails","The regional trail network passes near the village "+tbd("access route, with the local club"))}
{place("Littleton and Bethlehem","Dining, shopping, hospital and services")}
</tbody></table>
<p class="note" style="margin-top:16px">Places are listed for geographic reference only. Twin Peaks Village is not affiliated with any resort, railway or park.</p></div></section>
<section><div class="wrap"><p class="kicker">On the horizon</p><h2>The Presidential Range from above the village</h2><div class="hair"></div>
{gallery([g for g in GSITE if g[0] in ("DJI_0626","DJI_0619","DJI_0636","DJI_0623")],"site",[])}
<p class="note" style="margin-top:14px">Aerial photographs taken by drone above the property. Views from ground level and from individual homes vary. {tbd("foliage and winter photography")}</p></div></section>
{cta()}'''
write("location.html",page("location.html","Location","Twin Mountain, New Hampshire: between Franconia Notch and Crawford Notch.",location_body,
 hero("assets/img/site/DJI_0626_2000.jpg","Location","Between two notches","Twin Mountain sits where Routes 3 and 302 meet, with Bretton Woods, Cannon Mountain and the Presidential Range all around.",short=True)))

# ---------------- DOCUMENTS
documents_body=f'''<section><div class="wrap narrow"><p class="kicker">Offering package</p><h2>Documents</h2><div class="hair"></div>
<p class="lede">Everything a buyer or buyer's agent needs, in one place. Documents are added here as they are finalized.</p>
<h4 style="margin-top:36px">281 Solar Spring Circle</h4><div class="doclist">{doc("Floor plans with dimensions","CubiCasa, all levels","docs/281-solar-spring-circle-floor-plans.pdf")}{doc("State-approved septic plan","NHDES eCA2021112215","docs/281-solar-spring-circle-septic-plan.pdf")}{doc("Property brochure","In production")}{doc("Seller's property disclosure","From the seller")}</div>
<h4 style="margin-top:36px">37 Solar Spring Circle</h4><div class="doclist">{doc("Floor plans with dimensions","CubiCasa, all levels","docs/37-solar-spring-circle-floor-plans.pdf")}{doc("State-approved septic plan","NHDES eCA2023082407","docs/37-solar-spring-circle-septic-plan.pdf")}{doc("Accessibility feature sheet","In production")}{doc("Property brochure","In production")}{doc("Seller's property disclosure","From the seller")}</div>
<h4 style="margin-top:36px">The village</h4><div class="doclist">{doc("Declaration of covenants and bylaws","From Attorney Andy Sullivan")}{doc("Association budget and dues","From Attorney Andy Sullivan")}{doc("Purchase and sale agreement","Standard form, with any development addenda")}{doc("Illustrated site map","In production")}{doc("Construction specification","Westchester Modular Homes duplex and Hunter specifications")}{doc("Community offering package","In production, pending association documents")}</div>
</div></section>{cta()}'''
write("documents.html",page("documents.html","Documents","Offering documents for Twin Peaks Village.",documents_body))

# ---------------- CONTACT
contact_body=f'''<section><div class="wrap split top"><div><p class="kicker">Inquire</p><h2>Request a showing or the offering package</h2><div class="hair"></div>
<form name="inquiry" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="thanks.html">
<input type="hidden" name="form-name" value="inquiry"><p hidden><label>Leave this empty <input name="bot-field"></label></p>
<div class="two"><label for="f-name">Name<input id="f-name" name="name" required autocomplete="name"></label><label for="f-email">Email<input id="f-email" type="email" name="email" required autocomplete="email"></label></div>
<div class="two"><label for="f-phone">Phone<input id="f-phone" type="tel" name="phone" autocomplete="tel"></label><label for="f-interest">I am interested in<select id="f-interest" name="interest"><option>281 Solar Spring Circle</option><option>37 Solar Spring Circle</option><option>295 Solar Spring Circle</option><option>The Hunter model home</option><option>A single-family homesite</option><option>The village in general</option></select></label></div>
<div class="two"><label for="f-agent">Are you working with an agent?<select id="f-agent" name="agent"><option>No</option><option>Yes</option><option>I am an agent</option></select></label><label for="f-when">Timing<select id="f-when" name="timing"><option>Ready now</option><option>Within 6 months</option><option>6 to 12 months</option><option>Just looking</option></select></label></div>
<label for="f-msg">Message<textarea id="f-msg" name="message"></textarea></label>
<div><button class="btn fill" style="color:var(--forest-deep)" type="submit">Send inquiry</button></div>
<p class="note">Your inquiry goes to the listing agents at Badger Peabody &amp; Smith Realty. We do not share your information.</p></form></div>
<div><div class="people" style="grid-template-columns:1fr">
<div class="person"><b>Keegan Rice</b><span>REALTOR&reg;, NH Lic. #072031 &middot; Badger Peabody &amp; Smith Realty</span><a href="tel:+16033487261">603-348-7261</a><a href="mailto:KeeganR@BadgerPeabodySmith.com">KeeganR@BadgerPeabodySmith.com</a></div>
<div class="person"><b>Matthew Penner</b><span>Badger Peabody &amp; Smith Realty {tbd("title and license number")}</span><a href="tel:+16037145148">603-714-5148</a><a href="mailto:MatthewP@BadgerPeabodySmith.com">MatthewP@BadgerPeabodySmith.com</a></div>
<div class="person"><b>Badger Peabody &amp; Smith Realty</b><span>Bretton Woods office &middot; 603-259-0210<br>{tbd("office street address and brokerage disclosure line")}</span></div></div></div></div></section>'''
write("contact.html",page("contact.html","Inquire","Contact the listing agents for Twin Peaks Village.",contact_body))
write("thanks.html",page("thanks.html","Thank you","",'<section><div class="wrap narrow"><p class="kicker">Received</p><h2>Thank you</h2><div class="hair"></div><p class="lede">Your inquiry is on its way to Keegan Rice and Matthew Penner. One of us will be in touch shortly.</p><div class="btns"><a class="btn dark" href="index.html">Back to the village</a></div></div></section>'))

# ---------------- LEGAL
legal_body=f'''<section><div class="wrap narrow"><p class="kicker">Legal</p><h2>Disclosures</h2><div class="hair"></div>
{tbdblock("This page is a draft for Attorney Andy Sullivan","Every paragraph below is proposed wording and should be replaced or approved by counsel before the site is public.")}
<h3 style="margin-top:36px">Land sales registration</h3><p>{tbd("RSA 356-A registration or exemption statement, registration number and any required notice to purchasers")}</p>
<h3>Accuracy</h3><p>Information on this site comes from the seller, public records, engineering plans, the manufacturer's drawings and on-site scans, as noted on each page. It is believed accurate but is not guaranteed, and it may change without notice. Square footage and dimensions are approximate. Buyers should verify anything material to their decision.</p>
<h3>Images</h3><p>Photographs were taken at the property on August 31 and September 1, 2026. Images labeled "virtually staged" contain digital furnishings that are not included in the sale. Twilight images have a digitally enhanced sky. The image of The Hunter is an artist's rendering; landscaping, paving and background scenery are illustrative and the finished home may differ. Aerial views are from a drone above the property and do not represent the view from any home.</p>
<h3>Association and use</h3><p>All homes are subject to the declaration, bylaws and rules of the homeowners' association, which will be provided to buyers when final. Municipal zoning and ordinances of the Town of Carroll apply. Nothing on this site is a representation about rental income, appreciation or investment return.</p>
<h3>Brokerage</h3><p>Twin Peaks Village is exclusively listed by Badger Peabody &amp; Smith Realty. The listing agents represent the seller. {tbd("firm brokerage disclosure wording and office address")}</p>
<h3>Fair housing</h3><p>We are pledged to the letter and spirit of the Fair Housing Act and the New Hampshire Law Against Discrimination. Homes at Twin Peaks Village are offered without regard to race, color, religion, sex, disability, familial status, national origin, age, marital status, sexual orientation or gender identity.</p>
</div></section>'''
write("legal.html",page("legal.html","Legal and disclosures","Disclosures for Twin Peaks Village.",legal_body))

# ---------------- static
shutil.copy(os.path.join(ROOT,"src/site.css"),os.path.join(DIST,"assets/site.css"))
shutil.copy(os.path.join(ROOT,"src/site.js"),os.path.join(DIST,"assets/site.js"))
open(os.path.join(DIST,"robots.txt"),"w").write("User-agent: *\nDisallow: /\n")
open(os.path.join(DIST,"netlify.toml"),"w").write('[build]\n  publish = "."\n\n[[headers]]\n  for = "/*"\n  [headers.values]\n    X-Robots-Tag = "noindex, nofollow"\n    X-Content-Type-Options = "nosniff"\n    Referrer-Policy = "strict-origin-when-cross-origin"\n\n[[headers]]\n  for = "/assets/*"\n  [headers.values]\n    Cache-Control = "public, max-age=604800"\n')
print("built")
