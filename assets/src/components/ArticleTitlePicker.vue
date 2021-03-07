<template>
    <label class="placeholder"
        :class="{ off: !isFocused && !value }"
        @focusin="isFocused = true"
        @focusout="isFocused = false"
    ><span class="field_name">Article title -- e.g., Toni Morrison</span>
        <input type="text" v-model="value" id="title" />
    </label>
</template>

<script>
export default {
  name: "ArticleTitlePicker",
  data: function () {
    return {
      isFocused: false,
      value: "",
    };
  },
}
</script>