<template>
  <label class="placeholder"
    :class="{ off: !isFocused && !selected }"
    @focusin="isFocused = true"
    @focusout="isFocused = false"
  ><span class="field_name">Language code -- e.g., en for English</span>
    <select
      id="lang"
      v-model="selected"
    >
      <option value=""></option>
      <option value="en">English</option>
      <option value="fr">French</option>
    </select>
  </label>
</template>

<script>
export default {
  name: "LanguageSelector",
  data: function () {
    return {
      isFocused: false,
      selected: "",
    };
  },
}
</script>