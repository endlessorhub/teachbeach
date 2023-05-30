<template>
  <div class="teacher-group-price">
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
      <snack v-model="error"/>
    <v-container grid-list-md text-xs-center>

      <h1>{{ title }}</h1>
      <v-flex xs12 class="text-xs-left">
              <v-layout align-top justify-left row wrap>
                <v-flex xs12 class="text-xs-left" >
                    <v-radio-group v-model="flexibleDates" row>
                      <v-radio
                        label="Customers can select dates they want"
                        :value="true"
                        :disabled="isEditDisabled"
                      ></v-radio>

                      <v-radio
                        label="Fixed dates. Students attend all dates."
                        :value="false"
                        :disabled="isEditDisabled || isPremiumCommunity"
                      ></v-radio>

                    </v-radio-group>
                </v-flex>
                <v-flex xs12 md6 class="text-xs-left" >
                    <v-switch v-model="canBook" label="Students can book on this page"></v-switch>
                    <h3>Select day and time</h3>
                    <v-date-picker
                        :disabled="isCalendarEditDisabled"
                        :events="calendarEvents"
                        event-color="green lighten-1"
                        :picker-date.sync="pickerDate"
                        :min="minPickerDate"
                        v-model="newCalendarSchedule"
                        multiple
                        no-title
                      ></v-date-picker>
                </v-flex>
                <v-flex xs12 md6 class="text-xs-left" >
                    <div class="schedule-list-item" v-for="(item, index) in scheduleDatesList">
                        <a @click="deletePeriod(item.items)"><v-icon>cancel</v-icon></a> {{ item.dateStr }}

                    </div>
                    <div><b>Just click on the calendar to add or deselect days, or to edit times.</b></div>
                </v-flex>
              </v-layout>

                <v-dialog
                  v-model="dateOpened"
                  max-width="400"
                  persistent
                >
                  <v-card>
                    <v-card-title class="headline">{{dateOpenedDialog.title}}</v-card-title>
                    <v-card-text>
                      <form>
                          <v-alert
                              v-if="dateOpened && eventDict[dateOpenedDialog.date]"
                              :value="dateOpened && eventDict[dateOpenedDialog.date]"
                              type="error"
                              color="platform-error"
                              transition="scale-transition"
                          >
You already have {{eventDict[dateOpenedDialog.date].length}}
student{{eventDict[dateOpenedDialog.date].length > 1 ? 's' : ''}} enrolled at this time.
                          </v-alert>

                          <v-layout key="reschedule" align-top justify-space-between row wrap v-if="isRescheduling">
                              <v-flex xs5 class="text-xs-left">
                                <v-autocomplete
                                    v-model="dialogStartTime"
                                    :items="dialogStartTimeItems"
                                    placeholder="From"
                                    prepend-icon="schedule"
                                    :filter="timeAutocompleteFilter"
                                ></v-autocomplete>
                              </v-flex>
                              <v-flex xs5 class="text-xs-left">
                                <v-autocomplete
                                    v-model="dialogEndTime"
                                    :items="dialogEndTimeItems"
                                    placeholder="To"
                                    prepend-icon="schedule"
                                    :filter="timeAutocompleteFilter"
                                ></v-autocomplete>
                              </v-flex>
                              <v-flex xs12 class="text-xs-left">
                                  <v-menu
                                      v-model="rescheduleDateMenu"
                                      :close-on-content-click="false"
                                      :nudge-right="40"
                                      lazy
                                      transition="scale-transition"
                                      offset-y
                                      full-width
                                      max-width="290px"
                                      min-width="290px"
                                  >
                                      <template v-slot:activator="{ on }">
                                        <v-text-field
                                          :value="rescheduleDateFormatted"
                                          label="Set new date"
                                          clearable
                                          prepend-icon="event"
                                          v-on="on"
                                        ></v-text-field>
                                      </template>
                                      <v-date-picker
                                          v-model="rescheduleDateCal"
                                          no-title
                                          @input="rescheduleDateMenu = false"
                                          :allowed-dates="rescheduleAllowedDates"
                                      >
                                      </v-date-picker>
                                    </v-menu>
                              </v-flex>
                        </v-layout>

                        <v-layout key="original" align-top justify-space-between row wrap v-else>
                          <v-flex xs5 class="text-xs-left">
                            <v-autocomplete
                                v-model="dialogStartTime"
                                :items="dialogStartTimeItems"
                                placeholder="From"
                                prepend-icon="schedule"
                                :filter="timeAutocompleteFilter"
                            ></v-autocomplete>
                          </v-flex>
                          <v-flex xs5 class="text-xs-left">
                            <v-autocomplete
                                v-model="dialogEndTime"
                                :items="dialogEndTimeItems"
                                placeholder="To"
                                prepend-icon="schedule"
                                :filter="timeAutocompleteFilter"
                            ></v-autocomplete>
                          </v-flex>
                          <v-flex xs12 class="text-xs-left">
                            <v-checkbox
                              v-model="newCalendarWeeklyOngoing"
                              label="Repeat weekly, ongoing"
                            ></v-checkbox>
                              <v-menu
                                  ref="untilDateMenu"
                                  v-model="untilDateMenu"
                                  :close-on-content-click="false"
                                  :nudge-right="40"
                                  lazy
                                  transition="scale-transition"
                                  offset-y
                                  full-width
                                  max-width="290px"
                                  min-width="290px"
                              >
                                  <template v-slot:activator="{ on }">
                                    <v-text-field
                                      :value="untilDateFormatted"
                                      label="Set end date (optional)"
                                      clearable
                                      prepend-icon="event"
                                      v-on="on"
                                      :disabled="!newCalendarWeeklyOngoing"
                                    ></v-text-field>
                                  </template>
                                  <v-date-picker v-model="untilDateCal" no-title @input="untilDateMenu = false; newCalendarRepeatNum=''"></v-date-picker>
                                </v-menu>
                              <v-text-field
                                  v-model="newCalendarRepeatNum"
                                  type="number"
                                  label="Number of times (optional)"
                                  :disabled="!newCalendarWeeklyOngoing"
                                  @focus="untilDateCal=null"
                              ></v-text-field>
                          </v-flex>
                          <v-flex xs12 class="text-xs-left">

                          </v-flex>
                        </v-layout>

                      </form>
                    </v-card-text>

                    <v-card-actions>

                        <div class="sliding-actions" key="reschedule" v-if="isRescheduling">
                            <v-btn

                                @click="backFromReschedule"
                              >
                                Back
                              </v-btn>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="primary"
                                @click="saveReschedule"
                                :disabled="!rescheduleDateCal"
                                :loading="rescheduleLoading"
                              >
                                Save
                            </v-btn>
                        </div>
                        <div class="sliding-actions" key="original" v-else>
                            <v-btn
                                @click="clearDateData"
                              >
                                {{dateOpenedDialog.cancelTitle}}
                              </v-btn>
                              <v-spacer></v-spacer>
                              <v-btn
                                color="primary"
                                @click="saveDateData"
                              >
                                {{dateOpenedDialog.saveTitle}}
                            </v-btn>
                        </div>

                    </v-card-actions>
                  </v-card>
                </v-dialog>
      </v-flex>
      <v-flex v-if="calendarError" xs12 class="text-xs-left error-message">
          {{calendarError}}
      </v-flex>

    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </div>
</template>

<script>
import DateSelect from '@/components/basic/DateSelect.vue'
import Snack from '@/components/basic/Snack'
import utils from '@/lib/utils'

import _ from 'lodash'
import moment from 'moment'
import axios from 'axios'

export default {
    props: {

    },

    components: {
        DateSelect,
        Snack,
    },

    data: () => ({
        isLoading: false,
        newCalendarOngoingLimit: 183,
        tRootMenu: false,
        fakeWizardPage: '1',
        customDuration: null,
        lessonLengthGroup: null,
        lessonLengthPrivate: [],
        lessonPricePerHour: null,
        numOfLessonsGroup: null,
        numOfLessonsPrivate: [],
        numOfLessonsAvailable: [1, 5, 10],
        pricePerHourBlurred: false,
        lessonLengthAvailable: [
            {id: 20, name: '20 min'},
            {id: 45, name: '45 min'},
            {id: 60, name: '1 hour'},
            {id: 480, name: '1 day'},
        ],
        standardPackages: [],
        customPackages: [],
        activeTab: 'newRules',
        customTotOfLessons: null,
        packageTypes: ['standard', 'custom', 'wizard'],
        currency: 'usd',
        currencies: [
            {id: 'usd', label: 'US Dollar', logo: '$'},
            {id: 'mxn', label: 'Mexican Peso', logo: 'Mex$'},
        ],
        //schedule variables
        daySelectType: 'monthly',
        scheduleFrom: null,
        scheduleTo: null,
        scheduleDates: [],
        weekdaysScheduled: [],
        weekDayOpened: false,
        weekDayDialog: {
            title: '',
            scheduleFrom: null,
            scheduleTo: null,
            weekday: null,
        },
        flexibleDates: true,
        untilDate: null,
        isOngoing: false,
        isWeekly: false,

        startDate: null,
        weekDayNames: [
            'Sun',
            'Mon',
            'Tue',
            'Wed',
            'Thu',
            'Fri',
            'Sat',
        ],
        currencyDict: {},
        utils: utils,

        scheduleDatesExcluded: {},
        pickerDate: null,
        dropInRate: null,

        standardNumOfLessonsError: [],
        standardPerLessonError: [],
        calendarError: '',

        dateOpened: false,
        dateOpenedDialog: {},
        dateOpenedDialogStartError: '',
        dateOpenedDialogEndError: '',

        enrolled: null,

        canBook: true,

        newCalendarWeeklyOngoing: false,
        untilDateMenu: false,
        untilDateCal: null,

        rescheduleLoading: false,
        rescheduleDateMenu: false,
        rescheduleDateCal: null,
        isRescheduling: false,
        tmpDateOpenedDialog: {},
        isPremiumCommunity: false,
        error: ''
    }),

    created: function () {
        let _this = this
        this.lessonLengthGroup = null
        this.lessonLengthPrivate = []
        this.currencyDict = _.keyBy(this.currencies, 'id')
        if (this.$store.state.teacherGroupClass) {
            this.customDuration = _this.$store.state.teacherGroupClass.customDuration
            this.enrolled = _this.$store.state.teacherGroupClass.enrolled
            this.lessonLengthGroup = _this.$store.state.teacherGroupClass.lessonLengthGroup
            this.lessonLengthPrivate = _this.$store.state.teacherGroupClass.lessonLengthPrivate || []
            this.lessonPricePerHour = _this.$store.state.teacherGroupClass.lessonPricePerHour
            this.numOfLessonsPrivate = _this.$store.state.teacherGroupClass.numOfLessonsPrivate || []
            this.numOfLessonsGroup = _this.$store.state.teacherGroupClass.numOfLessonsGroup
            if(!this.customDuration) {
                let minutes = _.first(_.difference([this.lessonLengthGroup], _.map(this.lessonLengthAvailable, v => v.id)))
                if(minutes) {
                    this.customDuration = ('0'+Math.floor(minutes/60)).slice(-2)+':'+(('0'+(minutes%60)).slice(-2))
                }
            }
            this.standardPackages = _this.$store.state.teacherGroupClass.standardPackages || []
            this.customPackages = _this.$store.state.teacherGroupClass.customPackages || []
            this.currency = _this.$store.state.teacherGroupClass.currency || 'usd'
            this.dropInRate = _this.$store.state.teacherGroupClass.dropInRate || null

            // from schedule
            this.scheduleFrom = _this.$store.state.teacherGroupClass.scheduleFrom
            this.scheduleTo = _this.$store.state.teacherGroupClass.scheduleTo
            const savedDates = _this.$store.state.teacherGroupClass.scheduleDates || []
            this.scheduleDates = this.isEditDisabled ? savedDates : _.filter(savedDates, v => moment(v.date).isAfter(new Date()))
            //this.daySelectType = _this.$store.state.teacherGroupClass.daySelectType || 'weekly'
            this.weekdaysScheduled = _this.$store.state.teacherGroupClass.weekdaysScheduled || []
            this.untilDate = _this.$store.state.teacherGroupClass.untilDate
            this.startDate = _this.$store.state.teacherGroupClass.startDate
            this.flexibleDates = typeof _this.$store.state.teacherGroupClass.flexibleDates === 'boolean' ? _this.$store.state.teacherGroupClass.flexibleDates : true

            this.scheduleDatesExcluded = _this.$store.state.teacherGroupClass.scheduleDatesExcluded || {}

            this.canBook = typeof this.$store.state.teacherGroupClass.canBook == 'undefined' ? true : this.$store.state.teacherGroupClass.canBook
            this.pickerDate = _.first(_.sortBy(this.scheduleDatesCalendar, d => d))
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
        }

    },

    mounted() {
        if(this.$store.state.teacherGroupClass && this.$store.state.teacherGroupClass.groupPackageType) {
            this.activeTab = this.packageTypes.indexOf(this.$store.state.groupPackageType)
        } else {
            this.activeTab = 0
        }
        if(this.$store.state.teacherGroupClass && this.$store.state.teacherGroupClass.fakeWizardPage) {
            this.fakeWizardPage = this.$store.state.teacherGroupClass.fakeWizardPage
        } else {
            this.fakeWizardPage = '1'
        }
    },

    computed: {
        classId() {
            return this.$store.state.teacherGroupClass.id
        },
        eventDict() {
            return this.enrolled ? this.enrolled.reduce((acc, v) => {
                if(!acc[v.date])
                    acc[v.date] = []
                acc[v.date].push(v)
                return acc
            }, {}) : {}
        },
        calendarEvents() {
            return this.enrolled && this.enrolled.map(v => v.date)
        },
        untilDateFormatted() {
            return this.untilDateCal ? utils.stringToDate(this.untilDateCal).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'}) : ''
        },
        rescheduleDateFormatted() {
            return this.rescheduleDateCal ? utils.stringToDate(this.rescheduleDateCal).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'}) : ''
        },
        isEditDisabled() {
            return Boolean(this.enrolled && this.enrolled.length)
        },
        isCalendarEditDisabled() {
            return false;
            //return Boolean(this.enrolled && this.enrolled.length && !this.flexibleDates)
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
        dialogStartTimeItems() {
            let res = []
            for (let i=0; i<24; i++) {
                if(this.disabledHoursStart.indexOf(i) > -1)
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
        dialogEndTimeItems() {
            let res = []
            for (let i=0; i<24; i++) {
                if(this.disabledHoursEnd.indexOf(i) > -1)
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
        dialogStartTime: {
            set(v) {
                if(!this.dateOpenedDialog)
                    return
                this.dateOpenedDialog.start = v
            },
            get() {
                if(!this.dateOpenedDialog || !this.dateOpenedDialog.start)
                    return
                return this.dateOpenedDialog.start
            }
        },
        dialogEndTime: {
            set(v) {
                if(!this.dateOpenedDialog)
                    return
                this.dateOpenedDialog.end = v
            },
            get() {
                if(!this.dateOpenedDialog || !this.dateOpenedDialog.end)
                    return
                return this.dateOpenedDialog.end
            }
        },
        minPickerDate() {
            return utils.dateToString(new Date())
        },
        lessonLengthMinutes() {
            return this.lessonLengthGroup ? [this.lessonLengthGroup] : []
        },
        customMinutes() {
            let v = this.customDuration ? _.sum(_.map(this.customDuration.split(':'), (v, i) => i ? Number(v) : v*60)) : null
            //this.lessonLength = v

            return v
        },
        customerPays() {
            if(this.lessonLengthMinutes.length && this.lessonPricePerHour && !isNaN(Number(this.lessonPricePerHour))) {
                return _.map(this.lessonLengthMinutes, minutes => '$'+(Number(minutes/60*this.lessonPricePerHour).toFixed(2))).join(', ')
            } else {
                return null
            }
        },
        lessonPricePerHourFormatted: {
            set(newVal) {
                this.lessonPricePerHour = Number(newVal.replace(/[^0-9\.]/g, ''))
            },
            get() {
                return !this.lessonPricePerHour ? '' : '$'+(this.pricePerHourBlurred ? this.lessonPricePerHour.toFixed(2) : this.lessonPricePerHour)
            },
        },
        numOfLessons: {
            set(v) {
                this.numOfLessonsGroup = v
            },
            get() {
                this.numOfLessonsGroup
            }
        },
        lastStandardPackage: {
            set(v) {
                if(!this.standardPackages.length) {
                    this.standardPackages.push({
                        numberOfLessons: '',
                        perLesson: '',
                        currency: this.currency,
                        totalPrice: '',
                        charge: 'upfront',
                        isGlobalPackage: false,
                        key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
                    })
                }
                let last = _.last(this.standardPackages)

                _.each(v, (newVal, k) => {
                    last[k] = newVal
                })
                if(last.numberOfLessons && last.perLesson && last.currency) {
                    last.totalPrice = last.numberOfLessons*last.perLesson
                }
            },
            get() {
                return _.last(this.standardPackages) || {
                    numberOfLessons: '',
                    perLesson: '',
                    currency: this.currency,
                    totalPrice: '',
                    charge: 'upfront',
                    isGlobalPackage: false,
                    key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
                }
            },
        },
        lastCustomPackage: {
            set(v) {
                if(!this.customPackages.length) {
                    this.customPackages.push({
                        description: '',
                        currency: this.currency,
                        totalPrice: '',
                        key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                    })
                }
                let last = _.last(this.customPackages)
                _.each(v, (newVal, k) => {
                    last[k] = newVal
                })
            },
            get() {
                return _.last(this.customPackages) || {
                    description: '',
                    currency: this.currency,
                    totalPrice: '',
                    key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                }
            },
        },
        lastDayOfWeek: {
            set(v) {
                if(!this.weekdaysScheduled.length) {
                    this.weekdaysScheduled.push({
                        weekday: '',
                        start: '',
                        end: '',
                    })
                }
                let last = _.last(this.weekdaysScheduled)
                _.each(['weekday', 'start', 'end'], (k) => {
                    if(k in v) {
                        last[k] = v[k]
                    }
                })
            },
            get() {
                return _.last(this.weekdaysScheduled) || {
                    weekday: '',
                    start: '',
                    end: '',
                }
            },
        },
        scheduleDatesList() {
            return utils.formatDatesSchedule(this.scheduleDates)
            /*
            return _.map(this.scheduleDates, v => ({
                dateStr: utils.stringToDate(v.date).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'})
            }))
            */
        },
        newCalendarSchedule: {
            set(v) {
                console.log(v)
                let oldDates = _.map(this.scheduleDates, v => v.date)

                let lastFromSchedule = _.last(this.scheduleDates) || {}
                let date = (oldDates.length > v.length ? _.difference(oldDates, v) : _.difference(v, oldDates))[0]
                this.dateOpenedDialog = _.assign({}, _.find(this.scheduleDates, {date: date}) || {date: date, start: lastFromSchedule.start, end: lastFromSchedule.end})
                this.dateOpenedDialog.title = utils.stringToDate(date).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'})
                if(oldDates.length > v.length) {
                    //removed item
                    if(this.eventDict[this.dateOpenedDialog.date]) {
                        this.dateOpenedDialog.cancelTitle = 'Reschedule anyway'
                        this.dateOpenedDialog.saveTitle = 'Cancel'
                    } else {
                        this.dateOpenedDialog.cancelTitle = 'Remove'
                        this.dateOpenedDialog.saveTitle = 'Ok'
                    }
                } else {
                    //added item
                    this.dateOpenedDialog.cancelTitle = 'Cancel'
                    this.dateOpenedDialog.saveTitle = 'Save'
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
        scheduleDatesCalendar: {
            set(v) {
                console.log(v)
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
        selectedMonthlyDate: {
            set(v) {
                console.log(v)
            },
            get() {
                return {
                    date: '',
                    start: '',
                    end: '',
                }
            },
        },
        filteredWeekdays() {
            /*
            return _.map(this.weekDayNames, (v, i) => ({
                id: i,
                name: v,
            }))
            */
            const excludeIdDict = _.keyBy(this.weekdaysScheduled.slice(0, -1), 'weekday')
            return _.filter(_.map(this.weekDayNames, (v, i) => ({
                id: i,
                name: v,
            })), (v) => !excludeIdDict[v.id])

        },
        startDateErrors() {
            const errors = []
            if(!this.startDate)
                errors.push('Start Date should not be empty')
            return errors
        },
        untilDateErrors() {
            const errors = []
            if(!this.untilDate && !this.isOngoing)
                errors.push('Please select Until or check Ongoing')
            return errors
        },
        includedInCalendar: {
            set(val) {
                //console.log(arguments)
                let y = new Date().getFullYear()
                let m = new Date().getMonth()
                if (this.pickerDate) {
                    y = this.pickerDate.split('-')[0]
                    m = this.pickerDate.split('-')[1]-1
                }
                this.$set(this.scheduleDatesExcluded, m, _.difference(this.getDatesForMonth(y, m), val))
            },
            get() {
                let y = new Date().getFullYear()
                let m = new Date().getMonth()
                if (this.pickerDate) {
                    y = this.pickerDate.split('-')[0]
                    m = this.pickerDate.split('-')[1]-1
                }
                return this.getCalendarDatesForMonth(y, m)
            }
        },
        title() {
            return this.isPremiumCommunity ? 'What days will the group meet?' : 'Schedule event';
        },
    },

    methods: {
        rescheduleAllowedDates(date) {
            return new Date(date)-24*3600000 > new Date()
        },
        timeAutocompleteFilter(item, queryText, itemText) {
            if(!queryText)
                return true
            let reg = /([\d]{0,2})([:]{0,1})([\d]{0,2})([\s]{0,1})(am|pm|a|p|)/i
            const parts = reg.exec(queryText)
            if(!parts[0])
                return false
            const found = reg.exec(itemText)
            if(parts[1] && Number(parts[1]) != Number(found[1]))
                return false
            if(parts[3] && found[3].search(parts[3]) == -1)
                return false
            if(parts[5] && found[5].toLowerCase().search(parts[5].toLowerCase()) == -1)
                return false
            return true
        },
        deletePeriod(items) {
            this.scheduleDates = _.differenceWith(this.scheduleDates, items, (base, remove) => {
                return base.date == remove.date
            })
        },
        saveData() {
            if(this.daySelectType == 'monthly' && this.scheduleDates.length) {
                let datesSorted = _.map(this.scheduleDates, v => v.date).sort()
                this.startDate = _.first(datesSorted)
                this.untilDate = _.last(datesSorted)
            }
            this.$store.commit('setGroupClass', {
                customDuration: this.customDuration,
                lessonLengthGroup: this.lessonLengthGroup,
                lessonLengthPrivate: this.lessonLengthPrivate,
                lessonPricePerHour: this.lessonPricePerHour,
                numOfLessonsPrivate: this.numOfLessonsPrivate,
                numOfLessonsGroup: this.numOfLessonsGroup,
                standardPackages: this.standardPackages,
                customPackages: this.customPackages,
                groupPackageType: this.activeTab,
                scheduleFrom: this.scheduleFrom,
                scheduleTo: this.scheduleTo,
                scheduleDates: this.scheduleDates,
                daySelectType: this.daySelectType,
                weekdaysScheduled: _.filter(this.weekdaysScheduled, v => ((v.weekday || v.weekday === 0) && v.start && v.end)),
                untilDate: this.isOngoing ? null : this.untilDate,
                startDate: this.startDate,
                flexibleDates: this.flexibleDates,
                dropInRate: this.dropInRate,
                fakeWizardPage: this.fakeWizardPage,
                scheduleDatesExcluded: this.scheduleDatesExcluded,
                canBook: this.canBook,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            if(this.daySelectType == 'weekly' && (this.startDateErrors.length || this.untilDateErrors.length)) {
                return
            }
            if(!this.scheduleDates.length) {
                this.calendarError = "Choose at least one date from calendar"
                return
            }
            this.saveData()
            this.$emit('next:step')
        },
        clear () {

        },
        addStandardPackage() {
            if(!this.lastStandardPackage.numberOfLessons) {
                this.standardNumOfLessonsError = ["Number of lessons can't be empty"]
            }
            if(!this.lastStandardPackage.perLesson) {
                this.standardPerLessonError = ["Per lesson can't be empty"]
            }
            if(this.standardNumOfLessonsError.length || this.standardPerLessonError.length) {
                return
            }
            this.standardPackages.push({
                numberOfLessons: '',
                perLesson: '',
                totalPrice: '',
                charge: 'upfront',
                isGlobalPackage: false,
                currency: this.currency,
                key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
            })
        },
        removeStandardPackage(i) {
            this.standardPackages.splice(i, 1)
        },
        addCustomPackage() {
            this.customPackages.push({
                description: '',
                totalPrice: '',
                currency: this.currency,
                key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
            })
        },
        removeCustomPackage(i) {
            this.customPackages.splice(i, 1)
        },
        saveWeekDayData(event) {
        /*
            console.log('saveWeekDayData', event)
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
            */
        },
        addWeekday() {
            const last = _.last(this.weekdaysScheduled)
            if (!last || !(last.weekday || last.weekday === 0) || !last.start || !last.end)
                return
            this.weekdaysScheduled.push({
                weekday: '',
                start: last.start ,
                end: last.end,
            })
        },
        removeWeekday(weekday) {
            const index = _.findIndex(this.weekdaysScheduled, {weekday: weekday})
            if(index != -1) {
                this.weekdaysScheduled.splice(index, 1)
            }
        },

        standardNumOfLessonsInput(event) {
            if(isNaN(event)) {
                this.standardNumOfLessonsError = ['Only numbers available']
                return
            }
            this.standardNumOfLessonsError = []
            this.lastStandardPackage = {
                numberOfLessons: event
            }
        },
        standardPerLessonInput(event) {
            if(isNaN(event)) {
                this.standardPerLessonError = ['Only numbers available']
                return
            }
            this.standardPerLessonError = []
            this.lastStandardPackage = {
                perLesson: event
            }
        },
        saveReschedule() {
            const newDateTime = moment(this.rescheduleDateCal+' '+this.dateOpenedDialog.start)
            this.rescheduleLoading = true
            axios.post('/api/teacher_date_reschedule', {
                class_id: this.classId,
                message: `This class has been rescheduled for ${newDateTime.toDate().toLocaleString('en-us', {month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric'})}`,
                date_from: this.dateOpenedDialog.date,
                date_to: this.rescheduleDateCal,
                enrollment_ids: this.eventDict[this.dateOpenedDialog.date].map(v => v.id),
                time_start: this.dateOpenedDialog.start,
                time_end: this.dateOpenedDialog.end,
            }).then(res => {
                if(!res.data.success) {
                    this.error = res.data.error_message
                } else {
                    this.enrolled = this.enrolled.map(v => {
                        if(v.date === this.dateOpenedDialog.date)
                            v.date = this.rescheduleDateCal
                        return v
                    })
                    this.scheduleDates = this.scheduleDates.map(v => {
                        if(v.date === this.dateOpenedDialog.date) {
                            v.date = this.rescheduleDateCal
                            v.start = this.dateOpenedDialog.start
                            v.end = this.dateOpenedDialog.end
                        }
                        return v
                    })
                    this.backFromReschedule()
                    this.dateOpened = false
                    this.rescheduleLoading = false
                    this.rescheduleDateCal = null
                }
            }).catch(e => console.log(e)).finally(() => {
                this.rescheduleLoading = false
            })
        },
        saveDateData() {
            this.dateOpenedDialogStartError = ''
            this.dateOpenedDialogEndError = ''
            if(!this.dateOpenedDialog.start) {
                this.dateOpenedDialogStartError = 'Set start time please'
            }
            if(!this.dateOpenedDialog.end) {
                this.dateOpenedDialogEndError = 'Set end time please'
            }
            if(this.dateOpenedDialogStartError || this.dateOpenedDialogEndError) {
                return
            }
            const index = _.findIndex(this.scheduleDates, {date: this.dateOpenedDialog.date})
            if(index > -1) {
                this.scheduleDates.splice(index, 1)
            }
            if(this.newCalendarWeeklyOngoing) {
                if(this.newCalendarRepeatNum) {
                    for (let i=0;i<this.newCalendarRepeatNum;i++) {
                        let startDate = utils.stringToDate(this.dateOpenedDialog.date)
                        startDate.setDate(startDate.getDate()+i*7)
                        this.scheduleDates.push({
                            date: utils.dateToString(startDate),
                            start: this.dateOpenedDialog.start,
                            end: this.dateOpenedDialog.end,
                        })
                    }
                } else if (this.untilDateCal && this.untilDateFormatted) {
                    let startDate = utils.stringToDate(this.dateOpenedDialog.date)
                    let untilDate = utils.stringToDate(this.untilDateCal)
                    while (startDate <= untilDate) {
                        this.scheduleDates.push({
                            date: utils.dateToString(startDate),
                            start: this.dateOpenedDialog.start,
                            end: this.dateOpenedDialog.end,
                        })
                        startDate.setDate(startDate.getDate()+7)
                    }
                } else {
                    for (let i=0;i<this.newCalendarOngoingLimit;i+=7) {
                        let startDate = utils.stringToDate(this.dateOpenedDialog.date)
                        startDate.setDate(startDate.getDate()+i)
                        this.scheduleDates.push({
                            date: utils.dateToString(startDate),
                            start: this.dateOpenedDialog.start,
                            end: this.dateOpenedDialog.end,
                        })
                    }
                }
            } else {
                this.scheduleDates.push(_.pick(this.dateOpenedDialog, ['date', 'start', 'end']))
            }
            this.calendarError = ""
            this.dateOpened = false
        },
        backFromReschedule() {
            this.dateOpenedDialog = Object.assign({}, this.tmpDateOpenedDialog)
            this.isRescheduling = false
        },
        clearDateData() {
            const index = _.findIndex(this.scheduleDates, {date: this.dateOpenedDialog.date})
            const enrollment = index > -1 && this.enrolled && this.enrolled.find(v => v.date === this.scheduleDates[index].date)
            if(enrollment) {
                this.tmpDateOpenedDialog = Object.assign({}, this.dateOpenedDialog)
                this.isRescheduling = true
                return
            }
            if(index > -1) {
                this.scheduleDates.splice(index, 1)
            }
            this.dateOpened = false
        },
    },
    watch: {
        customMinutes(newVal, oldVal) {
            if (this.lessonLengthPrivate.indexOf(oldVal) != -1) {
                _.pull(this.lessonLengthPrivate, oldVal)
            }
            this.lessonLengthGroup = newVal
            if (newVal && _.indexOf(this.lessonLengthPrivate, newVal) == -1) {
                this.lessonLengthPrivate.push(newVal)
            } else {

            }
        },
        currency(newVal, oldVal) {
            _.each(this.standardPackages, (p) => {
                p.currency = newVal
            })
        },
        flexibleDates(newVal, oldVal) {
            if(!newVal) {
                this.isOngoing = false
            }
        },
        startDate(newVal, oldVal) {
            if(!newVal)
                return
            if(this.weekdaysScheduled.length == 1) {
                this.weekdaysScheduled[0].weekday = utils.stringToDate(newVal).getDay()
            }
            if(!this.weekdaysScheduled.length) {
                this.lastDayOfWeek = {weekday: utils.stringToDate(newVal).getDay()}
            }
        }
    }
}
</script>
<style lang="scss">
.teacher-group-price {
    a.v-tabs__item--active {
        font-weight: bold;
        background-color: yellow;
    }
    .schedule-list-item {
        margin-bottom: 10px;
    }
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.sliding-actions {
    width: 100%;
    display: flex;
}
</style>