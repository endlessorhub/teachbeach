import axios from "axios";
const state = () => ({
  chat:[],
  webSocketConnection: null,
  discussionId:null
});

const mutations = {

  pushMessage(state, discussionMessage) {
    let replyPushed = false;
    let parentIdentified = false

    // adding child if reply is for the main comment
    if (state.chat.length > 0) {
      // loop through each main comment
      state.chat = state.chat.map((chat) => {
        //if parent id matches to that of the main comment
        if (chat.id === discussionMessage.parent_comment_id) {
          // check for replies array , if exsist than insert else create one and then insert
          if (Object.hasOwn(chat, "replies")) {
            replyPushed = true;
            parentIdentified = true;
            chat.replies.push(discussionMessage);
            return chat
          }
          else {
            replyPushed = true;
            parentIdentified = true;
            chat.replies = [];
            chat.replies.push(discussionMessage);
            return chat
          }
        }
        else {
          return chat
        }
      });
      
      // adding child if it is the reply to a reply
      if (!parentIdentified) { 
        if (discussionMessage.parent_comment_id)
          //loop through all the main comments 
          state.chat = state.chat.map(parent => {
            // check for replies array
            if (Object.hasOwn(parent, "replies")) { 

            // find index of the parent reply whose id matches the id of child reply
            const index = parent.replies.findIndex(
              (reply) => reply.id === discussionMessage.parent_comment_id
            );
              
            // if found add the child reply next to preant reply with in the array
            if (index >= 0) {
              parent.replies.splice(index + 1, 0, discussionMessage)
              parentIdentified = true
              replyPushed = true
            
            }
          }
          return parent

        })
      }

      // if the message is neither the reply of main comment nor the child reply of a reply
      if (!replyPushed)
        state.chat.push(discussionMessage);
    }

    // if it is the first comment of the discussion
    else
      state.chat.push(discussionMessage)
    
    // sort the discussion array in descending order according to created_at(time) attribute 
    state.chat = state.chat.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));


  },
  setWSConnection(state, connection) {
    state.webSocketConnection = connection;
  },
  setDiscussionId(state, discussionId) {
    state.discussionId = discussionId;
  },
  loadPreviousChat(state, previousChats) {
    state.chat = [...previousChats];

    // sort the discussion array in descending order according to created_at(time) attribute
    state.chat = state.chat.sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );
  },
};

const actions = {
  initiateChat({ commit }, discussionId) {
    const connection = new WebSocket(
      `${process.env.BASE_WEB_SOCKET_URL}/${discussionId}/`
    );
    connection.onopen = () => {
      commit("setWSConnection", connection);
      connection.onmessage = (message) => {
        commit("pushMessage", JSON.parse(message.data));
      };
    };
  },
  receiveMessage(commit, message) {
    commit("pushMessage", message);
  },
  sendMessage({ state }, payload) {
    if (state.webSocketConnection) {
      state.webSocketConnection.send(JSON.stringify(payload));
    }
  },
  async loadPreviousChats({ commit }, discussionId) {
    const response = await axios.get(`/api/comments/${discussionId}/`);
    if (response.status === 200) commit("loadPreviousChat", response.data);
  },
  discussionSetup(_, setupOption) {
    return axios.post("/api/discussion-setup/", setupOption);
  },
  setDiscussionId({ commit }, discussionId) {
    commit("setDiscussionId", discussionId);
  },
  loadDicussionDetails(_, discussionId) {
    return axios.get(`/api/discussion/${discussionId}/`);
  },
  loadAllDiscussionTitles(_, payload = null) {
    return axios.get("/api/discussion/all/");
  },
  loadRecentDiscussion(_, payload = null) {
    return axios.get("/api/discussion/");
  },
  closeSocket({ state }) {
    if (state.webSocketConnection) state.webSocketConnection.close();
  },
  emptyChats({ commit }) {
    commit("emptyChat");
  },
};

const getters = {
  chatMessages: (state) => state.chat,
  discussionId: (state) => state.discussionId
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
