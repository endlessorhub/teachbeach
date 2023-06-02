import axios from 'axios'
const state = () => ({
    facebookIsConnected: false,
    googleIsConnected: false
})

const mutations = {
  
}

const actions = {
   async facebookLogin(_,payload){
        const {success, data, error} = await axios.post('/social/facebook/',payload)
    },
    async googleLogin(_, payload) { 
        const { success, data, error } = await axios.post(
          "/social/google/",
          payload
        );   
    }
}

export default {
    namespaced: true,
    state,
    mutations,
    actions,
}