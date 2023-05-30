<template>
  <form>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
          <h4>Any dates you are not available? Deselect them here.</h4>
        </v-flex>

        <v-flex xs12 class="text-xs-left">
          <v-date-picker
            :allowed-dates="allowedDates"
            :picker-date.sync="pickerDate"
            v-model="includedInCalendar"
            multiple
            no-title
          ></v-date-picker>
        </v-flex>
        <v-flex xs12 md5 class="text-xs-left font-weight-bold">
              <DateSelect
                :disabled="isEditDisabled"
                v-model="startDate"
                :error-messages="startDateErrors"
                :max="maxStartDate"
                label="Set a different start date"
                v-bind="{
                showIcon: true,
              }" v-on:change="startDate=$event" />
        </v-flex>
        <v-flex xs8 md5 class="text-xs-left">
              <DateSelect
                v-model="untilDate"
                :error-messages="untilDateErrors"
                :min="minUntilDate"
                label="Set end date"
                v-bind="{
                showIcon: true,
              }" v-on:change="untilDate=$event" :disabled="isOngoing" />
        </v-flex>
        <v-flex xs4 md2 class="text-xs-left">
            <v-checkbox v-model="isOngoing" label="Ongoing" hide-details></v-checkbox>
        </v-flex>
      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import utils from '@/lib/utils.js'
import DateSelect from '@/components/basic/DateSelect.vue'

import _ from 'lodash'
import moment from 'moment'
import axios from 'axios'

export default {

    props: {
        weekdaysScheduled: Array,
    },

    data: () => ({
        isLoading: false,
        scheduleDatesExcluded: {},
        pickerDate: null,
        untilDate: null,
        startDate: utils.dateToString(new Date()),
        isOngoing: true,
        enrolled: null,
    }),

    components: {
        DateSelect,
    },

    created: function () {
        let _this = this
        if (this.$store.state.teacherGroupClass) {
            this.enrolled = this.$store.state.teacherGroupClass.enrolled
            this.scheduleDatesExcluded = _this.$store.state.teacherGroupClass.scheduleDatesExcluded || {}
            if('untilDate' in _this.$store.state.teacherGroupClass)
                this.untilDate = _this.$store.state.teacherGroupClass.untilDate
            if('startDate' in _this.$store.state.teacherGroupClass)
                this.startDate = _this.$store.state.teacherGroupClass.startDate
            if('isOngoing' in _this.$store.state.teacherGroupClass)
                this.isOngoing = _this.$store.state.teacherGroupClass.isOngoing
            let today = new Date()
            let limit = 3
            while(!this.getCalendarDatesForMonth(today.getFullYear(), today.getMonth()).length && limit) {
                today.setMonth(today.getMonth()+1)
                limit--
            }
            this.pickerDate = utils.dateToString(today)
        }
    },

    computed: {
        isEditDisabled() {
            return Boolean(this.enrolled && this.enrolled.length)
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
            if(this.untilDate && !this.isOngoing && moment(this.untilDate) < this.maxEnrolledDate)
                errors.push(`Please select Until after ${this.maxEnrolledDate.format('MMMM Do YYYY')} (last date enrolled) or check Ongoing`)
            return errors
        },
        maxStartDate() {
            if(!this.untilDate)
                return undefined
            let res = utils.stringToDate(this.untilDate)
            res.setDate(res.getDate()-1)
            return utils.dateToString(res)
        },
        minUntilDate() {
            if(!this.startDate)
                return undefined
            let res = utils.stringToDate(this.startDate)
            res.setDate(res.getDate()+1)
            return utils.dateToString(res)
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
        maxEnrolledDate() {
            return _.maxBy(_.map(this.enrolled, v => moment(v.date)), v => v.unix())
        },
        enrolledDates() {
            return _.keyBy(this.enrolled, v => v.date)
        }
    },

    methods: {
        allowedDates(val) {
            return !this.enrolledDates[val]
        },
        saveData() {
            this.$store.commit('setGroupClass', {
                scheduleDatesExcluded: this.scheduleDatesExcluded,
                untilDate: this.isOngoing ? null : this.untilDate,
                startDate: this.startDate,
                isOngoing: this.isOngoing,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            if(this.startDateErrors.length || this.untilDateErrors.length) {
                return
            }
            this.saveData()
            this.$emit('next:step')
        },
        clear () {

        },

        getDatesForMonth(y, m) {

            return utils.getDatesForMonth(y, m, this.weekdaysScheduled, this.startDate, this.untilDate)
/*
            const dayCount = utils.daysInMonth(y, m)
            const weekdayDict = _.keyBy(this.weekdaysScheduled, v => v.weekday)
            const untilDate = this.untilDate ? new Date(this.untilDate.split('-')[0], this.untilDate.split('-')[1]-1, this.untilDate.split('-')[2]) : null
            let res = []
            for (let d=1; d<=dayCount; d++) {
                const date = new Date(y, m, d)
                const str = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
                if (weekdayDict[date.getDay()] && (!this.untilDate || untilDate >= date)) {
                    res.push(str)
                }
            }
            return res
*/
        },


        getCalendarDatesForMonth(y, m) {

            return utils.getCalendarDatesForMonth(y, m, this.weekdaysScheduled, this.startDate, this.untilDate, this.scheduleDatesExcluded && this.scheduleDatesExcluded[m] ? this.scheduleDatesExcluded[m] : [])

            //const excludedDict = this.scheduleDatesExcluded[m] ? _.keyBy(this.scheduleDatesExcluded[m], v => v) : {}
            //return _.filter(this.getDatesForMonth(y, m), v => !excludedDict[v])
        }

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>