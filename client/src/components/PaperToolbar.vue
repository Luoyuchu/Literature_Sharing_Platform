<template>
  <div class="paper-toolbar">
    <div class="block-header">Annotations for this paper</div>
    <div class="tools">
      <el-switch
        v-model="annotationMode"
        active-text="Only show mine"
        inactive-text="Show all the annotation"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  emits: ["update:annotationMode"],
  watch: {
    annotationMode: {
      handler: function(val, oldval) {
        this.$emit("update:annotationMode", val);
      },
    },
  },
  data() {
    return {
      annotationMode: true,
    };
  },
};
</script>

<style lang="scss" scoped>
@use "@/assets/css/global";
.tools {
  @include global.card-style;
  margin: 0px auto;
  padding: 10px;
  font-size: 30px;
  .el-switch {
    transform: scale(1.2);
  }
}

.block-header {
  @include global.block-header-style;
}
</style>
