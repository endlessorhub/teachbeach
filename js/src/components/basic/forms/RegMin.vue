<template>
  <form v-if="mode === 'register'">
      <div style="margin: -10px;">or <a @click="openLoginForm">login</a></div>
    <v-text-field
      name="first_name"
      v-model.trim="first_name"
      :error-messages="firstNameErrors"
      :counter="30"
      label="Name"
      required
      @input="$v.first_name.$touch()"
      @blur="$v.first_name.$touch()"
    ></v-text-field>
    <v-text-field
      name="email"
      v-model.trim="email"
      :error-messages="emailErrors"
      label="Email Address"
      required
      @input="$v.email.$touch()"
      @blur="$v.email.$touch()"
    ></v-text-field>
      <div v-if="showLoginLink" class="v-messages theme--light error--text" style="text-align: left;">Try to <a @click="openLoginForm">login</a></div>
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
    ></v-text-field>
    <v-text-field
      name="phone"
      v-model.trim="phone"
      :error-messages="phoneErrors"
      label="Phone Number"
      required
      @input="$v.phone.$touch()"
      @blur="$v.phone.$touch()"
    ></v-text-field>
      <div v-if="teacherPhone">Or call teacher <a :href="`tel:${teacherPhone}`">{{teacherPhone}}</a></div>
    <v-btn @click="submit" class="platform-aqua" :loading="isLoading" :disabled="isLoading">GO</v-btn>
    <v-alert
      :value="true"
      color="info"
      icon="info"
      outline
    >
      {{alertText}}
    </v-alert>
  </form>
  <form v-else>
      <snack v-model="loginError"></snack>
      <div style="margin: -10px;">Login or <a @click="openRegisterForm">register</a></div>
      <v-text-field
          v-model.trim="login"
          :error-messages="loginErrors"
          label="Login (Email)"
          required
          @input="$v.login.$touch()"
          @blur="$v.login.$touch()"
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
      ></v-text-field>
    <v-btn @click="submitLogin" class="platform-aqua" :loading="isLoading" :disabled="isLoading">Login</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import Snack from '@/components/basic/Snack'

export default {
    mixins: [validationMixin],

    components: {
        Snack,
    },

    validations: {
        first_name: { required, maxLength: maxLength(30) },
        email: { required, email },
        login: { required, email },
        phone: { maxLength: maxLength(20) },
        password: { required, minLength: minLength(8) },
    },

    props: {
        class_id: Number,
        belongsTo: Number,
        teacherPhone: String,
        alertText: {
            type: String,
            default: 'You may receive sms of new classes in categories you select',
        },
        initialView: {
            type: String,
            default: 'register',
        }
    },

    data: function () {
        return {
            login: '',
            first_name: this.$store.state.user ? this.$store.state.user.first_name : '',
            email: this.$store.state.user ? this.$store.state.user.email : '',
            phone: this.$store.state.user ? this.$store.state.user.phone : '',
            password: '',
            alerts: false,
            isLoading: false,
            errors: {},
            showLoginLink: false,
            terms: false,
            privacy: false,
            mode: 'register',
            loginError: '',
        }
    },

    created: function () {
        if (this.$store.state.learnerData) {
            this.alerts = this.$store.state.learnerData.alerts
        }
        this.mode = this.initialView;
    },

    computed: {
        loginErrors() {
            const errors = []
            if (!this.$v.login.$dirty) return errors
            !this.$v.login.email && errors.push('Must be valid e-mail')
            !this.$v.login.required && errors.push('email is required.')
            return errors
        },
        firstNameErrors () {
            if (this.errors.first_name) {
                return this.errors.first_name
            }
            const errors = []
            if (!this.$v.first_name.$dirty) return errors
            !this.$v.first_name.maxLength && errors.push('Name must be at most 100 characters long')
            !this.$v.first_name.required && errors.push('Name is required.')
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

    watch: {
        initialView(v) {
            this.mode = v;
        },
    },

    methods: {
        openRegisterForm() {
            this.mode = 'register'
            this.$emit('change', { mode: 'register' })
        },
        openLoginForm() {
            this.mode = 'login'
            this.$emit('change', { mode: 'login' })
        },
        back() {
            this.$emit('cancelled')
        },
        next() {
            //this.$emit('update:step', 4)
        },
        submit () {
            this.$v.$touch()
            console.log('submit', this, arguments)
            this.showLoginLink = false
            this.errors = {}
            if (this.$v.first_name.$anyError || this.$v.email.$anyError || this.$v.phone.$anyError || this.$v.password.$anyError)
                return
            axios.post('/api/users/', {
                first_name: this.first_name,
                email: this.email,
                phone: this.phone,
                password: this.password,
                alerts: !!this.phone,
                class_id: this.class_id,
                belongs_to: this.belongsTo,
                is_company: !this.belongsTo,
            }).catch((err) => {
                ///handle errors
                this.isLoading = false
                if (err.response.data) {
                    let errs = {}
                    _.each(err.response.data, (v, k) => {
                        if(k == 'email' && v.indexOf("User with this email already exists") != -1) {
                            this.showLoginLink = true
                        }
                        errs[k] = v
                    })
                    this.errors = errs
                }
                throw err
            }).then((res) => {
                //console.log(arguments)
                //res.data.user.id
                fbq('trackCustom', 'studentRegistration')
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
                this.isLoading = false
                if(this.onSuccess) {
                    this.onSuccess.call(this)
                } else
                    this.$emit('done')
            }).catch((e) => {
                console.log('err!', arguments)
                this.$emit('error', e)
                this.isLoading = false
            })
            /*
            this.$store.commit('setLearnerData', {
                first_name: this.first_name,
                email: this.email,
                phone: this.phone,
                alerts: this.alerts,
            })
            this.$emit('next:step')
            */
        },
        clear () {
            this.$v.$reset()
            this.first_name = ''
            this.last_name = ''
            this.email = ''
            this.phone = ''
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
                throw e
            }).then(() => {
                return axios.get('/api/init/')
            }).then((res) => {
                this.$store.dispatch('setInitialdata', res)
                this.isLoading = false
                this.$emit('done')
            }).catch(e => {
                console.log('final', e)
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>