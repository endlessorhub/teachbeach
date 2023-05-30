<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 class="text-xs-left class-list">
            <h3>Orders history</h3>
        </v-flex>
        <v-flex v-if="isLoading" xs12>
            <v-progress-circular
                indeterminate
                color="grey"
            ></v-progress-circular>
        </v-flex>
      <v-flex v-else xs12 class="text-xs-left class-list">
        <v-list three-line class="full-height-list">
          <template v-for="(item, index) in classesList">
            <v-list-tile
              :key="item.key"
              avatar
              ripple
            >
              <v-list-tile-avatar :tile="true" class="hidden-sm-and-down">
                <img v-if="item.avatar" :src="item.avatar">
              </v-list-tile-avatar>
              <v-list-tile-content style="min-height: 96px;">
                <v-list-tile-title>
                    <b>{{item.isPrivate ? 'Private' : 'Group'}} </b>
                    <router-link :to="'/class/'+item.class_id">{{ item.name }}</router-link>,
                    <span v-if="item.isPrivate">{{item.teacherName}}, <a :href="'tel:'+item.phone">{{item.phone}}</a>, <a :href="'mailto:'+item.email">{{item.email}}</a></span>
                    <div v-if="item.zoomLink"><a :href="item.zoomLink">zoom link</a></div>
                </v-list-tile-title>

                <v-list-tile-sub-title>
                    <v-chip v-if="item.isCompleted" color="success" text-color="white">
                      <v-avatar>
                        <v-icon>check_circle</v-icon>
                      </v-avatar>
                      Completed
                    </v-chip>
                    <v-chip color="orange" text-color="white" v-if="item.pendingLessons">
                      <v-avatar class="orange darken-4">{{item.pendingLessons}}</v-avatar>
                      Pending
                    </v-chip>
                    <v-chip v-if="item.isRefunded" color="red" text-color="white">
                      <v-avatar>
                        <v-icon>check_circle</v-icon>
                      </v-avatar>
                      Refunded
                    </v-chip>
                    <v-chip v-if="item.isRemoved" color="grey" text-color="white">
                      <v-avatar>
                        <v-icon>delete_outline</v-icon>
                      </v-avatar>
                      Deleted
                    </v-chip>
                </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                <v-btn v-if="item.isRemoved" @click="restoreOrder(item.order_id)">Restore</v-btn>
                <v-btn v-if="item.canAgain" :to="`/learners/new_enroll/${item.class_id}/4/${item.order_id}`">Buy again</v-btn>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider
              v-if="index + 1 < classesList.length"
            ></v-divider>
          </template>
        </v-list>
      </v-flex>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import utils from '@/lib/utils.js'
import moment from 'moment'
import helperClass from '@/lib/helpers/Class'

export default {
    name: 'dashboard_learn',
    data: () => ({
        isLoading: false,
        private_enroll: [],
        group_enroll: [],
        orders: [],
        membership_classes: [],
        openedCSVStartDate: false,
        csvStartDate: '',
        openedCSVEndDate: false,
        csvEndDate: '',
        removedNotifications: [],
        removedOrders: [],
    }),
    props: [],
    components: {

    },
    created() {
        this.removedNotifications = (localStorage.getItem('rem_nots') || '').split(',');
        this.removedOrders = (localStorage.getItem('rem_ords') || '').split(',').map(v => Number(v));
        this.isLoading = true
        axios.get('/api/learner/classes/').then(res => {
            console.log(res)
            this.private_enroll = res.data.private_enroll
            this.group_enroll = res.data.group_enroll
            this.orders = res.data.orders
            this.membership_classes = res.data.membership_classes
        }).catch(e => {
            console.log(e)
        }).then(() => {
            this.isLoading = false
        })
    },
    computed: {
        classesList() {
            let res = []
            let privateEnrolls = _.groupBy(this.private_enroll, 'order')
            let groupEnrolls = _.groupBy(this.group_enroll, 'order')
            _.each(this.orders, (o) => {
                let isExpired = true
                if(o.data['class'].day_select_type == 'weekly') {
                    if(!o.data['class'].until_date)
                        isExpired = false
                    else {
                        let available_dates = utils.getCalendarDatesForPeriod(
                            o.data['class'].start_date,
                            o.data['class'].until_date,
                            o.data['class'].weekdays_schedule,
                            o.data['class'].start_date,
                            o.data['class'].until_date,
                            o.data['class'].schedule_excluded
                        )
                        if(available_dates.length) {
                            let lastDate = moment(`${_.last(available_dates)}`, 'YYYY-MM-DD')
                            let lastHour = moment(`${_.last(available_dates)} ${_.find(o.data['class'].weekdays_schedule, ws => ws.weekday == lastDate.day()).start}`, 'YYYY-MM-DD HH:mm')
                            isExpired = lastHour.diff(new Date()) < 0
                        } else {
                            isExpired = true
                        }
                    }
                } else {
                    let lastItem = _.last(_.sortBy(o.data['class'].schedule_dates, 'date'))
                    let lastHour = moment(`${lastItem.date} ${lastItem.start}`, 'YYYY-MM-DD HH:mm')
                    isExpired = lastHour.diff(new Date()) < 0
                }
                if(isExpired)
                    return
                let enrolls = []
                if(o.data['class'].is_private) {
                    enrolls = privateEnrolls[o.id] || []
                } else {
                    enrolls = groupEnrolls[o.id] || []
                }
                const timeDiff = enr => moment(`${enr.date} ${enr.time_from}`, 'YYYY-MM-DD HH:mm').diff(new Date())
                let nextLessons = _.sortBy(_.filter(enrolls, enr => (timeDiff(enr) > 0 && enr.status !== 'rejected')), timeDiff)
                let closestLesson = nextLessons.length && o.status !== 'refund' ? nextLessons[0] : null
                let type = o.data['class'].is_private ? 'private' : 'group'
                let totalLessons = o.num_lessons
                const enrollmentLeft = o.num_lessons - o.reserved_lessons
                const canBook = enrollmentLeft && !isExpired && (o.data['class'].flexible_dates || o.data['class'].is_private);
                res.push({
                    key: type+o.id,
                    type: type,
                    isPrivate: o.data['class'].is_private,
                    name: o.data['name'],
                    teacherName: o.data['class'].teacher.first_name+' '+o.data['class'].teacher.last_name,
                    phone: o.data['class'].teacher.phone || o.data['class'].teacher.user.phone,
                    email: o.data['class'].teacher.email || o.data['class'].teacher.user.email,
                    signedInLessons: _.filter(enrolls, {status: "approved"}).length,
                    pendingLessons: _.filter(nextLessons, {status: "requested"}).length,
                    totalLessons: totalLessons,
                    enrollmentLeft: enrollmentLeft,
                    canBook: canBook,
                    canAgain: totalLessons <= enrolls.length && !isExpired && !closestLesson,
                    isCompleted: totalLessons <= _.filter(enrolls, {status: "approved"}).length && !closestLesson,
                    isRefunded: o.status === 'refund',
                    avatar: helperClass.previewImageSrc(o.data['class'].teacher.media),
                    class_id: o.data['class'].id,
                    order_id: o.id,
                    dateTitle: closestLesson ? utils.stringToDate(closestLesson.date).toLocaleString('en-us', { weekday: 'long', month: 'long', day: 'numeric'}) : '',
                    timeFrom: closestLesson ? utils.time24HtoAMPM(closestLesson.time_from) : '',
                    timeTo: closestLesson ? utils.time24HtoAMPM(closestLesson.time_to) : '',
                    timezone: o.timezone,
                    closestTimestamp: closestLesson ? moment(`${closestLesson.date} ${closestLesson.time_from}`, 'YYYY-MM-DD HH:mm').unix() : null,
                    nextLessons: nextLessons,
                    step: 7,
                    editEnrollmentAvailable: (!!closestLesson || _.filter(enrolls, {status: "requested"}).length) && (o.data['class'].flexible_dates || o.data['class'].is_private),
                    zoomLink: o.zoomLink,
                    isRemoved: this.removedOrders.includes(o.id),
                })
            })
            return _.sortBy(res, v => {
                if(v.pendingLessons)
                    return '0'
                if(v.closestTimestamp && !v.isRefunded) {
                    return '1-'+v.closestTimestamp
                }
                if((v.canBook || v.editEnrollmentAvailable) && !v.isRefunded) {
                    return '2-'+v.order_id
                }
                if(v.canAgain && !v.isRefunded) {
                    return '3-'+v.order_id
                }
                if(v.isRefunded) {
                    return '4'
                }
                return '5'
            })
        }
    },
    methods: {
        restoreOrder(id) {
            this.removedOrders = this.removedOrders.filter(ro => ro !== id);
            localStorage.setItem('rem_ords', this.removedOrders.join(','));
        },
    },
}
</script>
<style lang="scss" scoped>
.action-button {
    padding: 0.5em;
}
</style>