<template>

    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 md6 style="padding: 2px;">
            <v-flex xs12 class="text-xs-left">
                <h3>Congratulations! You have credits for {{restNumLessons}} classes in {{name}}</h3>
                <div>Sign-in to classes below. </div>
            </v-flex>
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
              <div v-for="(v, i) in currentPeriodSchedule" :key="v.value">
                  <v-checkbox
                      v-model="selectedLessons"
                      :label="v.label"
                      :value="v.value"
                      hide-details
                      :disabled="v.isDisabled"
                  ></v-checkbox>
              </div>
          </v-flex>
        <v-flex xs12 class="text-xs-left">
            <div>{{selectedLessons.length}} of {{restNumLessons}} selected</div>
            <div>No Thanks, I’ll sign-in later from my dashboard.</div>
            <div>
                <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">GO</v-btn>
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
import moment from 'moment'

export default {

    components: {

    },
    props: [
        'class_media',
        'currency',
        'custom_packages',
        'day_select_type',
        'drop_in_rate',
        'enrolled',
        'flexible_dates',
        'master_media',
        'maxSize',
        'name',
        'orders',
        'package',
        'schedule_dates',
        'schedule_excluded',
        'standard_packages',
        'start_date',
        'until_date',
        'weekdays_schedule',

        'learnerData',
        'step',
        'orderId',
    ],

    data: () => ({
        isLoading: false,
        currentDate: new Date(),
        cardDetail: {
            number: '',
            name: '',
            expiry: '',
            cvc: ''
        },
        selectedLessons: [],
        //availableLessons: [],
        carouselHeight: 300,
        autoSwitchLimit: 5,
    }),

    created: function () {
        let _this = this
        if (this.schedule_dates.length === 1 && Number(this.package.numberOfLessons) === 1) {
            // enroll automatically
            const day = this.schedule_dates[0]
            this.selectedLessons = [`${day.date}_${day.start}-${day.end}`]
            this.submit()
        }
        if (!this.flexible_dates && this.day_select_type === 'monthly') {
            // enroll fixed dates automatically
            this.selectedLessons = this.allDatesSchedule;
            this.submit()
        }
        if (this.$store.state.learnerData) {
            this.selectedLessons = _this.$store.state.learnerData.selectedLessons || []
        }

        this.$nextTick(() => {
            this.update()
            window.addEventListener('resize', this.update);
            //console.log(this.carouselHeight)
        })
    },

    beforeDestroy() {
        window.removeEventListener('resize', this.update);
    },

    mounted() {
        this.$nextTick(() => {
            if(!_.filter(this.currentPeriodSchedule, d => !d.isDisabled).length && this.autoSwitchLimit) {
                this.nextWeek()
                this.autoSwitchLimit--
            }
            if(!this.currentWeekSchedule.length && !this.autoSwitchLimit) {
                this.currentDate = new Date()
            }
        })
    },

    computed: {
        /*
        selectedLessons: {
            get() {
                return []
            },
            set(v) {
                console.log(v)
            },
        },
        */
        restNumLessons() {
            return this.package ? this.package.numberOfLessons : ''
        },
        mediaUrl() {
            if(this.class_media && this.class_media.length)
                return this.class_media[0].class_media
            else
                return  this.master_media ? this.master_media : ''
        },
        allDatesSchedule() {
            return (this.schedule_dates || []).map(v => `${v.date}_${v.start}-${v.end}`);
        },
        currentPeriodSchedule() {
            return _.map(this.currentWeekSchedule, d => ({
                value: d.value,
                label: this.getLessonUnavailableText(d) ? `${d.label} (${this.getLessonUnavailableText(d)})` : d.label,
                isDisabled: this.isCheckboxDisabled(d),
            }))
        },
        currentWeekSchedule() {
            if(this.day_select_type == 'weekly') {
                let days = utils.getCalendarDatesForPeriod(
                    utils.dateToString(new Date()),
                    utils.dateToString(this.endCalDate),
                    this.weekdays_schedule,
                    utils.dateToString(this.startCalDate),
                    utils.dateToString(this.endCalDate),
                    this.schedule_excluded
                )
                let res = []
                _.each(days, d => {
                    _.each(_.filter(this.weekdays_schedule, {weekday: utils.stringToDate(d).getDay()}), l => {
                        res.push({
                            label: `${utils.stringToDate(d).toLocaleString('en-us', { weekday: 'long', month: 'short', day: 'numeric' })} ${utils.time24HtoAMPM(l.start)} to ${utils.time24HtoAMPM(l.end)}`,
                            value: `${d}_${l.start}-${l.end}`,
                        })
                    })
                })
                return res
            } else {
                let dayDict = _.keyBy(this.schedule_dates, 'date')
                let res = []
                for (let current = new Date(this.startCalDate); current <= this.endCalDate; current.setDate(current.getDate()+1)) {
                    if(dayDict[utils.dateToString(current)]) {
                        res.push({
                            label: `${current.toLocaleString('en-us', { weekday: 'long', day: 'numeric', month: 'short' })} ${utils.time24HtoAMPM(dayDict[utils.dateToString(current)].start)} to ${utils.time24HtoAMPM(dayDict[utils.dateToString(current)].end)}`,
                            value: `${utils.dateToString(current)}_${dayDict[utils.dateToString(current)].start}-${dayDict[utils.dateToString(current)].end}`
                        })
                    }
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
        timeEnrollsWithPersons() {
            const orderDict = this.orders.reduce((acc, v) => ({...acc, ...{[v.id]: v.data}}), {})
            return this.enrolled.reduce((acc, v) => {
                if(v.status !== 'approved')
                    return acc
                const key = this.getTimeKey(v.date, v.time_from)
                if(!acc[key])
                    acc[key] = {
                        persons: 0,
                    }
                if(orderDict[v.order_id]) {
                    acc[key].persons += Number(orderDict[v.order_id].persons) || 1
                }
                return acc
            }, {})
        }
    },

    methods: {
        getTimeKey(date, time_from) {
            return date+'_'+time_from
        },
        update() {
            if(this.step && this.$refs.carouselEl && this.$refs.carouselEl.$el && this.$refs.carouselEl.$el.clientWidth)
                this.carouselHeight = this.$refs.carouselEl.$el.clientWidth
        },
        isCheckboxDisabled(v) {
            //console.log(v, this.selectedLessons)
            const [date, from, to] = _.concat(v.value.split('_')[0], v.value.split('_')[1].split('-'))
            if(moment(`${date} ${from}`).toDate() < new Date())
                return true
            if (this.package && this.package.numberOfLessons <= this.selectedLessons.length && this.selectedLessons.indexOf(v.value) === -1) {
                return true
            }
            if(this.maxSize && this.timeEnrollsWithPersons[this.getTimeKey(date, from)]) {
                //console.log('check available space', this.maxSize, this.timeEnrollsWithPersons[this.getTimeKey(date, from)].persons, this.learnerData)
                if(this.learnerData && Number(this.learnerData.persons) > this.maxSize - this.timeEnrollsWithPersons[this.getTimeKey(date, from)].persons)
                    return true
            }
            return false
        },
        getLessonUnavailableText(v) {
            const [date, from, to] = _.concat(v.value.split('_')[0], v.value.split('_')[1].split('-'))
            if(this.maxSize && this.timeEnrollsWithPersons[this.getTimeKey(date, from)]) {
                //console.log('check available space', this.maxSize, this.timeEnrollsWithPersons[this.getTimeKey(date, from)].persons, this.learnerData)
                if(this.learnerData && Number(this.learnerData.persons) > this.maxSize - this.timeEnrollsWithPersons[this.getTimeKey(date, from)].persons)
                    return 'class full'
            }
            return ''
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
            this.$emit('prev:step')
        },
        submit () {
            this.$store.commit('mergeLearnerData', {
                selectedLessons: this.selectedLessons,
            })
            //this.$router.push({path: '/learner/checkout'})
            this.isLoading = true
            axios.post('/api/group_enroll/', _.assign({}, {
                orderId: this.orderId,
                selectedLessons: this.selectedLessons,
            })).then((res) => {
                console.log('done', res)
                if(res.data.isFirstLesson) {
                    this.$router.push('/dashboard/learn/classes/firstud')
                } else {
                    this.$router.push('/dashboard/learn/classes/')
                }
            }).catch(() => {
                //console.log(arguments)
            }).then(() => {
                this.isLoading = false
            })

        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>