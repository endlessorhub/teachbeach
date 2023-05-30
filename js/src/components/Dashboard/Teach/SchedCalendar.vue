<template>
    <v-layout align-start justify-center row wrap class="teacher-calendar">
        <v-flex xs6 class="text-xs-center">
            <Snack v-model="errMsg"></Snack>
            <PrivateLessonCalendarImport
                v-if="syncPopupClass && syncPopupEnrollment"
                :privateClass="syncPopupClass"
                :enrollment="syncPopupEnrollment"
                :isPopupOpened="syncPopupOpened"
                @closed="syncPopupOpened=null"
                :isButtonHidden="true"
                :isTooltipDynamic="true"
            />
            <google-calendar-sync></google-calendar-sync>
            <v-dialog
              v-model="isLoading"
              persistent
              width="300"
            >
              <v-card
                color="platform-aqua"
                dark
              >
                <v-card-text>
                  Loading...
                  <v-progress-linear
                    indeterminate
                    color="white"
                    class="platform-aqua"
                  ></v-progress-linear>
                </v-card-text>
              </v-card>
            </v-dialog>
        </v-flex>
        <v-flex xs6 class="text-xs-center">
            <v-btn to="/dashboard/teach/schedule_list">
                List
            </v-btn>
        </v-flex>
            <v-flex sm4 xs12 class="text-sm-left text-xs-center">
              <v-btn @click="$refs.calendar.prev()">
                <v-icon dark left>
                  keyboard_arrow_left
                </v-icon>
                Prev
              </v-btn>
            </v-flex>
            <v-flex sm4 xs12 class="text-xs-center">
              <v-select
                v-model="type"
                :items="typeOptions"
                label="Type"
              ></v-select>
            </v-flex>
            <v-flex
              sm4
              xs12
              class="text-sm-right text-xs-center"
            >
              <v-btn @click="$refs.calendar.next()">
                Next
                <v-icon
                  right
                  dark
                >
                  keyboard_arrow_right
                </v-icon>
              </v-btn>
            </v-flex>
        <v-flex xs12><h3>{{monthName}}</h3></v-flex>
            <v-flex xs12>
              <v-sheet height="600">
                <v-calendar
                  ref="calendar"
                  v-model="start"
                  :type="type"
                  :end.sync="end"
                  color="primary"
                >
                    <template v-slot:day="{ date }">
                        <template v-for="event in calendarEvents[date]">
                          <v-menu
                            :key="event.key"
                            v-model="event.open"
                            full-width
                            offset-x
                            :close-on-content-click="true"
                            :close-on-click="false"
                          >
                            <template v-slot:activator="{ on }">
                              <div
                                v-ripple
                                :class="'lesson-event '+event.classPG"
                                v-on="on"
                              >
                                  <v-icon v-if="event.status === 'rejected'" small class="platform-aqua">fas fa-ban</v-icon>
                                  <v-icon v-if="event.status === 'requested'" small class="platform-aqua">far fa-question-circle</v-icon>
                                  {{event.title}}
                              </div>
                            </template>
                            <v-card
                              color="grey lighten-4"
                              min-width="350px"
                              flat
                            >
                              <v-toolbar
                                :color="event.classPG"
                                dark
                              >

                                <v-toolbar-title v-html="event.fullTitle || event.title"></v-toolbar-title>
                                <v-spacer></v-spacer>

                                <v-btn icon>
                                  <v-icon @click="event.open = false">close</v-icon>
                                </v-btn>
                              </v-toolbar>
                              <v-card-text>

                                <v-list v-if="event.items" two-line>
                                  <template v-for="(item, index) in event.items">
                                    <v-list-tile
                                      :key="item.key"
                                      avatar
                                      @click=""
                                    >
                                      <v-list-tile-avatar>
                                        <img v-if="item.avatar" :src="item.avatar">
                                      </v-list-tile-avatar>

                                      <v-list-tile-content>
                                        <v-list-tile-title v-html="item.title"></v-list-tile-title>
                                        <v-list-tile-sub-title v-if="item.isExternal">
                                            <a :href="item.externalLink" target="_blank">{{ item.title }}</a>
                                        </v-list-tile-sub-title>
                                        <v-list-tile-sub-title v-else v-html="item.subtitle"></v-list-tile-sub-title>
                                      </v-list-tile-content>
                                        <v-list-tile-action v-if="!item.isExternal && item.isPrivate">
                                            <v-btn
                                                v-if="item.isPending"
                                                small
                                                v-on="on"
                                                @click.stop="confirmEnroll(item)"
                                              >
                                                Confirm
                                            </v-btn>
                                            <v-btn
                                              color="primary"
                                              @click="rescheduleFormOpen(item)"
                                            >
                                              Edit time
                                            </v-btn>
                                            <v-btn
                                              v-if="item.newEnrollmentAvailable"
                                              color="primary"
                                              @click="rescheduleFormOpen(item, 'add')"
                                            >
                                              Add next class date
                                            </v-btn>
                                        </v-list-tile-action>
                                    </v-list-tile>

                                    <v-divider
                                      v-if="index < event.items.length-1"
                                      :key="index"
                                    ></v-divider>
                                  </template>
                                </v-list>
                                <span v-else>
                                    <div><b>{{event.isExternal ? 'External Calendar' : event.isPrivate ? 'Private' : 'Group'}}</b></div>
                                    <div>{{event.time_from}} to {{event.time_to}}</div>
                                    <div class="details-container" v-html="event.details"></div>
                                    <v-list v-if="event.isPrivate">
                                      <v-list-tile
                                        v-for="student in event.students"
                                        :key="student.id"
                                        @click=""
                                      >

                                        <v-list-tile-content>
                                          <v-list-tile-title>{{student.first_name}} {{student.last_name}}</v-list-tile-title>
                                          <v-list-tile-sub-title><a :href="`tel:${student.phone}`">{{student.phone}}</a>, <a :href="`mailto:${student.email}`">{{student.email}}</a></v-list-tile-sub-title>
                                          <v-list-tile-sub-title>{{student.order.learnerNeeds}}</v-list-tile-sub-title>
                                        </v-list-tile-content>

                                      </v-list-tile>
                                    </v-list>
                                    <div v-if="event.students">{{event.students.length}} student{{event.students.length == 1 ? '' : 's'}}</div>
                                    <div v-if="event.isPrivate">
                                        <v-btn
                                            v-if="event.isPending"
                                            small
                                            v-on="on"
                                            @click.stop="confirmEnroll(event)"
                                          >
                                            Confirm
                                        </v-btn>
                                        <v-btn
                                            v-if="event.isPending"
                                            small
                                            v-on="on"
                                            @click.stop="declineLesson(event)"
                                          >
                                            Decline
                                        </v-btn>
                                        <v-btn
                                            small
                                            v-on="on"
                                            @click.stop="rescheduleFormOpen(event)"
                                          >
                                            Edit time
                                        </v-btn>
                                        <v-btn
                                            small
                                            v-on="on"
                                            @click.stop="rescheduleFormOpen(event, 'add')"
                                          >
                                            Add next class date
                                        </v-btn>
                                    </div>
                                </span>
                              </v-card-text>
                              <v-card-actions>
                                <v-btn
                                  flat
                                  color="secondary"
                                  @click="event.open = false"
                                >
                                  Ok
                                </v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-menu>
                        </template>
                    </template>
                </v-calendar>
              </v-sheet>
            </v-flex>
        <v-dialog v-model="rescheduleForm" max-width="500px" max-height="1000px">
            <v-card>
                <v-card-title>
                    <span class="headline">{{rescheduleFormName}}</span>
                </v-card-title>

              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12 text-xs-left>
                        {{rescheduleFormItem.studentName}},
                        <a :href="'tel:'+rescheduleFormItem.phone">{{rescheduleFormItem.phone}}</a>,
                        <a :href="'mailto:'+rescheduleFormItem.email">{{rescheduleFormItem.email}}</a>
                    </v-flex>
                    <v-flex xs12>
                      <v-text-field v-model="rescheduleFormNotice" label="Message"></v-text-field>
                    </v-flex>
                    <v-flex xs12 text-xs-left>
                      <Reschedule v-model="rescheduleFormDate" :duration="rescheduleFormDuration"></Reschedule>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="rescheduleForm=false">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click="rescheduleFormConfirm">Send</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <FormDeclineEnrollment
            :enrollment="declineEnrollment"
            ref="declineSubmitForm"
            v-on:done="reloadData"
        ></FormDeclineEnrollment>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import moment from 'moment'
import Reschedule from '@/components/basic/Reschedule'
import Snack from '@/components/basic/Snack'
import FormDeclineEnrollment from '@/components/basic/forms/DeclineEnrollment'
import PrivateLessonCalendarImport from './Components/PrivateLessonCalendarImport'
import GoogleCalendarSync from '@/components/bound/GoogleCalendarSync'
import {mapState, mapActions} from 'vuex';
import gapiMixin from '@/mixins/gapi'

export default {
    name: 'dashboard_teach_calendar',
    data: () => ({
        cellEventsLimit: 3,
        isLoading: false,
        type: 'month',
        start: utils.dateToString(new Date()),
        end: utils.dateToString(new Date()),
        typeOptions: [
            { text: 'Day', value: 'day' },
            { text: '4 Day', value: '4day' },
            { text: 'Week', value: 'week' },
            { text: 'Month', value: 'month' },
        ],
        classes: {},
        private_enroll: [],
        group_enroll: [],

        rescheduleForm: false,
        rescheduleFormType: 'edit',
        rescheduleFormItem: {},
        rescheduleFormDate: null,
        rescheduleFormDuration: 1,
        rescheduleFormNotice: '',
        rescheduleFormName: '',
        errMsg: '',

        declineEnrollment: {},

        syncPopupClass: null,
        syncPopupEnrollment: null,
        syncPopupOpened: false,
    }),
    mixins: [
        gapiMixin,
    ],
    components: {
        Snack,
        Reschedule,
        FormDeclineEnrollment,
        PrivateLessonCalendarImport,
        GoogleCalendarSync,
    },
    created() {
        this.reloadData()
        this.getSavedEvents()
    },
    computed: {
        dateEvents() {
            const dateEvents = {}
            _.each(this.private_enroll, v => {
                if(v.order.status === 'refund' || v.status === 'rejected')
                    return
                if(v.status === 'requested' && moment(`${v.date} ${v.time_from}`).toDate() < new Date())
                    return
                if(!dateEvents[v.date])
                    dateEvents[v.date] = []
                let curClass = this.classes[v.class_id]
                //for (let x = 0;x < 7; x++)
                dateEvents[v.date].push({
                    key: `${v.class_id}-${v.date}-${v.time_from}`,
                    title: curClass.private_className,
                    details: utils.formatTextToHtml(curClass.groupClassSummary),
                    date: v.date,
                    status: v.status,
                    classPG: v.status === 'approved' ? 'approved' : 'regular',
                    isPrivate: true,
                    isPending: v.status === 'requested' && moment(`${v.date} ${v.time_from}`).toDate() > new Date(),
                    open: false,
                    class_id: v.class_id,
                    students: [_.assign({}, v.student, {order: v.order})],
                    studentName: `${v.student.first_name} ${v.student.last_name}`,
                    phone: v.student.phone,
                    email: v.student.email,
                    datetime: moment(`${v.date} ${v.time_from}`),
                    time_from: utils.time24HtoAMPM(v.time_from),
                    time_to: utils.time24HtoAMPM(v.time_to),
                    enrollment: v,
                    class: this.classes[v.class_id],
                    newEnrollmentAvailable: v.order.num_lessons > v.order.reserved_lessons
                })
            })
            _.each(this.group_enroll, v => {
                if(v.order.status === 'refund' || v.status === 'rejected')
                    return
                if(!dateEvents[v.date])
                    dateEvents[v.date] = []
                let curClass = this.classes[v.class_id]
                //for (let x = 0;x < 5; x++)
                let curEvent = _.find(dateEvents[v.date], {class_id: v.class_id})
                if(!curEvent) {
                    curEvent = {
                        key: `${v.class_id}-${v.date}-${v.time_from}`,
                        title: curClass.name,
                        details: utils.formatTextToHtml(curClass.groupClassSummary),
                        date: v.date,
                        classPG: v.status === 'approved' ? 'approved' : 'regular',
                        status: v.status,
                        isPrivate: false,
                        open: false,
                        class_id: v.class_id,
                        students: [],
                        datetime: moment(`${v.date} ${v.time_from}`),
                        time_from: utils.time24HtoAMPM(v.time_from),
                        time_to: utils.time24HtoAMPM(v.time_to),
                        enrollment: v,
                        class: this.classes[v.class_id],
                    }
                    dateEvents[v.date].push(curEvent)
                }
                curEvent.students.push(_.assign({}, v.student, {order: v.order}))
            })
            for (let key in this.externalCalendarEvents) {
                if(!dateEvents[key])
                    dateEvents[key] = [...this.externalCalendarEvents[key]]
                else {
                    dateEvents[key] = [...this.externalCalendarEvents[key], ...dateEvents[key]]
                }
            }
            return dateEvents
        },
        calendarEvents() {
            let res2 = {}
            _.each(this.dateEvents, (v, k) => {
                res2[k] = _.sortBy(v, 'datetime').slice(0, v.length > this.cellEventsLimit ? this.cellEventsLimit - 1 : this.cellEventsLimit )
                if(v.length > this.cellEventsLimit) {
                    res2[k].push({
                        key: `${k}-rest`,
                        title: `+${v.length-this.cellEventsLimit} lessons`,
                        date: k,
                        open: false,
                        classPG: 'regular',
                        allForDate: true,
                        fullTitle: `All lessons ${utils.stringToDate(k).toLocaleString('en-us', {month: 'long', day: 'numeric'})}`,
                        items: _.map(_.sortBy(v, 'time_from'), lesson => ({
                            key: `${k}-${lesson.class_id}-${lesson.time_from}-${lesson.time_to}`,
                            title: `${this.classes[lesson.class_id][this.classes[lesson.class_id].is_private ? 'private_className' : 'name']}, ${lesson.time_from} to ${lesson.time_to}`,
                            avatar: null,
                            subtitle: lesson.students.length == 1 ? `${lesson.students[0].first_name} ${lesson.students[0].last_name}` : `${lesson.students.length} students`,
                            isPrivate: lesson.isPrivate,
                            enrollment: lesson.enrollment,
                            class: lesson.class,
                            studentName: lesson.studentName,
                            phone: lesson.phone,
                            email: lesson.email
                        }))
                    })
                }
            })
            return res2
        },
        monthName() {
            return utils.stringToDate(this.start).toLocaleString('en-us', {month: 'long'})
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
            const startTime = moment.tz(this.start, this.timezone).subtract(38, 'd');
            const endTime = moment.tz(this.end, this.timezone).add(38, 'd');
            const end = endTime.toDate()
            for (let start = moment(startTime);start.toDate() <= end; start.add(1, 'day')) {
                const key = start.format('YYYY-MM-DD')
                if(!perDayEvents[key])
                    continue
                res[key] = perDayEvents[key].map(v => {
                    const classStartTime = moment(v.start.dateTime).tz(this.timezone)
                    const classEndTime = moment(v.end.dateTime).tz(this.timezone)
                    return {
                        key: `external-${v.id}`,
                        dateTime: moment(classStartTime), // class timezone, moment object
                        orderTime: moment(classStartTime).tz(this.timezone).format('HH:mm'),
                        time: classStartTime.format('HH:mm'), // class timezone, string
                        duration: classEndTime.diff(classStartTime, 'minutes'),
                        time_from: utils.time24HtoAMPM(classStartTime.format('HH:mm')),
                        time_to: utils.time24HtoAMPM(classEndTime.format('HH:mm')),
                        title: v.summary, // order timezone, string
                        date: classStartTime.format('YYYY-MM-DD'), // class timezone, string
                        classPG: 'external',
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
        ...mapActions({
            getSavedEvents: 'gapi/getSavedEvents',
        }),
        reloadData() {
            this.isLoading = true
            return axios.get('/api/teacher_classes/').then(res => {
            //console.log(res)
                this.classes = _.keyBy(res.data.classes, 'pk')
                this.private_enroll = res.data.private_enroll
                this.group_enroll = res.data.group_enroll
            }).finally(() => this.isLoading = false)
        },
        rescheduleFormOpen(item, action) {
            this.rescheduleFormType = action || 'edit'
            this.rescheduleFormName = this.rescheduleFormType === 'edit' ? 'Edit time' : 'Add next class'
            this.rescheduleFormItem = item
            let todayAtSix = new Date()
            todayAtSix.setHours(6, 0, 0, 0)
            this.rescheduleFormDate = this.rescheduleFormType === 'edit' ? moment(`${this.rescheduleFormItem.enrollment.date} ${this.rescheduleFormItem.enrollment.time_from}`, 'YYYY-MM-DD HH:mm').toDate() : todayAtSix
            const durHours = this.rescheduleFormItem.enrollment.time_to.split(':')[0] - this.rescheduleFormItem.enrollment.time_from.split(':')[0]
            const durMinutes = this.rescheduleFormItem.enrollment.time_to.split(':')[1] - this.rescheduleFormItem.enrollment.time_from.split(':')[1]
            this.rescheduleFormDuration = 60*durHours+durMinutes
            this.rescheduleFormNotice = ''
            this.rescheduleForm = true
        },
        rescheduleFormConfirm() {
            //console.log(this.rescheduleFormItem, this.rescheduleFormDate, this.rescheduleFormNotice)
            const newDateTime = moment(this.rescheduleFormDate)
            const timeTo = moment(this.rescheduleFormDate).add(this.rescheduleFormDuration, 'minutes').format('HH:mm')
            axios.post(this.rescheduleFormType === 'edit' ? '/api/teacher_reschedule' : '/api/teacherd_schedule_enrollment/', {
                notice: this.rescheduleFormNotice,
                datetime: newDateTime.format('YYYY-MM-DD HH:mm'),
                enrollment_id: this.rescheduleFormItem.enrollment.id,
                enrollment_type: this.rescheduleFormItem.isPrivate ? 'private' : 'group',
                orderId: this.rescheduleFormItem.enrollment.order.id,
                selectedDate: newDateTime.format('YYYY-MM-DD'),
                timeFrom: newDateTime.format('HH:mm'),
                timeTo,
            }).then(res => {
                if(!res.data.status) {
                    this.errMsg = res.data.err || (res.data.overbooked ? 'No more available lessons' : 'something went wrong')
                } else {
                    this.rescheduleForm = false
                    const list = this.rescheduleFormItem.isPrivate ? this.private_enroll : this.group_enroll
                    const enrollment = list.find(v => v.id === this.rescheduleFormItem.enrollment.id)
                    if(!enrollment)
                        return
                    enrollment.date = newDateTime.format('YYYY-MM-DD')
                    enrollment.time_from = newDateTime.format('HH:mm')
                    enrollment.time_to = timeTo

                    const index = list.findIndex(v => v.id === enrollment.id)
                    this.$set(list, index, enrollment)

                    if(this.rescheduleFormType !== 'edit') {
                        // add reserved lessons
                        enrollment.order.reserved_lessons ++
                    }
                    this.syncPopupClass = this.rescheduleFormItem.class
                    this.syncPopupEnrollment = this.rescheduleFormItem.enrollment
                    this.syncPopupOpened = true
                    //return this.reloadData()
                }
            })
        },
        declineLesson(data) {
            console.log(data)
            this.declineEnrollment = data.enrollment
            this.$refs.declineSubmitForm.open()
        },
        confirmEnroll(data) {
            console.log('confirmEnroll', data.enrollment.id)
            this.isLoading = true
            axios.post(`/api/private_enroll/${data.enrollment.id}/confirm/`).then(res => {
                this.isLoading = false
                this.reloadData()
            })
        },
    },

    watch: {
        start() {
            console.log(this.start, this.end)
        }
    }
}
</script>
<style lang="scss">
@import "../../../styles/_variables.scss";

.details-container {
    text-align: left;
    max-width: 600px;
}
.teacher-calendar {

    .lesson-event {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        border-radius: 2px;
        color: #000000;
        width: 100%;
        font-size: 12px;
        padding: 3px;
        cursor: pointer;
        margin-bottom: 1px;

        &.approved {
            background-color: rgba(31, 190, 215, 0.1);
            border: 1px solid rgba(31, 190, 215, 1);
        }
        &.regular {
            background-color: rgba(31, 190, 215, 0.1);
            border: 1px solid rgba(31, 190, 215, 1);
        }
        &.external {
            background-color: $platform-blue;
            cursor: auto;
            a {
                color: black;
            }
        }
    }
}
.v-list__tile.v-list__tile--link {
    height: 56px;
}
</style>