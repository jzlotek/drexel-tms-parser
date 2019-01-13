import axios from 'axios';
import {
  UPDATE_CLASSES, CLEAR_QUERY, ADD_TO_SELCTED, ADD_TO_QUERY, REMOVE_FROM_SELCTED,
} from './constants';


const actions = {
  [CLEAR_QUERY]({ commit }) {
    commit(CLEAR_QUERY);
  },
  async [UPDATE_CLASSES]({ commit, getters }) {
    const queryParams = getters.getQueryString;
    let items;
    try {
      items = await axios.get(`/course${queryParams}`);
      items = items.data;
    } catch (error) {
      items = [];
    }
    commit(UPDATE_CLASSES, items);
  },
  [ADD_TO_SELCTED]({ commit }, payload) {
    commit(ADD_TO_SELCTED, payload);
  },
  [ADD_TO_QUERY]({ commit }, payload) {
    commit(ADD_TO_QUERY, payload);
  },
  [REMOVE_FROM_SELCTED]({ commit }, payload) {
    commit(REMOVE_FROM_SELCTED, payload);
  },
};

export default actions;
