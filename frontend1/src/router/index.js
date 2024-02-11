import Vue from "vue";
import VueRouter from "vue-router";

import RegisterView from '../views/auth/RegisterView.vue'
import LoginView from '../views/auth/LoginView'
import CommonHomeView from '../views/home/CommonHomeView.vue'

Vue.use(VueRouter)

const routes = [
    {
        path:"/register",
        name:"Registration-Page",
        component: RegisterView,
    },

    {
        path:"/login",
        name:"Login-Page",
        component: LoginView,
    },
    {
        path:"/",
        name:"UserHomeView",
        component: CommonHomeView,
    }   

];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;