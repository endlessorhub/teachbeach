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
            <Timezone :timezone="timezone"></Timezone>
            <div v-if="true">
              <v-btn  @click="submit" :loading="isLoading" :disabled="isLoading">See packages</v-btn>
              <!--div v-if="isSubscription">
                  <v-checkbox
                      v-model="selectAllFromStart"
                      :label="`Select all ${lessonsAvailable} from starting date/time`"
                  ></v-checkbox>
              </div-->
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
                    <div>{{curMonth}}</div>
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
                  interval-minutes="60"
                  first-interval="6"
                  interval-count="18"
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
                        :style="{ top: timeToY(item.time)+1 + 'px', height: minutesToPixels(item.duration)-2 + 'px' }"
                        :class="'my-event with-time' + (item.isActive ? ' active' : '') + (item.isPast || !item.isAvailable ? ' past' : '')"
                        @click.stop="setSlot(item)"
                      >
                        <span class="time hidden-xs-only" v-html="item.title"></span>
                      </div>
                    </template>
                  </template>
                </v-calendar>
            </div>

          </v-flex>
        </v-flex>
      </v-layout>
    </v-container>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import moment from 'moment'
import utils from '@/lib/utils.js'
import Timezone from "@/components/basic/Timezone";

export default {

    props: [
        'classData',
    ],

    components: {
        Timezone,
    },

    data: () => ({
        isLoading: false,
        pickerDate: null,
        selectedDate: null,
        selectedItems: {},
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
        selectAllFromStart: false,
        timezone: '',
    }),

    created: function () {
        let _this = this
        console.log(this.classData)
        this.instant_booking = this.classData.instant_booking
        let selectedItems = {}
        const ownEnrollments = {}
        /*
        _.each(this.orderData.class_enrolled, (v) => {
            if(ownEnrollments[v.id])
                return
            let k = v.date
            if(!selectedItems[k])
                selectedItems[k] = []
            selectedItems[k].push({
                timeFrom: moment(v.time_from, 'HH:mm'),
                timeTo: moment(v.time_to, 'HH:mm'),
                isCurrentOrder: false,
                id: v.id,
            })
        })
        */
        // switch to closest available date from today
        this.selectedItems = selectedItems
        const initialToday = this.today
        for (this.today = initialToday; utils.stringToDate(this.today)<moment(initialToday).add(183, 'days').toDate(); this.today=moment(this.today).add(7, 'days').format('YYYY-MM-DD')) {
            if(_.some(_.map(this.eventsMap, v => v), v => (v.items && _.some(v.items, item => (item.isAvailable && !item.isPast))))) {
                break
            }
        }
        if(this.isSubscription) {
            this.selectAllFromStart = true
        }
        this.timezone = this.classData.timezone
    },

    mounted() {
        this.$nextTick(() => {
            if(!Object.keys(this.eventsMap).length && this.autoSwitchLimit) {
                this.$refs.calendar.next()
                this.autoSwitchLimit--
            }
            if (!Object.keys(this.eventsMap).length && !this.autoSwitchLimit) {
                this.today = utils.dateToString(new Date())
            }
        })
    },

    computed: {
        avatar() {
            return this.classData ? this.classData.teacher.media : null
        },
        packagesLink() {
            return `/learners/${this.classData.id}/4`
        },
        duration() {
            return _.min(_.map(_.filter(this.classData.custom_packages, v => (v.isPrivate && v.lessonLength)), v => v.lessonLength.value)) || 60
        },
        isSubscription() {
            return false
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
            return this.numLessons - _.reduce(this.selectedItems, (res, val, key) => {
                return res+_.filter(val, v => (v.isCurrentOrder && !v.isExpiredPending)).length
            }, 0)
        },
        eventsMap() {
            if(!this.today || !this.classData)
                return {}
            let res = {}
            this.startDate = moment(this.today).day(0).format('YYYY-MM-DD')
            this.endDate = moment(this.today).day(6).add(1, 'd').format('YYYY-MM-DD')
            let calendarDates = utils.getCalendarDatesForPeriod(this.startDate, this.endDate, this.classData.weekdays_schedule, this.classData.start_date, this.classData.until_date, this.classData.schedule_excluded)
            console.log(this.startDate, this.endDate)
            //let startDate = utils.stringToDate(this.startDate)
            //let endDate = utils.stringToDate(this.endDate)
            for (let startDate = utils.stringToDate(this.startDate); utils.dateToString(startDate) != this.endDate; startDate.setDate(startDate.getDate()+1)) {
                if(calendarDates.indexOf(utils.dateToString(startDate)) !== -1) {
                    let day = _.find(this.classData.weekdays_schedule, v => v.weekday == startDate.getDay())
                    let endTime = moment(day.end, 'HH:mm').subtract(this.duration, 'm')
                    for (let curTime = moment(day.start, 'HH:mm'); endTime.diff(curTime) >= 0; curTime.add(this.duration, 'm')) {
                        const foundEnrollment = _.find(this.selectedItems[utils.dateToString(startDate)], v => (v.timeFrom.format('HH:mm') == curTime.format('HH:mm') && v.timeTo.format('HH:mm') == moment(curTime).add(this.duration, 'm').format('HH:mm')))
                        if(foundEnrollment)
                            foundEnrollment.shownOnCalendar = true
                        if(true) {
                            //add slot
                            if(!res[startDate.getDay()]) {
                                res[startDate.getDay()] = {
                                    items: []
                                }
                            }
                            let isAvailable = !this.selectedItems[utils.dateToString(startDate)]
                                || !_.some(this.selectedItems[utils.dateToString(startDate)], (v, k) => {
                                    const end = moment(curTime).add(this.duration, 'm')
                                    return !v.isCurrentOrder && (curTime < v.timeTo && end >= v.timeTo || end > v.timeFrom && curTime <= v.timeFrom || curTime >= v.timeFrom && end <= v.timeTo)
                                })
                            let ownLesson = _.find(this.selectedItems[utils.dateToString(startDate)], (v, k) => {
                                return v.isCurrentOrder && v.timeFrom.format('HH:mm') == curTime.format('HH:mm') && v.timeTo.format('HH:mm') == moment(curTime).add(this.duration, 'm').format('HH:mm')
                            })

                            if(ownLesson && ownLesson.status !== 'requested') {
                                //deny update of enrolls for status other than 'requested'
                                isAvailable = false
                            }

                            let isActive = this.selectedItems[utils.dateToString(startDate)]
                                && _.some(this.selectedItems[utils.dateToString(startDate)], (v, k) => {
                                    return v.isCurrentOrder && v.timeFrom.format('HH:mm') == curTime.format('HH:mm') && v.timeTo.format('HH:mm') == moment(curTime).add(this.duration, 'm').format('HH:mm')
                                })
                            res[startDate.getDay()].items.push({
                                time: curTime.format('HH:mm'),
                                duration: this.duration,
                                title: curTime.format('hh:mm a'),
                                date: utils.dateToString(startDate),
                                status: ownLesson ? ownLesson.status : null,
                                enrollment: ownLesson,
                                isAvailable: isAvailable,
                                isActive: isActive,
                                isPast: moment(`${utils.dateToString(startDate)} ${curTime.format('HH:mm')}`, 'YYYY-MM-DD HH:mm').diff(new Date()) < 0
                            })
                        }
                    }
                }
            }
            // another loop to show enrollments that are out of schedule
            for (let startDate = utils.stringToDate(this.startDate); utils.dateToString(startDate) != this.endDate; startDate.setDate(startDate.getDate()+1)) {
                if(this.selectedItems[utils.dateToString(startDate)]) {
                    _.each(this.selectedItems[utils.dateToString(startDate)], item => {
                        if(item.isCurrentOrder && !item.shownOnCalendar) {
                            res[startDate.getDay()].items.push({
                                time: item.timeFrom.format('HH:mm'),
                                duration: this.duration,
                                title: item.timeFrom.format('hh:mm a'),
                                date: utils.dateToString(startDate),
                                status: item.status,
                                enrollment: item,
                                isAvailable: false,
                                isActive: true,
                                isPast: moment(`${utils.dateToString(startDate)} ${item.timeFrom.format('HH:mm')}`, 'YYYY-MM-DD HH:mm').diff(new Date()) < 0
                            })
                        }
                    })
                }
            }
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
        curMonth() {
            return moment(this.today).format('MMMM')
        }
    },

    methods: {
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
            return
            console.log(item)
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
            if(moment(`${item.date} ${item.time}`, 'YYYY-MM-DD HH:mm').diff(new Date()) < 0)
                return
            let existingIndex = _.findIndex(this.selectedItems[item.date], (v) =>
                v.timeFrom.format('HH:mm') == item.time
                && v.timeTo.format('HH:mm') == moment(item.time, 'HH:mm').add(item.duration, 'm').format('HH:mm'))
            if(existingIndex == -1) {
                if (this.lessonsAvailable) {
                    this.selectedItems[item.date].push({
                        timeFrom: moment(item.time, 'HH:mm'),
                        timeTo: moment(item.time, 'HH:mm').add(item.duration, 'm'),
                        isCurrentOrder: true,
                        status: 'requested',
                    })
                } else {
                    this.error = 'Please deselect a time to add this one'
                }
            } else {
                if(this.selectedItems[item.date][existingIndex].isCurrentOrder)
                    this.selectedItems[item.date].splice(existingIndex, 1)
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
                    if(ditem.isCurrentOrder && ditem.status === 'requested' && utils.isTimeInFuture(`${k} ${ditem.timeFrom.format('HH:mm')}`)) {
                        dates.push({
                            selectedDate: k,
                            timeFrom: ditem.timeFrom.format('HH:mm'),
                            timeTo: ditem.timeTo.format('HH:mm'),
                        })
                    }
                })
            })
            this.$emit('next:step')
            /*
            axios.post('/api/private_enroll/', _.assign({}, this.orderData.data, {
                orderId: this.orderId,
                classId: this.classData.id,
                dates: dates,
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
            */
            //replace by saving on frontend
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
        }
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
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
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
}
.custom-head-weekday {
    text-align: center;
    color: #424242;
}

</style>