import { createI18n } from "vue-i18n";

const messages = {
  en: {
    wikiLanguage: {
      en: "English",
      fr: "French"
    },
    articlePlaceholder: "Article title—e.g., Toni Morrison",
    countryByArticleTitle: "Country Inference by Article",
    disclaimerNote: "No guarantees are made that this tool will be maintained.",
    introductionText: `
      This tool labels Wikipedia articles with countries that are
      predicted to relate to the article. The countries are drawn from
      <a href="{0}">places that are instance-of sovereign state on Wikidata (193 in total).</a>
    `,
    submitButton: "Submit",
    thresholdPlaceholder: "Threshold—e.g., 0.5 (percentage) or 12 (no. of links)",
    wikiLanguagePlaceholder: 'Wikipedia language to query',
    wikimediaResearch: "Wikimedia Research"
  },
  es: {
    wikiLanguage: {
      en: "Inglés",
      fr: "Francés"
    },
    articlePlaceholder: "Título del artículo: p. Ej. Toni Morrison",
    countryByArticleTitle: "Inferencia de país por artículo",
    disclaimerNote: "No se ofrecen garantías de mantenimiento de esta herramienta.",
    introductionText: `
      Esta herramienta etiqueta los artículos de Wikipedia con países que son
      predice que se relacionará con el artículo. Los países se extraen de
      <a href="{0}">lugares que son instancias de estado soberano en Wikidata (193 en total).</a>
    `,
    submitButton: "Enviar",
    thresholdPlaceholder: "Umbral: p. Ej., 0,5 (porcentaje) o 12 (número de enlaces)",
    wikiLanguagePlaceholder: 'Lenguaje de Wikipedia para consultar',
    wikimediaResearch: "Investigación de Wikipedia"
  },
  qqq: {
    articlePlaceholder: "Placeholder text for article title input",
    countryByArticleTitle: "Page title for the country by article title view",
    disclaimerNote: "Disclaimer text explaining that this tool is not production-quality or -stability.",
    introductionText: "Text introducing this tool",
    submitButton: "Button label for submitting the query form",
    thresholdPlaceholder: "Placeholder text for threshold field",
    wikiLanguagePlaceholder: "Placeholder text for wiki language selector",
    wikimediaResearch: "Title for the Wikimedia Research team"
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
