<template>
  <div class="paper-rating">
    <div class="block-header">{{ paperInfo.title }}</div>
    <div class="rating-grid">
      <div class="title"><span>Average Rating:</span></div>
      <el-rate :modelValue="averageRating" allow-half disabled />
      <div class="label">
        <span v-if="!!averageRating">{{ averageRating * 2 }} / 10</span>
        <span v-if="!averageRating">No record</span>
      </div>
      <div class="title"><span>My Rating:</span></div>
      <el-rate
        :modelValue="myRating"
        @update:modelValue="updateRating($event)"
        allow-half
        :disabled="!isLoggedIn && '_id' in paperInfo"
      />
      <div class="label">
        <span v-if="!!myRating">{{ myRating * 2 }} / 10</span>
        <span v-if="!myRating">No record</span>
      </div>
    </div>

    <div class="stat-container">
      <el-tooltip content="Number of Ratings" placement="left-start">
        <div class="stat-item">
          <i class="el-icon-star-off"></i>
          <span class="label">{{ numberOfRatings }}</span>
        </div>
      </el-tooltip>
      <el-tooltip content="Number of Intensive Readers">
        <div class="stat-item">
          <i class="el-icon-view"></i>
          <span class="label">{{ numberOfIntensive }}</span>
        </div>
      </el-tooltip>
      <el-tooltip content="Number of Extensive readers" placement="left-end">
        <div class="stat-item">
          <i class="el-icon-search"></i>
          <span class="label">{{ numberOfExtensive }}</span>
        </div>
      </el-tooltip>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  props: {
    paperInfo: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      myRating: 0,
      averageRating: 0,
      numberOfRatings: 0,
      numberOfIntensive: 0,
      numberOfExtensive: 0,
    };
  },
  computed: {
    ...mapGetters("account", ["isLoggedIn", "userId"]),
  },
  watch: {
    paperInfo: {
      immediate: true,
      deep: false,
      handler: function(val, oldval) {
        console.log(val);
        if ("_id" in val) {
          axios
            .get("/rating/query", {
              params: {
                paper_id: this.paperInfo._id.$oid,
              },
            })
            .then((resp) => {
              if (!resp.data.norecord) {
                this.averageRating = resp.data.rating;
                this.numberOfRatings = resp.data.num_rating;
              } else {
                this.averageRating = undefined;
                this.numberOfRatings = resp.data.num_rating;
              }
            })
            .catch((err) => {
              console.log(err);
            });
          axios
            .get("/rating/query", {
              params: {
                paper_id: this.paperInfo._id.$oid,
                user_id: this.userId,
              },
            })
            .then((resp) => {
              if ("rating" in resp.data) {
                this.myRating = resp.data.rating;
              } else {
                this.myRating = undefined;
              }
            })
            .catch((err) => {
              console.log(err);
            });
        }
      },
    },
  },
  methods: {
    updateRating(event) {
      this.myRating = event;
      if (event == 0) {
        return;
      }
      axios
        .post("/rating/update", {
          paper_id: this.paperInfo._id.$oid,
          user_id: this.userId,
          rating: event,
        })
        .then((resp) => {
          this.averageRating = resp.data.rating;
          this.numberOfRatings = resp.data.num_rating;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
@use "@/assets/css/global";

.paper-rating {
  @include global.card-style;
}

.rating-grid {
  display: grid;
  grid-template-columns: 35% 38% 32%;
  grid-auto-rows: 50px;
  font-size: 18px;
  .title {
    margin: auto 0px auto auto;
  }
  .label {
    padding-top: 3px;
    margin: auto auto auto 0px;
  }
  span {
    vertical-align: middle;
  }
  .el-rate {
    margin-top: auto;
    margin-bottom: auto;
    // transform: scale(1.4);
  }
}

.stat-container {
  margin-top: 15px 10px 10px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 50px;
  .stat-item {
    margin: auto auto;
    i {
      font-size: 20px;
      vertical-align: middle;
      display: inline-block;
    }
    span {
      margin: auto 10px auto;
      vertical-align: middle;
      font-size: 20px;
    }
  }
}

.block-header {
  @include global.block-header-style;
  .note-stat {
    position: absolute;
    left: 10px;
  }
}
</style>
