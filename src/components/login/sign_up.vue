<!-- sign_up -->
<template>
  <div class="container a-container" id="a-container">
    <el-form class="form" ref="form" :model="UserRegisterInfo" :rules="rules">
      <h2 class="form_title title">创建您的帐号，我们一起出发！</h2>

      <el-form-item prop="Name">
        <el-input v-model="UserRegisterInfo.Name" type="text" placeholder="用户名"></el-input>
      </el-form-item>
      <el-form-item prop="Email">
        <el-input v-model="UserRegisterInfo.Email" type="text" placeholder="邮箱"></el-input>
      </el-form-item>
      <el-form-item prop="PassWord">
        <el-input v-model="UserRegisterInfo.PassWord" type="password" placeholder="密码"></el-input>
      </el-form-item>
      <el-form-item prop="RePassWord">
        <el-input v-model="UserRegisterInfo.RePassWord" type="password" placeholder="确认密码"></el-input>
      </el-form-item>
      <button class="form__button button submit" type="primary" @click="submitForm" style="margin-top: 10px;">注册</button>
    </el-form>
  </div>
</template>
<script>
import axios from "axios";
import { ref } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus'
import router from "@/router"; // 导入Vue.js路由器
import { useStore } from "vuex";

export default {

  setup() {
    const store = useStore();
    const UserRegisterInfo = ref({
      Name: '',
      Email: '',
      PassWord: '',
      RePassWord: '',
    });

    const form = ref(null);

    const rules = {
      Name: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
      ],
      Email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
      ],
      PassWord: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
      RePassWord: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== UserRegisterInfo.value.PassWord) {
              callback(new Error("两次输入的密码不一致"));
            } else {
              callback();
            }
          },
          trigger: "blur",
        },
      ],
    };

    const submitForm = () => {

      form.value.validate(async (valid) => {
        if (valid) {

          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(UserRegisterInfo.value.Email)) {
            ElMessageBox.alert('邮箱格式有误', '注册失败', {
                  confirmButtonText: '确定',
                  showClose: false
                });
            return;
          }

          axios.post('/api/user/register/', {
            username: UserRegisterInfo.value.Name,
            password: UserRegisterInfo.value.PassWord,
            email: UserRegisterInfo.value.Email
          }).then((response) => {
            console.log(response.data);
            axios.post('/api/user/login/', {
              username: UserRegisterInfo.value.Name,
              password: UserRegisterInfo.value.PassWord,
            }).then((response) => {
              console.log(response);
              const token = response.data.data.token;
              console.log(token)
              store.commit("setToken", token);
              store.commit("setLogin", true)
              router.push({ path: "/WELCOME" });
            })
              .catch((error) => {
                console.log(error);
              });
          })
            .catch((error) => {
              if (error.response.status === 400) {
                ElMessageBox.alert('用户名已存在', '注册失败', {
                  confirmButtonText: '确定',
                  showClose: false
                });
              }
            });
        }
      });
    };

    return { UserRegisterInfo, form, rules, submitForm };
  },
};
</script>

<style scoped>
@import '../../assets/login.css';

.el-input {
  width: 200px;
}
</style>