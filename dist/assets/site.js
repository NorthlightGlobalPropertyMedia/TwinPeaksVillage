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
})();
