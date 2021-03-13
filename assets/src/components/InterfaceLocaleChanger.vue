<template>
  <div class="locale-changer">
    <select v-model="locale" @input="saveLocale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">
        {{ ownNames[lang] }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "InterfaceLocaleChanger",
  data() {
    const ownNames = {
        en: "English",
        es: "Español"
    };
    return {
      langs: Object.keys(ownNames),
      locale: this.$i18n.locale,
      ownNames
    };
  },
  watch: {
    locale(newLocale) {
      // Apply
      this.$i18n.locale = newLocale;
      // Make sticky.
      localStorage.setItem("locale", newLocale);
    }
  }
};
</script>

<style lang="scss">
.locale-changer {
  display: inline-block;
  margin-left: 20vw;
}
</style>
