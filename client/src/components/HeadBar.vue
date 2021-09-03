<template>
  <div class="head-bar">
    <img class="logo" src="@/assets/lab_logo.svg" />
    <div class="tags">
      <div class="tag" @click="$router.push('/')"><span>Home</span></div>
      <div class="tag" @click="$router.push('/')"><span>PaperList</span></div>
      <div class="tag" @click="$router.push('/About')"><span>About</span></div>
    </div>
    <div class="user-name">
      <el-dropdown
        v-if="isLoggedIn"
        split-button
        type="primary"
        class="user-panel userinfo"
        trigger="click"
      >
        {{ userName }}
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item disabled
              ><div class="label" style="font-size: 20px; margin: auto 10px;">
                <p style="margin-bottom: 0px; color: black;">
                  {{ userName }}
                </p>
                <p style="font-size: 15px; padding-top: 0px; margin-top: 0px">
                  {{ userEmail }}
                </p>
              </div></el-dropdown-item
            >
            <el-dropdown-item divided disabled
              ><div class="label" style="font-size: 20px; margin: auto 10px;">
                Profile
              </div></el-dropdown-item
            >
            <el-dropdown-item divided disabled
              ><div class="label" style="font-size: 20px; margin: auto 10px;">
                Setting
              </div></el-dropdown-item
            >
            <el-dropdown-item divided @click="logout">
              <div class="label" style="font-size: 20px; margin: auto 10px;">
                Logout
              </div>
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-button
        v-if="!isLoggedIn"
        class="user-panel login"
        @click="signMode = 'signIn'"
        type="primary"
      >
        Sign In
      </el-button>
      <el-button
        v-if="!isLoggedIn"
        class="user-panel login"
        @click="signMode = 'signUp'"
        type="primary"
      >
        Sign Up
      </el-button>
      <transition name="fade">
        <Login
          :signMode="signMode"
          v-if="signMode != ''"
          @dismiss="signMode = ''"
        />
      </transition>
    </div>
  </div>
</template>

<script>
import Login from "@/components/Login.vue";
import { mapGetters } from "vuex";
export default {
  components: {
    Login,
  },
  data() {
    return {
      signMode: "",
    };
  },
  computed: {
    ...mapGetters("account", [
      "isLoggedIn",
      "user",
      "userId",
      "userEmail",
      "userName",
    ]),
  },
  methods: {
    logout() {
      this.$store.dispatch("account/logout");
      this.$router.go();
    },
  },
  mounted() {},
};
</script>

<style lang="scss" scoped>
.head-bar {
  width: 100%;
  height: 8vh;
  position: relative;
  display: flex;
  background-image: url("~@/assets/header-pattern.png");
  z-index: 2;
  .tags {
    font-family: sans-serif;
    font-weight: 600;
    display: flex;
    margin-left: 50px;
    margin-top: 20px;
    .tag {
      font-size: 18px;
      margin: auto 30px;
      cursor: pointer;
      &:hover {
        color: var(--red);
      }
      span {
        padding: 2px 0px 2px;
        border-top: solid black 1px;
        border-bottom: solid black 1px;
      }
    }
  }
}

.logo {
  margin-top: auto;
  margin-bottom: auto;
  margin-left: 15px;
  height: 50%;
}

.user-name {
  font-family: var(--font-family-sans-serif);
  margin-left: auto;
  margin-right: 50px;
  margin-top: auto;
  margin-bottom: auto;
  .user-panel {
    margin: auto 5px;
  }
}

.user-name::v-deep {
  .el-button {
    font-size: 18px;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
