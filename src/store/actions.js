import axios from 'axios';
import EventBus from '../EventBus';
import {
  UPDATE_CLASSES, CLEAR_QUERY, ADD_TO_SELCTED, ADD_TO_QUERY, REMOVE_FROM_SELCTED, REMOVE_FROM_QUERY,
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
  [REMOVE_FROM_QUERY]({ commit }, payload) {
    commit(REMOVE_FROM_QUERY, payload);
  },
  [ADD_TO_SELCTED]({ commit, state }, payload) {
    if (!state.selected.includes(payload)) {
      commit(ADD_TO_SELCTED, payload);
    } else {
      EventBus.$emit('error', payload);
    }
  },
  [ADD_TO_QUERY]({ commit }, payload) {
    commit(ADD_TO_QUERY, payload);
  },
  [REMOVE_FROM_SELCTED]({ commit }, payload) {
    commit(REMOVE_FROM_SELCTED, payload);
  },
};

export default actions;
