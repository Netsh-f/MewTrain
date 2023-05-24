import { createRouter, createWebHashHistory } from 'vue-router'


const Home = () => import('../components/Home.vue');
const Login = () => import('../components/Login.vue');
const page1 = () => import('../components/WELCOME.vue');
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
      redirect: {name: "WELCOME"},
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
        {
          path: "/WELCOME",
          name: "WELCOME",
          component:page1,
          meta:{
              title:"欢迎 "
          }
        },
        {
          path:'/mesdeal_home',
          name: 'mesdeal_home',
          component:mesdeal_home,
          meta:{
            title:""
        }
        },
        {
          path: '/mesdeal_message',
          name:'mesdeal_message',
          component:mesdeal_message,
          meta:{
            title:""
        }
        },
        {
          path: '/mesdeal_check',
          name:'mesdeal_check',
          component:mesdeal_check,
          meta:{
            title:""
        }
        },
        {
          path: '/mesdeal_setting',
          name:'mesdeal_setting',
          component:mesdeal_setting,
          meta:{
            title:""
        }
        },
      ],
    },
    //信息管理

]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})
 
export default router