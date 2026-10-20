// Commuted. Two small things, neither of which stores or sends anything.
//
// 1. One leg, recorded. The hero's copy of the app plays a commute once
//    by itself: Start, the route lights, Stop at 35 minutes, and the week
//    takes on the leg's hours and dollars. After that the button is the
//    visitor's. A minute of commute passes in a fifth of a second.
// 2. The number. The fuel share of a leg fills first, then the rest of
//    what the car costs fills in behind it.

(function () {
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- 1. One leg ----------

  var trip = document.getElementById('trip');
  if (trip) {
    var MS_PER_MIN = 200;          // a minute of commute in a fifth of a second
    var LEG_COST = 11, LEG_FUEL = 2; // 14.5 miles at the IRS rate; fuel at $3.52/gal
    var AUTO_MIN = 35, MAX_MIN = 120;

    var week = { min: 336, cost: 86, legs: 8, fuel: 16 };
    var today = 0, outbound = true;

    var go = document.getElementById('go');
    var clock = document.getElementById('clock');
    var since = document.getElementById('since');
    var lit = document.getElementById('lit');
    var car = document.getElementById('car');
    var toDot = trip.querySelector('.stop-dot.to');
    var names = trip.querySelectorAll('.stop-name');
    var which = trip.querySelector('.which');
    var legs = document.getElementById('legs');
    var todayTotal = document.getElementById('today-total');
    var wk = document.getElementById('wk');

    var running = false, t0 = 0, raf = 0, autoStop = 0, touched = false, played = false;

    function hm(min) {
      var h = Math.floor(min / 60), m = min % 60;
      return h ? h + ' h ' + m + ' min' : m + ' min';
    }

    function clockText(ms) {
      var s = Math.floor(ms / MS_PER_MIN * 60);
      var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), sec = s % 60;
      return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(sec).padStart(2, '0');
    }

    function nowText() {
      return new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
    }

    function place(p) {
      lit.style.width = (p * 100) + '%';
      car.style.left = (p * 100) + '%';
      toDot.classList.toggle('is-reached', p >= 1);
    }

    function paintWeek(flash) {
      wk.textContent = hm(week.min);
      document.getElementById('wk-cost').textContent = '$' + week.cost;
      document.getElementById('wk-legs').textContent = week.legs;
      document.getElementById('wk-fuel').textContent = '$' + week.fuel;
      if (flash) {
        wk.classList.remove('flash');
        void wk.offsetWidth;
        wk.classList.add('flash');
      }
    }

    function frame() {
      var ms = performance.now() - t0;
      var min = ms / MS_PER_MIN;
      clock.textContent = clockText(ms);
      place(Math.min(1, min / AUTO_MIN));
      if (autoStop && min >= autoStop) { stop(true); return; }
      if (min >= MAX_MIN) { stop(); return; }
      raf = requestAnimationFrame(frame);
    }

    function start(auto) {
      running = true;
      autoStop = auto ? AUTO_MIN : 0;
      t0 = performance.now();
      clock.hidden = false;
      since.hidden = false;
      since.textContent = 'Since ' + nowText();
      go.textContent = 'Stop';
      trip.classList.add('is-running');
      place(0);
      raf = requestAnimationFrame(frame);
    }

    function stop(auto) {
      cancelAnimationFrame(raf);
      running = false;
      var min = Math.max(1, Math.round((performance.now() - t0) / MS_PER_MIN));
      if (auto) min = autoStop;

      week.min += min; week.cost += LEG_COST; week.legs += 1; week.fuel += LEG_FUEL;
      today += min;
      paintWeek(true);

      var row = document.createElement('div');
      row.className = 'leg';
      row.innerHTML = '<span></span><span></span>';
      row.firstChild.textContent = outbound ? 'Home to office' : 'Office to home';
      var small = document.createElement('small');
      small.textContent = since.textContent.replace('Since ', '');
      row.firstChild.appendChild(small);
      row.lastChild.textContent = min + ' min';
      legs.insertBefore(row, legs.firstChild);
      todayTotal.textContent = hm(today);

      // The next leg runs the other way.
      outbound = !outbound;
      names[0].textContent = outbound ? 'Home' : 'Office';
      names[1].textContent = outbound ? 'Office' : 'Home';
      which.textContent = outbound ? 'Home to office' : 'Office to home';

      clock.hidden = true;
      since.hidden = true;
      go.textContent = 'Start commute';
      trip.classList.remove('is-running');
      setTimeout(function () { if (!running) place(0); }, 1200);
    }

    function press(fn) {
      go.classList.add('is-pressed');
      setTimeout(function () { go.classList.remove('is-pressed'); fn(); }, 140);
    }

    go.addEventListener('click', function () {
      touched = true;
      if (running) stop(); else start(false);
    });

    paintWeek(false);

    // Play once by itself, when the trip is on screen and nobody has
    // pressed anything yet.
    if (!still && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries, obs) {
        if (!entries[0].isIntersecting || played) return;
        played = true;
        obs.disconnect();
        setTimeout(function () { if (!touched && !running) press(function () { start(true); }); }, 900);
      }, { threshold: 0.6 }).observe(trip.querySelector('.phone'));
    }
  }

  // ---------- 2. The number ----------

  var number = document.getElementById('number');
  if (number) {
    var num = document.getElementById('cost-num');
    var label = document.getElementById('cost-label');
    function all() {
      number.classList.add('is-fuel', 'is-all');
      num.textContent = '$11';
      label.textContent = 'a leg, all in, at the IRS rate';
    }
    if (still || !('IntersectionObserver' in window)) {
      all();
    } else {
      new IntersectionObserver(function (entries, obs) {
        if (!entries[0].isIntersecting) return;
        obs.disconnect();
        number.classList.add('is-fuel');
        setTimeout(all, 1900);
      }, { threshold: 0.6 }).observe(number.querySelector('.cost'));
    }
  }
})();
