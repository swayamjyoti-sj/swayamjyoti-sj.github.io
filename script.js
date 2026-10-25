const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#primary-nav');
menuButton.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}));
document.getElementById('year').textContent = new Date().getFullYear();
// Seeded, deterministic illustration: no dependencies or remote assets.
let seed = 117;
const rand = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
const ns = 'http://www.w3.org/2000/svg';
const points = [];
for (let i = 0; i < 58; i++) {
  const t = rand() * Math.PI * 2;
  const u = rand() * 2 - 1;
  const r = 95 + rand() * 124;
  const squash = Math.sqrt(1-u*u);
  points.push({x:280 + r*squash*Math.cos(t), y:255 + r*squash*Math.sin(t)*.91, z:u, r:3.3+rand()*4.4});
}
points.sort((a,b) => a.z - b.z);
const bonds = document.getElementById('bonds');
for (let i=0;i<points.length;i++) {
  const closest = points.map((p,j) => ({j,d:Math.hypot(points[i].x-p.x,points[i].y-p.y)})).filter(x=>x.j!==i).sort((a,b)=>a.d-b.d).slice(0,3);
  closest.forEach(({j,d})=>{if(j<i || d>95)return;const l=document.createElementNS(ns,'line');l.setAttribute('x1',points[i].x);l.setAttribute('y1',points[i].y);l.setAttribute('x2',points[j].x);l.setAttribute('y2',points[j].y);l.setAttribute('opacity',String(.22+(points[i].z+1)*.22));bonds.appendChild(l)});
}
const atoms = document.getElementById('atoms');
points.forEach((p,i)=>{const c=document.createElementNS(ns,'circle');c.setAttribute('cx',p.x);c.setAttribute('cy',p.y);c.setAttribute('r',p.r*(.88+(p.z+1)*.16));c.setAttribute('fill',i%4===0?'url(#atom)':'url(#atomSoft)');c.setAttribute('opacity',String(.55+(p.z+1)*.21));atoms.appendChild(c)});

// DFG proposal details populated from proposal-config.js.
const proposal = window.dfgProposal || {};
const assignText = (id, value) => {
  const element = document.getElementById(id);
  if (element && typeof value === 'string') element.textContent = value;
};
assignText('dfg-status', proposal.status);
assignText('dfg-project-title', proposal.title);
assignText('dfg-summary', proposal.summary);
const fillList = (id, items) => {
  const list = document.getElementById(id);
  if (!list || !Array.isArray(items)) return;
  list.replaceChildren();
  for (const item of items) { const li = document.createElement('li'); li.textContent = item; list.append(li); }
};
fillList('dfg-objectives', proposal.objectives);
fillList('dfg-workpackages', proposal.workPackages);
if (typeof proposal.url === 'string' && /^https:\/\//.test(proposal.url)) {
  document.getElementById('dfg-project-link').href = proposal.url;
}
const dfgToggle = document.getElementById('dfg-toggle');
const dfgDetails = document.getElementById('dfg-details');
dfgToggle?.addEventListener('click', () => {
  const expanded = dfgToggle.getAttribute('aria-expanded') === 'true';
  dfgToggle.setAttribute('aria-expanded', String(!expanded));
  dfgDetails.hidden = expanded;
  dfgToggle.querySelector('span').textContent = expanded ? '+' : '−';
});
