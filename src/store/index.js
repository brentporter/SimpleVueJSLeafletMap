import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex);

//const debug = process.env.NODE_ENV !== 'production'

const state = {
    count: 0,
    //The next ones are for txcap
    txCapQueryTotalRecordsCount:null,
    txCapQueryCurrentDate:null,
    txCapQuerySpatial:null,
};

const mutations = {
    increment (state){
        state.count++
    },
    decrement (state){
        state.count--
    }
};

const actions = {
    increment: ({ commit }) => commit('increment'),
    decrement: ({ commit }) => commit('decrement'),
    incrementIfOdd ({ commit, state }) {
        if ((state.count + 1) % 2 === 0) {
            commit('increment');
        }
    },
    incrementAsync ({ commit }) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                commit('increment');
                resolve()
            }, 1000)
        })
    }
};

const getters = {
    evenOrOdd: state => state.count % 2 === 0 ? 'even' : 'odd'
};

export default new Vuex.Store({
    modules:{

    },
    state,
    mutations,
    actions,
    getters
    /*    strict: debug,
        plugins: debug ? [createLogger()] : []*/
})