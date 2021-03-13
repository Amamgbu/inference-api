<template>
  <div id="origin_bar">
    <div class="boxwidth--1-1 padded--left padded--right">
      <a href="https://research.wikimedia.org/" class="origin_title"
        ><img
          src="@/assets/Wikimedia-Foundation-logo.svg"
          alt="Wikimedia Foundation logo"
        />{{ $t("wikimediaResearch") }}</a
      >
      <interface-locale-changer />
    </div>
  </div>
</template>

<script>
import InterfaceLocaleChanger from "./InterfaceLocaleChanger.vue";

export default {
  name: "TopBar",
  components: {
    InterfaceLocaleChanger
  }
};
</script>

<style lang="scss">
#origin_bar {
  position: fixed;
  width: 100vw;
  top: 0;
  left: 0;
  z-index: 1;
  display: flex;

  .origin_title {
    height: calc(var(--gutter) * 2);
    line-height: calc(var(--gutter) * 2);
    text-transform: uppercase;
    font-weight: 700;
    font-size: 1.3rem;
    letter-spacing: 1px;
    text-decoration: none;
    color: inherit;

    img {
      vertical-align: middle;
      height: 24px;
      margin-right: 0.8rem;
      margin-bottom: 0.4rem;
    }
  }

  @media all and (max-width: 720px) {
    text-align: center;
  }
}
</style>
