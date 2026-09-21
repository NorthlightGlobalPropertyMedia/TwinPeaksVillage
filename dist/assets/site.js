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

  // site plan
  var lots=document.querySelectorAll('.siteplan .lot');
  if(lots.length){
    var $=function(i){return document.getElementById(i)};
    function pick(g,sticky){
      lots.forEach(function(x){x.classList.remove('on')});g.classList.add('on');
      var d=g.dataset;
      $('sp-k').textContent='Lot '+d.n+(d.kind==='duplex'?' \u00b7 Duplex':d.kind==='model'?' \u00b7 Model home':' \u00b7 Homesite');
      $('sp-t').textContent=d.title;$('sp-a').textContent=d.kind==='lot'?'Solar Spring Circle, Carroll NH 03595':d.addr+', Carroll NH 03595';
      $('sp-s').textContent=d.status;$('sp-p').textContent=d.price;$('sp-z').textContent=d.sf+' sq ft \u00b7 about '+d.ac+' ac';
      $('sp-d').hidden=false;var l=$('sp-l');l.hidden=false;l.href=d.link;l.textContent=d.kind==='lot'?'Ask about this homesite':'View details';
    }
    var locked=false;
    lots.forEach(function(g){
      g.addEventListener('mouseenter',function(){if(!locked)pick(g)});
      g.addEventListener('focus',function(){pick(g)});
      g.addEventListener('click',function(){locked=true;pick(g)});
      g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();locked=true;pick(g);$('sp-l').focus();}});
    });
  }
})();
