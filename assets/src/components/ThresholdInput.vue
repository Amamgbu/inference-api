<template>
  <label
    class="placeholder"
    :class="{ off: !isFocused && !modelValue }"
    @focusin="isFocused = true"
    @focusout="isFocused = false"
    ><span class="field_name"
      >Threshold -- e.g., 0.5(percentage) or 12(no. of links)</span
    >
    <input
      id="threshold"
      type="text"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>

<script>
export default {
  name: "ThresholdInput",
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
