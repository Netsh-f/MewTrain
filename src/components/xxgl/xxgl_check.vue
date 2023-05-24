<template>
    <fornav msg1=信息管理 msg2=主页 msg3=个人信息 msg4=信息查询 msg5=设置
        href1=#/xxgl1 href2=#/xxgl2 href3=#/xxgl3 href4=#/xxgl4 href5=#/ ></fornav>
    <h1>查询信息</h1>
    <hr>
    <div style="text-align:center;vertical-align:middel;">
        <el-input class="input1" v-model="state" clearable placeholder="请输入用户id进行查询" float="left">
            <template #append>
                <el-button :icon="Search" type="primary" float="left" @click="open2" >Search</el-button>
            </template>
        </el-input>
    </div>
    <hr>
    <div class="table1">
        <el-table :data="tableData" stripe style="width: 100%" border height="500" :row-style="{height:'20px'}">
            <el-table-column prop="id" label="Id" width="180" />
            <el-table-column prop="username" label="Name" width="180" />
            <el-table-column prop="password" label="password" />
            <el-table-column prop="abstractuser_ptr_id" label="abstractuser_ptr_id" />
            <el-table-column prop="email" label="Email" />
            <el-table-column prop="balance" label="Balance" />
            <el-table-column fixed="right" label="Operations" width="120">
                <template #default>
                  <el-button link type="primary" size="small" @click="open3">编辑</el-button>
                  <el-button link type="primary" size="small" @click="open3">删除</el-button>
                </template>
              </el-table-column>
        </el-table>
    </div>
</template>


<script scoped>
import fornav from './fornav.vue';
import { ElMessage } from 'element-plus'
const tableData = [
    {
              "id": 8,
              "username": "testcase3",
              "password": "",
              "abstractuser_ptr_id": 8,
              "email": "870041158@qq.com",
              "balance": 0.0
          },
          {
              "id": 6,
              "username": "newusername",
              "password": "",
              "abstractuser_ptr_id": 6,
              "email": "new_email@example.com",
              "balance": 0.0
          },
          {
              "id": 5,
              "username": "ElaikonaHost",
              "password": "",
              "abstractuser_ptr_id": 5,
              "email": "21371193@buaa.edu.cn",
              "balance": 0.0
          },
          {
              "id": 4,
              "username": "Elaikona4",
              "password": "",
              "abstractuser_ptr_id": 4,
              "email": "21371193@buaa.edu.cn",
              "balance": 0.0
          },
          {
              "id": 3,
              "username": "Elaikona3",
              "password": "",
              "abstractuser_ptr_id": 3,
              "email": "21371193@buaa.edu.cn",
              "balance": 0.0
          },
          {
              "id": 2,
              "username": "Elaikona2",
              "password": "",
              "abstractuser_ptr_id": 2,
              "email": "21371193@buaa.edu.cn",
              "balance": 0.0
          },
          {
              "id": 1,
              "username": "Elaikona",
              "password": "",
              "abstractuser_ptr_id": 1,
              "email": "new_email@test.com",
              "balance": 0.0
          }
]

const open1 = () => {
  ElMessage('this is a message.')
}
const open2 = () => {
  ElMessage({
    message: 'Congratulation,获取用户列表成功!',
    type: 'success',
  })
}
const open3 = () => {
  ElMessage({
    message: 'Warning, this is a warning message!',
    type: 'warning',
  })
}
const open4 = () => {
  ElMessage.error('Oops,Some error!')
}
const reop = ($rme) => {
    switch ($rme){
        case 1:
            break
        case 2:
            break
        case 3:
            break
        case 4:
            break
    }
}
export default {
    name: "My_xxgl_check",
    data() {
        return {
            tableData,
        }
    },
    props: {},
    methods:{
        reop,
        open1,
        open2,
        open3,
        open4,
    },
    components: {
        fornav,
    }
}
</script>

<style scoped>
.input1{
    padding: 0 2rem 0 6.75rem;
    text-align: center;
}
.table1{
    padding: 0 0.5rem 0 6.75rem;
    text-align: center;
}
</style>