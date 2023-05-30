import api from '@/lib/api'

export const VIEWING_COMPANY_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  LOADED: 'loaded',
  SAVED: 'saved',
  ERROR: 'error',
};

const state = () => ({
    status: VIEWING_COMPANY_STATES.IDLE,
    error: null,
    company: null,
});

const getters = {
    isLoading: (state) => state.status === VIEWING_COMPANY_STATES.LOADING,
};

const mutations = {
    setStatus(state, payload) {
        state.status = payload
    },
    setCompany(state, payload) {
        state.company = payload
    },
    setError(state, payload) {
        state.error = payload
    }
}

const actions = {
    loadCompany({ commit }, id) {
        commit('setStatus', VIEWING_COMPANY_STATES.LOADING);
        return api.getCompanyProfile(id).then(data => {
            commit('setCompany', data);
            commit('setStatus', VIEWING_COMPANY_STATES.LOADED);
        }).catch((err) => {
            commit('setError', err);
            commit('setStatus', VIEWING_COMPANY_STATES.ERROR);
        })
    },
    sendCompanyTeacherRequest({ commit }, data) {
        commit('setStatus', VIEWING_COMPANY_STATES.LOADING);
        return api.sendTeacherRequest(data).then(res => {
            commit('setStatus', VIEWING_COMPANY_STATES.SAVED);
        }).catch((err) => {
            if (err.response.data) {
                commit('setError', err.response.data);
            }
            commit('setStatus', VIEWING_COMPANY_STATES.ERROR);
        })
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}