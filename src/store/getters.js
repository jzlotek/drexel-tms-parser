const getters = {
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
        if (entry[1] !== undefined) {
          const param = `${entry[0]}=${entry[1]}`;
          if (i > 0) {
            queryParams += '&';
          }
          queryParams += param;
          i += 1;
        }
      });
    }
    return queryParams;
  },
  getSelected(state) {
    return state.selected;
  },
};

export default getters;
