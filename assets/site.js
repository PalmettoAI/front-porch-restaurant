/* Front Porch — shared behavior.
 *
 * ONLINE ORDERING: when the SkyTab (Shift4) online-ordering link is ready,
 * paste it into ORDER_URL below. Every "Order Pies" button on the site
 * switches from "call to order" to the online link automatically.
 */
var ORDER_URL = "";            // e.g. "https://order.skytab.com/..." (from the POS team)
var PHONE = "+13524894708";
var PHONE_PRETTY = "(352) 489-4708";

(function () {
  var doc = document.documentElement;
  doc.classList.add("js");

  /* ---- Order buttons ---- */
  document.querySelectorAll("[data-order]").forEach(function (a) {
    var label = a.querySelector("[data-order-label]");
    if (ORDER_URL) {
      a.href = ORDER_URL;
      a.target = "_blank";
      a.rel = "noopener";
      if (label && a.dataset.onlineLabel) label.textContent = a.dataset.onlineLabel;
    } else {
      a.href = "tel:" + PHONE;
      if (label && a.dataset.phoneLabel) label.textContent = a.dataset.phoneLabel;
    }
  });
  document.querySelectorAll("[data-if-online]").forEach(function (el) { el.hidden = !ORDER_URL; });
  document.querySelectorAll("[data-if-phone]").forEach(function (el) { el.hidden = !!ORDER_URL; });

  /* ---- Time in Dunnellon (Eastern) ---- */
  function nowET() {
    var p = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", minute: "numeric", hour12: false, year: "numeric", month: "numeric", day: "numeric" })
      .formatToParts(new Date()).reduce(function (o, x) { o[x.type] = x.value; return o; }, {});
    var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { day: days[p.weekday], mins: (+p.hour % 24) * 60 + +p.minute, y: +p.year, m: +p.month, d: +p.day };
  }
  // [open, close] in minutes; Monday closed
  var HOURS = { 0: [420, 1200], 1: null, 2: [420, 1230], 3: [420, 1230], 4: [420, 1230], 5: [420, 1230], 6: [420, 1230] };
  var BREAKFAST_END = { 0: 690, 6: 690, 2: 660, 3: 660, 4: 660, 5: 660 };
  var DAYNAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function fmt(m) { var h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? "PM" : "AM"; h = h % 12 || 12; return h + (mm ? ":" + String(mm).padStart(2, "0") : "") + " " + ap; }

  var t = nowET();
  var today = HOURS[t.day];
  var open = today && t.mins >= today[0] && t.mins < today[1];
  var msg;
  if (open) {
    var bEnd = BREAKFAST_END[t.day];
    msg = t.mins < bEnd ? "Open now · breakfast served till " + fmt(bEnd) : "Open now · until " + fmt(today[1]);
  } else {
    var n = t.day, add = 0;
    if (today && t.mins < today[0]) { msg = "Opens today at " + fmt(today[0]); }
    else {
      do { n = (n + 1) % 7; add++; } while (!HOURS[n]);
      msg = "Closed · opens " + (add === 1 ? "tomorrow" : DAYNAMES[n]) + " at " + fmt(HOURS[n][0]);
    }
  }
  document.querySelectorAll("[data-status]").forEach(function (el) {
    el.textContent = msg;
    var dot = el.previousElementSibling;
    if (dot && dot.classList.contains("dot")) dot.classList.toggle("shut", !open);
  });
  document.querySelectorAll(".hours li[data-day]").forEach(function (li) {
    if (+li.dataset.day === t.day) { li.classList.add("today"); li.setAttribute("aria-current", "date"); }
  });

  /* ---- Earliest whole-pie pickup (one day's notice, closed Mondays) ---- */
  var pick = document.querySelectorAll("[data-pickup]");
  if (pick.length) {
    var d = new Date(Date.UTC(t.y, t.m - 1, t.d));
    do { d.setUTCDate(d.getUTCDate() + 1); } while (d.getUTCDay() === 1);
    var s = d.toLocaleDateString("en-US", { timeZone: "UTC", weekday: "long", month: "long", day: "numeric" });
    pick.forEach(function (el) { el.textContent = s; });
  }

  /* ---- Mobile nav ---- */
  var btn = document.querySelector(".nav-toggle"), nav = document.getElementById("site-nav");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var o = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", o);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); btn.focus(); }
    });
  }

  /* ---- Reveal on scroll ---- */
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    els.forEach(function (el) { io.observe(el); });
    setTimeout(function () { els.forEach(function (el) { el.classList.add("in"); }); }, 4000);
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
