// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import Vuex from 'vuex';
import App from './App.vue';
import store from './store/store';
import './registerServiceWorker';


Vue.config.productionTip = false;
Vue.use(Vuetify, {
  theme: {
    primary: '#3f51b5',
    secondary: '#ffc107',
    accent: '#ff9800',
    error: '#f44336',
    warning: '#ff5722',
    info: '#2196f3',
    success: '#4caf50',
  },
});
Vue.use(Vuex);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  components: { App },
  template: '<App/>',
});
