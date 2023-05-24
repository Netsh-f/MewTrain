import { createRouter, createWebHashHistory } from 'vue-router'


const Home = () => import('../components/Home.vue');
// const TicketInquiry = () => import('../components/TicketInquiry.vue');
const Login = () => import('../components/Login.vue');
const page1 = () => import('../components/page1.vue');
const page2 = () => import('../components/page2.vue');
const page3 = () => import('../components/page3.vue');
const TicketInquiry = () => import('../components/TicketInquiry.vue')
const TicketOrder = () => import('../components/TicketOrder.vue')
const xxgl_home = () => import('../components/xxgl/xxgl_home.vue')
const xxgl_check = () => import('../components/xxgl/xxgl_check.vue')
const xxgl_message = () => import('../components/xxgl/xxgl_message.vue')
const xxgl_setting = () => import('../components/xxgl/xxgl_setting.vue')

const routes= [
    {
      path:'/Login',
      name: 'Login',
      component:Login,
    },

    {
      path : '/',
      name:'Home',
      component:Home,
      redirect: {name: "page1"},
      children:[
        {
          path: "/TicketInquiry",
          name: "TicketInquiry",
          component: TicketInquiry,
          meta: {
            title: "车票查询"
          }
        },
        {
          path: "/TicketOrder",
          name: "TicketOrder",
          component: TicketOrder,
          meta: {
            title: "车票订购"
          }
        },
      // 以下界面都是哪来测试跳转的
        {
          path: "/page1",
          name: "page1",
          component:page1,
          meta:{
              title:"测试界面1"
          }
        },
        {
          path: "/page2",
          name: "page2",
          component:page2,
          meta:{
              title:"测试界面2"
          }
        },
        {
          path: "/page3",
          name: "page3",
          component:page3,
          meta:{
              title:"测试界面3"
          }
        },
      ],
    },
    //信息管理
    {
      path:'/xxgl1',
      name: 'xxgl_home',
      component:xxgl_home,
    },
    {
      path: '/xxgl2',
      name:'xxgl_message',
      component:xxgl_message,
    },
    {
      path: '/xxgl3',
      name:'xxgl_check',
      component:xxgl_check,
    },
    {
      path: '/xxgl4',
      name:'xxgl_setting',
      component:xxgl_setting,
    },

]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})
 
export default router