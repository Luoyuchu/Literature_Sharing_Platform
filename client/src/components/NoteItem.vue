<template>
  <div class="note-item-wrapper">
    <div
      class="note-item"
      :class="{ empty: short, longer: opened }"
      @click="openEditor"
    >
      <div v-if="short" class="plus-icon-container">
        <el-icon :size="+30" color="black">
          <plus />
        </el-icon>
      </div>
      <div v-if="!short" class="item-text item-name">
        {{ noteInfo.username }}
      </div>
      <div v-if="!short" class="item-text item-update">
        <b>{{ noteInfo.content.length }}</b> words
      </div>
      <div v-if="!short" class="item-text item-length">
        {{ noteUpdateTime }}
      </div>
    </div>
    <NoteEditor
      v-if="opened"
      @update:opened="onCloseEditor($event)"
      :opened="opened"
      :editable="editable"
      :noteInfo="noteInfo"
    />
  </div>
</template>

<script>
import NoteEditor from "@/components/NoteEditor.vue";
export default {
  emits: ["closeAndUpdate", "createNote"],
  data() {
    return {
      opened: false,
    };
  },
  computed: {
    short() {
      return this.type == "empty";
    },
    noteUpdateTime() {
      return new Date(this.noteInfo.time.$date).toLocaleString("en-GB");
    },
  },
  components: {
    NoteEditor,
  },
  methods: {
    onCloseEditor(event) {
      this.opened = event;
      this.$emit("closeAndUpdate");
    },
    openEditor() {
      console.log("clicked");
      if (this.type == "empty") {
        this.$emit("createNote");
      } else {
        this.opened = true;
        this.visible = true;
      }
    },
  },
  props: {
    editable: {
      type: Boolean,
      required: true,
    },
    type: {
      type: String,
      default: "item",
    },
    noteInfo: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@mixin card-style {
  background: #fff;
  border: var(--main-border-color) solid 0.5px;
  box-shadow: 0 0 14px 0 var(--main-border-color);
}

.note-item {
  @include card-style;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  margin-left: 50px;
  margin-right: 0px;
  transition: all 0.5s;
  height: 60px;
  cursor: pointer;
  margin-top: 1px;
  position: relative;
  &.longer {
    margin-left: 20px;
  }
  &.longer:hover {
    margin-left: 10px;
  }
  &:hover {
    margin-left: 20px;
  }
  &:active {
    background-color: rgba(200, 200, 200, 0.5);
  }
  .item-text {
    position: absolute;
  }
  .item-name {
    left: 50px;
    top: 6px;
    font-size: 20px;
  }
  .item-update {
    right: 20px;
    top: 10px;
  }
  .item-length {
    right: 20px;
    bottom: 8px;
  }
  .plus-icon-container {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

.empty {
  margin-left: auto;
  width: 100px;
  &:hover {
    width: 130px;
    margin-left: auto;
    .plus-icon {
      box-shadow: 0px 0px 5px white;
    }
  }
}
</style>
