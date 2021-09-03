<template>
  <div class="login-component">
    <div class="login-panel-background" @click="$emit('dismiss')"></div>
    <div class="login-panel">
      <div class="login-panel-item">Email:</div>
      <el-input
        class="login-panel-item login-input"
        v-model="email"
        placeholder="email"
        type="email"
      ></el-input>
      <div class="login-panel-item">Password:</div>
      <el-input
        class="login-panel-item login-input"
        placeholder="password"
        v-model="password"
        show-password
      ></el-input>
      <div class="login-panel-item" v-if="signMode == 'signUp'">Username:</div>
      <el-input
        v-if="signMode == 'signUp'"
        class="login-panel-item login-input"
        placeholder="username"
        v-model="username"
      ></el-input>
      <div
        class="login-message"
        :class="{
          shaking: messageShaking,
          'transparent-div': loginMessage == '',
          'login-message--succeed': loginSucceed,
        }"
      >
        {{ loginMessage }}
      </div>
      <div class="login-button-container">
        <el-button class="login-button" type="primary" @click="sign">{{
          signMode == "signIn" ? "Sign In" : "Sign Up"
        }}</el-button>
      </div>
    </div>
  </div>
</template>

<script>
function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

function validateUsername(username) {
  const re = /[A-Za-z0-9._]+/;
  return re.test(username);
}

export default {
  props: {
    signMode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      email: "",
      password: "",
      loginMessage: "",
      username: "",
      messageShaking: false,
      loginSucceed: false,
    };
  },
  emits: ["dismiss"],
  watch: {
    loginMessage: function(val) {
      if (val != "") {
        this.shaking();
      }
    },
  },
  methods: {
    shaking() {
      this.messageShaking = true;
      setTimeout(() => {
        this.messageShaking = false;
      }, 1000);
    },
    formCheck() {
      if (!validateEmail(this.email)) {
        this.loginMessage = "Invalid email address.";
      } else if (this.password == "") {
        this.loginMessage = "Please enter the password.";
      } else if (
        this.signMode == "signUp" &&
        !validateUsername(this.username)
      ) {
        this.loginMessage =
          "Username can only consist of alphabetas, numbers, '.' and '_'.";
      } else {
        this.loginMessage = "";
        return true;
      }
      return false;
    },
    sign() {
      if (this.formCheck()) {
        let load = { email: this.email, passwd: this.password };
        if (this.signMode == "signUp") {
          load["username"] = this.username;
        }
        this.$store
          .dispatch(
            this.signMode == "signIn" ? "account/signIn" : "account/signUp",
            load
          )
          .then((resp) => {
            this.loginMessage = `Succeed`;
            this.loginSucceed = true;
            setTimeout(() => {
              this.loginSucceed = false;
              this.$emit("dismiss");
              this.$router.go();
              // console.log(this.$store.getters["account/isLoggedIn"]);
            }, 1000);
          })
          .catch((err) => {
            if (err == null) {
              this.loginMessage = "Network error, please retry";
              this.shaking();
            } else {
              this.loginMessage = err.message;
              this.shaking();
            }
          });
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.login-panel-background {
  position: fixed;
  top: 0px;
  left: 0px;
  height: 100vh;
  width: 100vw;
  background-color: rgba(0, 0, 0, 0.3);
}

.login-panel {
  font-size: 18px;
  padding: 30px 70px 10px;
  width: 40vw;
  top: 30vh;
  left: 30vw;
  position: fixed;
  border-radius: 10px;
  border: var(--main-border-color) solid 0.5px;
  box-shadow: 0 0 5px 0 var(--main-border-color);
  background-image: url("~@/assets/header-pattern.png");
  display: grid;
  grid-template-columns: 20% 80%;
  grid-auto-rows: 80px;
  box-sizing: border-box;
  .login-message {
    font-size: 16px;
    grid-column: 1 / 3;
    color: var(--red);
    text-align: left;
    margin: 10px 0px;
    padding: 0px;
  }
  .login-message--succeed {
    color: var(--success);
  }
  .transparent-div {
    opacity: 1;
  }
  .shaking {
    animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    transform: translate3d(0, 0, 0);
  }

  .login-panel-item {
    margin: auto 0px;
    text-align: left;
    font-family: var(--font-family-sans-serif);
  }
  .login-input {
    margin-right: 50px;
    font-size: 18px;
    padding: auto;
  }
  .login-button-container {
    grid-column-start: 1;
    grid-column-end: 3;
    display: flex;
    justify-content: space-evenly;
    margin-top: 0px;
    margin-bottom: 30px;
    .login-button {
      border-radius: 5px;
      border: var(--main-border-color) solid 0.5px;
      box-shadow: 0 0 14px 0 var(--main-border-color);
      height: 60px;
      width: 110px;
      font-size: 15px;
    }
  }
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }
  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }
  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }
  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>
