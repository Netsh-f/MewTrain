<template>
    <fornav msg1=信息管理 msg2=主页 msg3=个人信息 msg4=信息查询 msg5=设置
        href1=#/xxgl1 href2="#/xxgl2" href3=#/xxgl3 href4=#/xxgl4 href5=#/ ></fornav>
    <h1>主页内容</h1>
    <hr>
</template>

<script>
import fornav from './fornav.vue';

export default {
    name: "My_xxgl_home",
    components: {
        fornav,
    }
}
</script>