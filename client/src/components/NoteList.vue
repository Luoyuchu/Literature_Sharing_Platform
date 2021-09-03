<template>
  <div class="note-list" :v-loading="loading">
    <div class="note-list-header"></div>
    <div v-if="isLoggedIn" class="block-header">My note:</div>
    <div v-if="isLoggedIn" class="block-list owner-list">
      <NoteItem
        :type="'_id' in myNote ? 'item' : 'empty'"
        v-model:noteInfo="myNote"
        :editable="true"
        @createNote="onCreateNote"
        @closeAndUpdate="renewMyNote"
      />
    </div>
    <div class="block-header">
      <span>Shared notes:</span
      ><span class="note-stat"
        ><b>{{ noteNumber }}</b> Public Notes</span
      >
    </div>
    <div class="block-list guest-list">
      <NoteItem
        v-for="noteEntry in noteList"
        :key="getNoteId(noteEntry)"
        :noteInfo="noteEntry"
        :type="'item'"
        :editable="false"
      />
    </div>
  </div>
</template>

<script>
import NoteItem from "@/components/NoteItem.vue";
import axios from "axios";
import { mapGetters } from "vuex";
export default {
  props: {
    paperInfo: {
      type: Object,
      required: true,
    },
  },
  components: {
    NoteItem,
  },
  watch: {
    paperInfo: {
      handler: function(val, oldval) {
        if (!("_id" in val)) {
          this.noteList = {};
          this.mynote = {};
        } else {
          axios
            .get("/note/query", {
              params: { paper_id: val._id.$oid },
            })
            .then((resp) => {
              let otherNote = [];
              let userNote = {};
              for (let i = 0; i < resp.data.length; ++i) {
                console.log(resp.data[i].user_id, this.userId);
                if (resp.data[i].user_id !== this.userId) {
                  otherNote.push(resp.data[i]);
                } else {
                  userNote = resp.data[i];
                }
              }
              this.myNote = userNote;
              this.noteList = otherNote;
              console.log(this.noteList);
            })
            .catch((err) => {});
        }
      },
      immediate: true,
      deep: false,
    },
  },
  data() {
    return {
      loading: true,
      myNote: {},
      noteList: [],
    };
  },
  computed: {
    noteNumber() {
      return this.noteList.length;
    },
    ...mapGetters("account", ["isLoggedIn", "userId"]),
  },
  methods: {
    renewMyNote() {
      axios
        .get("note/query", {
          params: {
            user_id: this.userId,
            paper_id: this.paperInfo._id.$oid,
          },
        })
        .then((resp) => {
          this.myNote = resp.data[0];
          console.log(this.myNote);
        })
        .catch((err) => {});
    },
    getNoteId(noteEntry) {
      return noteEntry._id.$oid;
    },
    onCreateNote() {
      axios
        .post("note/create", {
          user_id: this.userId,
          paper_id: this.paperInfo._id.$oid,
        })
        .then((resp) => {
          this.myNote = resp.data;
        })
        .catch((err) => {});
    },
  },
};
</script>

<style lang="scss" scoped>
@use "@/assets/css/global";
.block-list {
  background-color: rgba(255, 255, 255, 0.7);
  border: var(--main-border-color) solid 0.5px;
  box-shadow: 0 0 14px 0 var(--main-border-color);
  border-radius: 5px;
  overflow: auto;
  max-height: 300px;
  position: relative;
  &.guest-list {
    min-height: 200px;
  }
  &:after {
    content: "";
    position: absolute;
    bottom: 0px;
    left: 0px;
    right: 0px;
    height: 10px;
    background-color: rgba(255, 255, 255, 0.5);
  }
}
.block-header {
  @include global.block-header-style;
  text-align: left;
  .note-stat {
    font-size: 20px;
    position: absolute;
    right: 10px;
    // bottom: 0px;
  }
}
</style>
