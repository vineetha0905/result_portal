/**
 * PDF.js viewer with in-document search and simple highlighting.
 *
 * Expects global `pdfjsLib` and `window.PDF_VIEWER_CONFIG`:
 *   { pdfUrl, workerSrc, prefillSearch }
 */
(function () {
  "use strict";

  var cfg = window.PDF_VIEWER_CONFIG || {};
  var pdfUrl = cfg.pdfUrl;
  if (!pdfUrl || typeof pdfjsLib === "undefined") {
    return;
  }

  var container = document.getElementById("pdfPages");
  var errEl = document.getElementById("pdfLoadError");
  var searchInput = document.getElementById("pdfSearchInput");
  var searchBtn = document.getElementById("pdfSearchBtn");
  var clearBtn = document.getElementById("pdfSearchClear");
  var prevBtn = document.getElementById("pdfSearchPrev");
  var nextBtn = document.getElementById("pdfSearchNext");
  var statusEl = document.getElementById("pdfSearchStatus");

  /** @type {HTMLElement[]} */
  var matchSpans = [];
  var matchIndex = 0;

  function showError(msg) {
    if (errEl) {
      errEl.textContent = msg;
      errEl.classList.remove("d-none");
    }
  }

  function setStatus(text) {
    if (statusEl) statusEl.textContent = text;
  }

  function clearHighlights() {
    document.querySelectorAll(".text-layer span.pdf-highlight").forEach(function (s) {
      s.classList.remove("pdf-highlight");
    });
    matchSpans = [];
    matchIndex = 0;
    prevBtn.disabled = true;
    nextBtn.disabled = true;
  }

  function scrollToMatch() {
    if (!matchSpans.length) return;
    var el = matchSpans[matchIndex];
    el.scrollIntoView({ behavior: "smooth", block: "center" });
    setStatus("Match " + (matchIndex + 1) + " of " + matchSpans.length);
    prevBtn.disabled = matchSpans.length <= 1;
    nextBtn.disabled = matchSpans.length <= 1;
  }

  function highlightQuery(query) {
    clearHighlights();
    var q = (query || "").trim();
    if (!q) {
      setStatus("Enter text and press Search.");
      return;
    }
    var lower = q.toLowerCase();

    /** @type {HTMLElement[]} */
    var found = [];
    document.querySelectorAll(".text-layer span").forEach(function (span) {
      var text = span.textContent || "";
      if (text.toLowerCase().indexOf(lower) !== -1) {
        span.classList.add("pdf-highlight");
        found.push(span);
      }
    });

    matchSpans = found;
    if (!matchSpans.length) {
      setStatus('No matches for "' + q + '".');
      return;
    }
    matchIndex = 0;
    scrollToMatch();
  }

  searchBtn.addEventListener("click", function () {
    highlightQuery(searchInput.value);
  });
  searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      highlightQuery(searchInput.value);
    }
  });
  clearBtn.addEventListener("click", function () {
    searchInput.value = "";
    clearHighlights();
    setStatus("Highlights cleared.");
  });
  prevBtn.addEventListener("click", function () {
    if (!matchSpans.length) return;
    matchIndex = (matchIndex - 1 + matchSpans.length) % matchSpans.length;
    scrollToMatch();
  });
  nextBtn.addEventListener("click", function () {
    if (!matchSpans.length) return;
    matchIndex = (matchIndex + 1) % matchSpans.length;
    scrollToMatch();
  });

  /**
   * Build a simple text layer over the canvas using PDF.js text content.
   * Positions are approximate but good enough for search + highlight demos.
   */
  function appendTextLayer(layer, textContent, viewport) {
    textContent.items.forEach(function (item) {
      if (!item.str) return;
      var transform = pdfjsLib.Util.transform(viewport.transform, item.transform);
      var span = document.createElement("span");
      span.textContent = item.str;
      var pdfX = transform[4];
      var pdfY = transform[5];
      var fontHeight = Math.hypot(transform[2], transform[3]) || 12;
      span.style.left = pdfX + "px";
      span.style.top = viewport.height - pdfY - fontHeight * 0.9 + "px";
      span.style.fontSize = fontHeight + "px";
      layer.appendChild(span);
    });
  }

  async function renderPdf() {
    try {
      var loadingTask = pdfjsLib.getDocument({ url: pdfUrl });
      var pdf = await loadingTask.promise;
      var scale = 1.35;

      for (var p = 1; p <= pdf.numPages; p++) {
        var page = await pdf.getPage(p);
        var viewport = page.getViewport({ scale: scale });

        var wrap = document.createElement("div");
        wrap.className = "pdf-page-wrap mb-3 border rounded shadow-sm position-relative bg-white";
        wrap.dataset.pageNumber = String(p);

        var canvas = document.createElement("canvas");
        var ctx = canvas.getContext("2d");
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        await page.render({ canvasContext: ctx, viewport: viewport }).promise;

        var layer = document.createElement("div");
        layer.className = "text-layer position-absolute top-0 start-0";
        layer.style.width = viewport.width + "px";
        layer.style.height = viewport.height + "px";

        var textContent = await page.getTextContent();
        appendTextLayer(layer, textContent, viewport);

        wrap.style.width = viewport.width + "px";
        wrap.appendChild(canvas);
        wrap.appendChild(layer);
        container.appendChild(wrap);
      }

      setStatus("PDF loaded. Enter text and press Search.");

      if (cfg.prefillSearch) {
        searchInput.value = cfg.prefillSearch;
      }
    } catch (e) {
      console.error(e);
      showError("Could not load PDF. Check that the file exists and try again.");
      setStatus("");
    }
  }

  renderPdf();
})();
