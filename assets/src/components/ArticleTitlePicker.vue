<template>
  <label
    class="placeholder"
    :class="{ off: !isFocused && !modelValue }"
    @focusin="isFocused = true"
    @focusout="isFocused = false"
    ><span class="field_name">Article title -- e.g., Toni Morrison</span>
    <input
      id="title"
      type="text"
      @input="$emit('update:modelValue', $event.target.value)"
      :value="modelValue"
    />
  </label>
</template>

<script>
export default {
  name: "ArticleTitlePicker",
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
