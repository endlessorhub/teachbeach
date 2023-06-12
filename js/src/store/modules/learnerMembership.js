import api from '@/lib/api'

export const DATA_STATES = {
  IDLE: 'idle',
  LOADING: 'loading',
  DONE: 'done',
  SAVED: 'saved',
  ERROR: 'error',
};

const state = () => ({
    status: DATA_STATES.IDLE,
    error: null,
    memberships: [],
    membershipSettings: [],
    currentMembershipId: null,
});

const getters = {
    isLoading: (state) => state.status === DATA_STATES.LOADING,
    currentMembership: (state) => state.memberships.find(v => v.id === state.currentMembershipId),
    currentMembershipSetting: (state) => {
        const membership = state.memberships.find(v => v.id === state.currentMembershipId);
        console.log(membership);
        return membership ? state.membershipSettings.find(v => v.id === membership.membership) : undefined;
    },
};

const mutations = {
    setStatus(state, payload) {
        state.status = payload
    },
    setMemberships(state, payload) {
        state.memberships = payload
    },
    membershipSettings(state, payload) {
        state.membershipSettings = payload
    },
    setCurrentMembershipId(state, payload) {
        state.currentMembershipId = payload
    },
    setError(state, payload) {
        state.error = payload
    }
}

const actions = {
    loadMemberships({ dispatch, state }) {
        if (state.status === DATA_STATES.LOADING || state.status === DATA_STATES.DONE) return;
        dispatch('reloadMemberships');
    },
    reloadMemberships({commit}) {
        commit('setStatus', DATA_STATES.LOADING);
        commit('setError', null);
        return api.getLearnerMemberships().then(data => {
            commit('setStatus', DATA_STATES.DONE);
            if (!data.success) {
                commit('setMemberships', []);
                commit('membershipSettings', []);
                commit('setCurrentMembershipId', null);
                return;
            }
            commit('setMemberships', data.memberships);
            commit('membershipSettings', data.membershipSettings);
            commit('setCurrentMembershipId', data.memberships[0].id);
            
        }).catch((err) => {
            commit('setError', err);
            commit('setStatus', DATA_STATES.ERROR);
        })
    },
    saveMembership({commit, state}, data) {
        commit('setStatus', DATA_STATES.LOADING);
        commit('setError', null);
        return api.saveLearnerMembership(data).then(res => {
            commit('setStatus', DATA_STATES.DONE);
            if (res.success) {
                commit('setMemberships', [...state.memberships.filter(m => m.id !== res.data.id), res.data]);
            }
        }).catch((err) => {
            commit('setError', err);
            commit('setStatus', DATA_STATES.ERROR);
        })
    },
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}