<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="hcontainer">
        <el-carousel height="500px" class="optimized-carousel">
            <el-carousel-item v-for="item in imgwrap" :key="item.url">
                <el-image :src="item.url" close-on-press-escape="false">img1</el-image>
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script setup>
const imgwrap = [
    { url: require('../assets/imgs/ChangSha1.jpg') },
    { url: require('../assets/imgs/TheGreatWall1.jpg') },
    { url: require('../assets/imgs/HongKong2.jpg') },
    { url: require('../assets/imgs/HongKong1.jpg') },
];
</script>

<style scoped>
.hcontainer{
    width: 1000px;
}
</style>