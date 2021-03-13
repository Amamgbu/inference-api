import { createI18n } from "vue-i18n";

const messages = {
  en: {
    wikiLanguage: {
      en: "English",
      fr: "French"
    },
    articlePlaceholder: "Article title—e.g., Toni Morrison",
    countryByArticleTitle: "Country Inference by Article",
    submitButton: "Submit",
    thresholdPlaceholder: "Threshold—e.g., 0.5 (percentage) or 12 (no. of links)",
    wikiLanguagePlaceholder: 'Wikipedia language to query'
  },
  es: {
    wikiLanguage: {
      en: "Inglés",
      fr: "Francés"
    },
    articlePlaceholder: "Título del artículo: p. Ej. Toni Morrison",
    countryByArticleTitle: "Inferencia de país por artículo",
    submitButton: "Enviar",
    thresholdPlaceholder: "Umbral: p. Ej., 0,5 (porcentaje) o 12 (número de enlaces)",
    wikiLanguagePlaceholder: 'Lenguaje de Wikipedia para consultar'
  },
  qqq: {
    articlePlaceholder: "Placeholder text for article title input",
    countryByArticleTitle: "Page title for the country by article title view",
    submitButton: "Button label for submitting the query form",
    thresholdPlaceholder: "Placeholder text for threshold field",
    wikiLanguagePlaceholder: "Placeholder text for wiki language selector"
  }
};

function getBrowserLocale(options = {}) {
  const defaultOptions = { trimCountryCode: true };

  const opt = { ...defaultOptions, ...options };

  const navigatorLocale =
    navigator.languages !== undefined
      ? navigator.languages[0]
      : navigator.language;

  if (!navigatorLocale) {
    return undefined;
  }

  const trimmedLocale = opt.trimCountryCode
    ? navigatorLocale.trim().split(/-|_/)[0]
    : navigatorLocale.trim();

  return trimmedLocale;
}

export const i18n = createI18n({
  locale: getBrowserLocale(),
  fallbackLocale: "en",
  messages
});
