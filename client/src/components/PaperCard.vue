<template>
  <div class="paper-card" @click="goToPaper">
    <div class="tags">
      <div class="tag">
        会议：{{ paperInfo.conference }}{{ paperInfo.year }}
      </div>
      <div class="tag">{{ paperInfo.category }}</div>
    </div>
    <div class="paper-title">{{ paperInfo.title }}</div>
    <div class="paper-author-container">
      <div
        class="paper-author"
        v-for="authorItem in paperInfo.author"
        :key="authorItem"
      >
        {{ authorItem }}
      </div>
    </div>
    <div class="paper-abstract"><b>Abstract</b>: {{ paperInfo.abstract }}</div>
    <el-divider></el-divider>
    <div class="paper-recommendation">
      <b>{{ paperInfo.recommender }}</b
      >: {{ paperInfo.reason }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    paperInfo: {
      type: Object,
      required: true,
    },
  },
  methods: {
    goToPaper() {
      this.$router.push({
        name: "paper",
        params: { filename: this.paperInfo.filename },
      });
    },
  },
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.paper-card {
  margin: 5px 5px;
  padding: 8px 15px;
  border-radius: 5px;
  border: var(--main-border-color) solid 0.5px;
  box-shadow: 0 0 14px 0 var(--main-border-color);
  background: #fff;
  text-align: left;
  position: relative;
  &:hover {
    transition: all 0.5s;
    background: #eeeeee;
  }
  .paper-keyword-container {
    font-size: 20px;
  }
  .paper-title {
    margin-top: 5px;
    margin-bottom: 5px;
    font-size: 20px;
  }
  .paper-author-container {
    font-size: 15px;
    .paper-author {
      border-radius: 5px;
      border: solid grey 0.5px;
      display: inline-block;
      margin-right: 10px;
      padding: 2px;
    }
  }
  .paper-abstract {
    margin-top: 2px;
    font-size: 15px;
  }
  .paper-recommendation {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 15px;
  }

  .tags {
    font-size: 14px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: 600;
    display: flex;
    color: var(--primary);
    .tag {
      border-radius: 5px;
      border: solid var(--primary) 0.5px;
      margin: 1px 3px;
      vertical-align: middle;
      padding: 1px 2px;
    }
  }
}

.paper-card::v-deep .el-divider--horizontal {
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>
