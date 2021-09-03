import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import installElementPlus from "./plugins/element";
import "@/assets/css/color.scss";
import axios from "axios";
import * as config from "@/config.js";
import "@toast-ui/editor/dist/toastui-editor.css";
import { Plus, Loading, View, Star, Search } from "@element-plus/icons";

axios.defaults.baseURL = config.backendBaseUrl;
if (localStorage.getItem("loginToken")) {
  axios.defaults.headers.common["Authorization"] =
    "Bearer " + localStorage.getItem("loginToken");
}

const app = createApp(App);
installElementPlus(app);
app.component([Plus.name], Plus);
app.component([Loading.name], Loading);
app.component([View.name], View);
app.component([Star.name], Star);
app.component([Search.name], Search);
document.addEventListener("adobe_dc_view_sdk.ready", () => {
  app
    .use(store)
    .use(router)
    .mount("#app");
});
