<template>
    <div class="t-wrapper">
        <v-layout align-top justify-center row wrap class="t-container">
            <v-flex xs12 class="text-xs-left">
                <div class="top-head">Start Selling Live Lessons In Minutes</div>
            </v-flex>
            <v-flex xs7 class="text-xs-left">
                <div class="sub-head">You Do You. We Automate The Rest.<br/>What Teachers Love:</div>
                <v-layout align-top justify-center row wrap>
                    <v-flex xs12 lg6 class="text-xs-left t-small-text">
                        <ul>
                            <li><span class="t-icon">✓</span>No credit card fees</li>
                            <li><span class="t-icon">✓</span>No revenue share</li>
                            <li><span class="t-icon">✓</span>On or off your website</li>
                            <li><span class="t-icon">✓</span>Unlimited students</li>
                            <li><span class="t-icon">✓</span>Take appointments online</li>
                            <li><span class="t-icon">✓</span>Online payments</li>
                            <li><span class="t-icon">✓</span>Group or private</li>
                        </ul>
                    </v-flex>
                    <v-flex xs12 lg6 class="text-xs-left t-small-text">
                        <ul>
                            <li><span class="t-icon">✓</span>Workshop or ongoing</li>
                            <li><span class="t-icon">✓</span>Sync to private calendar</li>
                            <li><span class="t-icon">✓</span>Automated reminders</li>
                            <li><span class="t-icon">✓</span>Marketing support</li>
                            <li><span class="t-icon">✓</span>Stores student contracts</li>
                            <li><span class="t-icon">✓</span>Online or in/person</li>
                            <li><span class="t-icon">✓</span>Launches FaceTime and Zoom</li>
                        </ul>
                    </v-flex>

                </v-layout>
                <div class="bottom-sub-head">Just $5 per month</div>

            </v-flex>
            <v-flex xs5 class="text-xs-left">
                <div class="white--text t-form-wrapper">
                  <div class="headline">
                    ADD A CLASS NOW
                  </div>
                        <form v-if="mode === 'register'">
                            <v-text-field
                              name="class_name"
                              v-model.trim="className"
                              :error-messages="classNameErrors"
                              :counter="30"
                              label="Class Title"
                              required
                              @input="$v.className.$touch()"
                              @blur="$v.className.$touch()"
                              outline
                            ></v-text-field>
                            <v-text-field
                              name="email"
                              v-model.trim="email"
                              :error-messages="emailErrors"
                              label="Your Email"
                              required
                              @input="$v.email.$touch()"
                              @blur="$v.email.$touch()"
                              outline
                            >
                                <template v-slot:message="{message}">
                                    <div class="v-messages theme--light error--text" style="text-align: left;">{{message}}<span v-if="showLoginLink">, Try to <a @click="openLoginForm">login</a></span></div>
                                </template>
                            </v-text-field>

                            <v-text-field
                              name="password"
                              browser-autocomplete="new-password"
                              v-model="password"
                              :error-messages="passwordErrors"
                              counter
                              type="password"
                              label="Password"
                              required
                              @input="$v.password.$touch()"
                              @blur="$v.password.$touch()"
                              outline
                            ></v-text-field>
                            <v-text-field
                              name="phone"
                              v-model.trim="phone"
                              :error-messages="phoneErrors"
                              label="Phone Number"
                              required
                              @input="$v.phone.$touch()"
                              @blur="$v.phone.$touch()"
                              outline
                            ></v-text-field>
                        </form>
                      <form v-else>
                          <snack v-model="loginError"></snack>
                          <div style="margin: -1.2em 0 0 0; line-height: 1.2em;">or <a @click="openRegisterForm">register</a></div>
                          <v-text-field
                              v-model.trim="login"
                              :error-messages="loginErrors"
                              label="Login (Email)"
                              required
                              @input="$v.login.$touch()"
                              @blur="$v.login.$touch()"
                              outline
                          ></v-text-field>
                          <v-text-field
                              v-model="password"
                              :error-messages="passwordErrors"
                              counter
                              type="password"
                              label="Password"
                              required
                              @input="$v.password.$touch()"
                              @blur="$v.password.$touch()"
                              outline
                          ></v-text-field>
                      </form>
                    <v-btn block @click="submit" class="platform-green" :loading="isLoading" :disabled="isLoading">Submit</v-btn>
                </div>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
import _ from 'lodash'
import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import { mapGetters } from 'vuex'

export default {
    mixins: [validationMixin],
    name: 'teachers_promo',
    components: {

    },
    validations: {
        className: { required, maxLength: maxLength(300) },
        login: { required, email },
        email: { required, email },
        phone: { maxLength: maxLength(20) },
        password: { required, minLength: minLength(8) },
    },
    data: () => ({
        className: '',
        email: '',
        phone: '',
        password: '',
        nextRoute: '/teacher_check/',
        errors: {},
        isLoading: false,
        mode: 'register',
        loginError: '',
        showLoginLink: false,
    }),
    created: function () {
        if(this.isLoggedIn) {
            return this.$router.push(this.nextRoute)
        }
    },
    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        loginErrors() {
            const errors = []
            if (!this.$v.login.$dirty) return errors
            !this.$v.login.email && errors.push('Must be valid e-mail')
            !this.$v.login.required && errors.push('email is required.')
            return errors
        },
        classNameErrors() {
            const errors = []
            if (!this.$v.className.$dirty) return errors
            !this.$v.className.maxLength && errors.push('Class Name must be at most 300 characters long')
            !this.$v.className.required && errors.push('Class Name is required.')
            return errors
        },
        emailErrors () {
            if (this.errors.email) {
                return this.errors.email
            }
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.email && !this.phone && errors.push('E-mail or Phone is required')
            return errors
        },
        phoneErrors () {
            if (this.errors.phone) {
                return this.errors.phone
            }
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            //!this.phone && !this.email && errors.push('Phone or E-mail is required')
            return errors
        },
        passwordErrors () {
            if (this.errors.password) {
                return this.errors.password
            }
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.required && errors.push('Password is required.')
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters long')
            return errors
        },
    },
    methods: {
        openRegisterForm() {
            this.mode = 'register'
        },
        openLoginForm() {
            this.login = this.email
            this.mode = 'login'

        },
        submitLogin() {
            if (this.$v.login.$anyError || this.$v.password.$anyError)
                return
            this.loginError = ''
            this.isLoading = true
            axios.get('/api/handshake/').then((initial) => {
                const params = new URLSearchParams();
                params.append('username', this.login)
                params.append('password', this.password)
                params.append('csrftoken', initial.data.csrftoken)
                return axios.post('/api/auth/login/', params)
            }).catch(e => {
                console.log('err!', e)
                if(e.response.data.not_exist) {
                    this.loginError = 'Whoops! We don’t have that name please, register '
                } else
                    this.loginError = 'Password incorrect, try again or reset'
                this.isLoading = false
                return e
            }).then(() => {
                return axios.get('/api/init/')
            }).then((res) => {
                this.$store.dispatch('setInitialdata', res)
                this.$store.commit('setGroupClass', {
                    groupClassName: this.className,
                    privateClassName: this.className,
                })
                this.$router.push(this.nextRoute)
            }).catch(e => {
                console.log('final', e)
            }).finally(() => {
                this.isLoading = false
            })
        },
        submit() {
            if(this.mode === 'login')
                return this.submitLogin()
            this.$v.$touch()
            console.log('submit', this, arguments)
            this.errors = {}
            if (this.$v.className.$anyError || this.$v.email.$anyError || this.$v.phone.$anyError || this.$v.password.$anyError)
                return
            this.isLoading = true
            axios.post('/api/users/', {
                email: this.email,
                phone: this.phone,
                password: this.password,
                alerts: !!this.phone,
                is_basic_data: true,
            }).catch((err) => {
                ///handle errors
                if (err.response.data) {
                    let errs = {}
                    _.each(err.response.data, (v, k) => {
                        if(k === 'email' && v.indexOf("User with this email already exists") !== -1) {
                            this.showLoginLink = true
                        }
                        errs[k] = v
                    })
                    this.errors = errs
                }
                return err
            }).then((res) => {

                this.$store.commit('setUser', _.omit(res.data, 'password'))
                this.email = res.data.email
                return axios.get('/api/handshake/')
            }).then((initial) => {
                const params = new URLSearchParams();
                params.append('username', this.email)
                params.append('password', this.password)
                params.append('csrftoken', initial.data.csrftoken)
                return axios.post('/api/auth/login/', params)
            }).then((loginRes) => {
                    //console.log(loginRes)
                this.$store.commit('setGroupClass', {
                    groupClassName: this.className,
                    privateClassName: this.className,
                })
                this.$router.push(this.nextRoute)
            }).catch((e) => {
                console.log('err!', arguments)
                this.$emit('error', e)
            }).finally(() => {
                this.isLoading = false
            })
        }
    }
}
</script>
<style scoped lang="scss">
// this is for production, since by default webpack module configuration option don't go to vue config
@import "@/styles/_variables.scss";

.t-wrapper {
    background-color: $platform-green;
    height: 100%;
    .t-container {
        padding: 20px;
        border-top-right-radius: 60px;
        border-bottom-left-radius: 60px;
        background-color: white;

        .t-small-text {
            padding: 0 20px;
        }

        li {
            list-style: none;
            .t-icon {
                margin: 0 5px;
                color: $platform-green;
            }
        }
    }
    .top-head {
        font-size: 53px;
        font-weight: 900;
        margin: 20px;
    }
    .sub-head {
        font-size: 31px;
        font-weight: 900;
        margin: 0 20px;
    }
    .bottom-sub-head {
        font-size: 48px;
        font-weight: 900;
        text-transform: uppercase;
        margin: 20px;
    }
    .t-form-wrapper {
        background-color: $platform-blue;
        border-top-right-radius: 50px;
        border-bottom-left-radius: 50px;
        padding: 30px 40px;

        .headline {
            font-size: 48px;
            font-weight: 900;
            text-transform: uppercase;
            margin-bottom: 30px;
        }

        .v-text-field .v-input__control .v-input__slot {
            background-color: white !important;
            border: 2px solid white;
        }
    }
}
</style>
<style lang="scss">
.t-wrapper {
    .t-form-wrapper {
        .v-text-field .v-input__control .v-input__slot {
            background-color: white !important;
            border: 2px solid white;
            &:hover {
                border: 2px solid rgba(31,191,215, 0.3);
            }
        }
        .theme--light.v-text-field--outline:not(.v-input--is-focused):not(.v-input--has-state)>.v-input__control>.v-input__slot:hover{
            border: 2px solid rgba(31,191,215, 0.3);
        }
    }
}
</style>