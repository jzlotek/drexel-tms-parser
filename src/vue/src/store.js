import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    query: {},
  },
  mutations: {
    addToQuery: (state, query) => {
      Object.entries(query).forEach((entry) => {
        state.query[entry[0]] = entry[1];
      });
    },
    clearQuery: (state) => {
      state.query = {};
    },
  },
});
