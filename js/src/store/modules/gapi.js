import { gapiLoaded, init, handleAuth, handleSignout, listUpcomingEvents } from '@/lib/gapi'
import api from '@/lib/api'

const state = () => ({
    status: 'idle',
    error: null,
    isInitialized: false,
    isLoading: false,
    authState: null,
    events: [],
})

const mutations = {
    setStatus(state, payload) {
        state.status = payload
    },
    setAuthState(state, payload) {
        state.authState = payload
    },
    setEvents(state, payload) {
        const ids = payload.reduce((acc, v) => ({...acc, [v.id]: true}), {});
        const other = state.events.filter(v => !ids[v.id]);
        state.events = [...other, ...payload.map(v => ({...v, authState: state.authState}))]
    },
    setIsLoading(state, payload) {
        state.isLoading = payload
    },
    setError(state, payload) {
        state.error = payload
    }
}

const actions = {
    init({state, commit}) {
        if(state.status === 'idle') {
            commit('setStatus', 'initializing')
            gapiLoaded.then(() => {
                commit('setStatus', 'initialized')
                init((authState) => {
                    commit('setStatus', 'authcheckdone')
                    commit('setAuthState', authState)
                }, err => {
                    commit('setStatus', 'authcheckerror')
                    commit('setError', err)
                })
            })
        }
    },
    login() {
        return handleAuth()
    },
    logout() {
        return handleSignout()
    },
    syncEvents({commit, state}) {
        commit('setIsLoading', true)
        listUpcomingEvents().then((res) => {
            commit('setEvents', res)
            // do the rest in background
            commit('setIsLoading', false)
            // sync to server at once
            return api.saveSyncCalendar('google', state.authState, res)
        })
    },
    getSavedEvents({commit}) {
        commit('setIsLoading', true)
        return api.getSyncCalendar().then(data => {
            const events = data.calendars.filter(v => v.provider_type === 'google')
                .reduce((acc, v) => [...acc, ...(v.data || [])], [])
            commit('setEvents', events)
            commit('setIsLoading', false)
        })
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
}