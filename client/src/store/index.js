import { createStore } from "vuex";
import { backendBaseUrl } from "@/config";
import axios from "axios";

export default createStore({
  modules: {
    account: {
      namespaced: true,
      state: {
        token: localStorage.getItem("loginToken") || "",
        user: JSON.parse(localStorage.getItem("loginUser") || "{}"),
        status: localStorage.getItem("loginStatus") || "",
      },
      mutations: {
        auth_success(state, { token, user }) {
          state.token = token;
          state.user = user;
          localStorage.setItem("loginToken", token);
          localStorage.setItem("loginUser", JSON.stringify(user));
        },
        auth_status(state, { status }) {
          state.status = status;
          localStorage.setItem("loginStatus", status);
        },
        auth_logout(state) {
          state.token = "";
          state.user = {};
          localStorage.removeItem("loginToken");
          localStorage.removeItem("loginUser");
        },
      },
      actions: {
        signIn({ state, commit }, user) {
          return new Promise((resolve, reject) => {
            axios
              .post("auth/login", user)
              .then((resp) => {
                const token = resp.data.token;
                const user = resp.data.user;
                axios.defaults.headers.common["Authorization"] =
                  "Bearer " + token;
                commit("auth_success", { token, user });
                commit("auth_status", { status: "login" });
                resolve(resp);
              })
              .catch((err) => {
                if (err.response) {
                  reject(err.response.data);
                } else {
                  console.log("login post error");
                  reject(null);
                }
              });
          });
        },
        signUp(context, user) {
          return new Promise((resolve, reject) => {
            axios
              .post("auth/signup", user)
              .then((resp) => {
                resolve(resp);
              })
              .catch((err) => {
                if (err.response) {
                  reject(err.response.data);
                } else {
                  console.log("login post error");
                  reject(null);
                }
              });
          });
        },
        logout({ commit }) {
          delete axios.defaults.headers.common["Authorization"];
          commit("auth_logout");
          commit("auth_status", { status: "" });
        },
      },
      getters: {
        isLoggedIn: (state) => state.status == "login",
        user: (state) => state.user,
        userId: (state) =>
          state.status == "login" ? state.user["_id"]["$oid"] : null,
        userName: (state) =>
          state.status == "login" ? state.user["username"] : null,
        userEmail: (state) =>
          state.status == "login" ? state.user["email"] : null,
      },
    },
  },
  state: {},
  mutations: {},
  actions: {},
});
