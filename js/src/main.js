import Vue from 'vue'
import {defaultLogoSrc, defaultLogoAlt} from '@/store'
//import VueMeta from 'vue-meta'
/*
Vue.use(VueMeta, {
    attribute: 'data-some-meta-attr'
})
*/
import MinimalLayout from './layouts/MinimalisticLayout.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import _ from 'lodash'
// custom icons
import DashboardIcon from '@/components/icons/Dashboard';
import CollabIcon from '@/components/icons/Collab';
import ChatIcon from '@/components/icons/Chat';
import CrmIcon from '@/components/icons/Crm';
import ActivitiesIcon from '@/components/icons/Activities';
import EditIcon from '@/components/icons/Edit';
import HistoryIcon from '@/components/icons/History';
import LogoutIcon from '@/components/icons/Logout';
import MembershipsIcon from '@/components/icons/Memberships';


import wysiwyg from "vue-wysiwyg";
Vue.use(wysiwyg, {
    hideModules: {
        underline: true,
        code: true,
        orderedList: true,
        unorderedList: true,
        table: true,
    },
    image: {
        uploadURL: "/api/vue_editor_upload_file/",
        dropzoneOptions: {}
    },
    maxHeight: "200px",
});
import common from '@/plugins/common'
Vue.use(common)

//import 'vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
//import Vuetify from 'vuetify'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import './main.scss'
import './styles/chat-style.scss'

import config from './config.js'

//import VTooltip from 'v-tooltip'
import * as VueGoogleMaps from 'vue2-google-maps'

//import './styles/main.styl' // todo: figure out why styles are included twice with this approach
import 'vuetify/src/stylus/app.styl'
import Vuetify from 'vuetify/lib'
Vue.use(Vuetify, {
    icons: {
        'cust_activities': {
            component: ActivitiesIcon,
        },
        'cust_chat': {
            component: ChatIcon,
        },
        'cust_collab': {
            component: CollabIcon,
        },
        'cust_crm': {
            component: CrmIcon,
        },
        'cust_dashboard': {
            component: DashboardIcon,
        },
        'cust_edit': {
            component: EditIcon,
        },
        'cust_history': {
            component: HistoryIcon,
        },
        'cust_logout': {
            component: LogoutIcon,
        },
        'cust_memberships': {
            component: MembershipsIcon,
        },
    },
});

import './routes_to_sitemap'

import { library, dom } from '@fortawesome/fontawesome-svg-core'
import { faRocket, faBan, faCheckSquare } from '@fortawesome/free-solid-svg-icons'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons'
import { faFacebook, faLinkedin } from '@fortawesome/free-brands-svg-icons'
library.add(faRocket, faBan, faCheckSquare, faQuestionCircle, faFacebook, faLinkedin)
dom.watch()

//Vue.use(VTooltip)

Vue.use(VueGoogleMaps, {
  load: {
    key: config.google.mapApiKey,
    libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)

    //// If you want to set the version, you can do so:
    // v: '3.26',
  },

  //// If you intend to programmatically custom event listener code
  //// (e.g. `this.$refs.gmap.$on('zoom_changed', someFunc)`)
  //// instead of going through Vue templates (e.g. `<GmapMap @zoom_changed="someFunc">`)
  //// you might need to turn this on.
  // autobindAllEvents: false,

  //// If you want to manually install components, e.g.
  //// import {GmapMarker} from 'vue2-google-maps/src/components/marker'
  //// Vue.component('GmapMarker', GmapMarker)
  //// then disable the following:
  // installComponents: true,
})

Vue.config.productionTip = false

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// import fbmap from '@/lib/fbmap'

const availableGlobals = [
    'data-media-url',
    'data-password-reset',
    'data-uidb64',
    'data-token',
    'data-stripe-key',
]

const metatags = JSON.parse(document.getElementById('metatags').textContent)
store.commit('setMetatags', _.keyBy(metatags, 'route'))

router.beforeEach((to, from, next) => {
    console.log(this, to)
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // console.log(to, from, next)
        // check if user is not restored yet
        if ((!store.state.user || !store.state.user.id) && store.state.isAuthChecked) {
            if (from && from.fullPath) {
                next({
                    path: from.path,
                    query: {
                        login: true,
                        from: to.fullPath,
                    },
                })
            } else {
                next({
                    path: '/?register&from='+to.fullPath,
                    //query: { redirect: to.fullPath }
                })
            }
            return
        }
    }
    next()
})

try {
    const PayPalButton = paypal.Buttons.driver("vue", Vue);
    Vue.component('paypal-buttons', PayPalButton);
} catch (e) {
    console.log('paypal disabled');
}

new Vue({
    router,
    store,
    render: h => h(MinimalLayout),
    beforeMount: function () {
        let globals = {}
        _.each(availableGlobals, (g) => {
            if (this.$el.attributes[g]) {
                globals[g.substring(5)] = this.$el.attributes[g].value
            }
        })
        store.commit('setGlobals', globals)

        console.log('addEventListener', 'scroll');
        window.addEventListener('scroll', _.debounce(() => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
            if (bottomOfWindow) {
                console.log('triggered', 'endOfPage');
                document.documentElement.dispatchEvent(new Event('endOfPage'))
            }
        }, 250, {leading: true}), {passive: true})

    },
}).$mount('#app')

