<template>
    <v-layout align-center justify-center row wrap class="student-calendar">
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
                  :end="end"
                  color="primary"
                >
                    <template v-slot:day="{ date }">
                        <template v-for="event in calendarEvents[date]">
                          <v-menu
                            :key="event.title"
                            v-model="event.open"
                            full-width
                            offset-x
                          >
                            <template v-slot:activator="{ on }">
                              <div
                                v-ripple
                                :class="'lesson-event '+event.classPG"
                                v-on="on"
                              >
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
                                color="primary"
                                dark
                              >

                                <v-toolbar-title v-html="event.fullTitle || event.title"></v-toolbar-title>
                                <v-spacer></v-spacer>

                                <v-btn icon>
                                  <v-icon>close</v-icon>
                                </v-btn>
                              </v-toolbar>
                              <v-card-text>

                                <v-list v-if="event.items" two-line>
                                  <template v-for="(item, index) in event.items">
                                    <v-list-tile
                                      :key="item.title"
                                      avatar
                                      @click=""
                                    >
                                      <v-list-tile-avatar>
                                        <img v-if="item.avatar" :src="item.avatar">
                                      </v-list-tile-avatar>

                                      <v-list-tile-content>
                                        <v-list-tile-title v-html="item.title"></v-list-tile-title>
                                        <v-list-tile-sub-title v-html="item.subtitle"></v-list-tile-sub-title>
                                      </v-list-tile-content>
                                    </v-list-tile>

                                    <v-divider
                                      v-if="index < event.items.length-1"
                                      :key="index"
                                    ></v-divider>
                                  </template>
                                </v-list>
                                <span v-else>
                                    <div><b>{{event.classPG == 'private' ? 'Private' : 'Group'}}</b></div>
                                    <div>{{event.time_from}} to {{event.time_to}} {{event.timezone}}</div>
                                    <div class="text-xs-left">{{event.teacherName}}, <a :href="`tel:${event.teacher.phone}`">{{event.teacher.phone}}</a>, <a :href="`mailto:${event.teacher.email}`">{{event.teacher.email}}</a></div>
                                    <div class="details-container" v-html="event.details"></div>
                                    <div class="details-container" v-if="event.zoomLink" >zoom link: <a :href="event.zoomLink" target="_blank">{{ event.zoomLink }}</a></div>
                                </span>
                              </v-card-text>
                              <v-card-actions>
                                <v-btn
                                  flat
                                  color="secondary"
                                >
                                  Ok
                                </v-btn>
                                <v-btn
                                  v-if="event.class_id"
                                  color="platform-green"
                                  :to="`/class/${event.class_id}`"
                                >
                                  Join
                                </v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-menu>
                        </template>
                    </template>
                </v-calendar>
              </v-sheet>
            </v-flex>

    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import moment from 'moment'
import classHelper from '@/lib/helpers/Class'

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
        orders: {},
        private_enroll: [],
        group_enroll: [],
        membership_classes: [],
    }),
    props: [],
    components: {

    },
    created() {
        const filterFunc = v => (v.status === 'approved' || v.status === 'requested')
        axios.get('/api/learner/classes/').then(res => {
            //console.log(res)
            this.orders = _.keyBy(res.data.orders, 'id')
            this.private_enroll = _.filter(res.data.private_enroll, filterFunc)
            this.group_enroll = _.filter(res.data.group_enroll, filterFunc)
            this.membership_classes = res.data.membership_classes
        })
    },
    computed: {
        membershipClasses() {
            return classHelper.groupClassesByAvailability(this.membership_classes).current
        },
        membershipClassDates() {
            const dateParts = this.start.split('-').map(v => Number(v))
            const startDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2], 0, 0, 1)
            const endDate = new Date(new Date(dateParts[0], dateParts[1], 1, 23, 59, 59) - 3600000 * 24)
            const res = {};
            for (let i=0;i<this.membershipClasses.length;i++) {
                if (this.membershipClasses[i].day_select_type === 'monthly') {
                    this.membershipClasses[i].schedule_dates.forEach(v => {
                        const dateParts = v.date.split('-').map(v => Number(v))
                        const lessonDate = new Date(dateParts[0], dateParts[1] - 1, dateParts[2], 12, 0, 0)
                        if (startDate < lessonDate && endDate > lessonDate) {
                            res[v.date] = [...(res[v.date] || []), {
                                ...this.membershipClasses[i],
                                date: v.date,
                                time_to: v.start,
                                time_from: v.end,
                            }]
                        }
                    })
                }
            }
            return res;
        },
        dateEvents() {
            const dateEvents = {}
            _.each(this.private_enroll, v => {
                if(!dateEvents[v.date])
                    dateEvents[v.date] = []
                let curClass = this.orders[v.order].data['class']
                //for (let x = 0;x < 7; x++)
                dateEvents[v.date].push({
                    title: curClass.private_className,
                    details: utils.formatTextToHtml(curClass.groupClassSummary),
                    date: v.date,
                    classPG: 'private',
                    status: v.status,
                    open: false,
                    order_id: v.order,
                    teacher: _.assignWith(curClass.teacher, curClass.teacher.user, (t, u, key) => {
                        return key === 'phone' || key === 'email' ? t || u : t
                    }),
                    teacherName: `${curClass.teacher.first_name} ${curClass.teacher.last_name}`,
                    datetime: moment(`${v.date} ${v.time_from}`),
                    time_from: utils.time24HtoAMPM(v.time_from),
                    time_to: utils.time24HtoAMPM(v.time_to),
                    timezone: this.orders[v.order].timezone,
                    zoomLink: this.orders[v.order].zoomLink,
                })
            })
            _.each(this.group_enroll, v => {
                if(!dateEvents[v.date])
                    dateEvents[v.date] = []
                let curClass = this.orders[v.order].data['class']
                //for (let x = 0;x < 5; x++)
                dateEvents[v.date].push({
                    title: curClass.name,
                    details: utils.formatTextToHtml(curClass.groupClassSummary),
                    date: v.date,
                    classPG: 'group',
                    status: v.status,
                    open: false,
                    order_id: v.order,
                    teacher: _.assignWith(curClass.teacher, curClass.teacher.user, (t, u, key) => {
                        return key === 'phone' || key === 'email' ? t || u : t
                    }),
                    teacherName: `${curClass.teacher.first_name} ${curClass.teacher.last_name}`,
                    datetime: moment(`${v.date} ${v.time_from}`),
                    time_from: utils.time24HtoAMPM(v.time_from),
                    time_to: utils.time24HtoAMPM(v.time_to),
                    timezone: this.orders[v.order].timezone,
                    zoomLink: this.orders[v.order].zoomLink,
                })
            })
            Object.entries(this.membershipClassDates).forEach(([k, vals]) => {
                dateEvents[k] = [...(dateEvents[k] || []), ...vals.map(v => ({
                    title: v.day_select_type === 'monthly' ? v.name : v.private_className,
                    details: utils.formatTextToHtml(v.groupClassSummary),
                    date: k,
                    classPG: 'member',
                    status: null,
                    open: false,
                    order_id: null,
                    class_id: v.id,
                    teacher: _.assignWith(v.teacher, v.teacher.user, (t, u, key) => {
                        return key === 'phone' || key === 'email' ? t || u : t
                    }),
                    teacherName: `${v.teacher.first_name} ${v.teacher.last_name}`,
                    datetime: moment(`${v.date} ${v.time_from}`),
                    time_from: utils.time24HtoAMPM(v.time_from),
                    time_to: utils.time24HtoAMPM(v.time_to),
                    timezone: v.timezone,
                }))]
            })
            return dateEvents
        },
        calendarEvents() {
            let res2 = {}
            _.each(this.dateEvents, (v, k) => {
                res2[k] = _.sortBy(v, 'datetime').slice(0, v.length > this.cellEventsLimit ? this.cellEventsLimit - 1 : this.cellEventsLimit )
                if(v.length > this.cellEventsLimit) {
                    res2[k].push({
                        title: `+${v.length-this.cellEventsLimit} lessons`,
                        date: k,
                        open: false,
                        classPG: 'the-rest',
                        allForDate: true,
                        fullTitle: `All lessons ${utils.stringToDate(k).toLocaleString('en-us', {month: 'long', day: 'numeric'})}`,
                        items: _.map(_.sortBy(v, 'time_from'), lesson => ({
                            title: `${lesson.title}, ${lesson.time_from} to ${lesson.time_to}`,
                            avatar: lesson.teacher.media,
                            subtitle: `${lesson.teacher.first_name} ${lesson.teacher.last_name}, <a href="tel:${lesson.teacher.phone}">${lesson.teacher.phone}</a>, <a href="mailto:${lesson.teacher.email}">${lesson.teacher.email}</a>`,
                        }))
                    })
                }
            })
            return res2
        },
        monthName() {
            return utils.stringToDate(this.start).toLocaleString('en-us', {month: 'long'})
        }
    },
    methods: {

    },

    watch: {

    }
}
</script>
<style lang="scss">
.details-container {
    text-align: left;
    max-width: 600px;
}
.student-calendar {
    .lesson-event {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        border-radius: 2px;
        color: black;
        width: 100%;
        font-size: 12px;
        padding: 3px;
        cursor: pointer;
        margin-bottom: 1px;

        &.group {
            background-color: rgba(31, 190, 215, 0.1);
            border: 1px solid rgba(31, 190, 215, 1);
        }
        &.private {
            background-color: rgba(31, 190, 215, 0.1);
            border: 1px solid rgba(31, 190, 215, 1);
        }
        &.member {
            background: repeating-linear-gradient(
                45deg,
                white,
                white 10px,
                rgba(31, 190, 215, 0.1) 10px,
                rgba(31, 190, 215, 0.1) 20px
              );
            border: 1px solid rgba(31, 190, 215, 1);
        }
        &.the-rest {
            background-color: rgba(31, 190, 215, 0.1);
            border: 1px solid rgba(31, 190, 215, 1);
        }
    }
}

</style>