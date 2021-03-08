<template>
  <section class="form">
    <form action="#topic-models">
      <div class="cols cols3">
        <div class="col col1">
          <language-selector v-model="this.lang" />
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
            value="Submit"
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
import LanguageSelector from "./LanguageSelector";
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
  emits: ["query-results"],
  components: {
    ArticleTitlePicker,
    LanguageSelector,
    ThresholdInput
  },
  methods: {
    submit: async function() {
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
