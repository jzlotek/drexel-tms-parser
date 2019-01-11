import Vue from 'vue';
import {
  UPDATE_CLASSES,
  CLEAR_QUERY,
  ADD_TO_QUERY,
  ADD_TO_SELCTED,
  REMOVE_FROM_SELCTED,
} from './constants';

const mutations = {
  [ADD_TO_QUERY](state, query) {
    Object.entries(query).forEach((entry) => {
      Vue.set(state.query, entry[0], entry[1]);
    });
  },
  [CLEAR_QUERY](state) {
    state.query = {};
  },
  [UPDATE_CLASSES](state, items) {
    state.classes = items;
  },
  [ADD_TO_SELCTED](state, c) {
    Vue.set(state.selected, state.selected.length, c);
  },
  [REMOVE_FROM_SELCTED](state, crn) {
    const index = state.selected.map(c => c.crn).indexOf(crn);
    if (index !== -1) {
      Vue.delete(state.selected, index);
    }
  },
};

export default mutations;
