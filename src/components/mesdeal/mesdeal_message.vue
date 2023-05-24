<template>
    <h1>个人信息</h1>
    <hr>
    <div class="table1">
        <div class="profile-card">
            <div class="card-header">
                <div class="pic">
                <img src="pic.png" alt="">
                </div>
                <div class="name">{{ AdminName }}</div>
                <div class="desc">System Administrator(Admin)</div>
                <div class="sm"></div>
            </div>
            <div class="card-footer">
                <div class="numbers">
                    <div class="item">
                        <span>已登录</span>状态
                    </div>
                    <div class="border"></div>
                    <div class="item">
                        <span>系统管理员</span>权限
                    </div>
                </div>
            </div>
        </div>
        <el-table :data="tableData" stripe style="width: 100%" border height="633px" :row-style="{height:'20px'}">
            <el-table-column prop="datatype" label="\" width="550" />
            <el-table-column fixed="right" label="Operations" width="550">
                <template #default>
                  <el-button link type="primary" size="small" @click="open3">编辑</el-button>
                  <el-button link type="primary" size="small" @click="open3">删除</el-button>
                </template>
              </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    name: "My_mesdeal_message",
    data(){
        return{
            AdminName:'MewTrain Admin',
        }
    },
}
</script>

<style scoped>
@import '../../assets/css/forMessage.css';
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css';
.table1{
    padding: 0 0.5rem 0 6.75rem;
    text-align: center;
    justify-content:space-between;
    display: flex;
}
.container2{
    padding: 0 0.5rem 0 32.75rem;
}
</style>