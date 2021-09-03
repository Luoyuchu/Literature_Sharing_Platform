<template>
  <div class="paper-board">
    <HeadBar />
    <div class="paper-board-main">
      <div class="paper-list" v-loading="filterLoading">
        <div class="paper-list-container">
          <PaperCard
            class="paper-entry"
            v-for="paperItem in paperListFiltered"
            :key="paperItem._id"
            :paperInfo="paperItem"
          />
        </div>
      </div>
      <div class="paper-filter">
        <div class="filter-name">Conference<br />Journal</div>
        <div class="conference-filter filter-panel checkbox">
          <el-checkbox-group v-model="conferenceSelected">
            <el-checkbox-button
              v-for="conferenceItem in conference"
              :label="conferenceItem"
              :key="conferenceItem"
              >{{ conferenceItem }}</el-checkbox-button
            >
          </el-checkbox-group>
        </div>
        <div class="filter-name">Category</div>
        <div class="category-filter filter-panel checkbox">
          <el-checkbox-group v-model="categorySelected">
            <el-checkbox-button
              v-for="categoryItem in category"
              :label="categoryItem"
              :key="categoryItem"
              >{{ categoryItem }}</el-checkbox-button
            >
          </el-checkbox-group>
        </div>
        <div class="filter-name">Year</div>
        <div class="year-filter filter-panel slider">
          <el-slider
            v-model="yearSelected"
            range
            show-stops
            :min="year[0]"
            :max="year[1]"
            :marks="yearMarks"
          >
          </el-slider>
        </div>
        <div class="filter-name">Priority</div>
        <div class="priority-filter filter-panel slider">
          <el-slider
            v-model="prioritySelected"
            range
            show-stops
            :min="0"
            :max="priority.length - 1"
            :marks="priorityMarks"
            :format-tooltip="priorityTooltip"
          >
          </el-slider>
        </div>
        <el-button
          class="filter-button"
          ref="filterbtn"
          type="primary"
          :loading="filterLoading"
          :onclick="filter"
          >Filter</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import HeadBar from "../components/HeadBar.vue";
import PaperCard from "../components/PaperCard.vue";

const conferenceOptions = ["VIS", "CHI", "TVCG", "EuroVis"];
const yearRange = [1980, 2020];
const category = [
  "树图可视化",
  "交互",
  "理论",
  "用户感知",
  "高位数据",
  "时空数据",
  "AIxVIS",
];
const priority = ["A", "B", "C"];
export default {
  data() {
    return {
      conference: conferenceOptions,
      year: yearRange,
      category: category,
      priority: priority,
      conferenceSelected: conferenceOptions,
      yearSelected: [yearRange[0], yearRange[1]],
      categorySelected: category,
      prioritySelected: [0, priority.length],
      yearMarks: {},
      priorityMarks: {},
      filterLoading: false,
      paperlist: [],
      paperListFiltered: [],
    };
  },
  components: {
    HeadBar,
    PaperCard,
  },
  methods: {
    filter() {
      this.filterLoading = !this.filterLoading;
      let resultList = [];
      for (let i of this.paperlist) {
        if (
          !!this.conferenceSelected.find((d) => d === i.conference) &&
          i.year >= this.yearSelected[0] &&
          i.year <= this.yearSelected[1]
        ) {
          resultList.push(i);
        }
      }
      this.paperListFiltered = resultList;
      // console.log("VIS" in this.conferenceSelected, this.paperListFiltered);
      setTimeout(() => {
        this.filterLoading = !this.filterLoading;
      }, 500);
    },
    priorityTooltip(val) {
      return this.priority[val];
    },
  },
  mounted() {
    const maxLabelCnt = 5;
    axios
      .get("paper/paperlist")
      .then((resp) => {
        this.paperlist = resp.data;
        this.paperListFiltered = this.paperlist;
      })
      .catch((err) => {
        console.log("get paper list failed!");
      });
    let labelInterval = (this.year[1] - this.year[0]) / (maxLabelCnt - 1);
    labelInterval = Math.max(1, labelInterval);
    for (let i = this.year[0]; i <= this.year[1]; i += labelInterval) {
      this.yearMarks[i] = i.toString();
    }
    this.yearMarks[this.year[1]] = this.year[1].toString();
    labelInterval = this.priority.length / (maxLabelCnt - 1);
    labelInterval = Math.max(1, labelInterval);
    for (let i = 0; i < this.priority.length; ) {
      this.priorityMarks[i] = this.priority[i].toString();
      i += labelInterval;
    }
  },
};
</script>

<style lang="scss" scoped>
.paper-board {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  .paper-board-main {
    width: 100%;
    flex: 1 1 0;
    display: flex;
    overflow: hidden;
    .paper-list {
      flex: 0.7 0 0;
      overflow: auto;
      .paper-list-container {
        margin: auto 10px;
        display: flex;
        flex-direction: column;
      }
    }
    .paper-filter {
      font-family: Arial, Helvetica, sans-serif;
      flex: 0.3 0 0;
      display: grid;
      grid-template-columns: 20% 80%;
      grid-auto-rows: auto;
      margin-bottom: auto;
      padding: 60px 40px 50px 20px;
      background: #fff;
      border: var(--main-border-color) solid 0.5px;
      box-shadow: 0 0 14px 0 var(--main-border-color);
      border-radius: 5px;
      .filter-panel {
        margin: 30px 5px;
      }
      .filter-panel::v-deep {
        .el-checkbox-group {
          text-align: left !important;
          .el-checkbox-button {
            margin-right: 7px !important;
            margin-top: 5px !important;
            .el-checkbox-button__inner {
              border-radius: var(--el-border-radius-base) !important;
              border-left: 1px solid #dcdfe6 !important;
            }
          }
        }
      }
      .filter-name {
        margin-top: auto;
        margin-bottom: auto;
        font-weight: 600;
      }
      .filter-button {
        margin: 40px auto 20px;
        width: 150px;
        height: 40px;
        grid-column-start: 1;
        grid-column-end: 3;
        font-size: 18px;
      }
    }
  }
}
</style>
