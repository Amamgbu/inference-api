<template>
  <section class="form">
    <form action="#topic-models">
      <div class="cols cols3">
        <div class="col col1">
          <wiki-language-selector v-model="this.lang" />
        </div>
        <div class="col col1">
          <article-title-picker v-model="this.title" />
        </div>
        <div class="col col1">
          <threshold-input v-model="this.threshold" />
        </div>
        <div class="col col1">
          <span class="field_name"></span>
          <input
            type="submit"
            :value="$t('submitButton')"
            id="btnSubmit"
            @click.stop="submit"
          />
        </div>
      </div>
    </form>
  </section>
</template>

<script>
import ArticleTitlePicker from "./ArticleTitlePicker";
import WikiLanguageSelector from "./WikiLanguageSelector";
import ThresholdInput from "./ThresholdInput";
import { getRandomTitle } from "../QueryRandomArticle";
import { queryCountryAPI } from "../QueryInferenceService";

export default {
  name: "QueryForm",
  data: function() {
    return {
      lang: "",
      title: "",
      threshold: "0.5"
    };
  },
  emits: ["query-begin", "query-results"],
  components: {
    ArticleTitlePicker,
    WikiLanguageSelector,
    ThresholdInput
  },
  methods: {
    submit: async function() {
      this.$emit("query-begin");

      if (this.lang && !this.title) {
        this.title = await getRandomTitle(this.lang);
      }

      const results = await queryCountryAPI(
        this.lang,
        this.title,
        this.threshold
      );
      this.$emit("query-results", this.title, results);
    }
  }
};
</script>
