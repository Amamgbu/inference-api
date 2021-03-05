<template>
  <article id="tool_holder">
    <introduction />

    <div class="separator"></div>

    <section id="topic-models" class="boxwidth--1-1 padded--left padded--right">
      <main id="tool_main">
        <query-form />
        <results-table />
      </main>
    </section>
  </article>
</template>

<script>
import Introduction from "./Introduction.vue";
import QueryForm from "./QueryForm.vue";
import ResultsTable from "./ResultsTable";

export default {
  name: "ToolHolder",
  components: {
    Introduction,
    QueryForm,
    ResultsTable
  }
};
</script>
