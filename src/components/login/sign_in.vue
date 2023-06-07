<template>
  <div class="container b-container" id="b-container">
    <el-form class="form" ref="form" :model="UserLoginInfo" :rules="rules">
      <h4 class="form_title title">请输入账号，共同开启列车旅程吧！</h4>
      <el-form-item prop="Name">
        <el-input v-model="UserLoginInfo.Name" type="text" placeholder="用户名" style="background-color: transparent;"></el-input>
      </el-form-item>
      <el-form-item prop="PassWord">
        <el-input v-model="UserLoginInfo.PassWord" type="password" placeholder="密码"></el-input>
      </el-form-item>
      <el-button class="form__button button submit" type="primary" @click="submitForm">登录</el-button>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from 'vue';
import router from "@/router"; // 导入Vue.js路由器
import { useStore } from "vuex";
import { ElMessageBox,ElMessage } from "element-plus";
export default {
  setup() {
    const store = useStore();
    const UserLoginInfo = ref({
      Name: '',
      PassWord: '',
    });
    const form = ref(null);

    const rules = {
      Name: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
      ],
      PassWord: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
    };
    const check = () => {
      console.log(axios.post('/api/user/login/'))
    }
    const submitForm = () => {

      form.value.validate(async (valid) => {
        if (valid) {
          axios.post('/api/user/login/', {
            username: UserLoginInfo.value.Name,
            password: UserLoginInfo.value.PassWord,
          }, {
            headers: {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
              'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'
            },
          }).then((response) => {
            console.log(response);
            const token = response.data.data.token;
            console.log(token)
            store.commit("setToken", token);
            store.commit("setLogin", true)
            store.commit("setUserID", response.data.data.user_id)
            router.push({ path: "/WELCOME" });
          })
            .catch((error) => {
              ElMessageBox.alert(error.response.data.message, '登陆失败', {
                  confirmButtonText: '确定',
                  showClose:false
                });
              console.log(error);
            });
        }
      });


    };
    return { UserLoginInfo, form, rules, submitForm, check };
  },
};
</script>

<style scoped>
@import '../../assets/login.css';

.el-input {
  width: 200px;
}</style>