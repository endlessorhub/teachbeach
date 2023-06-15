import Vue from 'vue'
import Vuex from 'vuex'
import _ from 'lodash'
import axios from 'axios'

import gapi from './modules/gapi'
import api from '@/lib/api'
import viewingCompany from './modules/viewingCompany';
import learnerMembership from './modules/learnerMembership';
import layout from './modules/layout'
import companyService from '@/lib/services/company'
import socialAuth from './modules/socialAuth'
import chatDiscussion from './modules/chatDisscusion'

Vue.use(Vuex)

export const defaultLogoSrc = require('@/assets/logo-blue.svg')
export const defaultLogoAlt = 'collab social logo'

export default new Vuex.Store({
    modules: {
        gapi,
        viewingCompany,
        layout,
        learnerMembership,
        socialAuth,
        chatDiscussion
    },
    state: {
        loginFormOpened: null, // object with login form params
        user: null,
        categoriesSelected: [],
        logoSrc: null,
        logoAlt: '',
        logoLink: '/',
        homeUrl: '',
        logoDimensions: {},
        classCompanyName: '',
        studentName: '',
        studentPhone: '',
        studentEmail: '',
        teacherMembership: null,
        isLoadingTeacherMembership: false,
        lastLesson: null,

    // refactor:
    zip: "",
    city: "",
    availableZips: [],
    teacher: {},
    profile: {},
    avatar: null,
    companyProfile: null,
    teacherLessonType: null,
    teacherGroupClass: {},
    globals: {},
    learnerSearch: {},
    learnerChoice: null,
    learnerData: {},
    learnerCards: null,
    metatags: null,
    isAuthChecked: false,
    globalError: "",
    timezone: null,
    hasOrder: false,
    teacherCreateMembership: false,
    belongingCompanyProfile: null,
    logoCompanyProfile: null,
    isLogoCompanyProfileChecked: false,
  },
  getters: {
    isLoggedIn(state) {
      return state.user && Object.keys(state.user).length;
    },
    isTeacher(state) {
      return state.teacher && Object.keys(state.teacher).length;
    },
    isTeacherOfCompany(state) {
      return state.user && state.user.belongs_to;
    },
    isLearner(state) {
      return state.hasOrder;
    },
    showClassCompanyName(state) {
      return (
        !state.logoDimensions ||
        !state.logoDimensions.height ||
        state.logoDimensions.width <= state.logoDimensions.height * 4
      );
    },
    isMember: (state) => (membershipId) => {
      return (
        state.user &&
        state.user.memberships &&
        state.user.memberships.some((m) => m.membership === membershipId)
      );
    },
    haveMembership(state) {
      return state.user && state.user.membership;
    },
  },
  mutations: {
    setLogoDimensions(state, { width, height }) {
      state.logoDimensions = { width, height };
    },
    setTimezone(state, v) {
      state.timezone = v;
    },
    setGlobalError(state, v) {
      state.globalError = v;
    },
    setIsAuthChecked(state, v) {
      state.isAuthChecked = v;
    },
    setLoginFormOpened(state, v) {
      state.loginFormOpened = v;
    },
    setStudentName(state, v) {
      state.studentName = v;
    },
    setStudentPhone(state, v) {
      state.studentPhone = v;
    },
    setStudentEmail(state, v) {
      state.studentEmail = v;
    },
    setLogoSrc(state, logo) {
      state.logoSrc = logo;
    },
    setLogoAlt(state, alt) {
      state.logoAlt = alt;
    },
    setLogoLink(state, val) {
      state.logoLink = val;
    },
    setHomeUrl(state, val) {
      state.homeUrl = val;
    },
    setClassCompanyName(state, name) {
      state.classCompanyName = name;
    },
    setZip(state, zip) {
      state.zip = zip;
    },
    setCity(state, city) {
      state.city = city;
    },
    setAvailableZips(state, zips) {
      state.availableZips = zips;
    },
    setUser: function(state, user) {
      state.user = user;
      state.timezone = user && user.timezone;
    },
    setTeacher: function(state, data) {
      state.teacher = { ...state.teacher, ...data };
      /*
            if (!state.teacher) {
                state.teacher = {}
            }
            _.each(data, (v, k) => {
                state.teacher[k] = v
            })
            */
    },
    setTeacherCategory: function(state, categoriesSelected) {
      state.categoriesSelected = categoriesSelected;
    },
    setTeacherProfile: function(state, profile) {
      state.profile = { ...state.profile, ...profile };
      /*
            if (!state.profile) {
                state.profile = {}
            }
            _.each(profile, (v, k) => {
                state.profile[k] = v
            })
            */
    },
    setTeacherAvatar: function(state, avatar) {
      state.avatar = avatar;
    },
    setCompanyProfile: function(state, profile) {
      state.companyProfile = profile;
    },
    logout(state) {
      state.user = {};
      state.categoriesSelected = [];
      state.profile = null;
      state.companyProfile = null;
      state.avatar = null;
      state.teacherLessonType = null;
      state.teacherGroupClass = null;
      state.teacherCreateMembership = false;
      state.lastLesson = null;
    },
    setTeacherLessonType(state, teacherLessonType) {
      state.teacherLessonType = teacherLessonType;
    },
    setGroupClass: function(state, groupClass) {
      state.teacherGroupClass = { ...state.teacherGroupClass, ...groupClass };
    },
    setGroupClassForce: function(state, groupClass) {
      state.teacherGroupClass = groupClass || {};
    },
    setGlobals: function(state, globals) {
      state.globals = Object.entries(globals).reduce(
        (acc, [k, v]) => ({
          ...acc,
          ...{ [k]: v === "True" ? true : v === "False" ? false : v },
        }),
        {}
      );
    },
    setLearnerSearch: function(state, data) {
      state.learnerSearch = { ...state.learnerSearch, ...data };
    },
    setLearnerChoice: function(state, data) {
      state.learnerChoice = data;
    },
    resetLearnerData(state, saveKeys) {
      state.learnerData = _.pick(state.learnerData || {}, saveKeys);
    },
    mergeLearnerData(state, data) {
      state.learnerData = { ...(state.learnerData || {}), ...data };
    },
    setLearnerData(state, data) {
      state.learnerData = data;
    },
    setLearnerCards: function(state, data) {
      state.learnerCards = data;
    },
    setMetatags: function(state, data) {
      state.metatags = data;
    },
    setHasOrder(state, data) {
      state.hasOrder = data;
    },
    setCreateMembership(state, data) {
      state.teacherCreateMembership = data;
    },
    setTeacherMembership(state, data) {
      state.teacherMembership = data;
    },
    setIsLoadingTeacherMembership(state, data) {
      state.isLoadingTeacherMembership = data;
    },
    setBelongingCompanyProfile(state, data) {
      state.belongingCompanyProfile = data;
    },
    setLogoCompanyProfile(state, data) {
      state.logoCompanyProfile = data;
    },
    setIsLogoCompanyProfileChecked(state, data) {
      state.isLogoCompanyProfileChecked = data;
    },
    setLastLesson(state, data) {
      state.lastLesson = data;
    },
  },
  actions: {
    updateLogoCompanyProfile(store, data) {
      store.commit("setLogoCompanyProfile", data);
      store.commit("setIsLogoCompanyProfileChecked", true);
    },
    async syncLogoCompanyProfile(store, id) {
      if (!id) {
        store.commit("setLogoCompanyProfile", null);
        store.commit("setIsLogoCompanyProfileChecked", true);
        return;
      }
      if (
        !store.state.logoCompanyProfile ||
        (store.state.logoCompanyProfile.id !== id &&
          store.state.logoCompanyProfile.slug !== id)
      ) {
        store.commit("setIsLogoCompanyProfileChecked", false);
        const profile = await api.getCompanyProfile(id);
        store.commit("setLogoCompanyProfile", profile);
        store.commit("setIsLogoCompanyProfileChecked", true);
      }
    },
    async loadBelongingCompanyProfile(store, id) {
      if (!id) return store.commit("setBelongingCompanyProfile", null);
      const profile = await api.getCompanyProfile(id);
      store.commit("setBelongingCompanyProfile", profile);
    },
    setCompanyProfile(store, profile) {
      if (profile) {
        store.commit("setLogoSrc", profile.media);
        store.commit("setLogoAlt", profile.name);
        store.commit("setLogoLink", companyService.getLink(profile));
        store.commit("setClassCompanyName", profile.name);
        store.commit("setHomeUrl", profile.home_url);
      } else {
        store.commit("setLogoSrc", defaultLogoSrc);
        store.commit("setLogoAlt", defaultLogoAlt);
        store.commit("setLogoLink", "/");
        store.commit("setClassCompanyName", "");
        store.commit("setHomeUrl", "");
      }
    },
    loadDraft(store) {
      return axios.get("/api/draft/").then((res) => {
        if (res.data.drafts && res.data.drafts.length) {
          const draft = res.data.drafts[0].class_data;
          store.dispatch("setDraft", draft);
        }
      });
    },
    setDraft(store, draft) {
      if (draft.teacherGroupClass) {
        store.commit("setGroupClass", draft.teacherGroupClass);
      }
      if (draft.teacherLessonType) {
        store.commit("setTeacherLessonType", draft.teacherLessonType);
      }
      if (draft.categoriesSelected) {
        store.commit("setTeacherCategory", draft.categoriesSelected);
      }
    },
    setInitialdata(store, res) {
      console.log("update init data", res.data);
      if (res.data.metatags) {
        store.commit("setMetatags", _.keyBy(res.data.metatags, "route"));
      }
      if (res.data.learner_needs) {
        store.commit("mergeLearnerData", {
          learnerNeeds: res.data.learner_needs,
        });
      }
      if (res.data.user) {
        store.commit("setUser", res.data.user);
        if (res.data.user.company_profile) {
          store.commit("setCompanyProfile", {
            id: res.data.user.company_profile.id,
            companyName: res.data.user.company_profile.name,
            description: res.data.user.company_profile.description,
            imageUrl: res.data.user.company_profile.media,
            mainImageUrl: res.data.user.company_profile.main_media,
          });
        }
      }
      if (res.data.teacher) {
        store.commit("setTeacher", res.data.teacher);
        store.commit("setTeacherProfile", res.data.teacher);
      }

      if (res.data.user_cards) {
        store.commit("setLearnerCards", res.data.user_cards);
      }

      if (res.data.draft_classes && res.data.draft_classes.length) {
        // console.log('draft_classes', res.data.draft_classes)
        store.dispatch("setDraft", res.data.draft_classes[0].class_data);
      } else if (res.data.last_class) {
        store.commit(
          "setTeacherLessonType",
          res.data.last_class.is_private ? "private" : "group"
        );
        store.commit("setTeacherCategory", res.data.last_class.subcategories);
        store.commit("setLastLesson", res.data.last_lesson);
      }
      if (res.data.zips && res.data.zips.length) {
        store.commit("setAvailableZips", res.data.zips);
      }
      if (res.data.has_order) {
        store.commit("setHasOrder", res.data.has_order);
      }
    },
    loadTeacherMembership(store) {
      store.commit("setIsLoadingTeacherMembership", true);
      return axios
        .get("/api/teacher_membership/")
        .then((res) => {
          if (res.data.success) {
            store.commit("setTeacherMembership", res.data.membership);
          }
        })
        .finally(() => store.commit("setIsLoadingTeacherMembership", false));
    },
    saveTeacherMembership(store, payload) {
      store.commit("setIsLoadingTeacherMembership", true);
      return axios
        .post("/api/teacher_membership/", payload)
        .then((res) => {
          if (res.data.success) {
            store.commit("setTeacherMembership", res.data.membership);
            store.commit("setUser", {
              ...store.state.user,
              membership: res.data.membership.id,
            });
          }
        })
        .finally(() => store.commit("setIsLoadingTeacherMembership", false));
    },
    async logout() {},
    async handShake() {
      const { data } = await axios.get("/api/handshake/");
      return data.csrftoken;
    },
  },
});
