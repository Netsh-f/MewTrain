<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <el-carousel height="650px" class="optimized-carousel">
        <el-carousel-item v-for="item in imgwrap" :key="item.url">
            <el-image :src="item.url" close-on-press-escape="false">img1</el-image>
        </el-carousel-item>
        </el-carousel>
</template>

<script setup>
const imgwrap=[
    {url:require('../assets/imgs/zc1.jpg')},
    {url:require('../assets/imgs/zc2.jpg')},
];
</script>