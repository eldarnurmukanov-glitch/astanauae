// Astana Real Estate — shared behaviour for project pages: header state, mobile menu, reveal on scroll.
(function(){
  document.documentElement.classList.add('js');
  const header = document.querySelector('header.site');
  if (header) {
    const onScroll = () => header.classList.toggle('solid', window.scrollY > 40);
    onScroll(); window.addEventListener('scroll', onScroll, {passive:true});
  }
  const burger = document.querySelector('.burger');
  if (burger) {
    burger.addEventListener('click', () => {
      const open = document.body.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
    });
    document.querySelectorAll('.menu a').forEach(a => a.addEventListener('click', () => {
      document.body.classList.remove('open'); burger.setAttribute('aria-expanded', false);
    }));
  }
  const els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), {threshold:.08, rootMargin:'0px 0px -40px 0px'});
    els.forEach(el => io.observe(el));
  } else {
    els.forEach(el => el.classList.add('in'));
  }
  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
