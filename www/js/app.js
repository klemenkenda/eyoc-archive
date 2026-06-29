// Hash router + Alpine bootstrap. Must be loaded (with `defer`) before the Alpine.js
// CDN <script> tag in index.html, so the alpine:init listener below is registered
// before Alpine auto-starts.
window.Eyoc = window.Eyoc || {};

Eyoc.parseHash = function (hash) {
  const clean = (hash || "").replace(/^#/, "");
  const [pathPart, queryPart] = clean.split("?");
  const segments = pathPart.split("/").filter(Boolean);
  const params = {};
  if (queryPart) {
    for (const pair of queryPart.split("&")) {
      const [k, v] = pair.split("=");
      if (k) params[decodeURIComponent(k)] = decodeURIComponent(v || "");
    }
  }
  if (segments.length === 0) return { name: "home", params };
  const [name, ...rest] = segments;
  if (name === "year") return { name: "year", params: { ...params, year: rest[0] } };
  if (name === "athlete") return { name: "athlete", params };
  if (name === "medals") return { name: "medals", params };
  if (name === "country") return { name: "country", params: { ...params, code: rest[0] } };
  if (name === "countries") return { name: "countries", params };
  if (name === "rankings") return { name: "rankings", params };
  return { name: "home", params };
};

// Fire-and-forget visit log; never blocks navigation or surfaces errors to the user.
Eyoc.logPageview = function () {
  const payload = JSON.stringify({ path: location.hash || "#/", referrer: document.referrer });
  try {
    if (navigator.sendBeacon) {
      navigator.sendBeacon("api/stats.php", new Blob([payload], { type: "application/json" }));
    } else {
      fetch("api/stats.php", { method: "POST", body: payload, keepalive: true, headers: { "Content-Type": "application/json" } }).catch(() => {});
    }
  } catch (_) {
    // visitor stats are best-effort only
  }
};

Eyoc.appRoot = function () {
  return {
    route: Eyoc.parseHash(location.hash),

    init() {
      Eyoc.store.init();
      window.addEventListener("hashchange", () => {
        this.route = Eyoc.parseHash(location.hash);
        window.scrollTo(0, 0);
        Eyoc.logPageview();
      });
      Eyoc.logPageview();
    },
  };
};

document.addEventListener("alpine:init", () => {
  Alpine.store("eyoc", Eyoc.store);
  Alpine.data("appRoot", Eyoc.appRoot);
});
