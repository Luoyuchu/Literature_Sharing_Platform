<template>
  <VueModelWindow
    :width="+900"
    :height="+400"
    title="note editor"
    @dismiss="onDimiss"
    ><div class="note-editor">
      <div v-if="editable" class="note-toolbar">
        <el-switch
          class="button"
          v-model="sharing"
          active-text="Public"
          inactive-text="Private"
        >
        </el-switch>
        <div v-if="status == 'autosaving'" class="status autosaving">
          <span>Autosaving</span>
          <el-icon class="is-loading">
            <loading />
          </el-icon>
        </div>
        <div v-if="status == 'success'" class="status success">
          <span>Autosaving succeed.</span>
        </div>
        <div v-if="status == 'fail'" class="status fail">
          <span>Failed! Retrying.</span>
          <el-icon class="is-loading">
            <loading />
          </el-icon>
        </div>
      </div>
      <div class="tui-editor" ref="editor"></div></div
  ></VueModelWindow>
</template>

<script>
import VueModelWindow from "@/components/lib/VueModalWindow.vue";
import Editor from "@toast-ui/editor";
import axios from "axios";
export default {
  components: {
    VueModelWindow,
  },
  emits: ["update:opened"],
  props: {
    editable: {
      type: Boolean,
      required: true,
    },
    noteInfo: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editor: undefined,
      sharing: true,
      status: "",
      retryCnt: 0,
      savingPlan: false,
      saving: false,
      closing: false,
    };
  },
  watch: {
    sharing: {
      handler: function() {
        this.planSave();
      },
    },
  },
  methods: {
    onDimiss() {
      console.log("on dismiss");
      if (this.saving) {
        this.closing = true;
      } else {
        this.$emit("update:opened", false);
      }
    },
    planSave() {
      this.savingPlan = true;
      if (!this.saving) {
        this.savingPlan = false;
        this.autoSave();
      }
    },
    autoSave() {
      this.status = "saving";
      this.saving = true;
      axios
        .post("/note/update", {
          content: this.editor.getMarkdown(),
          _id: this.noteInfo._id ? this.noteInfo._id.$oid : "",
          public: this.sharing,
        })
        .then((resp) => {
          this.retryCnt = 0;
          this.status = "success";
          setTimeout(() => {
            this.status = "";
          }, 2000);
          if (this.savingPlan) {
            this.savingPlan = false;
            this.autoSave();
          } else {
            this.saving = false;
            if (this.closing) {
              this.$emit("update:opened", false);
            }
          }
        })
        .catch((err) => {
          this.retryCnt += 1;
          if (this.retryCnt >= 3) {
            this.$notify({
              title: "Note autosaving failed",
              message:
                "Can not upload your note to server temporarily. Please save it locally now!",
              type: "warning",
            });
          } else {
            this.status = "fail";
            setTimeout(() => {
              this.status = "";
            }, 2000);
            this.planSave();
          }
        });
    },
  },
  mounted() {
    let editorConfig = {
      el: this.$refs.editor,
      initialEditType: "markdown",
      toolbarItems: [
        ["heading", "bold", "italic", "strike"],
        ["hr", "quote"],
        ["ul", "ol", "task", "indent", "outdent"],
        ["table", "link"],
        ["code", "codeblock"],
      ],
      previewStyle: "vertical",
      initialValue: this.noteInfo.content,
    };
    if (!this.editable) {
      editorConfig.viewer = true;
    }
    this.editor = Editor.factory(editorConfig);
    this.editor.addHook("change", () => {
      this.planSave();
    });
    this.sharing = this.noteInfo.public;
    // setInterval(() => {
    //   this.autoSave();
    // }, 2000);
  },
};
</script>

<style lang="scss" scoped>
.note-editor {
  cursor: auto;
  height: 100%;
  position: relative;
  .note-toolbar {
    display: flex;
    align-items: center;
    .button {
      margin: 5px 20px 5px;
    }
    .status {
      font-size: 15px;
      height: min-content;
      margin-right: 15px;
      margin-left: auto;
      .el-icon {
        font-size: 15px;
      }
    }
    .autosaving,
    .success {
      color: var(--green);
    }
    .fail {
      color: var(--danger);
    }
  }
  .tui-editor {
    text-align: left;
  }
  .tui-editor::v-deep {
    .toastui-editor-contents {
      h1 {
        border-bottom: 3px solid #999;
      }
    }
  }
}

.el-notification {
  position: absolute;
}
</style>
