<template>
    <v-layout align-center justify-center row wrap>
      <v-flex xs12 class="text-xs-left class-list">
        <h3>Upcoming sessions</h3>
      </v-flex>
        <v-flex xs12 md10 v-if="notifications && notifications.length">
            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="grey"
            ></v-progress-circular>
          <v-card v-else>
            <v-card-title primary-title>
              <div>
                <h3 class="headline mb-0">Notifications</h3>
              </div>
            </v-card-title>

            <v-list class="full-height-list">
                <template v-for="(item, index) in notifications">
                  <v-list-tile
                    :key="item.key"
                    avatar
                  >
                    <v-list-tile-content>
                      <v-list-tile-title>
                          {{item.text}}
                          <a v-if="item.urlType === 'absolute'" :href="item.url">{{ item.urlText || item.url }}</a>
                          <router-link v-else :to="item.url">here</router-link>
                      </v-list-tile-title>
                    </v-list-tile-content>
                    <v-list-tile-action style="min-width: 80px;">
                      <v-btn flat icon @click="removeNotification(item.id);">
                            <v-icon>clear</v-icon>
                        </v-btn>
                    </v-list-tile-action>
                  </v-list-tile>
                  <v-divider
                      v-if="index + 1 < notifications.length"
                  ></v-divider>
                </template>
            </v-list>
          </v-card>
        </v-flex>
      <v-flex xs12 v-if="notification">
        <v-alert
          ref="notificationAlert"
          :value="true"
          :color="notification.color"
          icon="new_releases"
        >
          {{notification.html}}
          <v-btn
            v-if="notification.button"
            :color="notification.color+' darken-1'"
            @click="$refs.notificationAlert.value=false"
          >
            {{notification.button}}
          </v-btn>
        </v-alert>
      </v-flex>
        <v-flex xs12>
            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="grey"
            ></v-progress-circular>
        </v-flex>
      <v-flex xs12 class="text-xs-left class-list">
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
                    <span v-if="item.dateTitle">Next session is on {{ item.dateTitle }}, <b>{{item.timeFrom}} - {{item.timeTo}} {{item.timezone}}</b>. See calendar for all sessions.</span>
                    <span v-else>Please sign in to attend sessions.</span>
                    <!--span v-if="item.nextLessons.length > 1">, and {{item.nextLessons.length-1}} after</span-->
                    <span v-if="!isUnlimitedTotalLessons(item)">{{ item.enrollmentLeft }} of {{ item.totalLessons }} session credits left.</span>
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
                    <div></div>
                </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action>
                  <v-chip v-if="item.isRefunded" color="red" text-color="white">
                      <v-avatar>
                        <v-icon>check_circle</v-icon>
                      </v-avatar>
                      Refunded
                  </v-chip>
                  <template v-if="(item.canBook || item.editEnrollmentAvailable) && !item.isRefunded">
                    <v-menu offset-y>
                      <template v-slot:activator="{ on }">
                          <v-btn
                            small
                            v-on="on"
                            class="hidden-xs-only action-button"
                          >
                            <v-icon dark left>create</v-icon>
                              Actions
                          </v-btn>
                          <v-btn
                            icon
                            v-on="on"
                            class="hidden-sm-and-up"
                          >
                              <v-icon>create</v-icon>
                          </v-btn>
                      </template>
                      <v-list>
                        <v-list-tile
                          v-if="item.canBook"
                          @click="rescheduleFormOpen(item, 'add')"
                        >
                          <v-list-tile-title>Add date</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile
                          v-if="item.editEnrollmentAvailable"
                          @click="rescheduleFormOpen(item, 'edit')"
                        >
                            <v-list-tile-title>Reschedule</v-list-tile-title>
                        </v-list-tile>
                      </v-list>
                    </v-menu>
                  </template>
                  <v-btn v-else-if="item.canAgain" :to="`/learners/new_enroll/${item.class_id}/4/${item.order_id}`">Buy again</v-btn>
                  <v-btn flat icon @click="removeOrder(item.order_id)">
                      <v-icon>clear</v-icon>
                  </v-btn>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider
              v-if="index + 1 < classesList.length"
            ></v-divider>
          </template>
        </v-list>
        <div class="text-xs-center">
            <v-btn color="primary" :to="exploreMoreLink">{{ exploreMoreLabel }}</v-btn>
        </div>
      </v-flex>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import notifications from '@/lib/notifications.js'
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
        this.removedOrders = (localStorage.getItem('rem_ords') || '').split(',');
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
        exploreMoreLabel() {
            return this.singleCompany ? `More classes at ${this.singleCompany.name}` : 'Explore more classes';
        },
        exploreMoreLink() {
            return this.singleCompany ? `/company/${this.singleCompany.slug}` : '/';
        },
        singleCompany() {
            if (this.orders && this.orders.length) {
                const comps = this.orders.reduce((acc, v, k) => acc && v.data.class.teacher.user.company_profile ? {
                    ...acc,
                    [v.data.class.teacher.user.company_profile.id]: v.data.class.teacher.user.company_profile} : null, {});
                return comps && Object.keys(comps).length === 1 ? Object.values(comps)[0] : null;
            }
            return null;
        },
        ordersEnrolled() {
            return _.mapValues(_.keyBy(_.concat([], this.private_enroll, this.group_enroll), 'order'), v => true)
        },
        notifications() {
            const getText = (order) => order.data.class.is_private ?
                `Thanks for your payment! Please schedule a time for your sessions with ${order.data.class.teacher.first_name} ${order.data.class.teacher.last_name}` :
                `Thank you for your payment. Please schedule your first session in ${order.data.name}`
            let res = _.map(_.filter(this.orders, o => !this.ordersEnrolled[o.id] && !helperClass.checkExpired(o.data.class)), v => ({
                text: getText(v),
                url: `/learners/${v.klass}/7/${v.id}`,
                key: v.id,
                id: 'p-'+v.id,
            }))
            res = [...this.orders.filter(v => v.zoomLink && !helperClass.checkExpired(v.data.class)).map((v) => ({
                text: `You are enrolled in ${v.data.name} `,
                urlText: 'zoom link',
                urlType: 'absolute',
                url: v.zoomLink,
                key: 'z-'+v.id,
                id: 'z-'+v.id,
            })), ...res];
            return res.filter(v => !this.removedNotifications.includes(v.id));
        },
        notification() {
            return this.$route.params.notification && notifications[this.$route.params.notification] ? notifications[this.$route.params.notification]() : null
        },
        lessonsList () {
            let ordersDict = _.keyBy(this.orders, 'id')
            const pendingDict = _.groupBy(_.filter(this.private_enroll, {status: 'requested'}), 'order')
            let res = []
            let func = _.bind((type) => {
                return function (enrollment) {
                    let date = utils.stringToDate(enrollment.date)
                    const total_lessons = ordersDict[enrollment.order].data.package ? ordersDict[enrollment.order].data.package.numberOfLessons : 0
                    const reserved_lessons = 'x'
                    res.push({
                        date: date,
                        type: type,
                        dateTitle: date.toLocaleString('en-us', { weekday: 'long', month: 'long', day: 'numeric'}),
                        timeFrom: utils.time24HtoAMPM(enrollment.time_from),
                        timeTo: utils.time24HtoAMPM(enrollment.time_to),
                        name: type === 'private' ? `${ordersDict[enrollment.order].data['class'].private_className} with
                            ${ordersDict[enrollment.order].data['class'].teacher.first_name}
                            ${ordersDict[enrollment.order].data['class'].teacher.last_name}` : ordersDict[enrollment.order].data['class'].name,
                        key: type+enrollment.id,
                        canBook: total_lessons != reserved_lessons,
                        avatar: helperClass.previewImageSrc(ordersDict[enrollment.order].data['class'].teacher.media),
                        total_lessons: total_lessons,
                        reserved_lessons: reserved_lessons,
                        class_id: ordersDict[enrollment.order].data['class'].id,
                        order_id: enrollment.order,
                        step: 7,
                    })
                }
            }, this)
            _.each(this.private_enroll, func('private'))
            _.each(this.group_enroll, func('group'))
            return _.sortBy(res, 'date')
        },
        classesList() {
            let res = []
            let privateEnrolls = _.groupBy(this.private_enroll, 'order')
            let groupEnrolls = _.groupBy(this.group_enroll, 'order')
            _.each(this.orders, (o) => {
                if (this.removedOrders.includes(o.id)) return;
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
        isUnlimitedTotalLessons(item) {
            return item.totalLessons === 999;
        },
        rescheduleFormOpen(item, mode) {
            console.log(item, mode)
            this.$router.push(`/learners/${item.class_id}/${item.step}/${item.order_id}`)
        },
        downloadCSVReport() {
            axios.get(`/api/csv_student_export/`, {
                params: {
                    from_date: this.csvStartDate,
                    to_date: this.csvEndDate,
                }
            }).then(res => {
                console.log(res)
                const blob = new Blob([res.data], { type: res.headers['content-type'] })
                const link = document.createElement('a')
                link.href = window.URL.createObjectURL(blob)
                const contentDispositionParsed = res.headers['content-disposition'].match(/filename="(.+)"/)
                link.setAttribute('download', contentDispositionParsed[1])
                link.click()
            }).catch(e => console.log(e))
        },
        removeNotification(id) {
          this.removedNotifications.push(id);
          localStorage.setItem('rem_nots', this.removedNotifications.join(','));
        },
        removeOrder(id) {
          this.removedOrders.push(id);
          localStorage.setItem('rem_ords', this.removedOrders.join(','));
        },
    },

    watch: {

    }
}
</script>
<style lang="scss" scoped>
.action-button {
    padding: 0.5em;
}
</style>