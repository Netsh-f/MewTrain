<!-- sign_in -->
<template>
    <div class="container b-container" id="b-container">
        <form class="form" id="b-form" method="" action="">
          <h2 class="form_title title">Sign in to Website</h2>
          <div class="form__icons">
            <img class="form__icon" src=" ">
            <img class="form__icon" src=" ">
            <img class="form__icon" src=" ">
          </div>
          <span class="form__span">or use your email account</span>
          <!-- <input class="form__input" type="text" placeholder="用户名" v-model="loginFrom.username">
          <input class="form__input" type="password" placeholder="密码" v-model.lazy="loginFrom.password"> -->
          <el-input class="form__input" type="text" placeholder="用户名" ></el-input>
          <el-input class="form__input" type="password" placeholder="密码" ></el-input>
          <a class="form__link">Forgot your password?</a>
          <button class="form__button button submit">SIGN IN</button>
        </form>
    </div>
    </template>
    <style scoped>
    @import '../../assets/login.css';
    </style>
    <script>
import { onMounted, inject } from 'vue'
import mitt from 'mitt'

export default {
  setup() {
    // 使用 inject 函数获取 appContext 对象
    const appContext = inject('appContext')

    // 获取或创建 emitter 对象
    const emitter = appContext?.config.globalProperties.emitter ?? mitt()

    // 在 onMounted 钩子中使用 emitter
    onMounted(() => {
      emitter.on('change', () => {
        let aContainer = document.querySelector("#a-container");
        aContainer.classList.toggle("is-txl");
      })
    })

    // ... 子组件的逻辑 ...
  }
}
    </script>