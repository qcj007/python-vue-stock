

import { createRouter, createWebHistory } from "vue-router";


// 静态路由
export const constantRoutes = [
  {
    path: "/",
     component: () => import(`../views/index.vue`),
    name: "index",
  },
 

];

const base = process.env.NODE_ENV === "development" ? "/" : "/dist/";
const router = createRouter({
  history: createWebHistory(base), // hash模式：createWebHashHistory，history模式：createWebHistory
  scrollBehavior: () => ({
    top: 0,
  }),
  routes: constantRoutes,
});

export default router;
