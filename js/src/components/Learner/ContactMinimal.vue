<template>
  <form>
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
      <div v-if="showLoginLink" class="v-messages theme--light error--text" style="text-align: left;">Try to <a @click="$emit('openLoginForm')">login</a></div>
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
      <v-alert
      :value="true"
      color="info"
      icon="info"
      outline
    >
      You may receive sms of new classes in categories you select
    </v-alert>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit">Next</v-btn>

  </form>
</template>

<script>
import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
    mixins: [validationMixin],

    components: {

    },

    validations: {
        first_name: { required, maxLength: maxLength(30) },
        email: { email },
        phone: { maxLength: maxLength(20) },
        password: { required, minLength: minLength(8) },
    },

    props: {
        isPrivate: Boolean,
    },

    data: function () {

        return {
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
            class_id: null,
        }
    },

    created: function () {
        if (this.$store.state.learnerData) {
            this.alerts = this.$store.state.learnerData.alerts
        }
        if(this.$store.state.learnerChoice) {
            this.class_id = this.$store.state.learnerChoice.id
        }
        if(!this.$store.state.user) {
            this.first_name = this.$store.state.studentName
            this.email = this.$store.state.studentEmail
            this.phone = this.$store.state.studentPhone
        }
    },

    computed: {

        firstNameErrors () {
            const errors = []
            if (!this.$v.first_name.$dirty) return errors
            !this.$v.first_name.maxLength && errors.push('Name must be at most 100 characters long')
            !this.$v.first_name.required && errors.push('Name is required.')
            return errors
        },
        lastNameErrors () {
            const errors = []
            if (!this.$v.last_name.$dirty) return errors
            !this.$v.last_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.last_name.required && errors.push('Name is required.')
            return errors
        },
        emailErrors () {
            const errors = []
            if (this.errors.email) {
                return this.errors.email
            }
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.email && !this.phone && errors.push('E-mail or Phone is required')
            return errors
        },
        phoneErrors () {
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            //!this.phone && !this.email && errors.push('Phone or E-mail is required')
            return errors
        },
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters long')
            return errors
        },
        repeatPasswordErrors () {
            const errors = []
            if (!this.$v.repeat_password.$dirty) return errors
            //!this.$v.repeat_password.minLength && errors.push('Password must be at least 8 characters long')
            !this.$v.repeat_password.sameAsPassword && errors.push('Repeated password does not match original')
            return errors
        },
    },

    methods: {
        back() {
            this.$emit('prev:step')
        },
        next() {
            //this.$emit('update:step', 4)
        },
        submit () {
            let userData = null
            this.$v.$touch()
            console.log('submit', this, arguments)
            this.showLoginLink = false
            if (this.$v.$anyError)
                return
            axios.post('/api/users/', {
                first_name: this.first_name,
                email: this.email,
                phone: this.phone,
                password: this.password,
                alerts: !!this.phone,
                class_id: this.class_id,
            }).catch((err) => {
                ///handle errors
                this.isLoading = false
                if (err.response.data) {
                    let errs = {}
                    _.each(err.response.data, (v, k) => {
                        if(k === 'email' && v.indexOf("User with this email already exists") != -1) {
                            this.showLoginLink = true
                        }
                        errs[k] = v
                    })
                    this.errors = errs
                }
                return err
            }).then((res) => {
                //console.log(arguments)
                //res.data.user.id
                fbq('trackCustom', 'studentRegistration')
                //this.$store.commit('setUser', _.omit(res.data, 'password'))
                userData = _.omit(res.data, 'password')
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
                // basically we use user in vuex to update step
                this.$store.commit('setUser', userData)
                // so the call of this.$emit('next:step') will be ignored in wizard
                if(this.onSuccess) {
                    this.onSuccess.call(this)
                } else
                    this.$emit('next:step')
            }).catch((e) => {
                console.log('err!', arguments)
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
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>