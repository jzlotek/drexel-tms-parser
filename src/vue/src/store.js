import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export const UPDATE_CLASSES = 'updateClasses';
export const CLEAR_QUERY = 'clearQuery';
export const ADD_TO_QUERY = 'addToQuery';

export default new Vuex.Store({
  state: {
    query: {},
    classes: [],
  },
  mutations: {
    [ADD_TO_QUERY](state, query) {
      Object.entries(query).forEach((entry) => {
        Vue.set(state.query, entry[0], entry[1]);
        // state.query[entry[0]] = entry[1];
      });
    },
    [CLEAR_QUERY](state) {
      state.query = {};
    },
    [UPDATE_CLASSES](state, classes) {
      state.classes = classes;
    },
  },
  getters: {
    getQuery(state) {
      return state.query;
    },
    getClasses(state) {
      return state.classes;
    },
    getQueryString({ query }) {
      let queryParams = '';
      const L = Object.entries(query).length;

      let i = 0;
      if (L > 0) {
        queryParams = '?';
        Object.entries(query).forEach((entry) => {
          const param = `${entry[0]}=${entry[1]}`;
          if (i > 0) {
            queryParams += '&';
          }
          queryParams += param;
          i += 1;
        });
      }
      return queryParams;
    },
  },
  actions: {
    [CLEAR_QUERY]({ commit }) {
      commit(CLEAR_QUERY);
    },
    async [UPDATE_CLASSES]({ commit, getters }) {
      let items;
      try {
        const queryParams = getters.getQueryString;
        items = await axios.get(`/course${queryParams}`);
        items = items.data;
      } catch (error) {
        items = [];
      }
      commit(UPDATE_CLASSES, items);
    },
  },
});
