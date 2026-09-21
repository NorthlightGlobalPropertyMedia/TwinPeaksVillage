(function(){
  var btn=document.querySelector('.menu-btn'),nav=document.querySelector('.nav');
  if(btn){btn.addEventListener('click',function(){var o=nav.classList.toggle('open');btn.setAttribute('aria-expanded',o);});}

  // gallery filters
  document.querySelectorAll('[data-gallery]').forEach(function(g){
    var wrap=g.closest('.gal-wrap'), fs=wrap.querySelectorAll('.filters button');
    fs.forEach(function(b){b.addEventListener('click',function(){
      fs.forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');
      var f=b.dataset.f;
      g.querySelectorAll('button').forEach(function(t){t.hidden=!(f==='all'||t.dataset.cat===f);});
    });});
  });

  // lightbox
  var lb,img,cap,items=[],idx=0,last;
  function visible(g){return Array.prototype.filter.call(g.querySelectorAll('button'),function(b){return !b.hidden;});}
  function show(i){idx=(i+items.length)%items.length;var b=items[idx];img.src=b.dataset.full;img.alt=b.querySelector('img').alt;cap.textContent=b.dataset.cap+' ('+(idx+1)+' of '+items.length+')';}
  function close(){if(lb){lb.remove();lb=null;document.body.style.overflow='';if(last)last.focus();}}
  function open(g,b){
    items=visible(g);last=b;
    lb=document.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Photo viewer');
    lb.innerHTML='<button class="x" type="button">Close</button><button class="p" type="button" aria-label="Previous photo">Prev</button><img alt=""><div class="cap"></div><button class="n" type="button" aria-label="Next photo">Next</button>';
    document.body.appendChild(lb);document.body.style.overflow='hidden';
    img=lb.querySelector('img');cap=lb.querySelector('.cap');
    lb.querySelector('.x').onclick=close;lb.querySelector('.p').onclick=function(){show(idx-1)};lb.querySelector('.n').onclick=function(){show(idx+1)};
    lb.addEventListener('click',function(e){if(e.target===lb)close();});
    show(items.indexOf(b));lb.querySelector('.x').focus();
  }
  document.querySelectorAll('[data-gallery]').forEach(function(g){
    g.addEventListener('click',function(e){var b=e.target.closest('button');if(b)open(g,b);});
  });
  document.addEventListener('keydown',function(e){if(!lb)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(idx-1);if(e.key==='ArrowRight')show(idx+1);});

  // site plan: the engineer's drawing with selectable lots, pan and zoom
  var sp=document.getElementById('sp');
  if(sp){
    var view=document.getElementById('sp-view'),stage=document.getElementById('sp-stage'),lots=sp.querySelectorAll('.lot');
    var PW=+sp.dataset.w,PH=+sp.dataset.h,$=function(i){return document.getElementById(i)};
    var s=1,tx=0,ty=0,home={s:1,tx:0,ty:0},locked=false,MAXS=7;
    function dims(){var vw=view.clientWidth,vh=view.clientHeight;return{vw:vw,vh:vh,u:vw/PW,bh:vw*PH/PW};}
    function clamp(){
      var d=dims(),w=d.vw*s,h=d.bh*s;
      tx=w<=d.vw?(d.vw-w)/2:Math.min(0,Math.max(d.vw-w,tx));
      ty=h<=d.vh?(d.vh-h)/2:Math.min(0,Math.max(d.vh-h,ty));
    }
    function apply(ease){
      clamp();stage.classList.toggle('ease',!!ease);
      stage.style.transform='translate('+tx.toFixed(1)+'px,'+ty.toFixed(1)+'px) scale('+s.toFixed(4)+')';
      view.classList.toggle('zoomed',s>home.s*1.02);
      var d=dims(),r=14*Math.pow(s/home.s,.3),k=r/(46*d.u*s);
      stage.style.setProperty('--k',k.toFixed(3));
    }
    function fit(x0,y0,x1,y1,cap){
      var d=dims();s=Math.min(d.vw/((x1-x0)*d.u),d.vh/((y1-y0)*d.u));if(cap)s=Math.min(s,cap);s=Math.min(MAXS,s);
      tx=d.vw/2-s*d.u*(x0+x1)/2;ty=d.vh/2-s*d.u*(y0+y1)/2;
    }
    function setHome(){
      var d=dims();
      if(d.vh<d.bh-2)fit(90,300,3300,2990);else{s=1;tx=0;ty=0;}
      clamp();home={s:s,tx:tx,ty:ty};
    }
    function zoomAt(cx,cy,f,ease){
      var ns=Math.max(Math.min(home.s,1),Math.min(MAXS,s*f));f=ns/s;
      tx=cx-(cx-tx)*f;ty=cy-(cy-ty)*f;s=ns;apply(ease);
    }
    function pick(g){
      lots.forEach(function(x){x.classList.remove('on')});g.classList.add('on');
      var d=g.dataset;
      $('sp-k').textContent='Lot '+d.n+(d.kind==='duplex'?' · Duplex':d.kind==='model'?' · Model home':' · Homesite');
      $('sp-t').textContent=d.title;$('sp-a').textContent=d.kind==='lot'?d.street+', Carroll NH 03595':d.addr+', Carroll NH 03595';
      $('sp-s').textContent=d.status;$('sp-p').textContent=d.price;$('sp-z').textContent=d.sf+' sq ft · about '+d.ac+' ac';
      $('sp-d').hidden=false;var l=$('sp-l');l.hidden=false;l.href=d.link;l.textContent=d.kind==='lot'?'Ask about this homesite':'View details';
    }
    function clear(){
      lots.forEach(function(x){x.classList.remove('on')});locked=false;
      $('sp-k').textContent='Phase One';$('sp-t').textContent='Select a lot';
      $('sp-a').textContent='Choose any numbered lot. Drag to move the plan, and use the buttons to zoom.';
      $('sp-d').hidden=true;$('sp-l').hidden=true;
    }
    function select(g){
      locked=true;pick(g);
      var b=g.dataset.box.split(' ').map(Number),pad=330;
      fit(b[0]-pad,b[1]-pad,b[2]+pad,b[3]+pad,home.s*2.4);if(s<home.s)s=home.s;apply(true);
    }
    // pointers: drag to pan, two fingers to zoom
    var pts={},moved=false,start=null,pinch=null;
    function count(){return Object.keys(pts).length}
    view.addEventListener('pointerdown',function(e){
      if(e.target.closest('.sp-tools,.sp-legend'))return;
      pts[e.pointerId]={x:e.clientX,y:e.clientY};moved=false;
      if(count()===1)start={x:e.clientX,y:e.clientY,tx:tx,ty:ty};
      if(count()===2){var a=Object.values(pts);pinch={d:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),s:s};}
    });
    window.addEventListener('pointermove',function(e){
      if(!pts[e.pointerId])return;pts[e.pointerId]={x:e.clientX,y:e.clientY};
      var r=view.getBoundingClientRect(),a=Object.values(pts);
      if(a.length===2&&pinch){
        var dd=Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y),cx=(a[0].x+a[1].x)/2-r.left,cy=(a[0].y+a[1].y)/2-r.top;
        moved=true;zoomAt(cx,cy,(pinch.s*dd/pinch.d)/s);return;
      }
      if(a.length===1&&start){
        var dx=e.clientX-start.x,dy=e.clientY-start.y;
        if(!moved&&Math.hypot(dx,dy)<5)return;
        moved=true;view.classList.add('drag');tx=start.tx+dx;ty=start.ty+dy;apply();
      }
    });
    function up(e){if(!pts[e.pointerId])return;delete pts[e.pointerId];if(count()<2)pinch=null;if(count()===0){start=null;view.classList.remove('drag');}
      else{var a=Object.values(pts)[0];start={x:a.x,y:a.y,tx:tx,ty:ty};}}
    window.addEventListener('pointerup',up);window.addEventListener('pointercancel',up);
    view.addEventListener('click',function(e){if(moved){e.stopPropagation();e.preventDefault();moved=false;}},true);
    view.addEventListener('wheel',function(e){
      if(!(e.ctrlKey||e.metaKey))return;e.preventDefault();
      var r=view.getBoundingClientRect();zoomAt(e.clientX-r.left,e.clientY-r.top,Math.exp(-e.deltaY*.0045));
    },{passive:false});
    view.addEventListener('dblclick',function(e){
      if(e.target.closest('.lot,.sp-tools'))return;var r=view.getBoundingClientRect();zoomAt(e.clientX-r.left,e.clientY-r.top,1.7,true);
    });
    function center(f){var d=dims();zoomAt(d.vw/2,d.vh/2,f,true);}
    $('sp-in').addEventListener('click',function(){center(1.6)});
    $('sp-out').addEventListener('click',function(){center(1/1.6)});
    $('sp-reset').addEventListener('click',function(){clear();s=home.s;tx=home.tx;ty=home.ty;apply(true);});
    lots.forEach(function(g){
      g.addEventListener('mouseenter',function(){if(!locked)pick(g)});
      g.addEventListener('focus',function(){if(!locked)pick(g)});
      g.addEventListener('click',function(){select(g)});
      g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();select(g);$('sp-l').focus();}});
    });
    var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){var on=sp.querySelector('.lot.on');setHome();if(on&&locked)select(on);else apply();},120);});
    setHome();apply();
  }
})();
