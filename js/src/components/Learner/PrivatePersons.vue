<template>
  <form>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex v-if="avatar" xs12 class="text-xs-center">
            <v-avatar
              v-if="avatar"
              :size="100"
              color="grey lighten-4"
            >
              <img :src="avatar" alt="avatar">
            </v-avatar>
        </v-flex>
        <v-flex xs12 class="text-xs-left">
          <v-radio-group
            v-model="personsSelected"
            :error-messages="personsSelectedErrors"
            required
            @input="$v.personsSelected.$touch()"
            @blur="$v.personsSelected.$touch()"
          >
            <v-radio v-for="v in availablePersons" :key="v.value" color="primary" :label="v.text" :value="v.value"></v-radio>
          </v-radio-group>
        </v-flex>
      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],

    validations: {
        personsSelected: { required },
    },

    props: [
        'step'
    ],

    data: () => ({
        isLoading: false,
        personsSelected: null,
        packageSelected: null,
        avatar: null,
    }),

    created: function () {
        if (this.$store.state.learnerChoice) {
            this.avatar = this.$store.state.learnerChoice.teacher.media
        }
        if (this.$store.state.learnerData) {
            this.packageSelected = this.$store.state.learnerData.package
            this.personsSelected = this.$store.state.learnerData.persons
            if (this.packageSelected && !this.personsSelected) {
                this.personsSelected = this.packageSelected.minPersons
            }
        }
    },

    computed: {
        availablePersons() {
            if(!this.packageSelected || this.packageSelected.isSubscription)
                return []
            return _.map(_.range(this.packageSelected.minPersons, Number(this.packageSelected.maxPersons)+1), v => ({
                value: v,
                text: `${v} person${v > 1 ? 's' : ''}`,
            }))
        },
        personsSelectedErrors() {
            const errors = []
            if (!this.$v.personsSelected.$dirty) return errors
            !this.$v.personsSelected.required && errors.push('Please, select how many persons will go')
            return errors
        }
    },

    methods: {
        back() {
            this.$emit('prev:step')
        },
        submit () {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.$store.commit('mergeLearnerData', {
                persons: this.personsSelected,
            })
            //this.$router.push({path: '/learner/checkout'})
            this.$emit('next:step')
        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>