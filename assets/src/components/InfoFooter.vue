<template>
  <footer id="tool_footer">
    <div id="tool_footer-in" class="boxwidth--1-1 padded--left padded--right">
      <p>
        Experimental tool developed by
        <span class="tool-author"
          ><a href="https://meta.wikipedia.org/wiki/User:Amamgbu"
            >Jesse (WMF intern)</a
          >
          as part of
          <a href="https://research.wikimedia.org/">Wikimedia Research</a></span
        >.
      </p>
      <ul>
        <li>
          <a href="https://github.com/amamgbu/inference-api">View Source</a>
        </li>
        <li>
          <a
            href="https://meta.wikimedia.org/wiki/Research:Language-Agnostic_Topic_Classification/Countries"
            >Meta</a
          >
        </li>
        <li>
          <a href="https://github.com/amamgbu/inference-api#license">License</a>
        </li>
      </ul>
    </div>
  </footer>
</template>

<style lang="scss">
#tool_footer {
  padding-top: 2.4rem;
  font-size: 1.2rem;
  padding-bottom: 2.4rem;
}

#tool_footer-in {
  & > * + * {
    padding-top: 1.6rem;
  }

  & > p + p {
    margin-top: 0;
  }

  ul {
    margin-top: -0.4rem;
    margin-left: -0.4rem;
  }

  li {
    display: inline-block;
    vertical-align: middle;
    margin-top: 0.4rem;
  }

  li a {
    display: block;
    padding: 0 0.4rem;
  }

  li + li {
    margin-left: 0.4rem;
    padding-left: 0.4rem;
    border-left: 1px solid var(--grey1);
  }
}
</style>
