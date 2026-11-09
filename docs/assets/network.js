'use strict';
(() => {
  const data=window.P4NETWORK, $=id=>document.getElementById(id), ns='http://www.w3.org/2000/svg';
  const lookup=new Map(data.nodes.map(n=>[n.id,n])), positions=new Map(), edgeElements=new Map();
  let index=0,timer=null;
  const make=(tag,attrs={})=>{const n=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))n.setAttribute(k,v);return n;};
  // A deterministic two-ring layout uses the whole year once, never re-layouts per frame.
  const filers=data.nodes.filter(n=>n.kind!=='Ticker'), tickers=data.nodes.filter(n=>n.kind==='Ticker');
  for(const [group,rx,ry]of [[filers,530,320],[tickers,330,220]])group.forEach((n,i)=>{const angle=2*Math.PI*i/group.length-Math.PI/2;positions.set(n.id,[600+rx*Math.cos(angle),380+ry*Math.sin(angle)]);});
  for(const n of data.nodes){const [x,y]=positions.get(n.id),g=make('g',{class:'node',transform:`translate(${x},${y})`,tabindex:'0','aria-label':`${n.label}, ${n.kind}`});const title=make('title');title.textContent=`${n.label} · ${n.kind}`;g.append(title,make('circle',{r:n.kind==='Ticker'?3:5,class:'dot '+n.kind}));n.element=g;$('nodes').append(g);}
  filers.forEach(n=>{const o=document.createElement('option');o.value=n.id;o.textContent=`${n.label} (${n.kind})`;$('filer').append(o);});
  function accepted(e){return ($('chamber').value==='All'||lookup.get(e.source).kind===$('chamber').value)&&($('filer').value==='All'||e.source===$('filer').value);}
  const key=e=>JSON.stringify([e.source,e.target]);
  function stop(){clearInterval(timer);timer=null;$('play').textContent='Play';}
  function render(){
    const current=new Map(data.frames[index].edges.filter(accepted).map(e=>[key(e),e]));
    const previous=new Map((index?data.frames[index-1].edges:[]).filter(accepted).map(e=>[key(e),e]));
    const union=new Map([...previous,...current]),active=new Set();let added=0,kept=0,removed=0;
    $('ties').replaceChildren();
    for(const [k,line]of edgeElements)if(!union.has(k)){line.remove();edgeElements.delete(k);}
    for(const [k,e]of union){const present=current.has(k),status=!present?'departing':index===0?'initial':previous.has(k)?'continuing':'new';
      if(status==='new')added++;if(status==='continuing')kept++;if(!present)removed++;
      if(present){active.add(e.source);active.add(e.target);}
      let line=edgeElements.get(k);if(!line){const [x1,y1]=positions.get(e.source),[x2,y2]=positions.get(e.target);line=make('line',{x1,y1,x2,y2});$('edges').append(line);edgeElements.set(k,line);}
      // Replace departing lines so a seek/replay starts a fresh fade.
      if(status==='departing'){const replacement=line.cloneNode(false);line.replaceWith(replacement);line=replacement;edgeElements.set(k,line);}
      line.setAttribute('class','edge '+status);line.setAttribute('stroke-width',Math.min(5,1+Math.log2(e.rows)));
      const tr=document.createElement('tr');for(const value of [lookup.get(e.source).label,lookup.get(e.target).label,status,present?e.rows:0]){const td=document.createElement('td');td.textContent=value;tr.append(td);}$('ties').append(tr);
    }
    for(const n of data.nodes){n.element.setAttribute('class','node'+(active.has(n.id)?' active':''));n.element.setAttribute('tabindex',active.has(n.id)?'0':'-1');n.element.querySelector('text')?.remove();if(active.has(n.id)&&$('filer').value!=='All'){const text=make('text',{x:8,y:4});text.textContent=n.label;n.element.append(text);}}
    $('month').value=index;$('date').textContent=new Date(2025,index,1).toLocaleDateString('en-US',{month:'long',year:'numeric'});
    $('stats').textContent=`${current.size} active connections · ${active.size} active nodes · ${index===0?current.size+' initial connections (no prior-month baseline)':added+' new · '+kept+' continuing · '+removed+' departing versus the preceding month'}`;
    $('back').disabled=index===0;$('forward').disabled=index===11;
  }
  function play(){stop();if(index===11){index=0;render();}$('play').textContent='Pause';timer=setInterval(()=>{index++;render();if(index===11)stop();},Number($('speed').value));}
  $('play').onclick=()=>timer?stop():play();$('month').oninput=()=>{stop();index=Number($('month').value);render();};
  $('back').onclick=()=>{stop();index=Math.max(0,index-1);render();};$('forward').onclick=()=>{stop();index=Math.min(11,index+1);render();};
  $('chamber').onchange=()=>{if($('filer').value!=='All'&&$('chamber').value!=='All'&&lookup.get($('filer').value).kind!==$('chamber').value)$('filer').value='All';render();};
  $('filer').onchange=render;$('speed').onchange=()=>{if(timer)play();};
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});render();
})();
