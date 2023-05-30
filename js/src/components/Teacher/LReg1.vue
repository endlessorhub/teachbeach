<template>
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 text-xs-center>
            <form>
            <v-card class="card">
                <v-card-title class="headline" primary-title>
                    {{ header }}
                </v-card-title>
                <v-card-text>
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
                      name="email"
                      v-model.trim="email"
                      :error-messages="emailErrors"
                      label="Email Address"
                      required
                      @input="$v.email.$touch()"
                      @blur="$v.email.$touch()"
                    ></v-text-field>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                      <v-spacer></v-spacer>
                    <v-btn @click="next">Next</v-btn>
                </v-card-actions>
            </v-card>
            </form>
        </v-flex>
    </v-layout>
</template>

<script>
import _ from 'lodash'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import axios from 'axios'

export default {
    mixins: [validationMixin],
    props: {
        header: {
            type: String,
            default: 'Looks like you’re new here',
        },
    },
    components: {

    },

    validations: {
        first_name: { required, maxLength: maxLength(30) },
        email: { required, email },
    },

    data: function () {

        return {
            first_name: this.$store.state.user ? this.$store.state.user.first_name : '',
            email: this.$store.state.user ? this.$store.state.user.email : '',
            isLoading: false,
            errors: {},
        }
    },

    mounted() {
        if(this.alreadyRegistered) {
            this.$router.push('/teachers/start');
        }
    },

    computed: {
        alreadyRegistered: function () {
            return this.$store.state.user && this.$store.state.user.id
        },

        firstNameErrors () {
            const errors = []
            if (!this.$v.first_name.$dirty) return errors
            !this.$v.first_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.first_name.required && errors.push('Name is required.')
            return errors
        },
        emailErrors () {
            const errors = []
            if (this.errors.email) {
                return this.errors.email
            }
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.$v.email.required && errors.push('E-mail is required')
            return errors
        },
    },

    methods: {
        next() {
            if(this.isAlreadyRegisterOpened)
                this.$router.push('/teachers/start');
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.$store.commit('setUser', {
                first_name: this.first_name,
                email: this.email,
            });
            this.$router.push('/promo');
        },
        clear () {
            this.$v.$reset()
            this.first_name = ''
            this.email = ''
        }
    },
    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.card {
    margin: 1em auto;
    width: 370px;
}
</style>