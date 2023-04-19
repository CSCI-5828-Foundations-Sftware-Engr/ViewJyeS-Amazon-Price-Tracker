const state = {
  email: null,
  full_name: "User Not Logged In",
  card_detail: []
};
const mutations = {
  setEmail(state, email) {
    state.email = email;
  },
  setFullName(state, full_name) {
    state.full_name = full_name;
  },
  setCardDetail(state, card_detail) {
    state.card_detail.push(card_detail);
  },
  setCardEmpty(state, card_empty) {
    state.card_detail = card_empty
  },
  removeCard(state, index) {
    state.card_detail.splice(index, 1);
  }
};
const actions = {
  updateEmailId({commit}, email) {
    commit("setEmail", email);
  },
  updateFullName({commit}, full_name) {
    commit("setFullName", full_name);
  },
  updateCardDetail({commit}, card_detail) {
    commit("setCardDetail", card_detail);
  },
  updateCardEmpty({commit}, card_empty) {
    commit("setCardEmpty", card_empty)
  },
  removeCardIndex({commit}, index) {
    commit("removeCard", index)
  }
};
const getters = {
  getEmail(state) {
    return state.email;
  },
  getFullName(state) {
    return state.full_name;
  },
  getCardDetail(state) {
    return state.card_detail;
  }
};


export default {
  namespaced: true,
  getters,
  mutations,
  actions,
  state
};