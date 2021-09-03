<template>
  <div class="about">
    <div class="logo">
      <img src="@/assets/lab_logo.svg" />
    </div>
    <div class="info">
      <h1>Online Literature Management and Share</h1>
      <a href="vis.pku.edu.cn">
        <h2>PKU Visualization and Visual Analytics Group</h2>
      </a>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
.about {
  height: 100vh;
  width: 100vw;
  background-image: url("~@/assets/header-pattern.png");
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  h1 {
    font-size: 30px;
  }
  .logo {
    height: 25vh;
    width: 25vw;
  }
}
</style>
