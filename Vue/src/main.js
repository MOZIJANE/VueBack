import Vue from "vue";

import "normalize.css/normalize.css"; // A modern alternative to CSS resets

import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
//英文版elementui
// import locale from "element-ui/lib/locale/lang/en"; // lang i18n

import "@/styles/index.scss"; // global css
import request from "@/utils/request";
import App from "./App";
import store from "./store";
import router from "./router";
import "@/icons"; // icon
import "@/permission"; // permission control
import clipboard from "clipboard";
import 'element-ui/lib/theme-chalk/display.css';
import echarts from "echarts";
import 'echarts/theme/green'  
import 'echarts/theme/dark-bold'  //不错
import '@/assets/js/echartsTheme/westeros' 

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */

Vue.prototype.$request = request;
// set ElementUI lang to EN
// Vue.use(ElementUI, { locale });
// 如果想要中文版 element-ui，按如下方式声明
Vue.use(ElementUI)
Vue.prototype.$echarts = echarts
Vue.prototype.clipboard = clipboard;
Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  store,
  render: h => h(App)
});
