import Vue from "vue";
import VueRouter from "vue-router";

import RegisterView from '../views/auth/RegisterView.vue'

Vue.use(VueRouter)

const routes = [
    {
        path:"",
        name:"Registration-Page",
        component: RegisterView,
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;