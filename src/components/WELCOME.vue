<template>
    <div class="hcontainer">
      <el-carousel class="optimized-carousel">
        <el-carousel-item v-for="item in imgwrap" :key="item.url">
          <div class="carousel-image-wrapper">
            <img :src="item.url" class="carousel-image" />
          </div>
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
.hcontainer {
  width: 100%;
  height: 100%;

}

.optimized-carousel {
  height: 100%;
  width: 100%;
}

.carousel-image-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>