(() => {
  const $ = id => document.getElementById(id);
  const songs = window.LOVE_SONGS || [];
  let currentIndex = 0;
  let playing = false;

  const show = el => el && el.classList.add('show');
  const hide = el => el && el.classList.remove('show');
  function current(){ return songs[currentIndex] || {}; }
  function setText(id, value){ const el=$(id); if(el) el.textContent=value || ''; }
  function updateUI(){
    const s=current();
    setText('playerTitle', s.title || 'Choose a song');
    setText('playerArtist', s.artist && s.movie ? `${s.artist} · ${s.movie}` : (s.artist || ''));
    setText('playerMood', `${(s.mood||'BOLLYWOOD').toUpperCase()} · ${s.year||''}`);
    setText('heroTitle', s.title || 'Love Roadways');
    setText('heroArtist', s.artist && s.movie ? `${s.artist} · ${s.movie}` : (s.artist || ''));
    setText('heroMood', (s.mood||'BOLLYWOOD').toUpperCase());
    setText('fullTitle', s.title || '');
    setText('fullArtist', s.artist && s.movie ? `${s.artist} · ${s.movie}` : (s.artist || ''));
    setText('fullMood', (s.mood||'BOLLYWOOD').toUpperCase());
    const thumb=$('ytThumb'); if(thumb) thumb.style.backgroundImage=s.yt?`url(https://i.ytimg.com/vi/${s.yt}/hqdefault.jpg)`:'';
    ['playBtn','heroCardPlay','fullPlay'].forEach(id=>{const el=$(id);if(el)el.textContent=playing?'Ⅱ':'▶'});
  }
  function youtubeUrl(id){ return `https://www.youtube.com/embed/${id}?autoplay=1&rel=0&playsinline=1`; }
  function openFull(song=current()){
    if(!song || !song.yt) return resolveSong(song);
    const full=$('fullscreenPlayer'), bg=$('fullBg'), frame=$('fullYoutube');
    if(bg) bg.style.backgroundImage=`url(https://i.ytimg.com/vi/${song.yt}/maxresdefault.jpg)`;
    if(frame) frame.innerHTML=`<iframe src="${youtubeUrl(song.yt)}" title="${(song.title||'YouTube song').replace(/"/g,'&quot;')}" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
    if(full) full.classList.add('open');
    playing=true; updateUI();
  }
  function closeFull(){ const full=$('fullscreenPlayer'); if(full) full.classList.remove('open'); const frame=$('fullYoutube'); if(frame) frame.innerHTML=''; playing=false; updateUI(); }
  function selectSong(index, open=true){
    if(!songs.length || index<0 || index>=songs.length) return;
    currentIndex=index; updateUI(); renderQueue();
    const s=current(); if(open) openFull(s);
  }
  async function resolveSong(song){
    if(!song || !song.title) return;
    try{
      const r=await fetch(`/api/youtube-search?q=${encodeURIComponent(`${song.title} ${song.artist||''}`)}`);
      const data=await r.json();
      if(!r.ok || !data.items || !data.items.length) throw new Error(data.error || 'Playable YouTube video nahi mila.');
      song.yt=data.items[0].yt; song.thumb=data.items[0].thumb; updateUI(); openFull(song);
    }catch(e){ alert(e.message || 'Song load nahi ho paya.'); }
  }
  function renderQueue(){
    const box=$('queueList'); if(!box)return;
    const list=[]; for(let n=1;n<=songs.length && list.length<5;n++) list.push(songs[(currentIndex+n)%songs.length]);
    const count=$('queueCount'); if(count)count.textContent=list.length;
    box.innerHTML=list.map((s,n)=>`<div class="queue-item" data-qid="${songs.indexOf(s)}"><b>${String(n+1).padStart(2,'0')}</b><div><b>${s.title}</b><small>${s.artist||''}</small></div></div>`).join('') || '<p style="padding:15px;color:#777;font-size:12px">Queue empty.</p>';
    box.querySelectorAll('[data-qid]').forEach(el=>el.onclick=()=>selectSong(Number(el.dataset.qid),true));
  }
  function cardSong(card){
    return {id:Number(card.dataset.id),title:card.querySelector('h3')?.textContent.trim()||'',artist:card.querySelector('p')?.textContent.split('·')[0].trim()||'',movie:card.querySelector('p')?.textContent.split('·').slice(1).join('·').trim()||'',year:card.querySelector('small')?.textContent.split('·')[0].trim()||'',mood:card.dataset.mood||'Bollywood',yt:card.querySelector('.song-photo')?.src?.match(/vi\/([^/]+)\//)?.[1]||''};
  }
  function filterCards(mood){ document.querySelectorAll('.song-card').forEach(c=>c.style.display=(mood==='All'||c.dataset.mood===mood)?'':'none'); }
  function bind(){
    $('searchOpen')?.addEventListener('click',e=>{e.preventDefault();show($('searchOverlay'));setTimeout(()=>$('searchInput')?.focus(),50);});
    $('searchClose')?.addEventListener('click',() => hide($('searchOverlay')));
    $('fullClose')?.addEventListener('click',closeFull);
    $('openVideo')?.addEventListener('click',()=>openFull());
    $('heroPlay')?.addEventListener('click',()=>selectSong(currentIndex,true));
    $('heroCardPlay')?.addEventListener('click',()=>selectSong(currentIndex,true));
    $('playBtn')?.addEventListener('click',()=>{ if(playing) closeFull(); else selectSong(currentIndex,true); });
    $('fullPlay')?.addEventListener('click',()=>{ if(playing) closeFull(); else openFull(); });
    $('nextBtn')?.addEventListener('click',()=>selectSong((currentIndex+1)%songs.length,true));
    $('prevBtn')?.addEventListener('click',()=>selectSong((currentIndex-1+songs.length)%songs.length,true));
    $('fullNext')?.addEventListener('click',()=>selectSong((currentIndex+1)%songs.length,true));
    $('fullPrev')?.addEventListener('click',()=>selectSong((currentIndex-1+songs.length)%songs.length,true));
    $('themeBtn')?.addEventListener('click',()=>document.body.classList.toggle('dark'));
    $('shuffleBtn')?.addEventListener('click',()=>{if(songs.length)selectSong(Math.floor(Math.random()*songs.length),true)});
    $('queueBtn')?.addEventListener('click',()=>show($('queueDrawer')));
    $('queueClose')?.addEventListener('click',()=>hide($('queueDrawer')));
    $('lyricsBtn')?.addEventListener('click',()=>{setText('lyricsTitle',current().title||'Song lyrics');show($('lyricsOverlay'))});
    $('lyricsClose')?.addEventListener('click',()=>hide($('lyricsOverlay')));
    document.querySelectorAll('.song-card').forEach(card=>card.addEventListener('click',e=>{
      if(e.target.closest('.heart'))return;
      const local=cardSong(card); let idx=songs.findIndex(s=>s.id===local.id);
      if(idx<0){songs.push(local);idx=songs.length-1;}
      selectSong(idx,true);
    }));
    document.querySelectorAll('.chip').forEach(ch=>ch.addEventListener('click',()=>{
      document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active')); ch.classList.add('active'); filterCards(ch.dataset.mood);
    }));
    document.querySelectorAll('.mood-card').forEach(c=>c.addEventListener('click',()=>{
      const ch=[...document.querySelectorAll('.chip')].find(x=>x.dataset.mood===c.dataset.moodJump); if(ch){ch.click();$('collection')?.scrollIntoView({behavior:'smooth'});}
    }));
    let timer;
    $('searchInput')?.addEventListener('input',e=>{
      clearTimeout(timer); const q=e.target.value.trim();
      if(q.length<2){setText('searchResults','');setText('searchStatus','Song, artist ya movie search karo.');return;}
      setText('searchStatus','Gaana dhoond rahe hain…');
      timer=setTimeout(async()=>{
        try{
          const r=await fetch(`/api/youtube-search?q=${encodeURIComponent(q)}`); const data=await r.json();
          if(!r.ok)throw new Error(data.error||'Search failed');
          const items=data.items||[]; setText('searchStatus',`${items.length} results — gaane par click karo`);
          $('searchResults').innerHTML=items.map((s,i)=>`<button class="search-result" data-search-index="${i}"><span class="search-thumb" style="background-image:url('${s.thumb||''}')"></span><span><b>${s.title}</b><small>${s.artist||'YouTube'} · ${s.year||''}</small></span><strong>▶</strong></button>`).join('')||'<div class="search-empty">Kuch nahi mila.</div>';
          document.querySelectorAll('[data-search-index]').forEach(el=>el.onclick=()=>{const s=items[Number(el.dataset.searchIndex)];songs.push(s);currentIndex=songs.length-1;hide($('searchOverlay'));updateUI();openFull(s);});
        }catch(err){setText('searchStatus',err.message);}
      },300);
    });
    window.addEventListener('keydown',e=>{if(e.key==='Escape'){closeFull();document.querySelectorAll('.overlay').forEach(hide);hide($('queueDrawer'));}});
  }
  function start(){ if(!songs.length)return; const first=songs.findIndex(s=>s.yt); currentIndex=first>=0?first:0; renderQueue(); updateUI(); bind(); }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();