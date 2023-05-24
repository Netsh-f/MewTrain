<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <el-container class="home-container">
      <!--  头部 -->
      <el-header>
        <div>
          <img src="" alt="">
          <span>MewTrain MewTrain MewTrain MewTrain </span>
        </div>
        <el-button class="LogoutButton" type="info" @click="logout">退出</el-button>
      </el-header>
      <!-- 页面主体 -->
      <el-container>
        <!-- 左侧导航 或许可以考虑实现伸缩 -->
        <el-aside width="200px">
        <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
        router="true"
      >
        <el-menu-item index="page1">
          <template #title>
            <el-icon><location /></el-icon>
            <span>首页</span>
          </template> 
        </el-menu-item>
        <el-menu-item index="TicketInquiry">
          <el-icon><document /></el-icon>
          <span>列车信息查询</span>
        </el-menu-item>
        <el-menu-item index="TicketOrder">
          <el-icon><setting /></el-icon>
          <span>购票界面</span>
        </el-menu-item>
        <el-menu-item index="page3">
          <el-icon><document /></el-icon>
          <span>Navigator Three</span>
        </el-menu-item>
      </el-menu>
        </el-aside>
        <!-- 右侧内容主体 -->
        <el-main>
          <!-- 路由占位 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
</template>
<script>
export default{
  methods:{
    logout(){
        window.sessionStorage.clear()
        this.$router.push('/Login')
    }
  }
}
</script>
<style lang="less" scoped>
  .el-menu-vertical-demo {
    background-color: white;
    color: white;
  }
  .home-container{
  height: 100%;
}
  .LogoutButton{
  align-items: center;
}
  .el-header{
    color: #ffff;
    align-items: right;
    padding-left: 0;
    display: flex;
    justify-content: space-between;
    width: 100;
    background-color: #373d41;
    font-size: 20px;
    > div{
      display: flex;
      align-items: center;
      span{
        margin-left :15px ;
      }
    }
    
  }
  
  .el-aside {
    background-color: #333744;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #EAEDF1;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  

</style>