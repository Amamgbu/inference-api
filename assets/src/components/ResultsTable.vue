<template>
  <section id="results">
    <div class="cols cols3">
      <div class="col col3">
        <section class="text" id="country-results">
          <!--
          if ("Error" in data) {
            $("#country-results").append("<br><p>Error: " + data["Error"] + "</p>");
          -->

          <ol>
            <br />
            <h3>
              <a :href="this.articleUrl">{{ this.title }}</a>
            </h3>
            <li>
              <b>{{ $t("outlinkTotal") }}</b> {{ this.results.outlink_count }}
            </li>
            <li>
              <b>{{ $t("inlinkTotal") }}</b> {{ this.results.inlink_count }}
            </li>
          </ol>

          <template v-if="this.results.outlink_summary.regions">
            <br />
            <h2>{{ $t("outlinkSummary") }}</h2>
            <div class="link-legend">
              <div class="legend-title">{{ $t("outlinkThresholdLegend") }}</div>
              <div class="legend-scale">
                <ul class="legend-labels">
                  <li><span style="background:#bae4bc;"></span>{{ $t("legendAbove") }}</li>
                  <li><span style="background:#fdae6b;"></span>{{ $t("legendBelow") }}</li>
                </ul>
              </div>
            </div>
            <table id="outlink-summary-table" class="display">
              <thead>
                <tr>
                  <th>{{ $t("countryColumn") }}</th>
                  <th>{{ $t("outlinkCountColumn") }}</th>
                  <th>{{ $t("outlinkPercentColumn") }}</th>
                </tr>
              </thead>
            </table>
          </template>
          <template v-else>
            <li>{{ $t("outlinkSummaryEmpty") }}</li>
          </template>

          <template v-if="this.results.inlink_summary.regions">
            <br />
            <h2>{{ $t("inlinkSummary") }}</h2>
            <div class="link-legend">
              <div class="legend-title">{{ $t("inlinkThresholdLegend") }}</div>
              <div class="legend-scale">
                <ul class="legend-labels">
                  <li><span style="background:#bae4bc;"></span>{{ $t("legendAbove") }}</li>
                  <li><span style="background:#fdae6b;"></span>{{ $t("legendBelow") }}</li>
                </ul>
              </div>
            </div>
            <table id="inlink-summary-table" class="display">
              <thead>
                <tr>
                  <th>{{ $t("countryColumn") }}</th>
                  <th>{{ $t("inlinkCountColumn") }}</th>
                  <th>{{ $t("inlinkPercentColumn") }}</th>
                </tr>
              </thead>
            </table>
          </template>
          <template v-else>
            <li>{{ $t("inlinkSummaryEmpty") }}</li>
          </template>
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

<script>
import $ from "jquery";
// TODO: vue.dataTables library?
import "datatables/media/css/jquery.dataTables.min.css";
import "datatables/media/js/jquery.dataTables.min.js";

export default {
  name: "ResultsTable",
  props: {
    response: Object,
    title: String
  },
  computed: {
    articleUrl() {
      return this.response.article;
    },
    results() {
      return this.response.results;
    },
    outlink_data() {
      return this.results.outlink_summary["link-percent-count-dist"];
    },
    outlink_above_thresh() {
      return this.results.outlink_summary["above-threshold"];
    },
    inlink_data() {
      return this.results.inlink_summary["link-percent-count-dist"];
    },
    inlink_above_thresh() {
      return this.results.inlink_summary["above-threshold"];
    }
  },
  // TODO: Should also handle update. Until then, we can destroy and recreate
  // the element. The problem is a mismatch between jQuery and Vue.
  mounted() {
    $("#outlink-summary-table").DataTable({
      data: this.outlink_data,
      ordering: false,
      createdRow: (row, data) => {
        if (this.outlink_above_thresh.includes(data.region)) {
          $(row).css("background-color", "#bae4bc");
        } else {
          $(row).css("background-color", "#fdae6b");
        }
      },
      columns: [
        { data: "region" },
        { data: "link-count" },
        { data: "percent-dist" }
      ]
    });
    $("#inlink-summary-table").DataTable({
      data: this.inlink_data,
      ordering: false,
      createdRow: (row, data) => {
        if (this.inlink_above_thresh.includes(data.region)) {
          $(row).css("background-color", "#bae4bc");
        } else {
          $(row).css("background-color", "#fdae6b");
        }
      },
      columns: [
        { data: "region" },
        { data: "link-count" },
        { data: "percent-dist" }
      ]
    });
  }
};
</script>
