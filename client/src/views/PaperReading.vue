<template>
  <div class="paper-reading">
    <HeadBar />
    <div class="paper-reading-main">
      <!-- <iframe class="paper-display" :src="paperUrl"> </iframe> -->
      <div
        v-loading="annotationReloading"
        id="adobe-dc-view"
        class="paper-display"
      ></div>
      <div class="sidebar">
        <PaperRating v-loading="!paperInfoReady" :paper-info="paperInfo" />
        <NoteList v-loading="!paperInfoReady" :paper-info="paperInfo" />
        <PaperToolbar v-model:annotationMode="annotationMode" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";
import HeadBar from "../components/HeadBar.vue";
import NoteList from "@/components/NoteList.vue";
import PaperRating from "@/components/PaperRating.vue";
import PaperToolbar from "@/components/PaperToolbar.vue";
export default {
  props: {
    filename: {
      type: String,
      required: true,
    },
  },
  components: {
    HeadBar,
    NoteList,
    PaperRating,
    PaperToolbar,
  },
  computed: {
    ...mapGetters("account", ["isLoggedIn", "userId", "userName"]),
    paperUrl() {
      return (
        axios.defaults.baseURL +
        `/paper/resources/paper?filename=${this.filename}`
      );
    },
    paperId() {
      return "_id" in this.paperInfo ? this.paperInfo._id.$oid : undefined;
    },
  },
  watch: {
    annotationMode: {
      handler: function(val, oldval) {
        // console.log(val);
        this.annotationReloading = true;
        this.reloadAnnotation();
      },
    },
  },
  data() {
    return {
      paperInfo: {},
      paperInfoReady: false,
      paperBlob: undefined,
      annotationMode: true, // true for personal, false for public
      annotationReloading: true,
      annotationUploading: false,
      annotationPlan: false,
      annotationUploadRetry: 0,
    };
  },
  methods: {
    initializeViewer() {
      this.adobeDCView = new window.AdobeDC.View({
        clientId: "314e5ed80b724eb8879ac18afef7caa3", //local
        divId: "adobe-dc-view",
      });
      this.registerUser();
      this.previewFilePromise = this.adobeDCView.previewFile(
        {
          content: {
            promise: this.paperBlob.arrayBuffer(),
          },
          metaData: {
            fileName: this.paperInfo.filename + ".pdf",
            id: this.paperId,
          },
          // content: {
          //   location: {
          //     url:
          //       "https://documentcloud.adobe.com/view-sdk-demo/PDFs/Bodea Brochure.pdf",
          //   },
          // },
          // metaData: {
          //   fileName: "Bodea Brochure.pdf",
          //   id: "77c6fa5d-6d74-4104-8349-657c8411a834",
          // },
        },
        {
          enableAnnotationAPIs: true,
        }
      );
      this.previewFilePromise.then((adobeViewer) => {
        adobeViewer.getAnnotationManager().then((annotationManager) => {
          this.annotationManager = annotationManager;
          this.downloadAnnnotation()
            .then(() => {
              this.reloadAnnotation();
            })
            .then(() => {
              this.registerAnnotationListener();
              // setInterval(() => this.uploadAnnotation(), 10000);
            });
        });
      });
    },
    registerAnnotationListener() {
      const eventOptions = {
        listenOn: [
          "ANNOTATION_ADDED",
          "ANNOTATION_UPDATED",
          "ANNOTATION_DELETED",
        ],
      };
      this.annotationManager.registerEventListener((event) => {
        this.onAnnotationEvent(event);
      }, eventOptions);
    },
    deleteAnnotation() {
      return new Promise((resolve, reject) => {
        this.annotationManager
          .deleteAnnotations()
          .then(() => {
            console.log("annotation cleaned!");
            resolve();
          })
          .catch((err) => {
            console.log(err);
            if (err.message === "Annotation not found for given filter") {
              resolve();
            } else {
              reject(err);
            }
          });
      });
    },
    reloadAnnotation() {
      return new Promise((resolve, reject) => {
        this.annotationReloading = true;
        let toAddAnnotation = [];
        let commentingChecker = (entry) => {
          if (
            entry.update === "deleted" ||
            (this.annotationMode && entry.content.creator.id !== this.userId)
          ) {
            return false;
          }
          return true;
        };
        for (let i in this.annotationTable) {
          let entry = this.annotationTable[i];
          if (entry.content.motivation == "commenting") {
            if (commentingChecker(entry)) {
              toAddAnnotation.push(entry.content);
            }
          } else {
            if (entry.content.target.source in this.annotationTable) {
              let parent = this.annotationTable[entry.content.target.source];
              if (commentingChecker(parent)) {
                toAddAnnotation.push(entry.content);
              }
            }
          }
        }
        toAddAnnotation = toAddAnnotation.sort((a, b) =>
          new Date(a.created) < new Date(b.created) ? -1 : 1
        );
        this.deleteAnnotation().then(() => {
          this.annotationManager
            .addAnnotations(toAddAnnotation)
            .then(() => {
              console.log("reload annotation success");
              this.annotationReloading = false;
              resolve();
            })
            .catch((err) => {
              console.log(err);
              if (
                err.message ===
                "Invalid value of Annotations: should be a non empty array"
              ) {
                this.annotationReloading = false;
                resolve();
              } else {
                reject(err);
              }
            });
        });
      });
    },
    downloadAnnnotation() {
      return new Promise((resolve, reject) => {
        axios
          .get("/annotation/query", {
            params: { paper_id: this.paperId },
          })
          .then((resp) => {
            for (let i = 0; i < resp.data.length; ++i) {
              this.annotationTable[resp.data[i].uid] = resp.data[i];
            }
            for (let i in this.annotationTable) {
              let entry = this.annotationTable[i];
              if (
                entry.content.motivation === "replying" &&
                !(entry.content.target.source in this.annotationTable)
              ) {
                entry.update = "deleted";
              }
            }
            resolve();
          })
          .catch((err) => {
            console.log(err);
            reject(err);
          });
      });
    },
    registerUser() {
      const profile = {
        userProfile: {
          name: this.userName,
          email: this.userId,
        },
      };

      this.adobeDCView.registerCallback(
        window.AdobeDC.View.Enum.CallbackType.GET_USER_PROFILE_API,
        function() {
          return new Promise((resolve, reject) => {
            resolve({
              code: window.AdobeDC.View.Enum.ApiResponseCode.SUCCESS,
              data: profile,
            });
          });
        },
        {}
      );
    },
    onAnnotationEvent(event) {
      if (this.annotationReloading) {
        return;
      }
      console.log(event.type, event.data);
      let entry = event.data;
      let eid = entry.id;
      if (this.userId !== entry.creator.id) {
        return;
      }
      if (event.type == "ANNOTATION_ADDED") {
        this.annotationTable[eid] = {
          user_id: this.userId,
          paper_id: this.paperId,
          uid: eid,
          content: entry,
          update: "added",
        };
      } else if (event.type == "ANNOTATION_UPDATED") {
        this.annotationTable[eid].content = entry;
        this.annotationTable[eid].update = "updated";
      } else if (event.type == "ANNOTATION_DELETED") {
        this.annotationTable[eid].update = "deleted";
      }
      if (this.isLoggedIn) {
        this.planUpload();
      }
    },
    uploadAnnotation() {
      let payload = { added: [], updated: [], deleted: [] };
      for (let i in this.annotationTable) {
        let entry = this.annotationTable[i];
        if (entry.user_id == this.userId) {
          if ((entry.update || "") == "added") {
            entry.update = "";
            payload.added.push(entry);
          } else if ((entry.update || "") == "updated") {
            entry.update = "";
            payload.updated.push(entry);
          } else if ((entry.update || "") == "deleted") {
            payload.deleted.push(entry);
            delete this.annotationTable[i];
          }
        }
      }
      axios
        .post("/annotation/update", payload)
        .then((resp) => {
          if (this.annotationPlan) {
            setTimeout(() => {
              this.annotationPlan = false;
              this.uploadAnnotation();
            }, 5000);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    planUpload() {
      if (this.annotationUploading) {
        this.annotationPlan = true;
      } else {
        this.uploadAnnotation();
      }
    },
  },
  mounted() {
    this.adobeDCView = null;
    this.previewFilePromise = null;
    this.annotationManager = null;
    this.annotationTable = {};
    axios
      .get("/paper/paperinfo", { params: { filename: this.filename } })
      .then((resp) => {
        this.paperInfo = resp.data;
        this.paperInfoReady = true;
        console.log(this.paperInfo);
      })
      .catch((err) => {});
    //
    console.log("adobe ready!!!");
    axios
      .get("/paper/resources/paper", {
        params: { filename: this.filename },
        responseType: "blob",
      })
      .then((resp) => {
        this.paperBlob = resp.data;
        this.initializeViewer();
      });
  },
};
</script>

<style lang="scss" scoped>
@use '@/assets/css/global';

.paper-reading {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  .paper-reading-main {
    width: 100%;
    display: flex;
    flex: 1 1 0;
    overflow: auto;

    .paper-display {
      flex: 1 1 0;
    }

    .sidebar {
      flex: 0 0 20%;
      display: flex;
      flex-direction: column;
      justify-content: stretch;
      align-items: stretch;
    }
  }
}
</style>
