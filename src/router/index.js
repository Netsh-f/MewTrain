import { createRouter, createWebHashHistory } from 'vue-router'


const Home = () => import('../components/Home.vue');
// const TicketInquiry = () => import('../components/TicketInquiry.vue');
const Login = () => import('../components/Login.vue');
const page1 = () => import('../components/page1.vue');
const page2 = () => import('../components/page2.vue');
const page3 = () => import('../components/page3.vue');
const TicketInquiry = () => import('../components/TicketInquiry.vue')
const TicketOrder = () => import('../components/TicketOrder.vue')
const mesdeal_home = () => import('../components/mesdeal/mesdeal_home.vue')
const mesdeal_check = () => import('../components/mesdeal/mesdeal_check.vue')
const mesdeal_message = () => import('../components/mesdeal/mesdeal_message.vue')
const mesdeal_setting = () => import('../components/mesdeal/mesdeal_setting.vue')

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
      path:'/mesdeal1',
      name: 'mesdeal_home',
      component:mesdeal_home,
    },
    {
      path: '/mesdeal2',
      name:'mesdeal_message',
      component:mesdeal_message,
    },
    {
      path: '/mesdeal3',
      name:'mesdeal_check',
      component:mesdeal_check,
    },
    {
      path: '/mesdeal4',
      name:'mesdeal_setting',
      component:mesdeal_setting,
    },

]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})
 
export default router