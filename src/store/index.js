import { createStore } from "vuex";
const store = createStore({
    state: {
        token: null,
      },
    mutations: {
        setToken(state, token) {
            console.log(token)
            state.token = token;
            console.log(state.token)
          },
    },
    actions: {},

    getters: {},

    modules: {},
})
export default store;

