#!/usr/bin/env python3
"""Assemble website/dist from the project folder. Run from anywhere:  python3 website/src/assemble.py
Copies web images, video, brand marks and public documents into dist/, then runs build.py. Reads only; never touches media/raw."""
import os, shutil, glob, subprocess, sys
import numpy as np
from PIL import Image
SRC=os.path.dirname(os.path.abspath(__file__)); WEB=os.path.dirname(SRC); P=os.path.dirname(WEB); D=os.path.join(WEB,"dist")
def cp(a,b):
    os.makedirs(os.path.dirname(b),exist_ok=True)
    if not os.path.exists(b) or os.path.getmtime(a)>os.path.getmtime(b): shutil.copy2(a,b)
for k in ["281","37","site","model"]:
    for f in glob.glob(f"{P}/media/edited/web/{k}/*.jpg"): cp(f,f"{D}/assets/img/{k}/{os.path.basename(f)}")
for f in glob.glob(f"{P}/media/edited/web/site/*.webp"): cp(f,f"{D}/assets/img/site/{os.path.basename(f)}")
cp(f"{P}/documents/plans/site-plans/Phase 1 Site Plan.pdf",f"{D}/docs/echo-lake-subdivision-phase-1-site-plan.pdf")
for src,dst in [
 ("association/HOA Budget 2026 Phase I (signed).pdf","hoa-budget-2026-phase-1.pdf"),
 ("association/HOA Rules effective 2026-10-01 (signed).pdf","hoa-rules-2026.pdf"),
 ("disclosures/HOA Disclosure Rider 2026-09-25.pdf","hoa-disclosure-rider.pdf"),
 ("disclosures/Property Disclosure Duplex 2026-09-25.pdf","property-disclosure-duplex.pdf"),
 ("disclosures/Property Disclosure Single Family 2026-09-25.pdf","property-disclosure-single-family.pdf"),
 ("disclosures/Property Disclosure Land 2026-09-25.pdf","property-disclosure-land.pdf"),
 ("sales-forms/Purchase and Sale Agreement 2026-09-01.pdf","purchase-and-sale-agreement.pdf"),
 ("sales-forms/Limited Warranty 2026-09-01.pdf","limited-warranty.pdf"),
 ("registration/NH AG Certificate of Registration 2026-09-16.pdf","nh-certificate-of-registration.pdf"),
]: cp(f"{P}/documents/{src}",f"{D}/docs/{dst}")
for f in glob.glob(f"{P}/media/edited/web/plans3d/*.jpg"): cp(f,f"{D}/assets/img/plans3d/{os.path.basename(f)}")
for f in glob.glob(f"{P}/media/edited/video/*"): cp(f,f"{D}/assets/video/{os.path.basename(f)}")
for f in glob.glob(f"{P}/brand/logos-vector/*.svg")+[f"{P}/brand/logos-vector/04_icon_mark_hires.png",f"{P}/brand/bps-logos/bps_logo_rev.png"]: cp(f,f"{D}/assets/brand/{os.path.basename(f)}")
for b in ["281","37"]:
    cp(glob.glob(f"{P}/documents/floor-plans/{b}-solar-spring-circle/pdf-with-dim/*.pdf")[0],f"{D}/docs/{b}-solar-spring-circle-floor-plans.pdf")
    cp(f"{P}/documents/plans/septic/{b} Solar Spring Septic Plan.pdf",f"{D}/docs/{b}-solar-spring-circle-septic-plan.pdf")
    # floor plan images: CubiCasa labels the basement "1st"; relabel and trim the footer text
    for lvl,name in [("1st","basement"),("2nd","main-level"),("3rd","upper-level")]:
        out=f"{D}/assets/img/plans/{b}-{name}.jpg"
        if os.path.exists(out): continue
        im=Image.open(f"{P}/media/edited/web/plans/{b}_{lvl}.jpg").convert("RGB")
        rows=(np.asarray(im.convert("L"))<235).sum(1)>0; gaps=[]; s=None
        for y,v in enumerate(rows):
            if not v and s is None: s=y
            if v and s is not None:
                if y-s>=30: gaps.append(s)
                s=None
        os.makedirs(os.path.dirname(out),exist_ok=True)
        im.crop((0,0,im.width,(gaps[-1] if gaps else im.height-20)+20)).save(out,quality=86)
subprocess.check_call([sys.executable,os.path.join(SRC,"build.py")])
