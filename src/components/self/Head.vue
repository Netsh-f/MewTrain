##
该组件为Home页右上方头像
##

<template #headPicture>
    <div class="demo-type">
      <div>
        <el-avatar> {{userName.substring(0,3)}} </el-avatar>
      </div>
    </div>
</template>
  
<script>
import axios from 'axios';
    export default {
        name:'Head',
        data(){
            return{
                userName:'aaaa'//此处应为用户名
            } 
        },
        mounted() {
    axios.post('/api/user/get_user_info/', {
      user_id: "4",
    }, {

    })
      .then((response) => {
        //console.log(response.data);
        let data = response.data;
        this.userName=data.username;
      })
      .catch((error) => {
        console.log(error);
        
      });
  }
   }
</script>
  
  <style scoped>
  .demo-type {
    display: flex;
  
  }
  .demo-type > div {
    flex: 1;
    text-align: center;
  }
  
 
  </style>
  