<template>
  <form>
    <h1>{{ title }}</h1>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <v-text-field
              v-model="groupClassName"
              :label="nameLabel"
              :placeholder="namePlaceholder"
              required
              @input="$v.groupClassName.$touch()"
              @blur="$v.groupClassName.$touch()"
              :error-messages="classNameErrors"
            ></v-text-field>
            <v-text-field
              v-model="privateClassWebsite"
              label="Website"
              placeholder="http://..."
            ></v-text-field>
            <h4>Student Experience required:</h4>
              <v-checkbox v-model="studentExperienceLevel" color="primary" label="Beginner" value="Beginner" hide-details></v-checkbox>
              <v-checkbox v-model="studentExperienceLevel" color="primary" label="Intermediate" value="Intermediate" hide-details></v-checkbox>
              <v-checkbox v-model="studentExperienceLevel" color="primary" label="Advanced" value="Advanced" hide-details></v-checkbox>
              <v-checkbox v-model="studentExperienceLevel" color="primary" label="Does not matter" value="Any" hide-details></v-checkbox>
            <v-text-field
              v-model="maxSize"
              label="Maximum  size"
              numeric
              placeholder="Maximum amount of group members"
              @input="$v.maxSize.$touch()"
              @blur="$v.maxSize.$touch()"
              :error-messages="maxSizeErrors"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-checkbox color="primary" v-model="showEmail" label="Show Email on the Profile Page" hide-details></v-checkbox>
        </v-flex>
        <v-flex xs12 sm6>
            <ShowPhoneRule v-model="showPhoneRule" />
            <v-checkbox color="primary" v-model="showPhone" label="Show Phone on the Profile Page" hide-details></v-checkbox>
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

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength, numeric } from 'vuelidate/lib/validators'
import ShowPhoneRule from './Teacher/ShowPhoneRule'

export default {
    mixins: [validationMixin],
    validations: {
        groupClassName: { required },
        maxSize: {numeric}
    },
    components: {
        ShowPhoneRule,
    },
    data: () => ({
        isLoading: false,
        studentExperienceLevel: [],
        groupClassName: '',
        groupClassDescription: '',
        privateClassWebsite: '',
        maxSize: null,
        showEmail: false,
        showPhone: false,
        showPhoneRule: 'text',
        isPremiumCommunity: false,
    }),

    created: function () {
        if (this.$store.state.teacherGroupClass) {
            this.studentExperienceLevel = this.$store.state.teacherGroupClass.studentExperienceLevel || []
            this.groupClassName = this.$store.state.teacherGroupClass.groupClassName
            this.groupClassDescription = this.$store.state.teacherGroupClass.groupClassDescription
            this.privateClassWebsite = this.$store.state.teacherGroupClass.privateClassWebsite
            this.maxSize = this.$store.state.teacherGroupClass.maxSize
            if('showEmail' in this.$store.state.teacherGroupClass) {
                this.showEmail = this.$store.state.teacherGroupClass.showEmail
            }
            if('showPhone' in this.$store.state.teacherGroupClass) {
                this.showPhone = this.$store.state.teacherGroupClass.showPhone
            }
            if('showPhoneRule' in this.$store.state.teacherGroupClass)
                this.showPhoneRule = this.$store.state.teacherGroupClass.showPhoneRule
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
        }
    },

    computed: {
        maxSizeErrors() {
            const errors = []
            if (!this.$v.maxSize.$dirty) return errors
            !this.$v.maxSize.numeric && errors.push('Max size is number')
            return errors
        },
        classNameErrors () {
            const errors = []
            if (!this.$v.groupClassName.$dirty) return errors
            !this.$v.groupClassName.required && errors.push('Name is required.')
            return errors
        },
        title() {
            return this.isPremiumCommunity ? 'Please start by naming your community' : 'Please start by describing a group class';
        },
        nameLabel() {
            return this.isPremiumCommunity ? 'Give you community a great name' : 'Give your class a great name';
        },
        namePlaceholder() {
            return this.isPremiumCommunity ? 'Enter a name that lets customers know what the community is about right away\n' : 'Give your class a great name';
        },
    },

    methods: {
        saveData() {
            this.$store.commit('setGroupClass', {
                studentExperienceLevel: this.studentExperienceLevel,
                groupClassName: this.groupClassName,
                groupClassDescription: this.groupClassDescription,
                privateClassWebsite: this.privateClassWebsite,
                //groupClassSummary: this.groupClassSummary,
                maxSize: this.maxSize,
                showEmail: this.showEmail,
                showPhone: this.showPhone,
                showPhoneRule: this.showPhoneRule,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.saveData()
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