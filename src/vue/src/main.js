// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify/es5/components/Vuetify';
import Vuex from 'vuex';
import 'vuetify/dist/vuetify.min.css';
import App from './App';
import store from './store/store';

Vue.config.productionTip = false;
Vue.use(Vuetify);
Vue.use(Vuex);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  components: { App },
  template: '<App/>',
});
