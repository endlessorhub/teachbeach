import axios from "axios";
import Vue from "vue";
const state = () => ({
  chat: [],
  webSocketConnection: null,
  discussionId: null,
  discussionPermission: "allowed",
  chatPermission:false,
});

const mutations = {
  pushMessage(state, discussionMessage) {
    let replyPushed = false;
    let parentIdentified = false;

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
            return chat;
          } else {
            replyPushed = true;
            parentIdentified = true;
            chat.replies = [];
            chat.replies.push(discussionMessage);
            return chat;
          }
        } else {
          return chat;
        }
      });

      // adding child if it is the reply to a reply
      if (!parentIdentified) {
        if (discussionMessage.parent_comment_id)
          //loop through all the main comments
          state.chat = state.chat.map((parent) => {
            // check for replies array
            if (Object.hasOwn(parent, "replies")) {
              // find index of the parent reply whose id matches the id of child reply
              const index = parent.replies.findIndex(
                (reply) => reply.id === discussionMessage.parent_comment_id
              );

              // if found add the child reply next to preant reply with in the array
              if (index >= 0) {
                parent.replies.splice(index + 1, 0, discussionMessage);
                parentIdentified = true;
                replyPushed = true;
              }
            }
            return parent;
          });
      }

      // if the message is neither the reply of main comment nor the child reply of a reply
      if (!replyPushed) state.chat.push(discussionMessage);
    }

    // if it is the first comment of the discussion
    else state.chat.push(discussionMessage);

    // sort the discussion array in descending order according to created_at(time) attribute
    state.chat = state.chat.sort(
      (a, b) => new Date(b.created_at) - new Date(a.created_at)
    );
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
  setDiscussionPermission(state, permission) {
    state.discussionPermission = permission;
  },
  uploadImage(state, discussionMessage) {
    let chat = [...state.chat];
    let comment = undefined;
    let reply = undefined;
    comment = chat.find(
      (comment) => comment.id === discussionMessage.comment_id
    );
    let commentIndex = chat.findIndex(
      (comment) => comment.id === discussionMessage.comment_id
    );
    if (comment && commentIndex > -1) {
      const updatedComment = { ...comment, image: discussionMessage.image_url };
      state.chat.splice(commentIndex, 1, updatedComment);
    } else {
      chat.forEach((comment, index) => {
        reply = comment.replies.find(
          (reply) => reply.id === discussionMessage.comment_id
        );
        let replyIndex = comment.replies.findIndex(
          (reply) => reply.id === discussionMessage.comment_id
        );
        if (reply && replyIndex > -1) {
          const updatedReply = { ...reply, image: discussionMessage.image_url };
          comment.replies.splice(replyIndex, 1, updatedReply);
        }
      });
      state.chat = [...chat];
    }
  },
  setChatPermission(state, chatPermission) { 
    state.chatPermission = chatPermission
  }
};

const actions = {
  initiateChat({ commit }, discussionId) {
    const connection = new WebSocket(
      `${process.env.BASE_WEB_SOCKET_URL}/${discussionId}/`
    );
    connection.onopen = () => {
      commit("setWSConnection", connection);
      connection.onmessage = (message) => {
        let discussionMessage = JSON.parse(message.data)
        if (!Object.hasOwn(discussionMessage, "image_url"))
          commit("pushMessage", discussionMessage);
        else
          commit("uploadImage", discussionMessage);
      };
    };
  },
  receiveMessage({ commit, dispatch }, message) {
    dispatch("checkBlockUser","");
    commit("pushMessage", message);
  },
  sendMessage({ state }, payload) {
    if (state.webSocketConnection) {
      state.webSocketConnection.send(JSON.stringify(payload));
    }
  },
  async loadPreviousChats({ commit , dispatch}, discussionId) {
    dispatch("checkBlockUser", "");
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
  setDiscussionPermission({ commit }, permission) { 
    commit('setDiscussionPermission',permission)
  },
  async blockUser(_, blockUserDetails) { 
    const response = await axios.post("/api/discussion/block/", blockUserDetails);
    return response.status
  },
  async checkBlockUser({ commit,state }, payload) { 
    const response = await axios.get(`/api/discussion/chat-allowed/${state.discussionId}/`)
    if (response.status === 200) { 
      localStorage.setItem("chatPermission",response.data.is_allowed_to_chat)
        commit("setChatPermission", response.data.is_allowed_to_chat);
    }
  }
};

const getters = {
  chatMessages: (state) => state.chat,
  discussionId: (state) => state.discussionId,
  discussionPermission: (state) => state.discussionPermission,
  chatPermission:(state)=>state.chatPermission
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
