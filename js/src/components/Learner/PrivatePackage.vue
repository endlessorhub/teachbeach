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
            v-model="packageSelected"
            :error-messages="packageSelectedErrors"
            required
            @input="$v.packageSelected.$touch()"
            @blur="$v.packageSelected.$touch()"
          >
            <v-radio v-for="v in availablePackages" :key="v.id" color="primary" :value="v.value" :disabled="v.isTrialSpent">
                <template v-slot:label>
                    <div>
                        <div>
                            {{v.isTrialSpent ? 'Congrats! You have completed a trial lesson. Keep learning!' : v.text }}
                            <v-chip v-if="v.isMemberPrice" color="platform-green" text-color="white">
                              <v-avatar>
                                <v-icon>check_circle</v-icon>
                              </v-avatar>
                              Premium Member Price
                            </v-chip>
                        </div>
                        <div>{{v.isTrialSpent ?  '' : v.description}}</div>
                    </div>
                </template>
            </v-radio>
          </v-radio-group>
        </v-flex>
          <v-flex xs12 class="text-xs-left" v-if="isMemberOfClass">
               <v-icon color="platform-green" left>check_circle</v-icon>You are a premium member of this organization!
          </v-flex>
          <v-flex xs12 class="text-xs-left" v-if="isMembershipAvailable">
               Join as a premium member first? <v-btn @click="buyMembership">GO</v-btn>
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
import { mapGetters } from 'vuex'
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'

import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],

    validations: {
        packageSelected: { required },
    },

    props: [
        'step'
    ],

    data: () => ({
        isLoading: false,
        packageSelected: null,
        customPackages: [],
        spentTrialPackages: [],
        rate: null,
        currency: 'usd',
        alreadyBoughtTrial: {},
        avatar: null,
    }),

    created: function () {
        if (this.$store.state.learnerChoice) {
            this.avatar = this.$store.state.learnerChoice.teacher.media
            axios.get(`/api/learner/class_packages/${this.$store.state.learnerChoice.id}/`).then(res => {
                console.log(res)
                _.each(res.data, p => {
                    if(p.isTrial) {
                        this.alreadyBoughtTrial[p.key] = p
                    }
                })
                this.customPackages = _.filter(_.uniq(this.$store.state.learnerChoice.custom_packages || []), p => {
                    return p.isPrivate && (!p.isTrial || !this.alreadyBoughtTrial[p.key] || p.totalPrice !== this.alreadyBoughtTrial[p.key].totalPrice)
                })
                this.spentTrialPackages = _.filter(_.uniq(this.$store.state.learnerChoice.custom_packages || []), p => {
                    return p.isPrivate && p.isTrial && this.alreadyBoughtTrial[p.key] && p.totalPrice === this.alreadyBoughtTrial[p.key].totalPrice
                })
                this.rate = Number(this.$store.state.learnerChoice.rate)
                this.currency = this.$store.state.learnerChoice.currency
                if (this.rate && Number(this.rate)) {
                    this.customPackages.unshift({
                        currency: this.currency,
                        perLesson: this.rate,
                        totalPrice: this.rate,
                        numberOfLessons: 1,
                        lessonLength: {text: "1 hour", value: 60},
                        minPersons: 1,
                        maxPersons: 1,
                        description: 'Single One-hour lesson for one person',
                        isPricePerPerson: false,
                        isPrivate: true,
                        isDropIn: true,
                    })
                }
                if(this.customPackages.length === 1) {
                    this.packageSelected = this.customPackages[0]
                }
                if (this.$store.state.learnerData && this.$store.state.learnerData.package && _.find(this.customPackages, _.pick(this.$store.state.learnerData.package, [
                    'currency',
                    'isPricePerPerson',
                    'totalPrice',
                    'numberOfLessons',
                    'isPrivate',
                    'minPersons',
                    'maxPersons',
                ]))) {
                    this.packageSelected = this.$store.state.learnerData.package
                }
            })
        }
    },

    computed: {
        ...mapGetters([
            'isMember',
        ]),
        availablePackages() {
            const isTrialSpent = _.keyBy(this.spentTrialPackages, 'key')
            const mode = this.isMemberOfClass ? 'isMember' : this.classMembershipId ? 'addMembership' : 'regular'
            const getPackageText = v => {
                if(v.isTrial) {
                    return `${v.lessonLength.text} trial lesson ${v.numberOfLessons} time${v.numberOfLessons == 1 ? '' : 's'} for ${utils.formatPrice(v.totalPrice, v.currency)}`
                } else if (v.isDropIn) {
                    return `Drop in for ${utils.formatPrice(v.totalPrice, v.currency)} (one hour) `
                }
                return classHelper.packageFormatter(v, mode)
            }
            return _.map(_.concat(this.spentTrialPackages, this.customPackages), v => ({
                id: _.uniqueId(),
                value: v,
                text: getPackageText(v),
                description: v.description,
                isTrialSpent: isTrialSpent[v.key],
                isMemberPrice: utils.useMemberPrice(mode, v),
            }))
        },
        packageSelectedErrors() {
            const errors = []
            if (!this.$v.packageSelected.$dirty) return errors
            !this.$v.packageSelected.required && errors.push('Please, select package')
            return errors
        },
        classMembershipId() {
            return this.$store.state.learnerChoice.teacher.user && this.$store.state.learnerChoice.teacher.user.membership
        },
        isMemberOfClass() {
            return this.isMember(this.classMembershipId)
        },
        isMembershipAvailable() {
            return this.classMembershipId && !this.isMemberOfClass
        },
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
                package: this.packageSelected,
            })
            //this.$router.push({path: '/learner/checkout'})
            this.$emit('next:step')
        },
        clear () {

        },
        buyMembership() {
            this.$router.push(`/learners/membership/${this.$store.state.learnerChoice.id}?return=${this.$route.path}`)
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>