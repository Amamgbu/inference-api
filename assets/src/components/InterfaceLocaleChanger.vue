<template>
  <div class="locale-changer">
    <select v-model="$i18n.locale">
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
      ownNames
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
