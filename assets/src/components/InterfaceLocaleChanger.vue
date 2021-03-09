<template>
  <div class="locale-changer">
    <select v-model="$i18n.locale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">
        {{ ownName[lang] }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: "InterfaceLocaleChanger",
  data() {
    return {
      langs: ["en"],
      ownName: {
        en: "English"
      }
    };
  }
};
</script>

<style lang="scss">
.locale-changer {
  display: inline-block;
  margin-left: 20vw;
}
</style>
