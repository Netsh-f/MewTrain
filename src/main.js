import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index'
import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import mitt from 'mitt'
import './assets/global.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
app.use(store)
const emitter = mitt()
app.config.globalProperties.emitter = emitter
app.provide('appContext', app)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.mount('#app')