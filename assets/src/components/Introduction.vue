<template>
  <div
    id="tool_header--holder"
    class="boxwidth--1-1 padded--left padded--right"
  >
    <header id="tool_header">
      <!-- Tool name -->
      <h1>{{ $t("countryByArticleTitle") }}</h1>
      <div class="meta">
        <div class="disclaimer note">
          <p>{{ $t('disclaimerNote1') }}</p>
          <p v-html="$t('disclaimerNote2', ['https://wikitech.wikimedia.org/wiki/Portal:Toolforge', 'https://wikitech.wikimedia.org/wiki/Wikitech:Cloud_Services_Terms_of_use'])"></p>
        </div>
        <div class="description padded--right">
          <p v-html="$t('introductionText', ['https://www.wikidata.org/wiki/Special:WhatLinksHere/Q3624078'])"></p>
        </div>
      </div>
    </header>
  </div>
</template>

<style lang="scss">
#tool_header {
  h1 {
    font-size: 250%;
    margin-bottom: var(--gutter);
  }

  .meta > * + * {
    margin-top: var(--gutter);
  }

  .note {
    margin-left: auto;
    margin-right: auto;
    color: var(--grey2);
    /*
    border-top: 1px solid var(--grey1);
    border-bottom: 1px solid var(--grey1);
  */
    border-left: 3px solid var(--color1);
    padding: 0.6rem 0 0.6rem 2.4rem;
    font-size: 1.4rem;

    time {
      font-weight: 700;
    }

    & > * + * {
      margin-top: 0.8rem;
    }
  }

  .duration time {
    font-weight: 700;
  }

  .description > * + * {
    margin-top: 1.6rem;
    padding-top: var(--gutter);
  }
}

@media all and (max-width: 1000px) {
  #tool_header {
    .description {
      padding-top: 0;

      &.padded--left {
        padding-left: 10rem;
      }
    }

    .note {
      border-left-width: 2px;
    }
  }
}
</style>
