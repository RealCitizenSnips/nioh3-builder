/* n3-v010 overlay: Level-tab lookups, sheet names/weights/reqs, icon files */
const N3_ICON_VER = "010";
const N3_STAT_ICON = {con:"stat-constitution",hrt:"stat-heart",sta:"stat-stamina",str:"stat-strength",skl:"stat-skill",int:"stat-intellect",mag:"stat-magic"};
const N3_SLOT_ICON = {head:"slot-head",chest:"slot-chest",arms:"slot-arms",waist:"slot-waist",feet:"slot-feet",w1:"slot-weapon",w2:"slot-weapon",bow:"slot-ranged",acc1:"slot-accessory",acc2:"slot-accessory"};
function n3WeaponIconId(tp){
  if(!tp || tp==="all") return "slot-weapon";
  return "weapon-"+String(tp).toLowerCase().replace(/ & /g,"-").replace(/ /g,"-");
}
function n3iconErr(el, id){
  const cur = el.getAttribute("src")||"";
  if(cur.indexOf(id+".png")>=0){ el.src = "icons/"+id+".svg?v="+N3_ICON_VER; return; }
  if(cur.indexOf(id+".svg")>=0){ el.src = "icons/"+id+".jpg?v="+N3_ICON_VER; return; }
  if(cur.indexOf(id+".jpg")>=0){ el.src = "icons/placeholder.svg?v="+N3_ICON_VER; return; }
}
function n3icon(id, title){
  if(!id) id = "placeholder";
  const t = title || id;
  return '<img class="ico" src="icons/'+id+'.png?v='+N3_ICON_VER+'" alt="" title="'+t+'" onerror="n3iconErr(this,\''+id+'\')">';
}

const N3_KEYS = ["conLife","hrtLife","hrtKi","hrtKiRec","staLife","staSamWt","staNinWt","strLife","strKiDmg","sklLife","sklArts","sklNin","intLife","intKiRec","intDur","magLife","magOnmyo"];
function n3row(n){
  n = Math.max(1, Math.round(+n||1));
  if(N3_LEVEL[n]) return N3_LEVEL[n];
  const last = 94;
  const prev = 93;
  const a = N3_LEVEL[last], b = N3_LEVEL[prev];
  if(!a || !b) return N3_LEVEL[last];
  const out = a.slice();
  const steps = n - last;
  for(let i=0;i<a.length;i++) out[i] = +(a[i] + (a[i]-b[i])*steps).toFixed(4);
  return out;
}
function n3val(n, key){
  const i = N3_KEYS.indexOf(key);
  if(i<0) return 0;
  const v = n3row(n)[i];
  return v==null ? 0 : v;
}
function n3delta(n, key){
  if(n<=1) return n3val(1, key);
  return +(n3val(n, key) - n3val(n-1, key)).toFixed(4);
}
function n3soft(stat, n){
  const map = {
    con:[["conLife","Life"]],
    hrt:[["hrtKi","Ki"],["hrtLife","Life"],["hrtKiRec","Ki Rec"]],
    sta:[["staLife","Life"],["staSamWt","Samurai Wt"],["staNinWt","Ninja Wt"]],
    str:[["strKiDmg","Ki Dmg"],["strLife","Life"]],
    skl:[["sklArts","Arts"],["sklNin","Ninjutsu"],["sklLife","Life"]],
    int:[["intDur","Duration"],["intKiRec","Ki Rec"],["intLife","Life"]],
    mag:[["magOnmyo","Onmyo"],["magLife","Life"]]
  };
  const cols = map[stat]||[];
  const bits = [];
  cols.forEach(([k,lab]) => {
    const d = n3delta(n, k);
    bits.push(lab+" "+(d>=0?"+":"")+d);
  });
  const mainKey = cols[0] && cols[0][0];
  let gain = "";
  if(mainKey){
    const d = Math.abs(n3delta(n, mainKey));
    const early = Math.abs(n3delta(Math.min(n,6), mainKey)) || d;
    const ratio = early ? d/early : 1;
    if(ratio >= 0.75) gain = "high gain";
    else if(ratio >= 0.45) gain = "mid gain";
    else if(ratio >= 0.2) gain = "lower gain";
    else gain = "low gain";
  }
  return (gain?gain+" · ":"") + bits.join(" · ");
}

function applySheetTruth(){
  if(typeof PIECES==="undefined") return;
  const ren = N3_TRUTH.renames||{};
  const by = {};
  (N3_TRUTH.truth||[]).forEach(t => { if(t && t.name) by[t.name] = t; });
  Object.keys(ren).forEach(old => {
    if(by[ren[old]] && !by[old]) by[old] = by[ren[old]];
  });
  Object.keys(PIECES).forEach(slot => {
    PIECES[slot].forEach(p => {
      if(!p || !p.name) return;
      if(ren[p.name]) p.name = ren[p.name];
      const t = by[p.name];
      if(!t) return;
      if(t.weight!=null && t.weight!=="") p.weight = +t.weight;
      if(t.req) p.req = t.req;
      if(t.wt) p.wt = t.wt;
      if(t.set && t.set!=="none") p.set = t.set;
    });
  });
  (N3_TRUTH.extras||[]).forEach(ex => {
    const list = PIECES[ex.slot];
    if(!list) return;
    if(list.some(p => p.name===ex.name)) return;
    const np = (typeof P==="function") ? P(ex.name, ex.set||"none", ex.style||"samurai") : {name:ex.name,set:ex.set||"none",style:ex.style||"samurai"};
    if(ex.wt) np.wt = ex.wt;
    if(ex.weight!=null) np.weight = +ex.weight;
    if(ex.req) np.req = ex.req;
    list.push(np);
  });
}

function coreFromLevels(){
  const ninja = stylesOn().includes("ninja") && !stylesOn().includes("samurai");
  const sam = stylesOn().includes("samurai") && !stylesOn().includes("ninja");
  const life = n3val(char.con,"conLife")+n3val(char.hrt,"hrtLife")+n3val(char.sta,"staLife")+n3val(char.str,"strLife")+n3val(char.skl,"sklLife")+n3val(char.int,"intLife")+n3val(char.mag,"magLife");
  const ki = n3val(char.hrt,"hrtKi");
  const kiRec = +(n3val(char.hrt,"hrtKiRec")+n3val(char.int,"intKiRec")).toFixed(1);
  const meleeKi = +n3val(char.str,"strKiDmg").toFixed(1);
  const arts = n3val(char.skl,"sklArts");
  const ninPow = n3val(char.skl,"sklNin");
  const onmyo = n3val(char.mag,"magOnmyo");
  const dur = +n3val(char.int,"intDur").toFixed(1);
  let melee = 0;
  if(sam) melee = char.hrt*2 + char.str*2 + char.int*2;
  else if(ninja) melee = char.hrt*1 + char.str*1 + char.mag*1;
  else melee = null;
  const wlim = ninja ? +(15 + n3val(char.sta,"staNinWt")).toFixed(1) : (sam ? +(20 + n3val(char.sta,"staSamWt")).toFixed(1) : null);
  return {life, ki, kiRec, meleeKi, arts, ninPow, onmyo, dur, melee, wlim, ninja, sam};
}
function maxWeight(){
  const ninja = stylesOn().includes("ninja") && !stylesOn().includes("samurai");
  const bonus = ninja ? n3val(char.sta,"staNinWt") : n3val(char.sta,"staSamWt");
  const base = ninja ? 15 : 20;
  return +(base + bonus).toFixed(1);
}
function softNote(v, stat){
  if(!stat) stat = "con";
  return n3soft(stat, v);
}
function pieceReq(p){
  if(!p) return null;
  if(p.req) return p.req;
  const m = SET_META[p.set];
  return m && m.req ? m.req : null;
}
function wIcon(type){
  return n3icon(n3WeaponIconId(type), type||"");
}

applySheetTruth();

function paintStatHints(){
  const {need, names} = equippedReqs();
  STATS.forEach(([k,lab]) => {
    const el = document.querySelector('[data-need="'+k+'"]');
    if(!el) return;
    const bits = [softNote(char[k], k)];
    if(need[k]){
      const ok = char[k] >= need[k];
      bits.push((ok?"meets ":"needs ")+lab+" "+need[k]+" ("+names[k]+")");
      el.classList.toggle("bad", !ok);
    } else el.classList.remove("bad");
    el.textContent = bits.join(" · ");
    el.style.fontSize="16px";
    el.style.webkitTextSizeAdjust="100%";
  });
}

(function n3wrapDraw(){
  const _drawChar = drawChar;
  drawChar = function(){
    const first = !document.getElementById("char-stats")?.dataset.ready;
    _drawChar();
    if(first){
      document.querySelectorAll("#char-stats .statrow").forEach(row => {
        const lab = row.querySelector(".lab");
        if(!lab) return;
        const k = row.querySelector("[data-st]")?.dataset.st;
        if(!k || row.querySelector(".ico")) return;
        lab.insertAdjacentHTML("afterbegin", n3icon(N3_STAT_ICON[k], lab.textContent)+" ");
      });
    }
  };
  const _fill = fillSelects;
  fillSelects = function(){
    _fill();
    document.querySelectorAll("#slots .slot > span").forEach((span, idx) => {
      if(span.querySelector(".ico")) return;
      const id = (SLOTS[idx]||[])[0];
      if(!id) return;
      span.insertAdjacentHTML("afterbegin", n3icon(N3_SLOT_ICON[id]||"placeholder", span.textContent)+" ");
    });
  };
})();

(function n3wrapItems(){
  if(typeof pieceItems!=="function") return;
  const _pi = pieceItems;
  pieceItems = function(id, wt){
    let html = _pi(id, wt);
    if(WEAPON_SLOTS && WEAPON_SLOTS.has(id)){
      html = html.replace(/<div class="(dd-name[^"]*)">([^<]*)<\/div>/g, (m, cls, name) => {
        if(name.indexOf("empty")>=0) return m;
        const piece = PIECES[id].find(x => x.name===name);
        const tp = piece ? weaponType(piece) : "";
        return '<div class="'+cls+'">'+n3icon(n3WeaponIconId(tp), tp)+" "+name+"</div>";
      });
    }
    return html;
  };
})();
