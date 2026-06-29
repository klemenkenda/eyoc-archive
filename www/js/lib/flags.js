// Renders a country flag as a small <img> from flagcdn.com, keyed by ISO 3166-1 alpha-2
// code. Flag *emoji* don't render as actual flags on Windows (no flag glyphs in the
// system color-emoji font, Chrome included) - an image is the only cross-platform way
// to show a real flag without bundling our own icon set. EYOC results use IOF-style
// codes (results/EYOC-COUNTRIES.md), which mostly differ from ISO alpha-2 (e.g.
// GBR/GB, GER/DE, SUI/CH), hence this lookup table.
window.Eyoc = window.Eyoc || {};
Eyoc.lib = Eyoc.lib || {};

Eyoc.COUNTRY_ISO2 = {
  AUT: "AT", AZE: "AZ", BEL: "BE", BLR: "BY", BUL: "BG", CRO: "HR", CYP: "CY",
  CZE: "CZ", DEN: "DK", ESP: "ES", EST: "EE", FIN: "FI", FRA: "FR", GBR: "GB",
  GER: "DE", HUN: "HU", IRL: "IE", ISR: "IL", ITA: "IT", LAT: "LV", LIE: "LI",
  LTU: "LT", LUX: "LU", MDA: "MD", MKD: "MK", MNE: "ME", NED: "NL", NOR: "NO",
  POL: "PL", POR: "PT", ROU: "RO", RUS: "RU", SLO: "SI", SRB: "RS", SUI: "CH",
  SVK: "SK", SWE: "SE", TUR: "TR", UKR: "UA",
};

// Fetches a 2x-resolution image (rendered at 20x15 via CSS in style.css's .flag rule)
// so it stays crisp on standard displays and doesn't look soft on HiDPI/Retina ones.
// "" if there's no ISO mapping for this code - callers x-show on this to skip the <img>.
Eyoc.lib.flagUrl = function (code) {
  const iso2 = Eyoc.COUNTRY_ISO2[code];
  return iso2 ? `https://flagcdn.com/40x30/${iso2.toLowerCase()}.png` : "";
};
