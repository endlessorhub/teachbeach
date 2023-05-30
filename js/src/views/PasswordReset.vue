<template>
  <div class="password-reset">
    <v-layout align-center justify-center>
        <div class="flex xs12 md6 lg4">
          <v-card>
            <v-card-title primary-title>
              <div>
                <h3>Reset password</h3>
              </div>
            </v-card-title>
            <v-card-text>
            <div v-if="passwordResetSuccess === true">Password was reset, now <router-link to="/?login">login</router-link></div>
            <div v-else>
                <v-text-field
                  v-model="password"
                  :error-messages="passwordErrors"
                  counter
                  type="password"
                  label="New Password"
                  required
                  @input="$v.password.$touch()"
                  @blur="$v.password.$touch()"
                ></v-text-field>
                <v-text-field
                  v-model="repeat_password"
                  :error-messages="repeatPasswordErrors"
                  type="password"
                  label="Repeat Password"
                  required
                  @input="$v.repeat_password.$touch()"
                  @blur="$v.repeat_password.$touch()"
                ></v-text-field>
                <div class="v-messages theme--light error--text"><div class="v-messages__wrapper"><div class="v-messages__message">{{ serverErrors }}</div></div></div>
            </div>
            </v-card-text>
            <v-card-actions>
              <v-btn v-if="!passwordResetSuccess" @click="saveNewPassword" :disabled="isLoading">Save</v-btn>

            </v-card-actions>
          </v-card>
        </div>
    </v-layout>
  </div>
</template>

<script>

import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'
import metadata from '@/mixins/metadata'

export default {
    data: function () {

        return {
            password: '',
            repeat_password: '',
            passwordResetSuccess: null,
            perrors: null,
            //passwordResetError: '',
            isLoading: false,
        }
    },
    mixins: [validationMixin, metadata],
    validations: {
        password: { required, minLength: minLength(8) },
        repeat_password: { required, sameAsPassword: sameAs('password') },
    },
    created() {
        console.log(this.$route)
    },
    components: {

    },
    methods: {
        saveNewPassword() {
            this.isLoading = true
            this.perrors = null
            axios.post('/api/user/reset_password/finish/', {
                token: this.$store.state.globals.token,
                uidb64: this.$store.state.globals.uidb64,
                new_password1: this.password,
                new_password2: this.repeat_password,
            }).then((resetRes) => {
                if(resetRes.data.success) {
                    this.passwordResetSuccess = true
                } else {
                    this.passwordResetSuccess = false
                    this.perrors = resetRes.data.errors ? resetRes.data.errors.new_password2 : ['Something went wrong, try again later']
                }
            }).catch((resetRes) => {
                //console.log('err!', arguments)
                this.passwordResetSuccess = false
                this.perrors = resetRes.response.data.errors ? resetRes.response.data.errors.new_password2 : ['Something went wrong, try again later']
            }).then(() => {
                this.isLoading = false
            })
        }
    },
    computed: {
        serverErrors() {
            return this.perrors && this.perrors.length ? this.perrors.join(', ') : ''
        },
        passwordErrors () {
            const errors = []
            if (!this.$v.password.$dirty) return errors
            this.perrors = []
            !this.$v.password.minLength && errors.push('Password must be at least 8 characters long')
            return errors
        },
        repeatPasswordErrors () {
            const errors = []
            if (!this.$v.repeat_password.$dirty) return errors
            this.perrors = []
            //!this.$v.repeat_password.minLength && errors.push('Password must be at least 8 characters long')
            !this.$v.repeat_password.sameAsPassword && errors.push('Repeated password does not match original')
            return errors
        },
    },
}
</script>
