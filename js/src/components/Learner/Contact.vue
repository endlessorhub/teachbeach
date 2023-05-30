<template>
  <form>
    <v-text-field
            name="first_name"
      v-model.trim="first_name"
      :error-messages="firstNameErrors"
      :counter="30"
      label="First Name"
      required
      @input="$v.first_name.$touch()"
      @blur="$v.first_name.$touch()"
    ></v-text-field>
    <v-text-field
      name="last_name"
      v-model.trim="last_name"
      :error-messages="lastNameErrors"
      :counter="30"
      label="Last Name"
      required
      @input="$v.last_name.$touch()"
      @blur="$v.last_name.$touch()"
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
            name="phone"
      v-model.trim="phone"
      :error-messages="phoneErrors"
      label="Phone Number"
      required
      @input="$v.phone.$touch()"
      @blur="$v.phone.$touch()"
    ></v-text-field>
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
            name="repeat_password"
            browser-autocomplete="new-password"
      v-model="repeat_password"
      :error-messages="repeatPasswordErrors"
      type="password"
      label="Repeat Password"
      required
      @input="$v.repeat_password.$touch()"
      @blur="$v.repeat_password.$touch()"
    ></v-text-field>
    <v-checkbox v-model="alerts">
      <div v-if="isPrivate" slot="label">
        Yes, it is ok to notify me of upcoming Classes by text.
      </div>
      <div v-else slot="label">
        Yes, Please send alerts the day of class, and for class changes.
      </div>
    </v-checkbox>
    <div style="text-align: left;">
      By registering, I agree to <a @click="terms = true">terms</a> and <a @click="privacy = true">privacy agreement</a>.
        <v-dialog v-model="terms" class="flex xs12 md8 lg6">
          <v-card>
            <v-card-title class="headline grey lighten-2" primary-title>
              Terms
            </v-card-title>
            <v-card-text>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat
                @click="terms = false">
                I accept
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="privacy" class="flex xs12 md8 lg6">
          <v-card>
            <v-card-title class="headline grey lighten-2" primary-title>
              Privacy agreement
            </v-card-title>
            <v-card-text>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat
                @click="privacy = false">
                I accept
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </div>
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
        last_name: { required, maxLength: maxLength(30) },
        email: { email },
        phone: { maxLength: maxLength(20) },
        password: { required, minLength: minLength(8) },
        repeat_password: { required, sameAsPassword: sameAs('password') },
    },

    props: {
        isPrivate: Boolean,
    },

    data: function () {

        return {
            first_name: this.$store.state.user ? this.$store.state.user.first_name : '',
            last_name: this.$store.state.user ? this.$store.state.user.last_name : '',
            email: this.$store.state.user ? this.$store.state.user.email : '',
            phone: this.$store.state.user ? this.$store.state.user.phone : '',
            password: '',
            repeat_password: '',
            alerts: false,
            isLoading: false,
            errors: {},
            showLoginLink: false,
            terms: false,
            privacy: false,
        }
    },

    created: function () {
        if (this.$store.state.learnerData) {
            this.alerts = this.$store.state.learnerData.alerts
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
            this.$v.$touch()
            console.log('submit', this, arguments)
            this.showLoginLink = false
            if (this.$v.$anyError)
                return
            axios.post('/api/users/', {
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                phone: this.phone,
                password: this.password,
                alerts: this.alerts
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
                return err
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