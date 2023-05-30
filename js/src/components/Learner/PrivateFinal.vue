<template>
  <form>
    <v-container grid-list-md text-xs-center style="padding: 0;">
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
          <v-flex xs12 class="text-xs-left">
              <div class="top-controls">
                  <BoundTimezone connect="/api/user/"></BoundTimezone>
                  <div v-if="!isWeeklySubscription && lessonsAvailable">Please select ({{lessonsAvailable}} of {{numLessons}}) date{{lessonsAvailable > 1 ? 's' : ''}} to meet.</div>
                  <div v-else-if="!isSubscription && !lessonsAvailable">All available dates selected</div>
                  <div v-else-if="isWeeklySubscription">
                      <div>Please select a time to meet</div>
                      <v-checkbox v-model="autoselectNextWeeks">
                          <template  v-slot:label>
                              <div class="auto-select-label">
                                  Select this day and time for all lessons
                              </div>
                          </template>
                      </v-checkbox>
                  </div>
                  <!--google-calendar-sync></google-calendar-sync-->
              </div>
              <v-layout align-center>
                <v-flex class="text-xs-center" style="flex: 0 0 auto;">
                  <v-btn
                          icon
                    outline
                    small
                    left
                    color="primary"
                    @click="$refs.calendar.prev()"
                  >
                    <v-icon dark>
                      keyboard_arrow_left
                    </v-icon>
                  </v-btn>
                </v-flex>
                <v-flex class="text-xs-center" style="flex: 0 0 200px; margin: 0 20px;">
                    <div>Select a slot</div>
                </v-flex>
                <v-flex class="text-xs-center" style="flex: 0 0 auto;">
                  <v-btn
                          icon
                    outline
                    small
                    right
                    color="primary"
                    @click="$refs.calendar.next()"
                  >
                    <v-icon
                      dark
                    >
                      keyboard_arrow_right
                    </v-icon>
                  </v-btn>
                </v-flex>

              </v-layout>
                <v-calendar
                  ref="calendar"
                  color="primary"
                  type="week"
                  :interval-minutes="intervalMinutes"
                  :first-interval="firstInterval"
                  :interval-count="intervalCount"
                  interval-height="40"
                  :day-format="dayFormat"
                  :weekday-format="weekdayFormat"
                  v-model="today"
                >
                  <!-- the events at the top (all-day) -->
                  <template
                    slot="dayHeader"
                    slot-scope="{ date, weekday, future, present, past }"
                  >
                    <template>
                      <div :class="'custom-head-weekday title' + (eventsMap[weekday] ? ' font-weight-bold' : '')">{{weekDayNames[weekday]}}</div>
                      <div class="custom-head-weekday">{{moment(date, 'YYYY-MM-DD').format('MMM Do')}}</div>
                    </template>
                  </template>
                  <template
                    slot="dayBody"
                    slot-scope="{ date, timeToY, minutesToPixels, weekday }"
                  >
                    <template v-if="eventsMap[weekday]">
                      <div
                        v-for="(item, index) in eventsMap[weekday].items"
                        :key="date+'_'+index"
                        :style="{ top: timeToY(item.orderTime)+1 + 'px', height: minutesToPixels(item.duration)-2 + 'px' }"
                        :class="'my-event with-time' + (item.isActive ? ' active' : '') + (item.isPast ? ' past' : '') + (item.isExternal ? ' external' : '')"
                        @click.stop="setSlot(item)"
                      >
                          <a v-if="item.isExternal" :href="item.externalLink" target="_blank">{{item.title}}</a>
                          <span v-else class="time hidden-xs-only" v-html="item.title"></span>
                      </div>
                    </template>
                  </template>
                </v-calendar>

          </v-flex>
        </v-flex>
        <v-snackbar
          v-model="snackbar"
          color="platform-error"
          timeout="5000"
          top
        >
          {{ error }}
          <v-btn
            dark
            flat
            @click="error = ''"
          >
            Close
          </v-btn>
        </v-snackbar>
          <v-dialog
              v-model="cancelLessonDialog"
              max-width="360"
          >
              <v-card>
                <v-card-title class="headline">{{cancelLessonDialogTitle}}</v-card-title>

                <v-card-text>
                  This lesson already confirmed by teacher, you can cancel it and choose another time.
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>

                  <v-btn
                    color="green darken-1"
                    flat="flat"
                    @click="cancelLessonDialog = false"
                  >
                    This time is fine
                  </v-btn>

                  <v-btn
                    color="green darken-1"
                    flat="flat"
                    @click="confirmCancelEnrollment"
                  >
                    Reschedule
                  </v-btn>
                </v-card-actions>
              </v-card>
          </v-dialog>
      </v-layout>
    </v-container>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Send request</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import moment from 'moment-timezone'
import utils from '@/lib/utils.js'
import BoundTimezone from "@/components/bound/BoundTimezone";
import GoogleCalendarSync from '@/components/bound/GoogleCalendarSync'
import {mapMutations, mapState, mapActions} from 'vuex';
import gapiMixin from '@/mixins/gapi'

export default {

    props: {
        'isPrivate': {
            type: Boolean,
            default: false,
        },
        'duration': {
            type: Number,
            default: 60,
        },
        'numLessons': {
            type: Number,
            default: 1,
        },
        'orderId': {
            type: Number,
            default: 1,
        },
        'classData': {
            type: Object,
            default: null,
        },
        'orderData': {
            type: Object,
            default: null,
        }
    },

    components: {
        BoundTimezone,
        GoogleCalendarSync,
    },

    mixins: [
        gapiMixin,
    ],

    data: () => ({
        isLoading: false,
        pickerDate: null,
        selectedDate: null,
        selectedItems: {}, // all items including other orders for this class
        timeFrom: null,
        timeTo: null,
        startDate: null,
        endDate: null,
        enrolled: {},
        instant_booking: null,
        weekDayNames: [
            'S',
            'M',
            'T',
            'W',
            'T',
            'F',
            'S',
        ],
        today: utils.dateToString(new Date()),
        moment: moment,
        autoSwitchLimit: 5,
        error: '',
        cancelLessonDialog: false,
        cancelLessonDialogTitle: '',
        cancelLessonDialogEnrollment: null,
        autoselectNextWeeks: true,
        weeklySelectionPlan: {},
    }),

    created: function () {
        if(!this.orderData)
            return
        let _this = this
        //console.log(this.orderData, this.classData)
        this.instant_booking = this.classData.instant_booking
        let selectedItems = {}
        const ownEnrollments = _.keyBy(this.orderData.order_enrolled, 'id')
        _.each(this.orderData.class_enrolled, (v) => {
            if(ownEnrollments[v.id])
                return
            let k = v.date
            if(!selectedItems[k])
                selectedItems[k] = []
            selectedItems[k].push({
                timeFrom: moment.tz(`${v.date} ${v.time_from}`, this.classData.timezone),
                timeTo: moment.tz(`${v.date} ${v.time_to}`, this.classData.timezone),
                isCurrentOrder: false,
                id: v.id,
            })
        })
        _.each(this.orderData.order_enrolled, (v) => {
            if(v.status === 'rejected')
                return
            let k = v.date
            if(!selectedItems[k])
                selectedItems[k] = []
            selectedItems[k].push({
                timeFrom: moment.tz(`${v.date} ${v.time_from}`, this.classData.timezone),
                timeTo: moment.tz(`${v.date} ${v.time_to}`, this.classData.timezone),
                isCurrentOrder: true,
                isExpiredPending: v.status === 'requested' && !utils.isTimeInFuture(`${v.date} ${v.time_from}`, this.classData.timezone),
                status: v.status,
                id: v.id,
                shownOnCalendar: false,
            })
        })
        // switch to closest available date from today
        this.selectedItems = selectedItems

    },

    mounted() {
        if(!this.orderData || !this.classData)
            return
        if(!this.isSubscription && this.numLessons === 1 && this.classData.until_date && this.classData.weekdays_schedule.length === 1) {
            // check if this is one lesson and one available with same duration
            console.log(this.classData, this.orderData)
            const endDate = moment(this.classData.until_date)
            let isValid = true
            let slot = null
            const day = this.classData.weekdays_schedule[0]
            for (let curTime = moment(this.classData.start_date); endDate.diff(curTime) >= 0; curTime.add(1, 'd')) {
                const weekday = Number(curTime.format('d'))
                if (day.weekday === weekday && moment(day.end, 'HH:mm').diff(moment(day.start, 'HH:mm'), 'minutes') === this.duration) {
                    // slot exactly match
                    if(slot) {
                        isValid = false
                        break;
                    }
                    slot = {
                        date: curTime.format('YYYY-MM-DD'),
                        timeFrom: moment(day.start, 'HH:mm'),
                        timeTo: moment(day.end, 'HH:mm'),
                    }
                }
            }
            if(slot && isValid) {
                this.selectedItems = {
                    [slot.date]: [
                        {
                            isCurrentOrder: true,
                            status: 'requested',
                            timeFrom: slot.timeFrom,
                            timeTo: slot.timeTo,
                        }
                    ],
                }
                this.submit()
                return
            }
        }
        this.$nextTick(() => {
            if(!Object.values(this.eventsMap).some(v => v.items.length) && this.autoSwitchLimit) {
                this.$refs.calendar.next()
                this.autoSwitchLimit--
            }
            if (!Object.values(this.eventsMap).some(v => v.items.length) && !this.autoSwitchLimit) {
                this.today = utils.dateToString(new Date())
            }
            setTimeout(() => {
                //console.log(this.$el.querySelectorAll('.my-event.with-time'));
                if([...this.$el.querySelectorAll('.my-event.with-time')].some(v => {
                    const rect = v.getBoundingClientRect();
                    return rect.top >= 0 && rect.bottom <= (window.innerHeight || document.documentElement.clientHeight)
                })) {
                    return
                }
                const topEl = [...this.$el.querySelectorAll('.my-event.with-time')].sort((a, b) => a.offsetTop-b.offsetTop).shift()
                if(topEl) {
                    topEl.scrollIntoView({behavior: 'smooth'})
                }
            }, 300)
        })
    },

    computed: {
        ...mapState({
            'user': state => state.user,
        }),
        intervalMinutes() {
            return this.duration >= 30 ? 60 : 30
        },
        avatar() {
            return this.classData ? this.classData.teacher.media : null
        },
        isSubscription() {
            return this.orderData && this.orderData.data && this.orderData.data.package && this.orderData.data.package.isSubscription
        },
        isWeeklySubscription() {
            return this.isSubscription && this.orderData && this.orderData.data && this.orderData.data.package && this.orderData.data.package.period === "week|1"
        },
        subscriptionStartDate() {
            return this.orderData && this.orderData.current_period_start
                ? new Date(this.orderData.current_period_start*1000)
                : null
        },
        subscriptionEndDate() {
            return this.orderData && this.orderData.current_period_end
                ? new Date(this.orderData.current_period_end*1000)
                : null
        },
        subscriptionEndAt() {
            return this.orderData && this.orderData.end_at
                ? new Date(this.orderData.end_at*1000)
                : null
        },
        subscriptionClassesPerInterval() {
            return this.orderData && this.orderData.data && this.orderData.data.package && this.orderData.data.package.classesPerInterval
        },
        snackbar: {
            get() {
                return !!this.error
            },
            set(v) {
                if(!v)
                    this.error = ''
            },
        },
        lessonsAvailable() {
            if(this.isSubscription) {
                return this.subscriptionClassesPerInterval - this.findLessonsForPeriod(this.subscriptionStartDate, this.subscriptionEndDate).length
            }
            return this.numLessons - _.reduce(this.selectedItems, (res, val, key) => {
                return res+_.filter(val, v => v.isCurrentOrder && !v.isExpiredPending).length
            }, 0)
        },
        firstInterval() {
            return Math.min(6, ...Object.values(this.eventsMap).map(
                w => Math.min(...w.items.map(
                    l => moment(l.dateTime).tz(this.timezone).hour()
                ))
            ))/this.intervalMinutes*60
        },
        intervalCount() {
            return 24/this.intervalMinutes*60-this.firstInterval
        },
        eventsMap() {
            if(!this.today || !this.classData || !this.timezone)
                return {}
            let res = {}
            const startTime = moment.tz(this.today, this.timezone).day(0).tz(this.classData.timezone);
            const endTime = moment.tz(this.today, this.timezone).day(6).add(1, 'd').tz(this.classData.timezone);
            const available = utils.getAvailableTimesForPeriod(startTime, endTime, this.classData);

/*
const shiftedStart = moment(`${v.date} ${v.start}`, this.classData.timezone).tz(this.timezone);
const shiftedEnd = moment(`${v.date} ${v.end}`, this.classData.timezone).tz(this.timezone);
return {
    start: shiftedStart,
    end: shiftedEnd,
}
*/

            available.forEach(slot => {
                let endTime = moment.tz(slot.date+' '+slot.end, this.classData.timezone).subtract(this.duration, 'm')
                for (let curTime = moment.tz(slot.date+' '+slot.start, this.classData.timezone); endTime.diff(curTime) >= 0; curTime.add(this.duration, 'm')) {
                    const foundEnrollment = _.find(this.selectedItems[slot.date], v => (v.timeFrom.format('HH:mm') === curTime.format('HH:mm') && v.timeTo.format('HH:mm') === moment(curTime).add(this.duration, 'm').format('HH:mm')))
                    if(foundEnrollment)
                        foundEnrollment.shownOnCalendar = true

                    //add slot
                    if(!res[moment(curTime).tz(this.timezone).day()]) {
                        res[moment(curTime).tz(this.timezone).day()] = {
                            items: []
                        }
                    }
                    let isAvailable = !this.selectedItems[slot.date]
                        || !_.some(this.selectedItems[slot.date], (v, k) => {
                            const end = moment(curTime).add(this.duration, 'm')
                            return !v.isCurrentOrder && (curTime < v.timeTo && end >= v.timeTo || end > v.timeFrom && curTime <= v.timeFrom || curTime >= v.timeFrom && end <= v.timeTo)
                        })
                    let ownLesson = _.find(this.selectedItems[slot.date], (v, k) => {
                        return v.isCurrentOrder && v.timeFrom.format('HH:mm') === curTime.format('HH:mm') && v.timeTo.format('HH:mm') === moment(curTime).add(this.duration, 'm').format('HH:mm')
                    })

                    if(ownLesson && ownLesson.status !== 'requested') {
                        //deny update of enrolls for status other than 'requested'
                        isAvailable = false
                    }

                    let isActive = this.selectedItems[slot.date]
                        && _.some(this.selectedItems[slot.date], (v, k) => {
                            return v.isCurrentOrder && v.timeFrom.format('HH:mm') === curTime.format('HH:mm') && v.timeTo.format('HH:mm') === moment(curTime).add(this.duration, 'm').format('HH:mm')
                        })
                    let isPlan = this.weeklySelectionPlan[slot.date]
                        && _.some(this.weeklySelectionPlan[slot.date], (v, k) => {
                            return v.timeFrom.format('HH:mm') === curTime.format('HH:mm') && v.timeTo.format('HH:mm') === moment(curTime).add(this.duration, 'm').format('HH:mm')
                        })
                    const isPast = curTime.diff(new Date()) < 0;
                    if((isAvailable || ownLesson) && !isPast) {
                        // show only available slots
                        res[moment(curTime).tz(this.timezone).day()].items.push({
                            dateTime: moment(curTime), // class timezone, moment object
                            orderTime: moment(curTime).tz(this.timezone).format('HH:mm'),
                            time: curTime.format('HH:mm'), // class timezone, string
                            duration: this.duration,
                            title: moment(curTime).tz(this.timezone).format('hh:mm a'), // order timezone, string
                            date: curTime.format('YYYY-MM-DD'), // class timezone, string
                            status: ownLesson ? ownLesson.status : null,
                            enrollment: ownLesson,
                            isAvailable,
                            isActive,
                            isPast,
                            isPlan,
                        })
                    }
                }
            })

            // another loop to show enrollments that are out of schedule
            for (let curTime = moment(startTime); curTime < endTime; curTime.add(1, 'd')) {
                if(this.selectedItems[curTime.format('YYYY-MM-DD')]) {
                    _.each(this.selectedItems[curTime.format('YYYY-MM-DD')], item => {
                        if(item.isCurrentOrder && !item.shownOnCalendar) {
                            if(!res[moment(curTime).tz(this.timezone).day()])
                                res[moment(curTime).tz(this.timezone).day()] = {items: []}
                            const dateTime = moment.tz(`${curTime.format('YYYY-MM-DD')} ${item.timeFrom.format('HH:mm')}`, this.classData.timezone);
                            res[moment(curTime).tz(this.timezone).day()].items.push({
                                dateTime,
                                orderTime: dateTime.tz(this.timezone).format('HH:mm'),
                                time: item.timeFrom.format('HH:mm'),
                                duration: this.duration,
                                title: moment(item.timeFrom).tz(this.timezone).format('hh:mm a'),
                                date: curTime.format('YYYY-MM-DD'),
                                status: item.status,
                                enrollment: item,
                                isAvailable: false,
                                isActive: true,
                                isPast: curTime.diff(new Date()) < 0
                            })
                        }
                    })
                }
            }
            /*
            for (let date in this.externalCalendarEvents) {
                if(date in res) {
                    res[date].items = [...res[date].items, ...this.externalCalendarEvents[date]]
                } else {
                    res[date] = {
                        items: [...this.externalCalendarEvents[date]],
                    }
                }
            }
            */
            return res
        },
        minFrom() {
            return this.currentDateTimes.length ? this.currentDateTimes[0].start : null
        },
        maxFrom() {
            let time = this.currentDateTimes.length ? this.currentDateTimes[this.currentDateTimes.length-1].end : null
            if(!time)
                return
            let dateTime = utils.stringToDate(this.selectedDate)
            dateTime.setHours(time.split(':')[0], time.split(':')[1])
            dateTime.setMinutes(dateTime.getMinutes()-this.duration)
            return String('0'+dateTime.getHours()+'').substr(-2)+':'+String('0'+dateTime.getMinutes()+'').substr(-2)
        },
        minTo() {
            let time = this.currentDateTimes.length ? this.currentDateTimes[0].start : null
            if(!time)
                return
            let dateTime = utils.stringToDate(this.selectedDate)
            dateTime.setHours(time.split(':')[0], time.split(':')[1])
            dateTime.setMinutes(dateTime.getMinutes()+Number(this.duration))
            return String('0'+dateTime.getHours()+'').substr(-2)+':'+String('0'+dateTime.getMinutes()+'').substr(-2)
        },
        maxTo() {
            return this.currentDateTimes.length ? this.currentDateTimes[this.currentDateTimes.length-1].end : null
        },
        currentDateTimes() {
            if(!this.selectedDate)
                return []
            const weekday = utils.stringToDate(this.selectedDate).getDay()
            return _.filter(this.classData.weekdays_schedule, {weekday}) || []
        },
        currentDateTimesFormatted() {
            return _.map(this.currentDateTimes, v => ({
                start: utils.time24HtoAMPM(v.start),
                end: utils.time24HtoAMPM(v.end),
            }))
        },
        availableDates() {
            let y = new Date().getFullYear()
            let m = new Date().getMonth()
            if (this.pickerDate) {
                y = this.pickerDate.split('-')[0]
                m = this.pickerDate.split('-')[1]-1
            }
            let startDate = new Date(Math.max(new Date(), utils.stringToDate(this.classData.start_date)))
            return _.keyBy(utils.getCalendarDatesForMonth(y, m, this.classData.weekdays_schedule, utils.dateToString(startDate), this.classData.until_date, this.classData.schedule_excluded || []), v => v)
        },
        selectedDateFormatted() {
            if(!this.selectedDate)
                return ''
            return utils.stringToDate(this.selectedDate).toLocaleString('en-us', { month: 'long', day: 'numeric' })
        },
        weeklySelectionPlanArray() {
            return Object.entries(this.weeklySelectionPlan).reduce((acc, [date, v]) => {
                return [...acc, ...v.map(slot => ({
                    date,
                    timeFrom: slot.timeFrom.tz(this.classData.timezone).format('HH:mm'),
                    timeTo: slot.timeTo.tz(this.classData.timezone).format('HH:mm'),
                }))]
            }, [])
        },
        externalCalendarEvents() {
            const res = {}
            const perDayEvents = this.externalEvents.reduce((acc, v) => {
                const date = moment(v.start.dateTime).tz(this.timezone).format('YYYY-MM-DD')
                if(!acc[date])
                    acc[date] = []
                acc[date].push(v)
                return acc
            }, {})
            const startTime = moment.tz(this.today, this.timezone).day(0).tz(this.classData.timezone);
            const endTime = moment.tz(this.today, this.timezone).day(6).add(1, 'd').tz(this.classData.timezone);
            const end = endTime.toDate()
            for (let start = moment(startTime);start.toDate() <= end; start.add(1, 'day')) {
                const key = start.format('YYYY-MM-DD')
                if(!perDayEvents[key])
                    continue
                res[start.day()] = perDayEvents[key].map(v => {
                    const classStartTime = moment(v.start.dateTime).tz(this.classData.timezone)
                    const classEndTime = moment(v.end.dateTime).tz(this.classData.timezone)
                    return {
                        key: `external-${v.id}`,
                        dateTime: moment(classStartTime), // class timezone, moment object
                        orderTime: moment(classStartTime).tz(this.timezone).format('HH:mm'),
                        time: classStartTime.format('HH:mm'), // class timezone, string
                        duration: classEndTime.diff(classStartTime, 'minutes'),
                        title: v.summary, // order timezone, string
                        date: classStartTime.format('YYYY-MM-DD'), // class timezone, string
                        status: null,
                        enrollment: null,
                        isAvailable: false,
                        isActive: false,
                        isPast: false,
                        isPlan: false,
                        isExternal: true,
                        externalLink: v.htmlLink,
                    }
                })
            }
            return res
        },
    },

    methods: {
        ...mapMutations(['setTimezone']),
        toggleAutoselectNextWeek() {
            this.autoselectNextWeeks = !this.autoselectNextWeeks
            this.recalcWeeklyPlan()
        },
        confirmCancelEnrollment() {
            this.isLoading = true
            axios.post(`/api/student_cancel_enrollment/${this.cancelLessonDialogEnrollment.id}`).then((res) => {
                if(res.data.status) {
                    _.each(this.selectedItems, (itemList, k) => {
                        if(_.find(itemList, {id: this.cancelLessonDialogEnrollment.id})) {
                            this.$set(this.selectedItems, k, _.filter(itemList, item => item.id !== this.cancelLessonDialogEnrollment.id))
                        }
                    })
                }
                return true
            }).catch(e => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
                this.cancelLessonDialog = false
            })
        },
        setSlot(item) {
            console.log(item)
            if(item.isExternal) {

                return
            }
            if(!item.isAvailable) {
                if(item.status === 'approved' || item.status === 'requested') {
                    //console.log()
                    this.cancelLessonDialogEnrollment = item.enrollment
                    this.cancelLessonDialogTitle = `${item.enrollment.timeFrom.format('MMM D')}, ${item.enrollment.timeFrom.format('h:mma')} - ${item.enrollment.timeTo.format('h:mma')}`
                    this.cancelLessonDialog = true
                    return
                } else
                    return this.error = 'This lesson is not available, try another one'
            }
            if(!this.selectedItems[item.date])
                this.$set(this.selectedItems, item.date, [])
            if(moment(item.dateTime).diff(new Date()) < 0)
                return
            let existingIndex = _.findIndex(this.selectedItems[item.date], (v) =>
                v.timeFrom.format('HH:mm') === item.time
                && v.timeTo.format('HH:mm') === moment(item.time, 'HH:mm').add(item.duration, 'm').format('HH:mm'))
            if(existingIndex === -1) {
                if(this.isWeeklySubscription && item.dateTime.toDate() > this.subscriptionEndDate && item.dateTime.toDate() < this.subscriptionEndAt) {
                    // slot is in the next time period, but before subscription end
                    const period = this.findSubscriptionPeriod(item.dateTime.toDate())
                    if(period) {
                        const reserverLessons = this.findLessonsForPeriod(...period)
                        if(reserverLessons.length < this.subscriptionClassesPerInterval) {
                            this.selectedItems[item.date].push({
                                timeFrom: moment.tz(`${item.date} ${item.time}`, this.classData.timezone),
                                timeTo: moment.tz(`${item.date} ${item.time}`, this.classData.timezone).add(item.duration, 'm'),
                                isCurrentOrder: true,
                                status: 'requested',
                            })
                            this.selectedItems = {...this.selectedItems}
                            //this.recalcWeeklyPlan()
                        }
                    }
                } else if (this.lessonsAvailable > 0) {
                    if(this.isSubscription) {
                        const selectedTime = moment(item.dateTime).toDate()
                        if(this.subscriptionStartDate > selectedTime || this.subscriptionEndDate < selectedTime) {
                            this.error = `Please select within active subscription period (${this.subscriptionStartDate.toLocaleString('en-us', { month: 'long', day: 'numeric' })} - ${this.subscriptionEndDate.toLocaleString('en-us', { month: 'long', day: 'numeric' })})`
                            return
                        }
                    }
                    this.selectedItems[item.date].push({
                        timeFrom: moment.tz(`${item.date} ${item.time}`, this.classData.timezone),
                        timeTo: moment.tz(`${item.date} ${item.time}`, this.classData.timezone).add(item.duration, 'm'),
                        isCurrentOrder: true,
                        status: 'requested',
                    })
                    this.selectedItems = {...this.selectedItems}
                    this.recalcWeeklyPlan()
                } else {
                    this.error = 'Please deselect a time to add this one'
                }

            } else {
                if(this.selectedItems[item.date][existingIndex].isCurrentOrder) {
                    this.selectedItems[item.date].splice(existingIndex, 1)
                    this.selectedItems = {...this.selectedItems}
                }
            }
            /*
            this.selectedDate = item.date
            this.timeFrom = moment(item.time, 'HH:mm')
            this.timeTo = moment(item.time, 'HH:mm').add(item.duration, 'm')
            */
        },
        requestTime() {

        },
        allowedDates(v) {
            return this.availableDates[v] ? true : false
        },
        back() {
            this.$emit('prev:step')
        },
        submit () {
            //console.log(this); return

            this.isLoading = true
            let _this = this
            let dates = []
            _.each(this.selectedItems, (v, k) => {
                _.each(v, ditem => {
                    if(ditem.isCurrentOrder && ditem.status === 'requested') {
                        dates.push({
                            selectedDate: k,
                            timeFrom: ditem.timeFrom.format('HH:mm'),
                            timeTo: ditem.timeTo.format('HH:mm'),
                        })
                    }
                })
            })
            axios.post('/api/private_enroll/', _.assign({}, this.orderData.data, {
                orderId: this.orderId,
                classId: this.classData.id,
                dates: dates,
                //plan: this.weeklySelectionPlanArray,
            })).then((res) => {
                console.log('done', res)
                //this.$emit('next:step')
                if(this.instant_booking && res.data.isFirstLesson) {
                    this.$router.push('/dashboard/learn/classes/firstud')
                } else {
                    this.$router.push('/dashboard/learn/classes/')
                }
            }).catch(() => {
                //console.log(arguments)
            }).then(() => {
                _this.isLoading = false
            })
        },
        clear () {

        },
        disabledHoursStart() {
            return _.concat(utils.disabledHoursFromTime(this.minFrom, true)(), utils.disabledHoursFromTime(this.maxFrom, false)())
        },
        disabledMinutesStart(hour) {
            return _.concat(utils.disabledMinutesFromTime(this.minFrom, true)(hour), utils.disabledMinutesFromTime(this.maxFrom, false)(hour))
        },
        disabledHoursEnd() {
            return _.concat(utils.disabledHoursFromTime(this.minTo, true)(), utils.disabledHoursFromTime(this.maxTo, false)())
        },
        disabledMinutesEnd(hour) {
            return _.concat(utils.disabledMinutesFromTime(this.minTo, true)(hour), utils.disabledMinutesFromTime(this.maxTo, false)(hour))
        },
        dayFormat() {
            return ''
        },
        weekdayFormat() {
            return ''
        },
        recalcWeeklyPlan() {
            if(this.isWeeklySubscription)
                this.cleanupWeeklyPlan()
            if(this.isWeeklySubscription && this.autoselectNextWeeks && this.subscriptionEndAt) {
                // add subscription plan
                const plan = {}
                for (let date in this.selectedItems) {
                    for (let item of this.selectedItems[date]) {
                        // skip slots for another orders or not in current subscription period
                        if(!item.isCurrentOrder || item.timeFrom.toDate() > this.subscriptionEndDate || item.timeTo.toDate() < this.subscriptionStartDate)
                            continue;
                        let mult = 1
                        while(moment(item.timeTo).add(mult, 'w').toDate() < this.subscriptionEndAt){
                            let current = moment(date).add(mult, 'w')
                            const timeFrom = moment(item.timeFrom).add(mult, 'w')
                            const timeTo = moment(item.timeTo).add(mult, 'w')
                            mult++
                            const period = this.findSubscriptionPeriod(timeFrom.toDate())
                            if(!period)
                                continue;
                            const lessons = this.findLessonsForPeriod(...period)
                            if(lessons.length >= this.orderData.data.package.classesPerInterval) {
                                continue;
                            }
                            if(!this.selectedItems[current.format('YYYY-MM-DD')])
                                this.selectedItems[current.format('YYYY-MM-DD')] = []

                            if(this.selectedItems[current.format('YYYY-MM-DD')].find(v => {
                                return v.timeFrom.format('HH:mm') === item.timeFrom.format('HH:mm')
                                    && v.timeTo.format('HH:mm') === item.timeTo.format('HH:mm')
                            })) {
                                continue
                            }
                            this.selectedItems[current.format('YYYY-MM-DD')].push({
                                timeFrom: timeFrom,
                                timeTo: timeTo,
                                isCurrentOrder: true,
                                status: 'requested',
                            })
                        }
                    }
                }
                //this.weeklySelectionPlan = plan
            }
            this.selectedItems = {...this.selectedItems}
        },
        cleanupWeeklyPlan() {
            if(!this.isWeeklySubscription)
                return
            for (let date in this.selectedItems) {
                this.selectedItems[date] = this.selectedItems[date].filter(v => v.id || v.timeTo.toDate() < this.subscriptionEndDate)
            }
            this.selectedItems = {...this.selectedItems}
        },
        findSubscriptionPeriod(dateTime) {
            for (let curStart = new Date(this.subscriptionStartDate); curStart < this.subscriptionEndAt; curStart.setDate(curStart.getDate() + 7)) {
                let curEnd = new Date(curStart)
                curEnd.setDate(curEnd.getDate() + 7)
                if(dateTime >= curStart && dateTime <= curEnd) {
                    return [curStart, curEnd]
                }
            }
            return null
        },
        findLessonsForPeriod(start, end) {
            let lessons = []
            for (let curStart = new Date(start); curStart <= end; curStart.setDate(curStart.getDate() + 1)) {
                const dateStr = moment(curStart).tz(this.classData.timezone).format('YYYY-MM-DD')
                if(this.selectedItems[dateStr])
                    lessons = [...lessons, ...this.selectedItems[dateStr].filter(v => {
                        return v.isCurrentOrder
                            && v.timeFrom.toDate() >= start
                            && v.timeTo.toDate() <= end
                            && v.status !== 'rejected'
                    })]
            }
            return lessons
        },
    },
    watch: {
        timeFrom(newVal, oldVal) {
            this.timeTo = moment(newVal).add(this.duration, 'm')
            /*
            let dateTime = utils.stringToDate(this.selectedDate)
            dateTime.setHours(newVal.split(':')[0], newVal.split(':')[1])
            dateTime.setMinutes(dateTime.getMinutes()+Number(this.duration))
            this.timeTo = String('0'+dateTime.getHours()+'').substr(-2)+':'+String('0'+dateTime.getMinutes()+'').substr(-2)
            */
        },
        timeTo(newVal, oldVal) {
            //this.timeFrom = moment(newVal).add(-this.duration, 'm')
            /*
            let dateTime = utils.stringToDate(this.selectedDate)
            dateTime.setHours(newVal.split(':')[0], newVal.split(':')[1])
            dateTime.setMinutes(dateTime.getMinutes()-this.duration)
            this.timeFrom = String('0'+dateTime.getHours()+'').substr(-2)+':'+String('0'+dateTime.getMinutes()+'').substr(-2)
            */
        },
        autoselectNextWeeks() {
            this.recalcWeeklyPlan()
        },

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

@import "../../styles/_variables.scss";

.my-event {
    overflow: visible;
    text-overflow: ellipsis;
    border-radius: 2px;
    //background-color: yellow;
    color: black;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;
    margin-right: 8px;
    position: relative;

    span.time {
        position: absolute;
    }

    &.with-time {
        position: absolute;
        right: 4px;
        margin-right: 0px;
    }
    &.active {
        background-color: yellow;
    }
    &.past {
        background-color: silver;
    }
    &.active.past {
        background: repeating-linear-gradient(
          -45deg,
          yellow,
          yellow 5px,
          silver 5px,
          silver 10px
        )
    }

    &.external {
        background-color: $platform-blue;
        cursor: auto;
        a {
            color: black;
        }
    }
}
.custom-head-weekday {
    text-align: center;
    color: #424242;
}
.top-controls {
    margin-left: 20px;
}
.auto-select-label {
    font-size: 18px;
    font-weight: bold;
}
</style>