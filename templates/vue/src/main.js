import { createApp } from "vue";
import App from "./App.vue";
import store from "./store"
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import router from "./router";
import "./assets/style/main.less"
import Directive from "@/plugins/directives/index.js";
const app = createApp(App);

app.use(Antd).use(router).use(store).use(Directive).mount("#app");
