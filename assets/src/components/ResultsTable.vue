<template>
  <section id="results">
    <div class="cols cols3">
      <div class="col col3">
        <section class="text" id="country-results">
          <!-- Empty section to hold results -->
        </section>
      </div>
    </div>
  </section>
</template>

<style lang="scss">
.link-legend {
  float: right;

  .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
  }
  .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
  }
  .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
  }
  ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
  }
}
</style>
