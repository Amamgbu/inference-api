<template>
  <section class="form">
    <form action="#topic-models">
      <div class="cols cols3">
        <div class="col col1">
          <label class="placeholder"><span class="field_name">Language code -- e.g., en for English</span>
            <select id="lang">
              <option value=""></option>
              <option value="en">English</option>
              <option value="fr">French</option>
            </select>
          </label>
        </div>
        <div class="col col1">
          <label class="placeholder"><span class="field_name">Article title -- e.g., Toni Morrison</span>
            <input type="text" value="" placeholder="Placeholder text" id="title" />
          </label>
        </div>
        <div class="col col1">
          <label class="placeholder"><span class="field_name">Threshold -- e.g., 0.5(percentage) or 12(no. of links)</span >
            <input type="text" value="0.5" placeholder="Placeholder text" id="threshold" />
          </label>
        </div>
        <div class="col col1">
          <span class="field_name"></span>
          <input type="submit" value="Submit" id="btnSubmit" />
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

$(function() {
  $("form label.placeholder").each(function() {
    if (!$("input, textarea, select", this).val()) {
      $(this).addClass("off");
    }
    $(this).on("focusin", function() {
      $(this).removeClass("off");
    });
    $(this).on("focusout", function() {
      if (!$("input, textarea, select", this).val()) {
        $(this).addClass("off");
      }
    });
    $("*[placeholder]", this).attr("placeholder", "");
  });

  $("#btnSubmit").click(function(e) {
    e.preventDefault();
    queryCountryAPI();
  });
});

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

var update_title = function(data) {
  document.getElementById("title").value = data["query"]["random"][0]["title"];
  document.getElementById("title").parentNode.className = "placeholder";
};

function queryCountryAPI() {
  if (
    document.getElementById("lang").value &&
    !document.getElementById("title").value
  ) {
    var randomPageQueryURL =
      "https://" + document.getElementById("lang").value +
      ".wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0&origin=*";
    $.ajax(randomPageQueryURL, {
      success: update_title.bind(this),
      error: function(jqxmlhr, status, error) {
        console.log(status + ": " + error);
      },
      async: false
    });
  }

  // TODO: API URL from configuration.
  var queryUrl =
    "/api/v1/get-summary?lang=" +
    document.getElementById("lang").value +
    "&title=" +
    document.getElementById("title").value +
    "&threshold=" +
    document.getElementById("threshold").value;
  $.ajax(queryUrl, {
    success: render_categories.bind(this),
    error: function(jqxmlhr, status, error) {
      console.log(status + ": " + error);
    }
  });
}

export default {
  name: "QueryForm"
};
</script>
