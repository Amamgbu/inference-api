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

<style lang="scss">
#tool_holder {
  width: 100%;
  overflow: hidden;
  -webkit-box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.25);
  -moz-box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.25);
  box-shadow: 0 1px 4px 0 rgba(0, 0, 0, 0.25);
  background: #fff;
  padding-top: calc(var(--gutter) * 2);
  padding-bottom: calc(var(--gutter) * 2);
  margin-top: calc(var(--gutter) * 2);
  position: relative;
  z-index: 2;
}

#tool_main {
  h2,
  h3,
  h4,
  h5,
  h6 {
    position: relative;
    margin-bottom: 0;
  }

  h2:not(.simple):after,
  h3:not(.simple):after,
  h4:not(.simple):after {
    content: " ";
    display: block;
    width: 50%;
    max-width: 30rem;
    position: absolute;
    border-top: 1px solid;
    height: 0;
    bottom: 0;
    left: 0;
  }

  h2:not(.simple):after {
    border-top-width: 2px;
    border-top-color: var(--color1);
  }

  h4:not(.simple):after {
    border-top-color: var(--grey1);
  }

  h2 {
    font-size: 200%;
    margin-bottom: calc(var(--gutter) * 2);
  }

  h3 {
    font-size: 175%;
    margin-bottom: 4.8rem;
  }

  h4 {
    font-size: 150%;
    margin-bottom: 4.8rem;
  }

  h2:not(.simple) {
    padding-bottom: var(--gutter);
  }

  h3:not(.simple) {
    padding-bottom: 2.4rem;
  }

  h4:not(.simple) {
    padding-bottom: 1.6rem;
  }

  h5 {
    font-size: 130%;
    margin-bottom: var(--gutter);
  }

  h6 {
    font-size: 115%;
    margin-bottom: var(--gutter);
  }

  .cols {
    width: calc(100% + (var(--gutter) * 1));
    margin-left: calc(var(--gutter) * -0.5);
    margin-top: calc(var(--gutter) * -1.5);
  }

  .cols:after {
    content: " ";
    display: block;
    clear: both;
    width: 100%;
    height: 0;
  }

  .cols .col {
    float: left;
    box-sizing: border-box;
    padding: calc(var(--gutter) * 1.5) calc(var(--gutter) * 0.5) 0;
  }

  .cols2 .col2,
  .cols3 .col3,
  .cols4 .col4 {
    width: 100%;
  }

  .cols4 .col3 {
    width: 75%;
  }

  .cols3 .col2 {
    width: 66.6666%;
  }

  .cols2 .col1,
  .cols4 .col2 {
    width: 50%;
  }

  .cols3 .col1 {
    width: 33.3333%;
  }

  .cols4 .col1 {
    width: 25%;
  }

  form label {
    display: block;
  }

  form .field_name {
    display: inline-block;
    white-space: nowrap;
    width: 100%;
    box-sizing: border-box;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 85%;
  }

  form input,
  form select,
  form textarea {
    display: block;
    box-sizing: border-box;
    width: 100%;
    font-family: inherit;
    font-size: 100%;
    padding: 1rem;
    border-radius: 3px;
    border: 1px solid var(--grey1);
    transition: border 0.5s ease-out;
  }

  form input:focus,
  form select:focus,
  form textarea:focus {
    border-color: var(--black);
  }

  form input[type="radio"],
  form input[type="checkbox"] {
    display: inline-block;
    vertical-align: middle;
    width: auto;
    padding: 0;
    border-radius: 0;
    border: none;
    margin: 0;
  }

  form .submit_holder {
    text-align: right;
  }

  form input[type="submit"] {
    -webkit-appearance: none;
    appearance: none;
    display: inline-block;
    vertical-align: middle;
    width: auto;
    padding: 1.4rem 2rem;
    font-size: 100%;
    border-radius: 0;
    border: none;
    border-left: 3px solid #acf;
    margin: 0;
    background-color: var(--color1);
    color: var(--color2);
    cursor: pointer;
    transition: none;
  }

  form input[type="submit"]:hover,
  form input[type="submit"]:focus {
    border-color: var(--grey2);
    background-color: var(--black);
  }

  form input[type="radio"] + .field_name,
  form input[type="checkbox"] + .field_name {
    display: inline-block;
    vertical-align: middle;
    margin-left: 1rem;
    width: auto;
    overflow: auto;
    text-overflow: initial;
    white-space: normal;
    font-size: 100%;
  }

  body.js & form label.placeholder {
    pointer-events: none;
  }

  body.js & form label.placeholder > *:not(.field_name) {
    pointer-events: auto;
  }

  body.js & form label.placeholder .field_name {
    transform-origin: left top;
    transition: opacity 0.5s ease-out,
      transform 0.75s cubic-bezier(0.19, 1, 0.22, 1);
  }

  body.js & form label.placeholder.off .field_name {
    transform: scale(1.1764705882) translateX(1rem) translateY(2.95rem);
    opacity: 0.5;
  }

  ul {
    list-style: disc;
  }

  ol {
    list-style: decimal;
  }

  ul a,
  ol a {
    text-decoration: underline;
  }

  ul a:hover,
  ol a:hover {
    text-decoration: none;
  }

  li {
    padding-left: 0rem;
    list-style-position: inside;
  }

  li + li,
  li ul,
  li ol {
    padding-top: 0.8rem;
    border-top: 1px solid var(--grey1);
    margin-top: 0.8rem;
  }

  li ul,
  li ol {
    padding-left: 1.8rem;
  }

  li ul {
    list-style: circle;
  }

  figure {
    padding: 0.4rem;
    margin-left: 0;
    margin-right: 0;
    margin-bottom: 0;
    border: 1px solid var(--grey1);
    text-align: right;
  }

  figure img {
    display: block;
    max-width: 100%;
    background: #eee;
  }

  figure figcaption {
    display: inline-block;
    max-width: 75%;
    font-size: 1.3rem;
    color: var(--grey2);
    padding: 0.6rem 0.8rem 0.3rem 0;
  }

  figure figcaption a {
    text-decoration: underline;
  }

  figure figcaption a:hover {
    color: var(--color1);
    text-decoration: none;
  }

  .card {
    display: block;
    box-sizing: border-box;
    overflow: hidden;
  }

  .card a {
    display: block;
  }

  .card.has--border {
    border: 1px solid var(--grey1);
    border-radius: 3px;
  }

  .card figure {
    padding: 0;
    margin: 0;
    border: none;
    position: relative;
    height: 0;
    padding-bottom: 18rem;
    overflow: hidden;
  }

  .card .img {
    display: block;
    margin-bottom: 2rem;
    background: #eee;
  }

  .card figure img {
    max-width: none;
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.75s cubic-bezier(0.19, 1, 0.22, 1);
    transform: scale(1) translateZ(0);
  }

  .card a.img:hover figure img {
    transform: scale(1.07) translateZ(0);
  }

  .card .texts {
    font-size: 1.4rem;
  }

  .card.has--border .texts > * {
    padding: 0 1.4rem;
  }

  .card .texts > * + * {
    margin-top: 1.4rem;
  }

  .card h3 {
    padding-bottom: 0;
    margin-bottom: 0;
    border: none;
    font-size: 160%;
  }

  .card h3:after {
    content: "";
    display: none;
  }

  .card h3 a {
    display: block;
  }

  .card:not(.has--border):hover .more {
    text-decoration: underline;
  }

  .card .description > * + * {
    margin-top: 0.8rem;
  }

  .card .more {
    color: var(--color1);
  }

  .card.has--border .more {
    padding-top: 1rem;
    padding-bottom: 1rem;
    border-top: 1px solid var(--grey1);
    text-align: right;
    margin-top: 2rem;
  }

  .card.has--border a:hover .more {
    background-color: var(--color2);
    text-decoration: underline;
  }

  & > section + section {
    margin-top: 7.2rem;
  }

  .description.padded--left {
    padding-left: 30rem;
  }

  .text > * + * {
    margin-top: 1.6rem;
  }

  .text > * + ul,
  .text > * + ol,
  .text > ul + *,
  .text > ol + * {
    margin-top: 4.2rem;
  }

  @media all and (max-width: 1000px) {
    .cols4 .col2 {
      width: 100%;
    }

    .cols3 .col2,
    .cols3 .col1,
    .cols4 .col1,
    .cols4 .col3 {
      width: 50%;
    }

    figure {
      padding: 0.3rem;
    }
  }
}
</style>
