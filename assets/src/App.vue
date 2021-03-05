<template>
  <top-bar />
  <tool-holder />
  <info-footer />
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import InfoFooter from "./components/InfoFooter.vue";
import TopBar from "./components/TopBar.vue";
import ToolHolder from "./components/ToolHolder.vue";

export default {
  name: "App",
  components: {
    // HelloWorld
    InfoFooter,
    ToolHolder,
    TopBar
  }
};
</script>

<style lang="scss">
@use 'assets/legacy.scss';

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
