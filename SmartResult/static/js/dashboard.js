/**
 * Dashboard — optional client-side polish.
 * (Core behaviour is server-rendered; this file keeps the bundle explicit for the resume project.)
 */
(function () {
  document.querySelectorAll(".dashboard-year-card .btn").forEach(function (btn) {
    btn.addEventListener("focus", function () {
      btn.closest(".dashboard-year-card")?.classList.add("shadow");
    });
    btn.addEventListener("blur", function () {
      btn.closest(".dashboard-year-card")?.classList.remove("shadow");
    });
  });
})();
