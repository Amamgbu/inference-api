<template>
  <div id="origin_bar">
    <div class="boxwidth--1-1 padded--left padded--right">
      <a href="https://research.wikimedia.org/" class="origin_title"
        ><img
          src="@/assets/Wikimedia-Foundation-logo.svg"
          alt="Wikimedia Foundation logo"
        />Wikimedia Research</a
      >
    </div>
  </div>
</template>

<style lang="scss">
#origin_bar {
  position: fixed;
  width: 100%;
  top: 0;
  left: 0;
  z-index: 1;

  .origin_title {
    display: inline-block;
    height: calc(var(--gutter) * 2);
    line-height: calc(var(--gutter) * 2);
    text-transform: uppercase;
    font-weight: 700;
    font-size: 1.3rem;
    letter-spacing: 1px;
    text-decoration: none;
    color: inherit;

    img {
      display: inline-block;
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
