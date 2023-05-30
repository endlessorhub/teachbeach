import router from '../../router';

export const LEFT_DRAWER_TYPE = {
    TEACH: 'teacherTypeDrawer',
    LEARN: 'learnerTypeDrawer',
}

const state = () => ({
    isLeftDrawerOpened: true,
    isLeftDrawerMini: false,
});

const getters = {
    
};

const mutations = {
    setIsLeftDrawerOpened(state, payload) {
        state.isLeftDrawerOpened = payload
    },
    setIsLeftDrawerMini(state, payload) {
        state.isLeftDrawerMini = payload
    },
}

const actions = {

}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
}