<template>
  <v-app id="app">
    <v-navigation-drawer
      v-if="isLoggedIn"
      :value="isLeftDrawerOpened"
      :mini-variant="isLeftDrawerMini"
      :width="160"
      class="left-drawer"
      absolute
      clipped
      app
      @input="(v) => setIsLeftDrawerOpened(v)"
      @update:mini-variant="(v) => setIsLeftDrawerMini(v)"
    >
      <v-list v-if="isTeacherLeftDrawer">
        <v-list-tile>
            <v-list-tile-title>Dashboard</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/profile?main">
            <v-list-tile-title>Collab Set-up</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/profile/teachers/">
            <v-list-tile-title>Edit Hosts</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/membership-setup">
            <v-list-tile-title>Memberships</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/membership-directory">
            <v-list-tile-title>Directory</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/classes?activities">
            <v-list-tile-title>Activities</v-list-tile-title>
        </v-list-tile>
        
        <v-list-tile
            class="list-subitem"
            to="/dashboard/teach/classes?events"
        >
            <v-list-tile-title>Events</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
            class="list-subitem"
            to="/dashboard/teach/classes?classes"
        >
            <v-list-tile-title>Classes</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
            class="list-subitem"
            to="/dashboard/teach/classes?groups"
        >
            <v-list-tile-title>Groups</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
            class="list-subitem"
            to="/dashboard/teach/classes?services"
        >
            <v-list-tile-title>Services</v-list-tile-title>
        </v-list-tile>
    
        <v-list-tile
            @click="redirectToDiscussionPage()"
        >
            <v-list-tile-title >Discussions</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/new_crm">
            <v-list-tile-title>CRM</v-list-tile-title>
        </v-list-tile>
        <v-list-tile to="/dashboard/teach/reports">
            <v-list-tile-title>Reports</v-list-tile-title>
        </v-list-tile>

      </v-list>
      <v-list v-else>
        <v-list-tile>
            <v-list-tile-title>Dashboard</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
          v-if="memberships && memberships.length > 1"
        >
          <v-select
            :value="currentMembershipId"
            :items="membershipOptions"
            class="select__collab-design"
            outline
            @input="setCurrentMembershipId"
          ></v-select>
        </v-list-tile>
        <v-list-tile
          v-if="currentMembershipSetting && currentMembershipSetting.isDirectoryEnabled"
          to="/dashboard/learn/profile"
        >
            <v-list-tile-title>Profile</v-list-tile-title>
        </v-list-tile>
        <v-list-tile 
          v-if="currentMembershipSetting && currentMembershipSetting.isDirectoryEnabled"
          to="/dashboard/learn/classes"
        >
            <v-list-tile-title>Activities</v-list-tile-title>
        </v-list-tile>
        
        <v-list-tile
          v-if="currentMembershipSetting && currentMembershipSetting.isDirectoryEnabled && currentMembershipSetting.isChatEnabled"
          to="/dashboard/learn/chat-setup"
        >
          <v-list-tile-title>Chat Set-Up</v-list-tile-title>
        </v-list-tile>
        <v-list-tile
        v-if="currentMembershipSetting && currentMembershipSetting.isDirectoryEnabled && currentMembershipSetting.isDMEnabled"
          to="/dashboard/learn/chat-discussion"
        >
          <v-list-tile-title>Discussions</v-list-tile-title>
        </v-list-tile>
    
      </v-list>
    </v-navigation-drawer>
    <v-toolbar class="main-toolbar" absolute flat app>
      <v-toolbar-title class="logo-container">
        <router-link v-if="isLearnerDashboard" to="/dashboard/learn" style="text-decoration: none; color: black;font-size: 1.2em;">
        Learning dashboard
        </router-link>
        <a v-else-if="actualLogo.homeUrl" :href="actualLogo.homeUrl">
        <img ref="logoImg" v-if="actualLogo.logoSrc" :alt="actualLogo.logoAlt" :src="actualLogo.logoSrc" style="height:48px;max-width: 100%;" @load="onLoadLogoImg"/>
        </a>
        <router-link v-else-if="actualLogo.logoLink" :to="actualLogo.logoLink" style="text-decoration: none; color: black;">
        <img ref="logoImg" v-if="actualLogo.logoSrc" :alt="actualLogo.logoAlt" :src="actualLogo.logoSrc" style="height:48px;max-width: 100%;" @load="onLoadLogoImg"/>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="search-bar">
        <input type="text" placeholder="search">
        <img src="../../../image/searchicon.png" alt="">
      </div>
     
      <v-toolbar-items class="hidden-md-and-down">
        <a
          class="switch-dashboard-link"
          @click="switchLeftDrawerType"
        >{{ isTeacherLeftDrawer ? "Switch to member" : "Switch to admin" }}</a>
        <v-btn
          v-if="isTeacherLeftDrawer"
          key="addClassBtn"
          dark
          class="add-class-top-btn"
          data-desktop-nav-addclass
          @click="onClickPlusClass"
        >+ Activity</v-btn>
        <v-btn icon flat key="calendar" data-desktop-nav-calendar to="/dashboard/teach/schedule_list">
          <v-icon>calendar_today</v-icon>
        </v-btn>
        <v-btn icon flat key="notifications" data-desktop-nav-notifications to="/dashboard/teach/classes">
          <v-icon>notifications_none</v-icon>
        </v-btn>
        <v-btn icon flat key="settings" data-desktop-nav-settings @click="setIsLeftDrawerOpened(!isLeftDrawerOpened)">
          <v-icon>settings</v-icon>
        </v-btn>
      </v-toolbar-items>
      <v-menu class="hidden-lg-and-up">
        <v-toolbar-side-icon slot="activator" data-mobile-nav-menu-icon></v-toolbar-side-icon>
        <v-list>
          <v-list-tile v-if="actualLogo.homeUrl" @click="openExternalLink(actualLogo.homeUrl)">
          <v-list-tile-content>
              <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-else :to="'/'">
          <v-list-tile-content>
              <v-list-tile-title>Home</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
          <v-list-tile @click="onClickPlusClass">
          <v-list-tile-content>
              <v-list-tile-title>Become an instructor</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-if="isLoggedIn && (!hideTeachAndLearn || isTeacher)" to="/dashboard/teach">
          <v-list-tile-content>
              <v-list-tile-title>Instruct</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-if="isLoggedIn && (!hideTeachAndLearn || isLearner) && !isTeacherOfCompany" to="/dashboard/learn">
          <v-list-tile-content>
              <v-list-tile-title>Learn</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
          <v-list-tile @click="() => onAccountClick(isLoggedIn ? null : {section: 'login'})">
          <v-list-tile-content>
              <v-list-tile-title>{{!isLoggedIn ? 'Log-in' : 'Logout'}}</v-list-tile-title>
          </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>
      <v-btn icon flat key="login" v-if="!isLoggedIn" @click="() => onAccountClick({section: 'login'})" data-desktop-nav-login>
        <v-icon>person_add</v-icon>
      </v-btn>
      <v-btn icon flat key="logout" v-if="isLoggedIn" @click="onAccountClick" data-desktop-nav-logout>
        <v-icon>account_circle</v-icon>
      </v-btn>
    </v-toolbar>
    <v-content app>
      <v-container fluid fill-height>
        <v-layout
          justify-center
          align-start
        >
        <router-view
                v-if="isAuthChecked"
                :city="city"
                :selectedCategory="selectedCategory"
                :category="category"
                :subcategory="subcategory"
                :classesLoaded="classesLoaded"
                v-on:openLoginForm="onAccountClick"
                v-on:register:done="registerDone"
                style="align-items: start;"
        />
        </v-layout>
      </v-container>
    </v-content>

        <v-dialog v-model="loginFormOpened" width="400" persistent>
          <v-card>
            <v-card-title class="headline grey lighten-2" primary-title>
              {{ minRegTitle }}
                <v-spacer></v-spacer>
                <v-btn icon dark @click="() => setLoginFormOpened(null)">
                  <v-icon>close</v-icon>
                </v-btn>
            </v-card-title>
            <v-card-text>
              <reg-min
                v-show="!passwordResetForm"
                :initial-view="minRegFormMode"
                :belongs-to="company && company.id"
                @done="onUserAuth"
                @change="onMinRegChange"
              />
              <div><a v-if="!passwordResetForm" href="javascript:void(0)" @click="() => resetPasswordFormOpen(true)">forgot password?</a></div>
                <div v-if="passwordResetForm">
                  <form>
                    <div v-if="passwordResetSuccess === true">Reset link was sent to your email</div>
                    <div v-else-if="passwordResetSuccess === false">Something went wrong try again</div>
                    <v-text-field
                      v-else
                      v-model.trim="passwordResetEmail"
                      :error-messages="resetPasswordEmailErrors"
                      required
                      @input="$v.passwordResetEmail.$touch()"
                      @blur="$v.passwordResetEmail.$touch()"
                      label="Enter email"
                    ></v-text-field>
                  </form>
                </div>
    
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                v-if="passwordResetForm"
                color="primary"
                flat
                @click="onResetPasswordClick" :disabled="isLoading || passwordResetSuccess">
                Reset password
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="logoutForm" width="400">
          <v-card>
            <v-card-title class="headline grey lighten-2" primary-title>
              Account Info
            </v-card-title>
            <v-card-text>
              <form>
                <div>{{full_name}}</div>
                <div>{{currentEmail}}</div>
    
              </form>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat
                @click="onLogoutClick" :disabled="isLoading">
                Logout
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="isOpenedCompanyTeacherRequestForm" max-width="600">
          <v-card>
            <v-card-title class="headline grey lighten-2" primary-title>
              Apply to Instruct at {{ currentPageCompanyName }}
            </v-card-title>
            <v-card-text>
              <form>
                <v-text-field
                    v-model.trim="teacherRequestName"
                    :error-messages="teacherRequestNameErrors"
                    label="Name"
                    required
                    @input="$v.teacherRequestName.$touch()"
                    @blur="$v.teacherRequestName.$touch()"
                ></v-text-field>
                <v-text-field
                    v-model.trim="teacherRequestAreas"
                    label="Areas of expertise"
                    required
                ></v-text-field>
                <v-text-field
                    v-model.trim="teacherRequestBackground"
                    label="Background"
                    required
                ></v-text-field>
                <v-text-field
                    v-model.trim="teacherRequestEmail"
                    :error-messages="teacherRequestEmailErrors"
                    label="Email"
                    required
                    @input="onTeacherRequestEamailChange"
                    @blur="onTeacherRequestEamailChange"
                ></v-text-field>
                <v-text-field
                    v-model.trim="teacherRequestPhone"
                    :error-messages="teacherRequestPhoneErrors"
                    label="Phone"
                    required
                    @input="$v.teacherRequestPhone.$touch()"
                    @blur="$v.teacherRequestPhone.$touch()"
                ></v-text-field>
              </form>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat
                :loading="isLoadingCompanyProfile"
                @click="sendTeacherRequest" :disabled="isLoadingCompanyProfile">
                {{ teacherRequestBtnLabel }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-app>
</template>
    
<script>
import _ from 'lodash'

import { mapState, mapActions, mapMutations, mapGetters } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, requiredIf, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import { VIEWING_COMPANY_STATES } from '@/store/modules/viewingCompany'
import RegMin from '@/components/basic/forms/RegMin'
import companyService from '@/lib/services/company'
import Snack from '@/components/basic/Snack'
import { defaultLogoSrc, defaultLogoAlt } from '@/store/index';
import CompanyNavBar from '@/components/basic/CompanyNavBar';
import { LEFT_DRAWER_TYPE } from '@/store/modules/layout';

export default {
    mixins: [validationMixin],

    validations: {
        email: { required, email },
        passwordResetEmail: { required, email },
        password: { required},
        teacherRequestName: { required },
        teacherRequestEmail: { required },
        teacherRequestPhone: { required: requiredIf((model) => !model.teacherRequestEmail) },
        teacherRequestValidationGroup: ['teacherRequestName', 'teacherRequestEmail', 'teacherRequestPhone'],
    },
    components: {
        Snack,
        RegMin,
        CompanyNavBar,
    },
    data: function () {
        return {
            //loginForm: false,
            logoutForm: false,
            email: '',
            password: '',
            isLoading: false,
            passwordResetForm: false,
            passwordResetEmail: '',
            passwordResetSuccess: null,
            city: {
                address_city: 'all',
                address_state: 'all',
            },
            //citiesList: [],
            classesLoaded: [],
            loginError: null,
            registerLink: false,
            category: '',
            subcategory: '',
            //categoriesSelected: {}
            categoryMenuVisible: false,
            categoryBtnStyle: {
                'width': '100%',
                'word-break': 'break-word',
                'white-space': 'normal',
                'line-height': '1em',
                'font-family': 'Montserrat, sans-serif',
                'font-weight': '500',
                'font-size': '14px',
                'color': 'rgba(0,0,0,0.87)',
            },
            subcategoryCountInColumn: 13,
            //isLoggedIn: false,
            savedRedirect: null,
            autocompleteMenuProps: {
                "closeOnClick":false,
                "closeOnContentClick":false,
                "openOnClick":false,
                "maxHeight":200,
                "top": true,
                "attach": '.type-autocomplete'
            },
            isAlreadyRegisterOpened: false,
            typeAutocompleteInput: '',
            isTeacherDashboardLoading: false,
            topTeachBtnActive: false,
            isOpenedCompanyTeacherRequestForm: false,
            teacherRequestName: '',
            teacherRequestAreas: '',
            teacherRequestBackground: '',
            teacherRequestEmail: '',
            teacherRequestPhone: '',
            minRegFormMode: 'register',
            drawer: true,
            mini: false,
        }
    },
    created() {

        axios.interceptors.response.use((response) => {
            return response
        }, (error) => {
            console.log('intercepted', error)
            if([400].includes(error.response.status)) {
                // ignore this headers used in custom errors processing
                return Promise.reject(error)
            }
            if(error.response.status === 401) {
                this.$store.commit('setUser', null)
                this.$router.push('/?login&from='+this.$route.fullPath)
                return Promise.reject(error)
            }
            if(error.response.status >= 500) {
                this.globalError = 'Server error, try again later'
            } else if(error.response.status >= 400) {
                this.globalError = 'Something went wrong, try again later'
            }
            return Promise.reject(error)
        })
        //console.log(this.$route)
        this.processOpenLoginRoute(this.$route)
        if('city' in this.$route.params) {
            this.city = {
                address_city: this.$route.params.city,
                address_state: this.$route.params.state
            }
        }
        if('category' in this.$route.params && Number(this.$route.params.category)) {
            this.category = Number(this.$route.params.category)
        }
        if('subcategory' in this.$route.params && Number(this.$route.params.subcategory)) {
            this.subcategory = Number(this.$route.params.subcategory)
        }
        this.restoreUser()
    },
    mounted() {

    },
    methods: {
        ...mapMutations([
            'setLoginFormOpened',
            'setIsAuthChecked',
            'setGlobalError',
            'viewingCompany/setError',
            'viewingCompany/setStatus',
            
        ]),
        ...mapMutations('layout', [
          'setIsLeftDrawerOpened',
          'setIsLeftDrawerMini',
        ]),
        ...mapMutations('learnerMembership', [
          'setCurrentMembershipId',
        ]),
        ...mapActions('viewingCompany', [
            'sendCompanyTeacherRequest',
        ]),
        ...mapActions([
            'loadBelongingCompanyProfile',
        ]),
        ...mapActions('chatDiscussion',['loadRecentDiscussion','setDiscussionId', 'initiateChat']),
        resetPasswordFormOpen(open) {
            if (open) {
                this.passwordResetForm = true;
                this.passwordResetSuccess = null;
            } else {
                this.passwordResetForm = false;
            }
        },
        onTeacherRequestEamailChange() {
            this['viewingCompany/setError'](null);
            this.$v.teacherRequestEmail.$touch();
        },
        onClickPlusClass() {
            if (!this.isLoggedIn && (this.$route.name === 'company_profile_slug' || this.$route.name === 'company_profile')) this.isOpenedCompanyTeacherRequestForm = true;
            else this.$router.push('/teachers/light-register');
        },
        sendTeacherRequest() {
            if (this.status === VIEWING_COMPANY_STATES.SAVED) {
                this.isOpenedCompanyTeacherRequestForm = false;
                return;
            }
            this.$v.$touch()
            if (this.$v.teacherRequestValidationGroup.$anyError)
                return;
            let timezone = 'America/New_York';
            try {
                timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            } catch (e) {}

            this.sendCompanyTeacherRequest({
                name: this.teacherRequestName,
                first_name: this.teacherRequestName.split(' ')[0],
                last_name: this.teacherRequestName.split(' ')[1] || '',
                areas: this.teacherRequestAreas,
                background: this.teacherRequestBackground,
                email: this.teacherRequestEmail,
                phone: this.teacherRequestPhone,
                company_id: this.company.id,
                timezone,
            }).then(() => {
                if (this.status === VIEWING_COMPANY_STATES.ERROR) {
                    this.globalError = 'Server error, check the form fields';
                } else if (this.status === VIEWING_COMPANY_STATES.SAVED) {
                    this.$router.push('/teachers/start')
                }
            });
        },
        registerDone() {
            //console.log('update login button')
            //this.user = this.$store.state.user
        },
        changeCity(city) {
            this.city = city
            this.searchClasses(this.subcategory, this.category)
        },
        searchClasses(scId=null, cId=null) {
            this.subcategory = scId
            this.category = cId
            this.categoryMenuVisible = false
            console.log(this.category, this.subcategory, this.city)
            if(!this.city)
                return
            if(this.city === 'online') {
                this.$router.push(`/learners/search/online/none/${this.category || '0'}/${this.subcategory || ''}`)
            } else {
                this.$router.push(`/learners/search/${this.city.address_city}/${this.city.address_state}/${this.category || '0'}/${this.subcategory || ''}`)
            }
        },
        onAccountClick: function (event) {
            this.isLoading = false
            if (!this.$store.state.user || !Object.keys(this.$store.state.user).length) {
                if(event && event.register === 'close') {
                    this.isAlreadyRegisterOpened = true
                } else {
                    this.isAlreadyRegisterOpened = false
                }
                if (event && event.section === 'login') {
                    this.minRegFormMode = 'login';
                } else {
                    this.minRegFormMode = 'register';
                }
                this.setLoginFormOpened({})
            } else {
                this.logoutForm = true
            }
        },
        onLogoutClick: function () {
            this.isLoading = true
            axios.post('/api/auth/logout/').then((logoutRes) => {
                console.log(logoutRes)
                if (this.$store.state.lastLesson) {
                    const classId = this.$store.state.lastLesson.klass;
                    const companyId = this.$store.state.lastLesson.data['class'] && 
                        this.$store.state.lastLesson.data['class'].teacher.user.company_profile && 
                        this.$store.state.lastLesson.data['class'].teacher.user.company_profile.slug
                    this.$nextTick(() => {
                        if (companyId) this.$router.push(`/company/${companyId}`);
                        else this.$router.push(`/class/${classId}`);
                    });
                }
                this.$store.commit('logout')
                //this.$router.go()
                this.logoutForm = false
                this.checkAuth()
            }).catch(() => {
                //console.log('err!', arguments)
            }).then(() => {
                this.isLoading = false
            })
        },
        async restoreUser() {
            const hs = await axios.get('/api/handshake/')
            if(hs.data.is_authenticated) {
                const init = await axios.get('/api/init/')
                await this.$store.dispatch('setInitialdata', init)
                if (init.data.user.belongs_to) {
                    // load company profile and set it's logo
                    await this.loadBelongingCompanyProfile(init.data.user.belongs_to);
                }
            }
            if(this.isLoggedIn && this.loginFormOpened) {
                // close login since already logged in
                this.setLoginFormOpened(null)
            }
            this.checkAuth()
            this.$store.commit('setIsAuthChecked', true)
            return true
        },
        checkAuth() {
            if(!this.isLoggedIn && this.$route.matched.some(v => v.meta.requiresAuth)) {
                // redirect to login
                this.$router.push('/?login&from='+this.$route.fullPath)
            }
        },
        onUserAuth() {
            // login or register
            this.setLoginFormOpened(null)
            if(this.savedRedirect) {
                this.$router.push(this.savedRedirect)
                this.savedRedirect = null
            }
        },
        onMinRegChange(event) {
            if (event.mode) {
                this.minRegFormMode = event.mode;
            }
        },
        onLoginClick: function () {
            this.loginError = ''
            this.registerLink = false
            this.isLoading = true
            axios.get('/api/handshake/').then((initial) => {
                const params = new URLSearchParams();
                params.append('username', this.email)
                params.append('password', this.password)
                params.append('csrftoken', initial.data.csrftoken)
                return axios.post('/api/auth/login/', params)
            }).catch((loginRes) => {
                console.log('err!', loginRes)
                if(loginRes.response.data.not_exist) {
                    this.registerLink = true
                    this.loginError = 'Whoops! We don’t have that name please, register '
                } else
                    this.loginError = 'Password incorrect, try again or reset'
                this.isLoading = false
            }).then((loginRes) => {
                console.log(loginRes)
                if(!loginRes)
                    return
                return this.restoreUser()
            }).then(res => {
                if(!res)
                    return
                //this.$store.dispatch('setInitialdata', res)
                //this.user = this.$store.state.user
                this.setLoginFormOpened(null)
                if(this.savedRedirect) {
                    this.$router.push(this.savedRedirect)
                    this.savedRedirect = null
                }
            }).catch(e => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
            })
        },
        onResetPasswordClick() {
            this.$v.$touch()
            if (this.$v.passwordResetEmail.$anyError)
                return
            this.isLoading = true
            axios.post('/api/user/reset_password/', {
                email: this.passwordResetEmail
            }).then((resetRes) => {
                console.log(resetRes)
                if(resetRes.data.success) {
                    this.passwordResetSuccess = true
                } else {
                    this.passwordResetSuccess = false
                }
            }).catch(() => {
                //console.log(arguments)
                this.passwordResetSuccess = false
            }).then(() => {
                this.isLoading = false
            })
        },
        clickRegister() {
            this.setLoginFormOpened(null)
            this.loginError = ''
            if(!this.isAlreadyRegisterOpened) {
                this.registerLink = false
                this.isLoading = true
                this.$router.push({path: '/register'})
            }

        },
        processOpenLoginRoute(route) {
            if('login' in route.query || 'register' in route.query) {
                this.minRegFormMode = 'login' in route.query ? 'login' : 'register';
                this.setLoginFormOpened({})
                if('from' in route.query) {
                    this.savedRedirect = route.query['from']
                }
                this.$router.replace(this.$route.path)
            }
        },
        async onTeacherDashboardClick() {
            if(/\/dashboard\/teach/.test(this.$route.path) || this.isTeacherDashboardLoading)
                return
            this.isTeacherDashboardLoading = true
            const {data: preloaded} = await axios.get('/api/teacher_dashboard_preload/')
            this.isTeacherDashboardLoading = false
            if(preloaded.upcoming) {
                return this.$router.push('/dashboard/teach/schedule_list?filter=upcoming')
            }
            /*
            // disabled by Alisa's request
            if (preloaded.previous) {
                return this.$router.push('/dashboard/teach/schedule_list?filter=previous')
            }
            */
            return this.$router.push('/dashboard/teach/classes')
        },
        onLoadLogoImg(event) {
            this.$store.commit('setLogoDimensions', {
                width: event.currentTarget.width,
                height: event.currentTarget.height,
            })
        },
        switchLeftDrawerType() {
          this.$router.push(this.isTeacherLeftDrawer ? '/dashboard/learn' : '/dashboard/teach' );
        },
        redirectToDiscussionPage() { 
            this.loadRecentDiscussion().then(async(res) => { 
                if (res.status === 200) { 
                    await this.setDiscussionId(res.data.id)
                    await this.initiateChat(res.data.id)
                    this.$router.push({path:'/dashboard/teach/teacher-chat-discussion'})
                }
            })
        }
    },
    computed: {
        ...mapGetters([
            'isLoggedIn',
            'showClassCompanyName',
            'isTeacher',
            'isLearner',
            'isTeacherOfCompany',
        ]),
        ...mapState('viewingCompany', [
            'company',
            'status',
            'error',
        ]),
        ...mapState('layout', [
            'isLeftDrawerOpened',
            'isLeftDrawerMini',
        ]),
        ...mapGetters('learnerMembership', [
            'currentMembership',
            'currentMembershipSetting',
        ]),
        ...mapState('learnerMembership', [
            'memberships',
            'membershipSettings'
        ]),
        ...mapState([
            'loginFormOpened',
            'isAuthChecked',
            'logoCompanyProfile',
            'belongingCompanyProfile',
            'isLogoCompanyProfileChecked',
        ]),
        membershipSettingsDict() {
          return this.membershipSettings ? this.membershipSettings.reduce((acc, v) => ({...acc, [v.id]: v}), {}) : {};
        },
        membershipOptions() {
          return this.memberships ? this.memberships.map(v => ({value: v.id, text: this.membershipSettingsDict[v.membership].name})) : [];
        },
        leftDrawerType() {
            if (this.$route.path.includes("/dashboard/teach")) return LEFT_DRAWER_TYPE.TEACH;
            return LEFT_DRAWER_TYPE.LEARN
        },
        isTeacherLeftDrawer() {
          return this.leftDrawerType === LEFT_DRAWER_TYPE.TEACH
        },
        actualLogo() {
            const pathMatch = /(learners_step|classpage|teacher_classes|teacher_profile|company_membership|buy_membership|company_profile|dashboard|company_group_calendar|company_classes_group_slug|teachers_start|teachers_class)/.test(this.$route.name);
            const defaultRes = {
                'logoAlt': defaultLogoAlt,
                'logoSrc': defaultLogoSrc,
                'logoLink': '/',
                'homeUrl': '',
                'classCompanyName': '',
            };
            if (this.belongingCompanyProfile && this.belongingCompanyProfile.replace_logo) {
                return {
                    'logoAlt': this.belongingCompanyProfile.name,
                    'logoSrc': this.belongingCompanyProfile.media,
                    'logoLink': companyService.getLink(this.belongingCompanyProfile),
                    'homeUrl': this.belongingCompanyProfile.home_url,
                    'classCompanyName': this.belongingCompanyProfile.name,
                }
            }
            if (!this.isLogoCompanyProfileChecked && pathMatch) {
                return {
                    'logoAlt': null,
                    'logoSrc': null,
                    'logoLink': null,
                    'homeUrl': null,
                    'classCompanyName': null,
                }
            }
            if (this.logoCompanyProfile && this.logoCompanyProfile.replace_logo && pathMatch) {
                return {
                    'logoAlt': this.logoCompanyProfile.name,
                    'logoSrc': this.logoCompanyProfile.media,
                    'logoLink': companyService.getLink(this.logoCompanyProfile),
                    'homeUrl': this.logoCompanyProfile.home_url,
                    'classCompanyName': this.logoCompanyProfile.name,
                }
            }
            return defaultRes;
        },
        minRegTitle() {
            return this.minRegFormMode === 'login' ? 'Please Login' : 'Looks like you’re new here!';
        },
        isTeacherDashboard() {
            return this.$route.path.includes('dashboard/teach');
        },
        isLearnerDashboard() {
            return this.$route.path.includes('dashboard/learn');
        },
        teacherRequestBtnLabel() {
            return this.status === VIEWING_COMPANY_STATES.SAVED ? 'Great!' : 'Save';
        },
        teacherRequestNameErrors() {
            const errors = []
            if (!this.$v.teacherRequestName.$dirty) return errors
            !this.$v.teacherRequestName.required && errors.push('Name is required')
            return errors
        },
        teacherRequestEmailErrors() {
            if (this.error && typeof this.error === 'object' && 'email' in this.error) {
                return this.error.email;
            }
            const errors = [];
            if (!this.$v.teacherRequestEmail.$dirty) return errors;
            !this.$v.teacherRequestEmail.required && errors.push('Email or Phone is required');
            return errors;
        },
        teacherRequestPhoneErrors() {
            const errors = []
            if (!this.$v.teacherRequestPhone.$dirty) return errors
            !this.$v.teacherRequestPhone.required && errors.push('Email or Phone is required')
            return errors
        },
        currentPageCompanyName() {
            return this.company && (this.company.title || this.company.name);
        },
        isLoadingCompanyProfile() {
            return this.status === VIEWING_COMPANY_STATES.LOADING;
        },
        globalError: {
            set(v) {
                this.setGlobalError(v)
            },
            get() {
                return this.$store.state.globalError
            }
        },
        first_name() {
            return this.$store.state.user && this.$store.state.user.first_name
        },
        last_name() {
            return this.$store.state.user && this.$store.state.user.last_name
        },
        currentEmail() {
            return this.$store.state.user && this.$store.state.user.email
        },
        isLoggedIn() {
            return this.$store.state.user && Object.keys(this.$store.state.user).length
            //return this.user && Object.keys(this.user).length
        },
        hideTeachAndLearn() {
            return this.$route.name === 'classpage' || this.$route.name === 'company_profile'
        },
        selectedCategory() {
            console.log(this.category)
            return {

            }
        },
        full_name: function () {
            return this.first_name+' '+this.last_name
        },
        emailErrors () {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.required && errors.push('Login(Email) is required')
            return errors
        },
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('Password is required')
            return errors
        },
        resetPasswordEmailErrors () {
            const errors = []
            if (!this.$v.passwordResetEmail.$dirty) return errors
            !this.$v.passwordResetEmail.email && errors.push('Must be valid e-mail')
            !this.$v.passwordResetEmail.required && errors.push('Email is required')
            return errors
        },
        isCompanyProfilePage() {
            const matched_routes = [
                'company_profile',
                'company_profile_slug',
                'company_classes_group_slug',
                'classpage',
            ];
            return matched_routes.includes(this.$route.name) && this.companySlug;
        },
        companySlug() {
            if (this.$route.name === 'classpage') return this.company && this.company.id;
            return this.$route.params.slug || this.$route.params.id;
        },
    },
    watch: {
        city(newCity) {

        },
        loginFormOpened(newVal, oldVal) {
            if(!newVal) {
                this.passwordResetSuccess = null
                this.passwordResetForm = false
            }
        },
        '$route' (to, from) {
            console.log(to, from)
            if(/\/dashboard\/teach/.test(to.path)) {
                this.topTeachBtnActive = true
            } else {
                this.topTeachBtnActive = false
            }
            this.processOpenLoginRoute(to)
        },
        isOpenedCompanyTeacherRequestForm(v, old) {
            if (!v && old) {
                this['viewingCompany/setStatus'](VIEWING_COMPANY_STATES.IDLE);
            }
        },
    }
}
</script>

<style lang="scss">
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    font-size: 17px;
    overflow: hidden;
    .main-toolbar {
        z-index: 12;
        height: 64px;
        background-color: white;
        .add-class-top-btn {
          background-color: #434343;
          color: #ffffff;
          margin-right: 40px;
          height: 32px;
        }
    }
    .left-drawer {
        width: 156px;
        display: flex;
        flex-flow: column;
        background-color: #434343;
        
        .v-list__tile__title {
            color: #ffffff;
            font-size: 18px;
        }
        .collapse-drawer-container {
          text-align: end;
          padding-right: 15px;
        }
        .v-list__tile--active {
          background: #F5F5F5;
          .v-list__tile__title {
            color: #262626;
            font-weight: bold;
          }
        }
        .list-subitem {
            .v-list__tile__title {
                padding-left: 2em;
            }
        }
    }
    .logo-container {
      position: absolute;
      left: 24px;
    }
}
.switch-dashboard-link {
  align-self: center;
  margin-right: 1em;
}
.search-bar{
    width: 71%;
    display: flex;
    margin-right: 79px;
    position: relative;
}
.search-bar input{
    border: 1px solid #D9D9D9;
    width: 344px;
    height: 40px;
    padding: 2px 5px;
    outline: none;
}
.search-bar img{
    position: absolute;
    top: 5px;
    left: 309px;
    cursor: pointer;
}
</style>
