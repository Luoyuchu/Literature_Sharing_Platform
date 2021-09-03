<template>
  <router-view />
</template>

<script>
import PaperBoard from "./views/PaperBoard.vue";

export default {
  name: "App",
  components: {
    PaperBoard,
  },
};
</script>

<style lang="scss">
html,
body {
  height: 100%;
  width: 100%;
  overflow: hidden;
  margin: 0px;
  background: var(--main-bg-color);
}

#app {
  // font-family: Avenir, Helvetica, Arial, sans-serif;
  font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
  width: 100%;
  overflow: hidden;
}
</style>
