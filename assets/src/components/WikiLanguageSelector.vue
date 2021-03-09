<template>
  <label
    class="placeholder"
    :class="{ off: !isFocused && !modelValue }"
    @focusin="isFocused = true"
    @focusout="isFocused = false"
    ><span class="field_name">{{ $t('wikiLanguagePlaceholder') }}</span>
    <select
      id="lang"
      @input="$emit('update:modelValue', $event.target.value)"
      :selected="modelValue"
    >
      <option value=""></option>
      <option value="en">{{ $t('wikiLanguage.en') }}</option>
      <option value="fr">{{ $t('wikiLanguage.fr') }}</option>
    </select>
  </label>
</template>

<script>
export default {
  name: "WikiLanguageSelector",
  props: {
    modelValue: String
  },
  data: function() {
    return {
      isFocused: false
    };
  }
};
</script>
