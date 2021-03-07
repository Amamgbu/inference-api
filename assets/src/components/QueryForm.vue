<template>
  <section class="form">
    <form action="#topic-models">
      <div class="cols cols3">
        <div class="col col1">
          <language-selector v-model="this.lang"/>
        </div>
        <div class="col col1">
          <article-title-picker v-model="this.title"/>
        </div>
        <div class="col col1">
          <threshold-input v-model="this.threshold"/>
        </div>
        <div class="col col1">
          <span class="field_name"></span>
          <input
            type="submit"
            value="Submit"
            id="btnSubmit"
            @click.stop="submit"
          />
        </div>
      </div>
    </form>
  </section>
</template>

<script>
// TODO: Stop using jQuery.
import $ from "jquery";
import "datatables/media/css/jquery.dataTables.min.css";
import "datatables/media/js/jquery.dataTables.min.js";
import ArticleTitlePicker from "./ArticleTitlePicker";
import LanguageSelector from "./LanguageSelector";
import ThresholdInput from "./ThresholdInput";
import {getRandomTitle} from "../QueryRandomArticle";
import {queryCountryAPI} from "../QueryInferenceService";

var render_categories = function(data) {
  $("#country-results").empty();

  if ("Error" in data) {
    $("#country-results").append("<br><p>Error: " + data["Error"] + "</p>");
  } else {
    console.log(data);
    $("#country-results").append(
      '<br><h3><a href="' + data["article"] + '">' +
        document.getElementById("title").value + "</a></h3>"
    );
    $("#country-results").append("<ol>");
    $("#country-results").append(
      "<li><b>Total Number of Outlinks: " + data["results"]["outlink_count"]
    );
    $("#country-results").append(
      "<li><b>Total Number of Inlinks: " + data["results"]["inlink_count"]
    );
    $("#country-results").append("</ol>");

    if (data["results"]["outlink_summary"]["regions"].length > 0) {
      $("#country-results").append("<br><h2> Outlink Summary </h2>");
      $("#country-results").append(
        '<div class="link-legend"><div class="legend-title">Outlink Threshold Guide</div><div class="legend-scale"><ul class="legend-labels"><li><span style="background:#bae4bc;"></span>Above</li><li><span style="background:#fdae6b;"></span>Below</li></ul></div></div>'
      );
      $("#country-results").append(
        '<table id="outlink-summary-table" class="display"><thead><tr><th>Region</th><th>Outlink Count</th><th>Percentage distribution of outlinks (%)</th></tr></thead></table>'
      );
    } else {
      $("#country-results").append("<li><No outlink summary generated.</li>");
    }
    if (data["results"]["inlink_summary"]["regions"].length > 0) {
      $("#country-results").append("<br><h2> Inlink Summary </h2>");
      $("#country-results").append(
        '<div class="link-legend"><div class="legend-title">Inlink Threshold Guide</div><div class="legend-scale"><ul class="legend-labels"><li><span style="background:#bae4bc;"></span>Above</li><li><span style="background:#fdae6b;"></span>Below</li></ul></div></div>'
      );
      $("#country-results").append(
        '<table id="inlink-summary-table" class="display"><thead><tr><th>Region</th><th>Inlink Count</th><th>Percentage distribution of inlinks (%)</th></tr></thead></table>'
      );
    } else {
      $("#country-results").append("<li><No Inlink summary generated.</li>");
    }

    var outlink_data =
      data["results"]["outlink_summary"]["link-percent-count-dist"];
    var outlink_above_thresh =
      data["results"]["outlink_summary"]["above-threshold"];
    var inlink_data =
      data["results"]["inlink_summary"]["link-percent-count-dist"];
    var inlink_above_thresh =
      data["results"]["inlink_summary"]["above-threshold"];

    $("#outlink-summary-table").DataTable({
      data: outlink_data,
      ordering: false,
      createdRow: function(row, data) {
        if (outlink_above_thresh.includes(data["region"])) {
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
      data: inlink_data,
      ordering: false,
      createdRow: function(row, data) {
        if (inlink_above_thresh.includes(data["region"])) {
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

export default {
  name: "QueryForm",
  data: function () {
    return {
      lang: "",
      title: "",
      threshold: "0.5",
    };
  },
  components: {
    ArticleTitlePicker,
    LanguageSelector,
    ThresholdInput,
  },
  methods: {
    submit: async function () {
      if (this.lang && !this.title) {
        this.title = await getRandomTitle(this.lang);
      }

      render_categories(
        await queryCountryAPI(this.lang, this.title, this.threshold)
      );
    },
  },
};
</script>
