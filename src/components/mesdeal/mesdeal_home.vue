<template>
    <fornav msg1=信息管理 msg2=主页 msg3=个人信息 msg4=信息查询 msg5=设置
    href1=#/mesdeal1 href2=#/mesdeal2 href3=#/mesdeal3 href4=#/mesdeal4 href5=#/ ></fornav>
    <h1 id="welcome">MewTrain欢迎您,尊敬的管理员大人！</h1>
    <hr>
    <div class="table1">
        <div class="block text-center">
            <span class="demonstration"></span>
            <el-carousel height="650px">
            <el-carousel-item v-for="item in imgwrap" :key="item.url">
                <el-image :src="item.url" close-on-press-escape="false">img1</el-image>
            </el-carousel-item>
            </el-carousel>
        </div>
    </div>
</template>

<script>
import fornav from './fornav.vue';
export default {
    name: "My_mesdeal_home",
    data(){
        return{
            imgwrap:[
                {url:require('../../assets/imgs/5.jpg')},
                {url:require('../../assets/imgs/6.jpg')},
                {url:require('../../assets/imgs/7.jpg')},
                {url:require('../../assets/imgs/8.jpg')},
            ]
        }
    },
    components: {
        fornav,
    },
    methods: {
    },
}
</script>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
}

.el-carousel__item:nth-child(2n + 1) {
}
.table1{
    padding: 0 0.5rem 0 6.75rem;
    text-align: center;
}

.demo-image .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>