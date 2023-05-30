<template>
    <v-layout align-start justify-center row wrap class="teacher-schedule-list">
        <snack v-model="snackMsg" :timeout="0"></snack>
        <v-flex xs6 class="text-xs-center">
            <v-radio-group v-model="filterClasses">
                <v-radio value="upcoming" label="Upcoming"></v-radio>
                <v-radio value="previous" label="Previous"></v-radio>
            </v-radio-group>
        </v-flex>
        <v-flex xs6 class="text-xs-center">
            <v-btn to="/dashboard/teach/schedule_calendar">
                Calendar
            </v-btn>
        </v-flex>
        <v-flex xs12 class="text-xs-center">
            <v-data-table
                :headers="headers"
                :items="studentList"
                :loading="isLoading"
                class="elevation-1"
                :pagination.sync="pagination"

            >
                <v-progress-linear v-slot:progress color="blue" indeterminate></v-progress-linear>
                <template v-slot:items="props">
                  <td class="text-xs-left">
                      {{ props.item.datetimeText }}
                  </td>
                    <td class="text-xs-left">
                        <div>{{ props.item.className }}{{props.item.enrolledText ? ` / ${props.item.enrolledText}` : ''}}</div>
                        <div>{{props.item.amountText}}</div>
                    </td>
                  <td>{{ props.item.type }}</td>
                  <td v-if="props.item.studentNames" class="text-xs-left">
                      <span v-if="props.item.studentNames.length > studentsLimit && props.item.studentNamesExpanded"><span v-html="props.item.studentNames.join('<br/>')"></span> <a @click="extendStudents(props.item.datetimeText, false)">...less</a></span>
                      <span v-else-if="props.item.studentNames.length > studentsLimit && !props.item.studentNamesExpanded"><span v-html="props.item.studentNames.slice(0, studentsLimit).join('<br/>')"></span> <a @click="extendStudents(props.item.datetimeText, true)">...more</a></span>
                      <span v-else v-html="props.item.studentNames.join('<br/>')"></span>
                  </td>
                  <td v-else class="text-xs-left">
                      {{ props.item.studentName }}<br/>
                      <a :href="`tel:${props.item.studentPhone}`">{{ props.item.studentPhone }}</a><br/>
                      <a :href="`mailto:${props.item.studentEmail}`">{{ props.item.studentEmail }}</a>
                  </td>
                  <td class="text-xs-center">
                      <v-btn icon flat color="primary" @click.stop="videoFormOpen(props.item)">
                        <v-icon>message</v-icon>
                      </v-btn>
                  </td>
                  <td>
                    <v-menu v-if="props.item.isPrivate" offset-y>
                      <template v-slot:activator="{ on }">
                          <v-btn
                            small
                            v-on="on"
                          >
                            <v-icon v-if="props.item.status === 'requested'" dark left>far fa-question-circle</v-icon>
                            <v-icon v-else dark left>create</v-icon>
                              <template v-if="props.item.isExpired">Expired</template>
                              <template v-else>Schedule</template>
                          </v-btn>
                      </template>
                      <v-list>
                        <v-list-tile
                          v-if="props.item.isPending"
                          @click="confirmEnroll(props.item)"
                        >
                            <v-list-tile-title>Confirm</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile
                          v-if="props.item.isPending"
                          @click="declineLesson(props.item)"
                        >
                            <v-list-tile-title>Decline</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile
                          @click="rescheduleFormOpen(props.item)"
                        >
                            <v-list-tile-title>Reschedule</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile
                          v-if="props.item.newEnrollmentAvailable"
                          @click="rescheduleFormOpen(props.item, 'add')"
                        >
                          <v-list-tile-title>Add date</v-list-tile-title>
                        </v-list-tile>
                        <v-list-tile
                          v-if="props.item.isCompleted"
                          @click="openSendOffers(props.item)"
                        >
                          <v-list-tile-title>Send offers</v-list-tile-title>
                        </v-list-tile>
                      </v-list>
                    </v-menu>
                  </td>
                    <td>
                        <PrivateLessonCalendarImport
                            v-if="props.item.calendarImport"
                            :privateClass="props.item.class"
                            :enrollment="props.item.confirmedEnroll"
                            :isPopupOpened="props.item.isPopupOpened"
                            :isTooltipDynamic="true"
                            @closed="openedSyncPopup=null"
                        />
                    </td>
                </template>
            </v-data-table>
            <SendEmailsToStudents/>
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
                <v-btn color="blue darken-1" flat @click.stop="rescheduleForm=false">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click.stop="rescheduleFormConfirm">Send</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="sendOffersForm" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Send offers</span>
              </v-card-title>

              <v-card-text>
                  <v-layout wrap>
                    <v-flex xs12>
                      <v-textarea
                        v-model="sendOffersMessage"
                        auto-grow
                        box
                        label="Message"
                        rows="4"
                      ></v-textarea>
                    </v-flex>
                  </v-layout>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click.stop="sendOffersForm=false">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click.stop="sendOffers">Send</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="videoFormOpened" max-width="500px" max-height="1000px">
            <v-card>
              <v-card-title>
                <span class="headline">Message student/s here </span>
                  <v-spacer></v-spacer>

                <v-btn icon>
                  <v-icon @click.stop="videoFormOpened = false">close</v-icon>
                </v-btn>
              </v-card-title>

              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12>
                        <div class="subheading text-xs-left">Message students here with meeting/other instructions</div>
                    </v-flex>
                    <v-flex xs12>
                      <v-textarea
                        v-model="videoFormMessage"
                        auto-grow
                        box
                        label="Message"
                        rows="10"
                      ></v-textarea>
                    </v-flex>
                    <v-flex xs12>
                        <div class="subheading text-xs-left">Add link for zoom/online meetings:</div>
                    </v-flex>
                    <v-flex xs12>
                      <v-text-field v-model="videoFormUrl" label="URL"></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="darken-1" flat @click.stop="videoFormOpened=false">Cancel</v-btn>
                <v-btn color="blue darken-1" flat @click.stop="videoFormConfirm">Send</v-btn>
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
import FormDeclineEnrollment from '@/components/basic/forms/DeclineEnrollment'
import SendEmailsToStudents from './Components/SendEmailsToStudents'
import Snack from '@/components/basic/Snack'
import PrivateLessonCalendarImport from './Components/PrivateLessonCalendarImport'

export default {
    name: 'dashboard_teach_schedule_list',
    data: () => ({
        isLoading: false,
        classes: {},
        private_enroll: [],
        group_enroll: [],
        headers: [
            {
                text: 'Date/Time',
                align: 'left',
                sortable: true,
                value: 'datetime'
            },
            { text: 'Class', value: 'className', align: 'left'},
            { text: 'Type', value: 'type' },
            { text: 'Student', value: 'studentName', align: 'left'},
            { text: 'Message', value: 'amount', align: 'center'},
            { text: 'Actions', value: 'actions', sortable: false, align: 'center' },
            { text: 'Sync to calendar', value: 'calendarImport' },
        ],
        pagination: {
            descending: false,
            page: 1,
            rowsPerPage: -1,
            sortBy: 'datetime',
            totalItems: 0
        },
        openedSyncPopup: null,
        rescheduleForm: false,
        rescheduleFormType: 'edit',
        rescheduleFormItem: {},
        rescheduleFormDate: null,
        rescheduleFormDuration: 1,
        rescheduleFormNotice: '',
        rescheduleFormName: '',
        //errMsg: '',

        declineEnrollment: {},

        sendOffersForm: false,
        sendOffersItem: null,
        sendOffersMessage: '',

        videoFormData: {},
        videoFormOpened: false,
        videoFormUrl: '',
        videoFormMessage: '',
        snackMsg: '',
        studentsLimit: 2,
        extendedStudents: {},
    }),
    props: [],
    components: {
        Reschedule,
        FormDeclineEnrollment,
        Snack,
        SendEmailsToStudents,
        PrivateLessonCalendarImport,
    },
    created() {
        this.reloadData()
    },
    computed: {
        sendOffersMessageBlank() {
            return this.sendOffersItem ? `Hi ${this.sendOffersItem.confirmedEnroll.student.first_name}
You are on a roll! ${this.sendOffersItem['class'].teacher.first_name} invites you to keep learning.
Enroll with one click ${window.location.origin}/learners/new_enroll/${this.sendOffersItem['class'].pk}/4/${this.sendOffersItem.confirmedEnroll.order.id}
${this.sendOffersItem['class'].teacher.phone || this.sendOffersItem['class'].teacher.user.phone}` : ''
        },
        studentList() {
            let res = []
            _.each(this.private_enroll, v => {
                let curClass = this.classes[v.class_id]
                //for (let x = 0;x < 7; x++)
                const datetime = moment(`${v.date} ${v.time_from}`).toDate()
                const isPending = v.status === 'requested' && moment(`${v.date} ${v.time_from}`).toDate() > new Date()
                const isExpired = v.status === 'requested' && moment(`${v.date} ${v.time_from}`).toDate() < new Date()
                const enrollmentLeft = v.order.num_lessons - v.order.reserved_lessons
                const enrollments = _.filter(this.private_enroll, pe => (pe.order.id === v.order.id && moment(`${pe.date} ${pe.time_from}`).toDate() < new Date() && pe.status === 'approved'))
                const isCompleted = enrollments.length === Number(v.order.num_lessons)
                const amount = v.order.status === 'refund' ? 0 : Number(v.order.amount)
                res.push({
                    datetime: datetime,
                    datetimeText: datetime.toLocaleString('en-us', {hour12: true, hour: 'numeric', minute: 'numeric', month: 'short', day: 'numeric', year: 'numeric'}),
                    isPrivate: true,
                    type: 'Private',
                    className: curClass.name,
                    teacherName: `${curClass.teacher.first_name} ${curClass.teacher.last_name}`,
                    studentName: `${v.student.first_name} ${v.student.last_name}`,
                    student: v.student,
                    studentPhone: v.student.phone,
                    studentEmail: v.student.email,
                    amount: amount,
                    amountText: v.order.status === 'refund' ? 'Refunded' : utils.formatPrice(amount, 'usd'),
                    enrolledText: ``,
                    status: v.status,
                    isExpired,
                    isPending: isPending,
                    isCompleted: isCompleted,
                    phone: v.student.phone,
                    email: v.student.email,
                    id: v.id,
                    enrollment: v,
                    newEnrollmentAvailable: !!enrollmentLeft,
                    lessonsLeft: enrollmentLeft ? `${enrollmentLeft} of ${v.order.num_lessons} lessons left` : '',
                    calendarImport: true,
                    class: curClass,
                    confirmedEnroll: v,
                    isPopupOpened: this.openedSyncPopup === v.id,
                })
            })
            const tmpExistingDict = {}
            _.each(this.group_enroll, v => {
                if(v.status !=='approved')
                    return
                let curClass = this.classes[v.class_id]
                //for (let x = 0;x < 7; x++)
                const datetime = moment(`${v.date} ${v.time_from}`).toDate()
                const amount = v.order.status === 'refund' ? 0 : Number(v.order.amount)
                const enrolled = this.group_enroll.filter(
                    ge => ge.class_id === v.class_id
                    && ge.date === v.date
                    && ge.status ==='approved'
                    && ge.time_from === v.time_from
                ).length;
                const datetimeText = datetime.toLocaleString('en-us', {hour12: true, hour: 'numeric', minute: 'numeric', month: 'short', day: 'numeric', year: 'numeric'});
                if(datetimeText in tmpExistingDict) {
                    res[tmpExistingDict[datetimeText]].studentNames.push(`${v.student.first_name} ${v.student.last_name}`);
                    res[tmpExistingDict[datetimeText]].students.push(v.student);
                    return
                }
                tmpExistingDict[datetimeText] = res.length;
                res.push({
                    datetime: datetime,
                    datetimeText,
                    isPrivate: false,
                    type: 'Group',
                    className: curClass.name,
                    teacherName: `${curClass.teacher.first_name} ${curClass.teacher.last_name}`,
                    studentNames: [`${v.student.first_name} ${v.student.last_name}`],
                    studentNamesExpanded: this.extendedStudents[datetimeText],
                    students: [v.student],
                    amount: amount,
                    amountText: v.order.status === 'refund' ? 'Refunded' : utils.formatPrice(amount, 'usd'),
                    enrolledText: `${enrolled} enrolled`,
                    status: v.status,
                    phone: v.student.phone,
                    email: v.student.email,
                    id: v.id,
                    enrollment: v,
                })
            })
            return _.filter(res, s => {
                if(s.enrollment.order.status === 'refund' || s.enrollment.status === 'rejected')
                    return false
                if(s.datetime > new Date() && this.filterClasses === 'upcoming')
                    return true
                if(s.datetime <= new Date() && this.filterClasses === 'previous')
                    return true
                return false
            })
        },
        filterClasses: {
            get() {
                //console.log(this.$route)
                return this.$route.query.filter || 'upcoming'
            },
            set(v) {
                this.$router.push(`?filter=${v}`)
            },

        },
    },
    methods: {
        extendStudents(key, expand) {
            this.$set(this.extendedStudents, key, expand);
        },
        reloadData() {
            this.isLoading = true
            return axios.get('/api/teacher_classes/').then(res => {
            //console.log(res)
                this.classes = _.keyBy(res.data.classes, 'pk')
                this.private_enroll = res.data.private_enroll
                this.group_enroll = res.data.group_enroll
            }).finally(() => {
                this.isLoading = false
            })
        },
        rescheduleFormOpen(item, action) {
            this.rescheduleFormType = action || 'edit'
            this.rescheduleFormName = this.rescheduleFormType === 'edit' ? (item.datetime < new Date() ?  'If  your student missed this class, you can reschedule it here.' : 'Edit time') : 'Add next class'
            this.rescheduleFormItem = item
            let todayAtSix = new Date()
            todayAtSix.setHours(6, 0, 0, 0)
            this.rescheduleFormDate = this.rescheduleFormType === 'edit' ? new Date(this.rescheduleFormItem.datetime) : todayAtSix
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
                enrollment_id: this.rescheduleFormItem.id,
                enrollment_type: this.rescheduleFormItem.isPrivate ? 'private' : 'group',
                orderId: this.rescheduleFormItem.enrollment.order.id,
                selectedDate: newDateTime.format('YYYY-MM-DD'),
                timeFrom: newDateTime.format('HH:mm'),
                timeTo,
            }).then(res => {
                if(!res.data.status) {
                    this.snackMsg = res.data.err || (res.data.overbooked ? 'No more available lessons' : 'something went wrong')
                } else {
                    this.rescheduleForm = false
                    const enrollment = (this.rescheduleFormItem.isPrivate ? this.private_enroll : this.group_enroll)
                        .find(v => v.id === this.rescheduleFormItem.id)
                    if(!enrollment)
                        return
                    enrollment.date = newDateTime.format('YYYY-MM-DD')
                    enrollment.time_from = newDateTime.format('HH:mm')
                    enrollment.time_to = timeTo
                    this.openedSyncPopup = this.rescheduleFormItem.id
                    if(this.rescheduleFormType !== 'edit') {
                        // add reserved lessons
                        enrollment.order.reserved_lessons ++
                    }
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
        videoFormOpen(item) {
            if(item.students)
                this.videoFormMessage = `Hello,

Thanks for signing up for ${item.className}. We’ll be meeting on Zoom at this `
            else
                this.videoFormMessage = `Hi ${item.student.first_name},

Thanks for signing up for ${item.className}. We’ll be meeting on Zoom at this `
            this.videoFormData = item
            this.videoFormOpened = true
        },
        videoFormConfirm() {
            console.log('videoFormConfirm')
            this.isLoading = true
            axios.post(`/api/video_form_request/`, {
                url: this.videoFormUrl,
                message: this.videoFormMessage,
                data: this.videoFormData,
            }).catch(e => {

            }).then(res => {
                this.isLoading = false
                this.videoFormOpened = false
            })
        },
        openSendOffers(data) {
            this.sendOffersForm = true
            this.sendOffersItem = data
            if(!this.sendOffersMessage)
                this.sendOffersMessage = this.sendOffersMessageBlank
        },
        sendOffers() {
            this.isLoading = true
            axios.post(`/api/send_offers/`, {
                enrollment_id: this.sendOffersItem.id,
                is_private: this.sendOffersItem.isPrivate,
                message: this.sendOffersMessage,
            }).catch(e => {
                //this.snackMsg = 'Error sending offers'
            }).then(res => {
                if(!res.data.status) {
                    this.snackMsg = res.data.err;
                    return;
                }
                this.sendOffersForm = false
                this.sendOffersMessage = ''
                this.isLoading = false
                this.snackMsg = 'Offers sent! Your student/s will receive an email inviting them to keeping learning, and a link to your packages with one click ordering'
            })
        },
    },

    watch: {
        filterClasses(val, old) {
            if(this.pagination.descending && this.pagination.sortBy === 'datetime' && val === 'upcoming') {
                this.pagination.descending = false
            }
            if(!this.pagination.descending && this.pagination.sortBy === 'datetime' && val === 'previous') {
                this.pagination.descending = true
            }
        }
    }
}
</script>
<style lang="scss">

</style>