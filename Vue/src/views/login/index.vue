<template>
  <div class="login-container">
    <div class="login-group">
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container">
          <h1 class="title">LOGIN</h1>
        </div>

        <el-form-item prop="username" size="mini">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="Username"
            name="username"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <el-form-item prop="password" size="mini">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="Password"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon
              :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"
            />
          </span>
        </el-form-item>

        <el-button
          :loading="loading"
          type="info"
          plain
          style="width:100%;margin-bottom:30px;color:#000"
          @click.native.prevent="handleLogin"
          >Login</el-button
        >
      </el-form>
      <div class="logo-info">
        <div class="logo">
          <img src="@/static/images/avatar.jpg" alt="logo">
          <span>DSOC Smart Workplace</span>
        </div>
        <div class="info">
          @2020 All Rights Reserved.Privacy and Teems<br/>
          Smart Workplace Platform. Smart and self-serviced experience
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import { validUsername } from "@/utils/validate";

export default {
  name: "Login",
  data() {
    const validateUsername = (rule, value, callback) => {
      // if (!validUsername(value)) {
      if (value.length < 4) {
        callback(new Error("Please enter the correct user name"));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error("The password can not be less than 6 digits"));
      } else {
        callback();
      }
    };
    return {
      loginForm: {
        username: "admin",
        password: "Macroview292"
      },
      loginRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ]
      },
      loading: false,
      passwordType: "password",
      redirect: undefined
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true;
          this.$store
            .dispatch("user/login", this.loginForm)
            .then(() => {
              this.$router.push({ path: this.redirect || "/" });
              this.loading = false;
            })
            .catch(() => {
              this.loading = false;
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    }
  }
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: rgb(141, 149, 158);
$light_gray: #73879c;
$cursor: #73879c;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 25px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 35px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgb(211, 211, 211);
    box-shadow: 0 1px 0 #fff,0 -1px 4px rgba(0,0,0,.08) inset;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #f7f7f7;
$dark_gray: #889aa4;
$light_gray: #73879c;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  .login-group {
    max-width: 350px;
    min-width: 280px;
    margin: 5% auto 0;
    .login-form {
      // position: relative;
      max-width: 100%;
      padding: 35px 0px 0;
      overflow: hidden;
      border-bottom: 1px solid rgb(211, 211, 211);
    }
    .logo-info {
      text-align: center;
      margin-top: 30px;
      box-sizing: border-box;
      .logo {
        img {
          width: 45px;
          height: 45px;
          vertical-align: bottom;
        }
        span {
          line-height: 45px;
          color: $light_gray;
          font-size: 26px;
          font-weight: 400;
          letter-spacing: -0.09em;
          margin-left:15px;
        }
      }
      .info {
        color: $light_gray;
        font-size: 12px;
        margin-top:15px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      font-weight: 400;
      letter-spacing: -0.05em;
      margin: 0px auto 40px auto;
      text-align: center;
    }
    .title::before,
    .title::after {
      position: absolute;
      top: 16px;
      height: 1px;
      width: 20%;
      content: "";
      background-color: #7e7e7e;
    }
    .title::before {
      left: 0;
    }
    .title::after {
      right: 0;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
