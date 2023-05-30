<template>
    <div>
  <form>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
          <h3>Show your weekly availability</h3>
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <v-switch
              v-model="allowStudentsBookInstantly"
              label="Allow students to book dates instantly"
              hide-details
            ></v-switch>
        </v-flex>
        <v-flex xs12 class="text-xs-left">

            <v-calendar
              ref="calendar"
              color="primary"
              type="week"
              interval-minutes="60"
              first-interval="6"
              interval-count="18"
              interval-height="20"
              :day-format="dayFormat"
              :weekday-format="weekdayFormat"
              @click:day="openDay"
              @click:time="openDay"
            >
              <!-- the events at the top (all-day) -->
              <template
                slot="dayHeader"
                slot-scope="{ date, weekday, future, present, past }"
              >
                <template v-if="eventsMap[weekday] && !eventsMap[weekday].time">
                  <div
                    :key="date+'_fullday'"
                    :class="weekDayClasses(past, present, future)"
                    v-html="eventsMap[weekday].title"
                  ></div>
                </template>
                <template v-else>
                  <div :class="'custom-head-weekday title' + (eventsMap[weekday] ? ' font-weight-bold' : '')">{{weekDayNames[weekday]}}</div>
                </template>
              </template>

              <template
                slot="dayBody"
                slot-scope="{ date, timeToY, minutesToPixels, weekday }"
              >
                <template v-if="eventsMap[weekday] && eventsMap[weekday].time">
                  <div
                    v-if="eventsMap[weekday].time"
                    :key="date+'_timed'"
                    :style="{ top: timeToY(eventsMap[weekday].time) + 'px', height: minutesToPixels(eventsMap[weekday].duration) + 'px' }"
                    :class="weekdayBlockClass(weekday)"
                    @click.stop="openDay(eventsMap[weekday])"
                  >
                    <span v-if="minutesToPixels(eventsMap[weekday].duration) > 40" class="time" v-html="eventsMap[weekday].title"></span>
                    <div class="v-chip__close remove-weekday" @click.stop="tryRemoveWeekday(weekday)"><i aria-hidden="true" class="v-icon material-icons theme--light">cancel</i></div>
                  </div>
                </template>
              </template>
            </v-calendar>
            <v-dialog
              v-model="weekDayOpened"
              max-width="400"
              persistent
            >
              <v-card>
                <v-card-title class="headline">{{weekDayDialog.title}}</v-card-title>

                <v-card-text>
                  <v-layout align-top justify-space-between row wrap>
                    <v-flex xs5 class="text-xs-left">
                        <v-autocomplete
                            v-model="weekdayDialogStartTime"
                            :items="weekdayDialogStartTimeItems"
                            label="From"
                            placeholder="time"
                            prepend-icon="schedule"
                            :menu-props="autoMenuProps"
                        ></v-autocomplete>
                    </v-flex>
                    <v-flex xs5 class="text-xs-left">
                        <v-autocomplete
                            v-model="weekdayDialogEndTime"
                            :items="weekdayDialogEndTimeItems"
                            label="To"
                            placeholder="time"
                            prepend-icon="schedule"
                            :menu-props="autoMenuProps"
                        ></v-autocomplete>
                      </v-flex>
                      <v-flex xs12 class="text-xs-left">
                          <v-alert
                              :value="weekDayDialogErrorOpened"
                              type="error"
                              color="platform-error"
                              icon="warning"
                              outline
                              transition="scale-transition"
                            >
                              {{weekDayDialog.error}}
                            </v-alert>
                      </v-flex>

                  </v-layout>
                </v-card-text>

                <v-card-actions>

                  <v-btn
                    @click="clearWeekDayData"
                  >
                    Cancel
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    @click="saveWeekDayData"
                  >
                    Save
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
        </v-flex>
          <v-flex xs12 text-xs-left>
              <div v-for="v in weekdaysScheduledList">{{v}}</div>
          </v-flex>
      </v-layout>
        <snack v-if="localError" v-model="localError"/>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>

  <v-dialog
        v-model="isRescheduleOpened"
        max-width="400"
        persistent
    >
        <v-card>
        <v-card-title class="headline">Reschedule Confirmation</v-card-title>
        <v-card-text>
            <form>
                <v-alert
                    type="error"
                    color="platform-error"
                    transition="scale-transition"
                >
    You already have {{ enrolledNum }}
    student{{ enrolledNum > 1 ? 's' : '' }} enrolled at this time.
                </v-alert>

                <div class="title">Are you sure you want to cancel this time?</div>
                <div class="subtitle">Corresponding enrollments will be deleted</div>
                <v-textarea
                    v-model="rescheduleMessage"
                    auto-grow
                    box
                    label="Email to the students"
                    rows="3"
                ></v-textarea>
            </form>
        </v-card-text>

        <v-card-actions>
            <v-btn
                @click="isRescheduleOpened = false"
            >
                No
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
                color="primary"
                @click="saveReschedule"
                :loading="isRescheduleLoading"
            >
                Yes, reschedule
            </v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>

  </div>
</template>

<script>
import utils from '@/lib/utils.js'
import DateSelect from '@/components/basic/DateSelect.vue'
import Snack from '@/components/basic/Snack'
import api from '@/lib/api.js';

import _ from 'lodash'
import moment from 'moment'

import axios from 'axios'

export default {

    data: () => ({
        isLoading: false,
        scheduleFrom: null,
        scheduleTo: null,
        scheduleDates: [],
        allowStudentsBookInstantly: false,
        daySelectType: 'weekly',
        weekdaysScheduled: [],
        weekDayOpened: false,
        weekDayDialog: {
            title: '',
            scheduleFrom: null,
            scheduleTo: null,
            weekday: null,
        },
        weekDayNames: [
            'S',
            'M',
            'T',
            'W',
            'T',
            'F',
            'S',
        ],

        startDate: null,
        untilDate: null,
        isOngoing: true,

        utils: utils,

        dateOpened: false,
        dateOpenedDialog: {},
        dateOpenedDialogStartError: '',
        dateOpenedDialogEndError: '',

        enrolled: null,
        weekDayDialogErrorOpened: false,

        autoMenuProps: {
            "closeOnClick":false,
            "closeOnContentClick":false,
            "openOnClick":false,
            "maxHeight":300,
            "allow-overflow": true,
        },
        localError: '',

        isRescheduleOpened: false,
        isRescheduleLoading: false,
        reschedulingDay: -1,
        rescheduleMessage: '',
    }),

    components: {
        DateSelect,
        Snack,
    },

    created: function () {
        let _this = this
        if (this.$store.state.teacherGroupClass) {
            this.enrolled = this.$store.state.teacherGroupClass.enrolled
            this.scheduleFrom = _this.$store.state.teacherGroupClass.scheduleFrom
            this.scheduleTo = _this.$store.state.teacherGroupClass.scheduleTo
            this.scheduleDates = _this.$store.state.teacherGroupClass.scheduleDates || []
            if('allowStudentsBookInstantly' in _this.$store.state.teacherGroupClass)
                this.allowStudentsBookInstantly = _this.$store.state.teacherGroupClass.allowStudentsBookInstantly
            //this.daySelectType = _this.$store.state.teacherGroupClass.daySelectType || 'monthly'
            this.weekdaysScheduled = _this.$store.state.teacherGroupClass.weekdaysScheduled || []
        }
    },

    computed: {
        enrolledNum() {
            return this.enrolledNumWeekdays[this.reschedulingDay] && this.enrolledNumWeekdays[this.reschedulingDay].length;
        },
        isEditDisabled() {
            return Boolean(this.enrolled && this.enrolled.length)
        },
        enrolledWeekdays() {
            return _.keyBy(_.filter(this.enrolled, e => (e.status === 'requested' || e.status === 'approved')), v => moment(v.date).day())
        },
        enrolledNumWeekdays() {
            return _.groupBy(_.filter(this.enrolled, e => (e.status === 'requested' || e.status === 'approved')), v => moment(v.date).day())
        },
        weekdayDialogStartTimeItems() {
            let res = []
            for (let i=0; i<24; i++) {
                if(this.disabledWeekdayHoursStart.indexOf(i) > -1)
                    continue
                for (let j=0; j<60; j+=15) {
                    const HH = `0${i}`.substr(-2, 2)
                    const mm = `0${j}`.substr(-2, 2)
                    res.push({
                        text: utils.time24HtoAMPM(`${HH}:${mm}`),
                        value: `${HH}:${mm}`
                    })
                }

            }
            return res
        },
        weekdayDialogEndTimeItems() {
            let res = []
            for (let i=0; i<24; i++) {
                if(this.disabledWeekdayHoursEnd.indexOf(i) > -1)
                    continue
                for (let j=0; j<60; j+=15) {
                    const HH = `0${i}`.substr(-2, 2)
                    const mm = `0${j}`.substr(-2, 2)
                    res.push({
                        text: utils.time24HtoAMPM(`${HH}:${mm}`),
                        value: `${HH}:${mm}`
                    })
                }

            }
            return res
        },
        disabledWeekdayHoursStart() {
            let res = [0, 1, 2, 3, 4, 5]
            return res
            // the rest depends from selected end, disabled for now
            if(this.weekDayDialog && this.weekDayDialog.scheduleTo) {
                let h = Number(this.weekDayDialog.scheduleTo.split(':')[0])
                while (h < 24) {
                    res.push(h)
                    h++
                }
            }
            return res
        },
        disabledWeekdayHoursEnd() {
            let res = [0, 1, 2, 3, 4, 5]
            return res
            // the rest depends from selected start, disabled for now
            if(this.weekDayDialog && this.weekDayDialog.scheduleFrom) {
                let h = Number(this.weekDayDialog.scheduleFrom.split(':')[0])
                while (h > 5) {
                    res.push(h)
                    h--
                }
            }
            return res
        },
        disabledHoursStart() {
            let res = [0, 1, 2, 3, 4, 5]
            if(this.dateOpenedDialog && this.dateOpenedDialog.end) {
                let h = Number(this.dateOpenedDialog.end.split(':')[0])
                while (h < 24) {
                    res.push(h)
                    h++
                }
            }
            return res
        },
        disabledHoursEnd() {
            let res = [0, 1, 2, 3, 4, 5]
            if(this.dateOpenedDialog && this.dateOpenedDialog.start) {
                let h = Number(this.dateOpenedDialog.start.split(':')[0])
                while (h > 5) {
                    res.push(h)
                    h--
                }
            }
            return res
        },
        weekdayDialogStartTime: {
            set(v) {
                if(!this.weekDayDialog || !v)
                    return
                this.weekDayDialog.scheduleFrom = v
            },
            get() {
                if(!this.weekDayDialog || !this.weekDayDialog.scheduleFrom)
                    return
                return this.weekDayDialog.scheduleFrom
            }
        },
        weekdayDialogEndTime: {
            set(v) {
                if(!this.weekDayDialog || !v)
                    return
                this.weekDayDialog.scheduleTo = v
            },
            get() {
                if(!this.weekDayDialog || !this.weekDayDialog.scheduleTo)
                    return
                return this.weekDayDialog.scheduleTo
            }
        },
        dialogStartTime: {
            set(v) {
                if(!this.dateOpenedDialog || !v)
                    return
                this.dateOpenedDialog.start = v.format('HH:mm')
            },
            get() {
                if(!this.dateOpenedDialog || !this.dateOpenedDialog.start)
                    return
                return moment(this.dateOpenedDialog.start, 'HH:mm')
            }
        },
        dialogEndTime: {
            set(v) {
                if(!this.dateOpenedDialog || !v)
                    return
                this.dateOpenedDialog.end = v.format('HH:mm')
            },
            get() {
                if(!this.dateOpenedDialog || !this.dateOpenedDialog.end)
                    return
                return moment(this.dateOpenedDialog.end, 'HH:mm')
            }
        },
        eventsMap() {
            return _.keyBy(_.map(this.weekdaysScheduled, v => {
                const date = '2019-01-01'
                return {
                    busy: true,
                    title: String(utils.time24HtoAMPM(v.start)+'<br/>'+utils.time24HtoAMPM(v.end)),
                    weekday: v.weekday,
                    time: v.start,
                    start: v.start,
                    end: v.end,
                    duration: moment(date+' '+v.end, 'YYYY-MM-DD HH:mm').diff(moment(date+' '+v.start, 'YYYY-MM-DD HH:mm'), 'minutes'), // Math.round(((new Date(date+' '+v.end+':00').getTime()) - (new Date(date+' '+v.start+':00').getTime()))/60000)
                }
            }), 'weekday')
        },
        scheduleDatesCalendar: {
            set(v) {
                //console.log(v)
                let oldDates = _.map(this.scheduleDates, v => v.date)

                let lastFromSchedule = _.last(this.scheduleDates) || {}
                let date = (oldDates.length > v.length ? _.difference(oldDates, v) : _.difference(v, oldDates))[0]
                this.dateOpenedDialog = _.assign({}, _.find(this.scheduleDates, {date: date}) || {date: date, start: lastFromSchedule.start, end: lastFromSchedule.end})
                this.dateOpenedDialog.title = utils.stringToDate(date).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'})
                if(oldDates.length > v.length) {
                    //removed item
                    this.dateOpenedDialog.cancelTitle = 'Remove'
                } else {
                    //added item
                    this.dateOpenedDialog.cancelTitle = 'Cancel'
                }
                this.dateOpenedDialogStartError = ''
                this.dateOpenedDialogEndError = ''
                this.dateOpened = true
                //this.scheduleDates = v
            },
            get() {
                return _.map(this.scheduleDates, v => v.date)
            }
        },
        weekdaysScheduledList() {
            return _.map(this.weekdaysScheduled, v => {
                let date = new Date()
                date.setDate(date.getDate()+(v.weekday-date.getDay()))
                return `${date.toLocaleString('en-us', {weekday: 'long'})}, ${utils.time24HtoAMPM(v.start)} - ${utils.time24HtoAMPM(v.end)}`
            })
        }
    },

    methods: {
        isAllowedWeekday(val) {
            return true
            //return !this.enrolledWeekdays[val]
        },
        isNotEnrolledDay(val) {
            return !this.enrolledWeekdays[val]
        },
        saveData() {
            this.$store.commit('setGroupClass', {
                scheduleFrom: this.scheduleFrom,
                scheduleTo: this.scheduleTo,
                scheduleDates: this.scheduleDates,
                allowStudentsBookInstantly: this.allowStudentsBookInstantly,
                daySelectType: this.daySelectType,
                weekdaysScheduled: this.weekdaysScheduled,
                //untilDate: this.isOngoing ? null : this.untilDate,
                //startDate: this.startDate,
                //isOngoing: this.isOngoing,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            if(this.$store.state.teacherGroupClass.canBook && !this.weekdaysScheduled.length) {
                this.localError = 'Please provide your availability (at least one day)'
                return
            }
            this.saveData()
            this.$emit('next:step')
        },
        clear () {

        },
        openDay(event) {
            //console.log('openDay', event)
            if(this.isEditDisabled && !this.isAllowedWeekday(event.weekday))
                return
            let dialog = {}
            if(event.busy) {
                dialog.title = 'Update available hours'
                dialog.scheduleFrom = event.start
                dialog.scheduleTo = event.end
                dialog.weekday = event.weekday
                dialog.action = 'update'
            } else {
                const lastWeekday = _.last(this.weekdaysScheduled)
                dialog.title = 'Set available hours'
                dialog.scheduleFrom = lastWeekday ? lastWeekday.start : null
                dialog.scheduleTo = lastWeekday ? lastWeekday.end : null
                dialog.weekday = event.weekday
                dialog.action = 'add'
            }

            this.weekDayDialog = dialog
            this.weekDayOpened = true
        },
        saveWeekDayData(event) {
            //console.log('saveWeekDayData', event)
            if(!this.weekDayDialog.scheduleFrom) {
                this.$set(this.weekDayDialog, 'error', `Start time is required`)
                this.weekDayDialogErrorOpened = true
                return
            }
            if(!this.weekDayDialog.scheduleTo) {
                this.$set(this.weekDayDialog, 'error', `Until time is required`)
                this.weekDayDialogErrorOpened = true
                return
            }
            if(this.weekDayDialog.scheduleFrom >= this.weekDayDialog.scheduleTo) {
                this.$set(this.weekDayDialog, 'error', `Start time should be before end time`)
                this.weekDayDialogErrorOpened = true
                return
            }
            let i = _.findIndex(this.weekdaysScheduled, {weekday: this.weekDayDialog.weekday})
            if(i == -1) {
                this.weekdaysScheduled.push({
                    weekday: this.weekDayDialog.weekday,
                    start: this.weekDayDialog.scheduleFrom,
                    end: this.weekDayDialog.scheduleTo,
                })
            } else {
                this.weekdaysScheduled.splice(i, 1, {
                    weekday: this.weekDayDialog.weekday,
                    start: this.weekDayDialog.scheduleFrom,
                    end: this.weekDayDialog.scheduleTo,
                })
            }
            this.weekDayOpened = false
            this.weekDayDialogErrorOpened = false
        },
        removeWeekday(weekday) {
            if(this.isEditDisabled && !this.isAllowedWeekday(weekday))
                return
            const index = _.findIndex(this.weekdaysScheduled, {weekday: weekday})
            if(index != -1) {
                this.weekdaysScheduled.splice(index, 1)
            }
        },
        tryRemoveWeekday(weekday) {
            if (this.isNotEnrolledDay(weekday)) return this.removeWeekday(weekday);
            this.reschedulingDay = weekday;
            this.isRescheduleOpened = true;
        },
        async saveReschedule() {
            if (!this.enrolledNum) return;
            this.isRescheduleLoading = true;
            try {
                const res = await api.teacherCancelPrivateEnrollments(this.enrolledNumWeekdays[this.reschedulingDay].map(v => v.id), this.rescheduleMessage);
                this.isRescheduleOpened = false;
                this.removeWeekday(this.reschedulingDay);
            } catch (e) {
                console.log(e);
            }
            this.isRescheduleLoading = false;
        },
        clearWeekDayData(event) {
            this.weekDayDialog = {}
            this.weekDayOpened = false
            this.weekDayDialogErrorOpened = false
        },
        weekDayClasses(past, present, future) {
            return {
                'my-event': true,
                'v-calendar-daily_head-day': true,
                'v-past': past,
                'v-present': present,
                'v-future': future,
            }
        },
        dayFormat() {
            return ''
        },
        weekdayFormat() {
            return ''
        },
        weekdayClass(weekday) {
            return 'my-event'+(this.weekDayOpened && this.weekDayDialog.weekday === weekday ? ' active' : '')
        },
        weekdayBlockClass(weekday) {
            return `my-event with-time${this.isNotEnrolledDay(weekday) ? '' : ' unavailable'}`
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.my-event {
    overflow: visible;
    text-overflow: ellipsis;
    border-radius: 2px;
            background-color: yellow;
            color: black;
    border: 1px solid #1867c0;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 4px;
    margin-right: 8px;
    position: relative;
    &.active {
        color: darkorange;
    }

    span.time {
        position: absolute;
    }

    &.with-time {
        position: absolute;
        right: 4px;
        margin-right: 0px;

        &.unavailable {
            background: repeating-linear-gradient(
              -45deg,
              yellow,
              yellow 5px,
              silver 5px,
              silver 10px
            )
        }
    }

}
.custom-head-weekday {
    text-align: center;
    color: #424242;
}
.remove-weekday {
    position: absolute;
    top: -5px;
    right: -5px;
    width: 20px;
    height: 20px;
    margin: 0;
    color: #82b1ff;

     > .v-icon {
        opacity: 1;
        color: gray !important;
     }
}
</style>