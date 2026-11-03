// moteur de motivation, d'analyse et de conseils (tout est calculé sur le téléphone)
const P = {
  start: ['C’est parti, tu as tout ce qu’il faut !', 'Un premier pas, et le reste suit.', 'Concentre-toi sur ce seul moment.', 'Fais-le maintenant, tu te remercieras ce soir.', 'Petit à petit, tu deviens la personne que tu veux être.', 'Respire, lance-toi : tu en es capable.'],
  end: ['Bien joué, tu as tenu jusqu’au bout !', 'Fin de séance : coche-le et savoure.', 'Chaque programme tenu renforce ta discipline.', 'Beau travail, prends une courte pause.', 'Tu avances, même quand c’est dur.'],
  alarm: ['Debout, belle journée devant toi !', 'Tu avais promis de te lever : tiens parole.', 'Un nouveau jour, une nouvelle chance.', 'Lève-toi et fais le premier pas.', 'La discipline bat la motivation, et tu en as.'],
  task: ['Une tâche à la fois, tu gères.', 'C’est le moment, fais-la sans attendre.', 'Petit effort, grande fierté.', 'Termine-la et coche-la !'],
  focus: ['Super session ! Ton cerveau mérite une pause.', 'Concentration validée, bravo.', 'Tu viens de gagner du temps sur tes objectifs.'],
  morning: ['Bonne journée ! Choisis ta priorité du jour.', 'Aujourd’hui compte : fais-le bien.'],
}
export const motiv = (k, seed = 0) => { const a = P[k] || P.task; return a[Math.abs(Math.floor(seed)) % a.length] }

const sgn = n => (n > 0 ? '+' + n : '' + n)
export function catStats(s, day, len) {
  const a = Math.max(1, day - len + 1), pa = Math.max(1, a - len)
  return s.cats.map(c => {
    const avg = (x, y) => { let sum = 0, n = 0; for (let d = x; d <= y; d++) { const v = s.h[d]?.[c.id]; if (v != null) { sum += v; n++ } } return n ? Math.round(sum / n) : null }
    let act = 0, tot = 0
    for (let d = a; d <= day; d++) { const v = s.h[d]?.[c.id]; if (v != null) { tot++; if (v >= 50) act++ } }
    const cur = avg(a, day), prev = a > 1 ? avg(pa, a - 1) : null
    return { id: c.id, n: c.n, c: c.c, cur, prev, delta: cur != null && prev != null ? cur - prev : null, act, tot }
  })
}
export function trendLine(x) {
  let t = x.act + '/' + x.tot + ' jours réussis'
  if (x.delta != null) t += ' · ' + sgn(x.delta) + ' pts vs avant'
  t += x.cur >= 70 ? '. Très solide.' : x.cur >= 45 ? '. Correct, tu peux viser plus haut.' : '. À relancer : une seule tâche facile pour repartir.'
  return t
}
export function weekReview(s, day) {
  const a = Math.max(1, day - 6), ks = Object.keys(s.hs).map(Number), first = ks.length ? Math.min(...ks) : day
  const sc = d => (d < first ? null : (s.hs[d]?.sc ?? 0))
  const avg = (x, y) => { const v = []; for (let d = x; d <= y; d++) { const q = sc(d); if (q != null) v.push(q) } return v.length ? Math.round(v.reduce((p, q) => p + q, 0) / v.length) : null }
  const cur = avg(a, day), prev = a > 1 ? avg(Math.max(1, a - 7), a - 1) : null
  const days = []; for (let d = a; d <= day; d++) { const q = sc(d); if (q != null) days.push([d, q]) }
  const good = days.filter(x => x[1] >= 60).length
  const best = days.length ? [...days].sort((x, y) => y[1] - x[1])[0] : null
  const worst = days.length > 1 ? [...days].sort((x, y) => x[1] - y[1])[0] : null
  const verdict = cur == null ? 'Pas encore de données' : cur >= 70 ? 'Très bonne semaine' : cur >= 55 ? 'Bonne semaine' : cur >= 40 ? 'Semaine moyenne' : 'Semaine difficile'
  const delta = cur != null && prev != null ? cur - prev : null
  let line = cur == null ? 'Coche tes tâches et reviens faire le point.' : verdict + ' : ' + cur + ' % de moyenne' + (delta != null ? ' (' + sgn(delta) + ' pts vs la semaine d’avant)' : '') + ', ' + good + ' jour(s) sur ' + days.length + ' à plus de 60 %.'
  const weeks = []
  for (let k = 3; k >= 0; k--) { const e = day - 7 * k, b = Math.max(1, e - 6); if (e >= 1) weeks.push({ label: k ? 'Il y a ' + k + ' sem.' : 'Cette semaine', v: avg(b, e) }) }
  return { cur, prev, delta, verdict, line, good, n: days.length, best, worst, weeks }
}
const lvl = v => (v == null ? 'none' : v >= 70 ? 'good' : v >= 45 ? 'mid' : 'bad')
export function areaAdvice(s, day) {
  const out = []
  catStats(s, day, 7).forEach(x => {
    if (x.cur == null) return
    const st = lvl(x.cur)
    const tip = st === 'bad' ? (x.delta != null && x.delta < 0 ? 'Tu décroches : réduis à une seule tâche facile ici pour retrouver le rythme.' : 'Programme-la à heure fixe dans l’agenda pour en faire un rendez-vous.') : st === 'mid' ? 'Tu y es presque : vise un jour de plus cette semaine.' : 'Excellent. Ajoute un petit défi pour continuer à progresser.'
    out.push({ k: x.n, st, text: x.cur + ' % cette semaine' + (x.delta != null ? ' (' + sgn(x.delta) + ' pts)' : '') + ', ' + x.act + '/' + x.tot + ' jours réussis.', tip })
  })
  const mx = Math.max(0, ...s.quit.map(q => q.s)), lost = s.lost.filter(l => l.day >= day - 30).length
  if (s.quit.length) out.push({ k: 'Habitudes à arrêter', st: lost > 2 ? 'bad' : mx >= 7 ? 'good' : 'mid', text: 'Meilleure série en cours : ' + mx + ' j · ' + lost + ' rechute(s) sur 30 jours.', tip: lost > 2 ? 'Repère ce qui déclenche la rechute (heure, lieu) et remplace-le par une action simple.' : mx >= 7 ? 'Belle série ! Récompense-toi et ne change rien.' : 'Les 7 premiers jours sont les plus durs : tiens-les un par un.' })
  const t0 = new Date(); const lim = new Date(t0); lim.setDate(lim.getDate() - 7)
  const iso = d => d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
  const pl = s.plans.filter(p => p.date >= iso(lim) && (p.d || p.date < iso(t0)))
  if (pl.length) { const r = Math.round(pl.filter(p => p.d).length / pl.length * 100); out.push({ k: 'Programmes', st: lvl(r), text: r + ' % tenus sur 7 jours (' + pl.filter(p => p.d).length + '/' + pl.length + ').', tip: r < 45 ? 'Programme moins de choses mais tiens-les : 3 par jour maximum.' : r < 70 ? 'Mets une alarme début et fin sur tes programmes importants.' : 'Très régulier : tu peux ajouter un programme.' }) }
  const sp = s.sport.filter(Boolean).length
  out.push({ k: 'Sport', st: sp >= 4 ? 'good' : sp >= 2 ? 'mid' : 'bad', text: sp + ' séance(s) cette semaine (objectif 4).', tip: sp >= 4 ? 'Objectif atteint, pense à récupérer.' : 'Bloque 2 créneaux dans l’agenda dès maintenant.' })
  let fs = 0, fm = 0; for (let d = Math.max(1, day - 6); d <= day; d++) { fs += s.focus[d] || 0; fm += s.fmin?.[d] || 0 }
  out.push({ k: 'Concentration', st: fs >= 7 ? 'good' : fs >= 3 ? 'mid' : 'bad', text: fs + ' session(s) de focus sur 7 jours' + (fm ? ' (' + fm + ' min)' : '') + '.', tip: fs >= 7 ? 'Super rythme de concentration.' : 'Lance une session de 25 minutes sur ta tâche la plus importante.' })
  const ms = []; for (let d = Math.max(1, day - 6); d <= day; d++) if (s.mood[d]) ms.push(s.mood[d])
  if (ms.length) { const m = ms.reduce((a, b) => a + b, 0) / ms.length; out.push({ k: 'Humeur', st: m >= 3.5 ? 'good' : m >= 2.5 ? 'mid' : 'bad', text: 'Humeur moyenne : ' + m.toFixed(1) + '/5 sur 7 jours.', tip: m < 2.5 ? 'Allège ton programme et dors bien : l’énergie d’abord.' : 'Continue à noter ton bilan du soir.' }) }
  return out
}
