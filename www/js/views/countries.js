window.Eyoc = window.Eyoc || {};
Eyoc.views = Eyoc.views || {};

Eyoc.views.countries = function () {
  return {
    get countries() {
      return Eyoc.store.countriesWithResults().map((code) => ({
        code,
        name: Eyoc.store.countryName(code),
      }));
    },
  };
};
