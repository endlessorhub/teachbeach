<template>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
          <v-flex xs12 class="text-xs-left">
              {{tclass && tclass.groupClassSummary}}
          </v-flex>
        <v-flex xs12 md6 style="padding: 2px;">
          <v-flex xs12 class="text-xs-left">
              <v-layout align-center justify-center row wrap>
                <v-flex xs2 class="text-xs-center">
                  <v-btn
                    icon
                    outline
                    small
                    left
                    color="primary"
                    @click="prevMonth"
                  >
                    <v-icon dark>
                      keyboard_arrow_left
                    </v-icon>
                  </v-btn>
                </v-flex>
                <v-flex xs8 class="text-xs-center">
                <div>{{startCal}} to {{endCal}}</div>
                </v-flex>
                <v-flex xs2 class="text-xs-center">
                  <v-btn
                    icon
                    outline
                    small
                    right
                    color="primary"
                    @click="nextMonth"
                  >
                    <v-icon
                      dark
                    >
                      keyboard_arrow_right
                    </v-icon>
                  </v-btn>
                </v-flex>
              </v-layout>
              <div v-for="(v, i) in currentWeekSchedule" :key="i">
                  {{v}}
              </div>
          </v-flex>
        <v-flex xs12 class="text-xs-left">
          <v-radio-group
            v-model="package"
            :error-messages="packageErrors"
            required
            @input="$v.package.$touch()"
            @blur="$v.package.$touch()"
          >
              <v-template>
                  <v-radio color="primary" :label="v.label" :value="v.key" v-for="v in availablePackages" :key="v.key" :disabled="v.isTrialSpent">
                      <template v-slot:label>
                          <div>
                              <div>
                                  {{v.isTrialSpent ? 'You’ve used ' : '' }} {{v.label}}
                                  <span v-if="v.memberLabel" class="member-rate">{{v.memberLabel}}</span>
                                  <v-chip v-if="v.isMemberPrice" color="platform-green" text-color="white">
                                      <v-avatar>
                                        <v-icon>check_circle</v-icon>
                                      </v-avatar>
                                      Premium Member Price
                                  </v-chip>
                              </div>
                              <div v-if="v.description" class="caption">{{v.description}}</div>
                          </div>
                      </template>
                  </v-radio>
              </v-template>
          </v-radio-group>
        </v-flex>
        <v-flex xs12 class="text-xs-left" v-if="isMemberOfClass">
            <v-icon color="platform-green" left>check_circle</v-icon>You are a premium member of this organization!
        </v-flex>
        <v-flex xs12 class="text-xs-left" v-if="isMembershipAvailable">
            Join as a premium member first? <v-btn @click="buyMembership">GO</v-btn>
        </v-flex>
        <v-flex xs12 class="text-xs-center">
            <div>
                <v-btn @click="back">Back</v-btn>
                <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Sign Up</v-btn>
            </div>
            </v-flex>
        </v-flex>
          <v-flex xs12 md6 style="padding: 2px;">
              <v-flex xs6 md12  class="text-xs-left">
              <v-carousel ref="carouselEl" v-if="class_media && class_media.length" :height="carouselHeight">
                <v-carousel-item
                  v-for="(item,i) in class_media"
                  :key="i"
                  :src="item.class_media"
                ></v-carousel-item>
              </v-carousel>
              <v-img v-else-if="mediaUrl" :src="mediaUrl" style="margin:auto;" :aspect-ratio="1.25" />
              <v-divider style="margin: 3px;"></v-divider>
            </v-flex>
          </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import axios from 'axios'
import config from '@/config.js'
import { mapGetters } from 'vuex'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],

    validations: {
        package: { required },
    },
    components: {

    },
    props: [
        'class_media',
        'currency',
        'custom_packages',
        'drop_in_rate',
        'flexible_dates',
        'master_media',
        'schedule_excluded',
        'standard_packages',
        'start_date',
        'until_date',
        'weekdays_schedule',
        'day_select_type',
        'schedule_dates',
        'is_premium_community',
        'name',
        'step',
    ],

    data: () => ({
        isLoading: false,
        pp: null,
        currentDate: new Date(),

        numLessons: 0,
        tclass: null,
        lessonDuration: 0,
        duration: 0,
        selectedLessons: [],
        learnerNeeds: '',
        first_name: '',
        email: '',
        phone: '',
        alerts: false,

        //availableLessons: [],
        carouselHeight: 300,
        alreadyBoughtTrial: {},
    }),

    created: function () {
        if (this.$store.state.learnerData) {
            this.lessonDuration = this.$store.state.learnerData.lessonDuration
            this.duration = this.$store.state.learnerData.duration
            this.pp = this.$store.state.learnerData.package
            this.selectedLessons = this.$store.state.learnerData.selectedLessons
            this.numLessons = this.$store.state.learnerData.numLessons
            this.learnerNeeds = this.$store.state.learnerData.learnerNeeds
            this.first_name = this.$store.state.learnerData.first_name
            this.email = this.$store.state.learnerData.email
            this.phone = this.$store.state.learnerData.phone
            this.alerts = this.$store.state.learnerData.alerts
        }
        if(this.$store.state.learnerChoice) {
            this.tclass = this.$store.state.learnerChoice
        }
        if(this.tclass) {
            axios.get(`/api/learner/class_packages/${this.tclass.id}/`).then(res => {
                console.log(res)
                const alreadyBoughtTrial = {}
                _.each(res.data, p => {
                    if (p.isTrial) {
                        alreadyBoughtTrial[p.key] = true
                    }
                })
                this.alreadyBoughtTrial = alreadyBoughtTrial
            })
        }

    },

    mounted() {
        this.$nextTick(() => {
            //this.updateCarHeight()
            //window.addEventListener('resize', this.updateCarHeight);
            //console.log(this.carouselHeight)
            let switchLimit = 6;
            let initial = new Date(this.currentDate);

            while(!this.currentWeekSchedule.length && switchLimit) {
                let current = new Date(this.currentDate);
                current.setMonth(current.getMonth()+1);
                this.currentDate = current;
                switchLimit--;
            }
            if(!switchLimit && !this.currentWeekSchedule.length) {
                this.currentDate = initial;
            }
        })
    },

    beforeDestroy() {
        //window.removeEventListener('resize', this.updateCarHeight);
    },

    computed: {
        ...mapGetters([
            'isMember',
        ]),
        classMembershipId() {
            return this.tclass ? this.tclass.teacher.user.membership : null
        },
        isMemberOfClass() {
            return this.isMember(this.classMembershipId)
        },
        isMembershipAvailable() {
            return this.classMembershipId && !this.isMemberOfClass
        },
        // recalc
        package: {
            get() {
                return this.pp ? (this.availablePackages.find(v => v.package.key === this.pp.key) || {}).key : null
            },
            set(v) {
                this.pp = (this.availablePackages.find(p => p.key === v) || {}).package
            },
        },
        packageChoosen() {
            return (_.find(this.availablePackages, {key: this.package}) || {}).package
        },
        cost() {
            return utils.formatPrice(this.packageChoosen ? this.packageChoosen.totalPrice : '', this.currency)
        },
        mediaUrl() {
            if(this.class_media && this.class_media.length)
                return this.class_media[0].class_media
            else
                return  this.master_media ? this.master_media : ''
        },
        currentWeekSchedule() {
            if(this.day_select_type === 'weekly') {
                let days = utils.getCalendarDatesForPeriod(
                    utils.dateToString(new Date()),
                    utils.dateToString(this.endCalDate),
                    this.weekdays_schedule,
                    utils.dateToString(this.startCalDate),
                    utils.dateToString(this.endCalDate),
                    this.schedule_excluded
                )
                return _.map(days, v => {
                    let times = _.filter(this.weekdays_schedule, {weekday: utils.stringToDate(v).getDay()}).map(v => `${utils.time24HtoAMPM(v.start)} to ${utils.time24HtoAMPM(v.end)}`).join(', ')
                    return `${utils.stringToDate(v).toLocaleString('en-us', { weekday: 'long', day: 'numeric', month: 'short' })} ${times}`
                })
            } else {
                let dayDict = _.keyBy(this.schedule_dates, 'date')
                let res = []
                for (let current = new Date(this.startCalDate); current <= this.endCalDate; current.setDate(current.getDate()+1)) {
                    if(dayDict[utils.dateToString(current)])
                        res.push(`${current.toLocaleString('en-us', { weekday: 'long', day: 'numeric', month: 'short' })} ${utils.time24HtoAMPM(dayDict[utils.dateToString(current)].start)} to ${utils.time24HtoAMPM(dayDict[utils.dateToString(current)].end)}`)
                }
                return res
            }
        },
        startCalDate() {
            let date = new Date(this.currentDate)
            date.setDate(1)
            return date
        },
        endCalDate() {
            let date = new Date(this.startCalDate)
            date.setDate(1)
            date.setMonth(date.getMonth()+1)
            date.setDate(0)
            return date
        },
        startCal() {
            return this.startCalDate.toLocaleString('en-us', { month: 'long', day: 'numeric' })
        },
        endCal() {
            return this.endCalDate.toLocaleString('en-us', { day: 'numeric' })
        },
        currencyLogo() {
            return utils.getCurrencyLogo(this.currency || 'usd')
        },
        availablePackages() {
            let res = []
            const mode = this.isMemberOfClass ? 'isMember' : this.classMembershipId ? 'addMembership' : 'regular'
            const useMemberPrice = utils.useMemberPrice;
            if (this.drop_in_rate && Number(this.drop_in_rate)) {
                res.push({
                    key: 'drop_in',
                    label: `Drop in for ${utils.formatPrice(this.drop_in_rate, this.currency || 'usd')}`,
                    package: {
                        perLesson: this.drop_in_rate,
                        totalPrice: this.drop_in_rate,
                        numberOfLessons: 1,
                        isDropIn: true,
                    }
                })
            }
            if (this.standard_packages && this.standard_packages.length && this.flexible_dates) {
                res = _.concat(res, _.map(_.uniqBy(this.standard_packages, v => `${v.numberOfLessons}-${v.description}`), v => ({
                    key: 'standard-'+v.key+'-r',
                    label: `${utils.formatPrice(utils.useMemberPrice(mode, v) ? v.memberTotalPrice : v.totalPrice, this.currency)} for ${v.numberOfLessons} ${v.isTrial ? ' trial' : ''} lesson${v.numberOfLessons == 1 ? '' : 's'}`,
                    description: v.description && v.description.length > 50 ? v.description.substring(0, 50)+'...' : v.description,
                    isTrialSpent: this.alreadyBoughtTrial[v.key],
                    memberLabel: mode === 'addMembership' && v.memberTotalPrice ? `Premium Member Rate ${utils.formatPrice(v.memberTotalPrice, this.currency || 'usd')}` : '',
                    isMemberPrice: utils.useMemberPrice(mode, v),
                    package: v,
                })))
            }
            if (this.custom_packages && this.custom_packages.length && !this.flexible_dates) {
                res = _.concat(res, _.map(_.filter(this.custom_packages, v => !v.isPrivate), v => ({
                    key: 'custom-'+v.key+'-r',
                    label: `${utils.formatPrice(utils.useMemberPrice(mode, v) ? v.memberTotalPrice : v.totalPrice, this.currency)} for ${v.numberOfLessons} ${v.isTrial ? ' trial' : ''} lesson${v.numberOfLessons == 1 ? '' : 's'}`,
                    description: v.description && v.description.length > 50 ? v.description.substring(0, 50)+'...' : v.description,
                    isTrialSpent: this.alreadyBoughtTrial[v.key],
                    memberLabel: mode === 'addMembership' && Number(v.memberTotalPrice) ? `Premium Member Rate ${utils.formatPrice(v.memberTotalPrice, this.currency || 'usd')}` : '',
                    isMemberPrice: utils.useMemberPrice(mode, v),
                    package: v,
                })))
            }
            if (this.custom_packages && this.custom_packages.length && this.flexible_dates) {
                this.custom_packages.forEach(v => {
                    if (v.type !== 'limitedSubscription') return;
                    res.push({
                        key: 'custom-'+v.key+'-r',
                        label: `${utils.formatPrice(utils.useMemberPrice(mode, v) ? v.memberPricePerInterval : v.pricePerInterval, this.currency || 'usd')} ${v.interval}ly ${v.numberOfIntervals} time${v.numberOfIntervals > 1 ? 's' : ''}`,
                        description: v.description && v.description.length > 50 ? v.description.substring(0, 50)+'...' : v.description,
                        isTrialSpent: this.alreadyBoughtTrial[v.key],
                        memberLabel: '',
                        isMemberPrice: utils.useMemberPrice(mode, v),
                        package: v,
                    })
                });
            }
            return res
        },
        packageErrors() {
            const errors = []
            if (!this.$v.package.$dirty) return errors
            !this.$v.package.required && errors.push('Please, select a package')
            return errors
        },
        name() {
            if(!this.tclass)
                return ''
            return this.tclass.is_private ? this.tclass.private_className : this.tclass.name
        },
    },

    methods: {
        buyMembership() {
            this.$router.push(`/learners/membership/${this.tclass.id}?return=${this.$route.path}`)
        },
        updateCarHeight() {
            if(this.step && this.$refs.carouselEl && this.$refs.carouselEl.$el && this.$refs.carouselEl.$el.clientWidth)
                this.carouselHeight = this.$refs.carouselEl.$el.clientWidth
        },
        prevWeek() {
            let date = new Date(this.currentDate)
            date.setDate(this.currentDate.getDate()-7)
            this.currentDate = date
        },
        nextWeek() {
            let date = new Date(this.currentDate)
            date.setDate(this.currentDate.getDate()+7)
            this.currentDate = date
        },
        prevMonth() {
            let date = new Date(this.currentDate)
            date.setMonth(this.currentDate.getMonth()-1)
            this.currentDate = date
        },
        nextMonth() {
            let date = new Date(this.currentDate)
            date.setMonth(this.currentDate.getMonth()+1)
            this.currentDate = date
        },
        back() {
            this.$emit('back:to:start')
            //this.$router.go(-1)
        },
        submit () {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            if(!this.tclass.can_pay) {
                console.warn('add an order without payment, redirect do learner dashboard class list')
                axios.post('/api/enroll_class', {
                    'class': this.tclass,
                    'lessonDuration': this.lessonDuration,
                    'duration': this.duration,
                    'package': this.packageChoosen,
                    'selectedLessons': this.selectedLessons,
                    'numLessons': this.numLessons,
                    'name': this.name,
                    'rate': this.tclass.rate,
                    'cost': this.cost.replace(/\D+/g, ''),
                    'learnerNeeds': this.learnerNeeds,
                    'alerts': this.alerts,
                }).then((res) => {
                    this.isLoading = false
                    console.log(res)
                    if(res.data.success) {
                        this.$router.push('/dashboard/learn/classes')
                    }
                }).catch(err => {
                    this.isLoading = false
                    console.log(err)
                })
                return
            }
            this.$store.commit('mergeLearnerData', {
                package: this.packageChoosen
            })

            this.$emit('next:step')
        },
        clear () {

        },
    },
    watch: {
        step () {
            this.updateCarHeight()
        },
        availablePackages(res) {
            if(res && res.length === 1) {
                this.package = res[0].key
            }
        }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.member-rate {
    font-weight: bold;
}
</style>