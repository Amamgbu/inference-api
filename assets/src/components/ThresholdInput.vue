<template>
    <label class="placeholder"
        :class="{ off: !isFocused && !value }"
        @focusin="isFocused = true"
        @focusout="isFocused = false"
    ><span class="field_name">Threshold -- e.g., 0.5(percentage) or 12(no. of links)</span >
        <input type="text" v-model="value" placeholder="Placeholder text" id="threshold" />
    </label>
</template>

<script>
export default {
  name: "ThresholdInput",
  data: function () {
    return {
      isFocused: false,
      value: "0.5",
    };
  },
}
</script>