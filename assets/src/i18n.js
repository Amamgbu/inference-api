import { createI18n } from "vue-i18n";

const messages = {
  en: {
    wikiLanguage: {
      en: "English",
      fr: "French"
    },
    articlePlaceholder: "Article title—e.g., Toni Morrison",
    countryByArticleTitle: "Country Inference by Article",
    countryColumn: "Region",
    disclaimerNote1: "No guarantees are made that this tool will be maintained.",
    disclaimerNote2: `
      This is an experimental tool hosted on <a href="{0}">Toolforge</a>.
      No additional personal data is collected by this tool per the
      Cloud Services <a href="{1}" target="_blank" rel="noopener">Terms of Use</a>.
    `,
    inlinkCountColumn: "Inlink Count",
    inlinkPercentColumn: "Percentage distribution of inlinks (%)",
    inlinkSummary: "Inlink Summary",
    inlinkSummaryEmpty: "No inlink summary generated.",
    inlinkThresholdLegend: "Inlink Threshold Guide",
    inlinkTotal: "Total Number of Inlinks:",
    introductionText: `
      This tool labels Wikipedia articles with countries that are
      predicted to relate to the article. The countries are drawn from
      <a href="{0}">places that are instance-of sovereign state on Wikidata (193 in total).</a>
    `,
    legendAbove: "Above",
    legendBelow: "Below",
    outlinkCountColumn: "Outlink Count",
    outlinkPercentColumn: "Percentage distribution of outlinks (%)",
    outlinkSummary: "Outlink Summary",
    outlinkSummaryEmpty: "No outlink summary generated.",
    outlinkThresholdLegend: "Outlink Threshold Guide",
    outlinkTotal: "Total Number of Outlinks:",
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
    countryColumn: "Región",
    disclaimerNote1: "No se ofrecen garantías de mantenimiento de esta herramienta.",
    disclaimerNote2: `
      Esta es una herramienta experimental alojada en <a href="{0}">Toolforge</a>.
      Esta herramienta no recopila datos personales adicionales según el
      <a href="{1}" target="_blank" rel="noopener">Condiciones de uso</a> de los servicios en la nube.
    `,
    inlinkCountColumn: "Recuento de enlaces entrantes",
    inlinkPercentColumn: "Distribución porcentual de enlaces entrantes (%)",
    inlinkSummary: "Resumen de enlaces entrantes",
    inlinkSummaryEmpty: "No se generó un resumen de enlaces entrantes.",
    inlinkThresholdLegend: "Leyenda para umbral de enlaces entrantes",
    inlinkTotal: "Número total de enlaces entrantes:",
    introductionText: `
      Esta herramienta etiqueta los artículos de Wikipedia con países que son
      predice que se relacionará con el artículo. Los países se extraen de
      <a href="{0}">lugares que son instancias de estado soberano en Wikidata (193 en total).</a>
    `,
    legendAbove: "Por encima",
    legendBelow: "Por debajo",
    outlinkCountColumn: "Recuento de enlaces salientes",
    outlinkPercentColumn: "Distribución porcentual de enlaces salientes (%)",
    outlinkSummary: "Resumen de enlaces salientes",
    outlinkSummaryEmpty: "No se generó un resumen de enlaces salientes.",
    outlinkThresholdLegend: "Leyenda para umbral de enlaces salientes",
    outlinkTotal: "Número total de enlaces salientes:",
    submitButton: "Enviar",
    thresholdPlaceholder: "Umbral: p. Ej., 0,5 (porcentaje) o 12 (número de enlaces)",
    wikiLanguagePlaceholder: 'Lenguaje de Wikipedia para consultar',
    wikimediaResearch: "Investigación de Wikipedia"
  },
  qqq: {
    articlePlaceholder: "Placeholder text for article title input",
    countryByArticleTitle: "Page title for the country by article title view",
    countryColumn: "Column title for the detected region",
    disclaimerNote1: "Disclaimer text explaining that this tool is not production-quality or -stability",
    disclaimerNote2: "Disclaimer text linking to context",
    inlinkCountColumn: "Column label for inlink count",
    inlinkPercentColumn: "Column label for inlink count as a percentage of all inlinks",
    inlinkSummary: "Label for the result section summarizing incoming links",
    inlinkSummaryEmpty: "Message displayed when no inlink summary is present",
    inlinkThresholdLegend: "Label for the threshold legend for incoming links",
    inlinkTotal: "Label for the total number of incoming links",
    introductionText: "Text introducing this tool",
    legendAbove: "Legend label for color applied to regions above the threshold",
    legendBelow: "Legend label for color applied to regions below the threshold",
    outlinkCountColumn: "Column label for outlink count",
    outlinkPercentColumn: "Column label for outlink count as a percentage of all outlinks",
    outlinkSummary: "Label for the result section summarizing outgoing links",
    outlinkSummaryEmpty: "Message displayed when no outlink summary is present",
    outlinkThresholdLegend: "Label for the threshold legend for outgoing links",
    outlinkTotal: "Label for the total number of outgoing links",
    submitButton: "Button label for submitting the query form",
    thresholdPlaceholder: "Placeholder text for threshold field",
    wikiLanguagePlaceholder: "Placeholder text for wiki language selector",
    wikimediaResearch: "Title for the Wikimedia Research team"
  }
};

function getBrowserLocale(options = {}) {
  if (localStorage.getItem("locale")) {
    // FIXME: group with the logic across in InterfaceLocaleChanger.vue
    return localStorage.getItem("locale");
  }

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
