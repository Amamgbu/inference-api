<template>
  <label
    class="placeholder"
    :class="{ off: !isFocused && !modelValue }"
    @focusin="isFocused = true"
    @focusout="isFocused = false"
    ><span class="field_name">Language code -- e.g., en for English</span>
    <select
      id="lang"
      @input="$emit('update:modelValue', $event.target.value)"
      :selected="modelValue"
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
