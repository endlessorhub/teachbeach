<template>
    <v-layout align-center justify-center row wrap class="dashboard-teacher-classes">
        <v-flex xs12 md10>Welcome {{first_name}}!</v-flex>
        <v-flex xs12 md10 v-if="notification">
            <v-alert
              ref="notificationAlert"
              :value="true"
              :color="notification.color"
              icon="new_releases"
              class="notification"
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
        <Notifications
            :classes="classes"
            :private_enroll="private_enroll"
            :new_orders="new_orders"
            :bank_message="bankMessage"
            @removeNewOrder="removeNewOrder"
          >
            <template v-slot:empty >

            </template>
        </Notifications>
        <v-flex xs12 md10 text-xs-left>
            <v-btn to="/teachers/start/">+Class</v-btn>
            <v-btn to="/dashboard/teach/membership">+Membership</v-btn>
        </v-flex>
        <v-flex xs12 text-xs-center v-if="isLoading">
            <v-progress-circular
              indeterminate
              color="grey"
            ></v-progress-circular>
        </v-flex>
        <v-flex xs12 md10 v-else-if="classList && classList.length">

            <template v-for="(item, index) in pageClassList">
                <ClassListItem v-bind="item" :key="item.id" @copy="copyClass(item.id)"></ClassListItem>
                <v-divider
                    v-if="index + 1 < classList.length"
                ></v-divider>
            </template>

            <v-pagination
                v-if="classList.length > paginationPerPage"
                v-model="paginationPage"
                :length="paginationLength"
            ></v-pagination>

            <v-dialog
              v-model="sendMessageForm"
              max-width="490"
            >
              <v-card>
                <v-card-title class="headline">
                    Message to all class students
                  <v-spacer></v-spacer>
                  <v-btn icon @click.native="sendMessageForm = false" color="gray darken-1">
                    <v-icon>close</v-icon>
                  </v-btn>
                </v-card-title>

                <v-card-text>
                    <h3>{{sendMessageFormTitle}}</h3>
                    <v-checkbox
                        v-model="sendMessageFormCopyMe"
                        label="Send me a copy"
                    ></v-checkbox>
                  <v-textarea
                      v-if="!isMessageSent"
                      v-model.trim="classMessage"
                      label="Message"
                      :error-messages="classMessageErrors"
                      required
                      auto-grow
                      box
                      rows="10"
                      @input="$v.classMessage.$touch()"
                      @blur="$v.classMessage.$touch()"
                  ></v-textarea>
                    <v-alert
                      type="success"
                      transition="scale-transition"
                      :value="isMessageSent">
                        Message was sent
                    </v-alert>
                </v-card-text>

                <v-card-actions>
                  <v-btn
                    flat="flat"
                    @click="sendMessageForm = false"
                  >
                    {{isMessageSent ? `Close` : `Decide later`}}
                  </v-btn>
                  <v-spacer></v-spacer>

                  <v-btn
                    v-if="!isMessageSent"
                    :loading="isMessageLoading"
                    :disabled="isMessageLoading"
                    class="platform-green"
                    flat="flat"
                    @click="sendMessageToClassStudents()"
                  >
                    Submit
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
        </v-flex>

        <v-flex v-if="classList && classList.length" xs12 md10 text-xs-left>
            <v-btn to="/teachers/start/">+Class</v-btn>
        </v-flex>

        <v-dialog
          v-model="deleteClassForm"
          max-width="390"
        >
          <v-card>
            <v-card-title class="headline">
                Delete Class
              <v-spacer></v-spacer>
              <v-btn icon @click.native="deleteClassForm = false" color="gray darken-1">
                <v-icon>close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text>
              Delete {{deleteClassName}}?
            </v-card-text>

            <v-card-actions>
              <v-btn
                flat="flat"
                @click="deleteClassForm = false"
              >
                No
              </v-btn>
              <v-spacer></v-spacer>

              <v-btn
                :loading="isLoading"
                :disabled="isLoading"
                color="primary"
                @click="deleteClass(deleteClassId)"
              >
                Yes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog
          v-model="boostForm"
          max-width="390"
        >
          <v-card>
            <v-card-title class="headline">
                {{boostClassesNum || isBoostFormSent ? 'Launch Class' : 'Whoops, out of credits!' }}
              <v-spacer></v-spacer>
              <v-btn icon @click.native="boostForm = false" color="gray darken-1">
                <v-icon>close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text v-if="boostClassesNum || isBoostFormSent">
                <div class="title text-xs-left">{{boostFormTitle}}</div>
                <div class="text-xs-left">Your listing is already
                    submitted to 900 community calendars</div>
                <div v-if="boostClass && boostClass.is_private && !isBoostFormSent">
                    <div class="subheading text-xs-left" v-if="!isBoostFormSent">First, select your best day to teach. This day will be posted to the community event listing calendars.</div>
                    <v-btn-toggle v-model="boostFormPrivateWeekday" :disabled="isBoostFormSent">
                      <v-btn :value="item.weekday" v-for="item in boostClass.weekdays_schedule" :key="item.weekday">
                        {{weekdayName(item.weekday)}}
                      </v-btn>
                    </v-btn-toggle>
                </div>
                <v-alert
                  icon="fas fa-rocket"
                  color="platform-green"
                  transition="scale-transition"
                  :value="isBoostFormSent">
                    <span style="font-size: 22px;">All set

                    </span>
                </v-alert>
            </v-card-text>
            <v-card-text v-else>
                Upgrade your plan to earn more.
            </v-card-text>

            <v-card-actions v-if="boostClassesNum || isBoostFormSent">
              <v-btn
                flat="flat"
                @click="boostForm = false"
              >
                {{isBoostFormSent ? `Close` : `No`}}
              </v-btn>
              <v-spacer></v-spacer>

              <v-btn
                v-if="!isBoostFormSent"
                :loading="isBoostFormLoading"
                :disabled="isBoostFormConfirmDisabled"
                color="primary"
                @click="sendBoostForm()"
              >
                Yes
              </v-btn>
            </v-card-actions>
            <v-card-actions v-else>
              <v-spacer></v-spacer>

              <v-btn
                color="primary"
                to="/join_as_member"
              >
                See options
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <AddStudentDialog
            v-model="addStudentForm"
            :item="addStudentFormItem"
            :students="allStudents"
        />

        <v-dialog v-model="enrollStudentsFormGroup" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Class sign in</span>
              </v-card-title>

              <v-card-text>
                  <v-menu
                    v-model="enrollStudentsFormMenu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on }">
                        <v-btn v-on="on">{{enrollStudentsFormDateBtnTitle}}</v-btn>
                    </template>
                    <v-date-picker
                        v-model="enrollStudentsFormDate"
                        @input="enrollStudentsFormMenu=false"
                        :allowed-dates="isDateAvailable"
                        :picker-date.sync="enrollStudentsFormCalendarDate"
                    ></v-date-picker>
                  </v-menu>
                  <v-list class="full-height-list">
                    <template v-for="(item, index) in enrollStudentsFormItems">
                      <v-list-tile
                        :key="item.key"
                        avatar
                      >
                          <v-list-tile-avatar tile>
                            <v-tooltip top content-class="teachbeach-tooltip">
                              <template v-slot:activator="{ on }">
                                  <v-chip small v-on="on" :color="item.chipColor" :dark="!!item.chipColor">
                                     {{item.reserved_lessons}}/{{item.num_lessons}}
                                  </v-chip>
                              </template>
                                <span>
                                    {{item.num_lessons-item.reserved_lessons}} of {{item.num_lessons}} credit{{item.num_lessons === 1 ? '' : 's'}} left
                                </span>
                            </v-tooltip>
                          </v-list-tile-avatar>
                        <v-list-tile-content>

                          <v-list-tile-title>
                            {{item.name}}
                          </v-list-tile-title>
                          <v-list-tile-sub-title >
                            <span v-if="item.plannedEnroll">
                                Enroll to: {{item.plannedEnroll}}
                                <ActionableOnClick
                                    :action="() => submitPlannedEnroll(item.order)"
                                    @success="reloadData"
                                    v-slot="{loading, click}"
                                >
                                    <v-btn color="platform-green" :loading="loading" @click="click">
                                      {{ 'Save' }}
                                    </v-btn>
                                </ActionableOnClick>
                                <v-btn icon @click="removePlannedEnroll(item.order)">
                                  <v-icon color="error">cancel</v-icon>
                                </v-btn>
                            </span>
                          </v-list-tile-sub-title>

                        </v-list-tile-content>
                        <v-list-tile-action>
                            <ActionableOnClick
                                v-if="enrollStudentsFormDate && item.isEnrollAvailable"
                                :action="() => submitEnrollStudentsFormGroup(item.order)"
                                v-slot="{loading, click, isDone, isFail}"
                            >
                                <v-btn color="platform-green" :loading="loading" @click="click" :disabled="isDone">
                                  {{ isDone ? 'Great!' : 'Sign in' }}
                                </v-btn>
                            </ActionableOnClick>
                        </v-list-tile-action>
                      </v-list-tile>
                      <v-divider
                          v-if="index + 1 < enrollStudentsFormItems.length"
                      ></v-divider>
                    </template>
                  </v-list>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="enrollStudentsFormGroup=false">Close</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="enrollStudentsFormPrivate" max-width="400px">
            <SignInStudent
                v-model="enrollStudentsFormValue"
                :classData="enrollStudentsFormClass"
                :studentsAvailable="enrollStudentsFormStudents"
                @change="submitEnrollStudentsForm"
            />
        </v-dialog>

    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import moment from 'moment'

import ClassListItemActions from './Components/ClassListItemActions'
import ActionableOnClick from '@/components/basic/ActionableOnClick'
import Snack from '@/components/basic/Snack'
import Hint from '@/components/basic/Hint'
import Reschedule from '@/components/basic/Reschedule'
import utils from '@/lib/utils.js'
import api from '@/lib/api'
import classHelper from '@/lib/helpers/Class'
import notifications from '@/lib/notifications.js'
import fbmap from '@/lib/fbmap';
import PrivateLessonCalendarImport from './Components/PrivateLessonCalendarImport'
import ClassOrderStudentEnroll from './Components/ClassOrderStudentEnroll'
import SignInStudent from '@/components/Dashboard/Components/SignInStudent'
import ClassListItem from './Components/ClassListItem'
import Notifications from './Components/Notifications'
import AddStudentDialog from './Components/AddStudentDialog'

import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
import { mapMutations } from 'vuex'

export default {
    name: 'dashboard_teach_classes',
    mixins: [validationMixin],
    data: () => ({
        isLoading: false,
        classes: [],
        orders: [],
        private_enroll: [],
        group_enroll: [],
        new_orders: [],
        deleteClassForm: false,
        deleteClassName: '',
        deleteClassId: '',
        openedCSVStartDate: false,
        csvStartDate: '',
        openedCSVEndDate: false,
        csvEndDate: '',
        bankMessage: '',
        sendMessageForm: false,
        sendMessageFormTitle: '',
        sendMessageFormId: null,
        sendMessageFormCopyMe: false,
        classMessage: '',
        isMessageSent: false,
        isMessageLoading: false,

        boostForm: false,
        boostFormTitle: '',
        boostFormId: null,
        boostFormPrivateWeekday: null,
        isBoostFormSent: false,
        isBoostFormLoading: false,
        boostFormLocalMedia: false,
        boostFormLocalMediaLeft: 0,
        boostFormWeeklyNewsletter: false,
        boostFormWeeklyNewsletterLeft: 0,
        boostClassesNum: 0,
        boostClass: null,

        addStudentForm: false,
        addStudentFormItem: {},

        loadingActivations: {},

        helpHintVisible: true,
        helpHintExpanded: false,
        helpHintBgcolor: '#eee',

        privateEnrollsConfirmed: {},

        enrollStudentsFormPrivate: false,
        enrollStudentsFormGroup: false,
        enrollStudentsFormClass: null,
        enrollStudentsFormDate: '',
        enrollStudentsFormMenu: false,
        enrollStudentsFormCalendarDateValue: undefined,
        //enrollStudentsFormDateMenu: false,

        enrollStudentsFormValue: {
            student: null,
            date: null,
            step: 1,
        },
        enrollStudentsFormDates: [],
        enrollStudentsFormStudents: [],

        pendingCardNotice: false,

        paginationPage: 1,
        paginationPerPage: 10,
    }),
    props: [],
    validations: {
        classMessage: { required },
    },
    components: {
        Reschedule,
        Snack,
        Hint,
        PrivateLessonCalendarImport,
        ClassListItemActions,
        ClassOrderStudentEnroll,
        ActionableOnClick,
        SignInStudent,
        ClassListItem,
        Notifications,
        AddStudentDialog,
    },
    created() {
        this.reloadData().then(() => api.getUserSettings()).then(settings => {
            this.helpHintExpanded = !settings.collapsedHints || !settings.collapsedHints.dashboardTeacherClasses
        })
    },
    computed: {
        paginationLength() {
            return Math.ceil(this.classList.length / this.paginationPerPage);
        },
        pageClassList() {
            return this.classList.slice((this.paginationPage - 1) * this.paginationPerPage, Math.min(this.paginationPage * this.paginationPerPage, this.classList.length))
        },
        allStudents() {
            return this.orders.map(v => v.student).filter((v, i, arr) => arr.findIndex(v2 => v2.email === v.email) === i)
        },
        isBoostFormConfirmDisabled() {
            return this.isBoostFormLoading || (this.boostClass && this.boostClass.is_private && typeof this.boostFormPrivateWeekday !== 'number')
        },
        notification() {
            if(this.$route.params.notification && notifications[this.$route.params.notification])
                return notifications[this.$route.params.notification]()
        },
        classMessageErrors() {
            const errors = []
            if (!this.$v.classMessage.$dirty) return errors
            !this.$v.classMessage.required && errors.push('Message is required.')
            return errors
        },

        first_name() {
            //console.log(this.$store.state)
            return this.$store.state.user.first_name
        },
        orderEnrollments() {
            return [
                ...this.group_enroll,
                ...this.private_enroll,
            ].filter(en => en.status !== 'rejected').reduce((acc, en) => {
                if(!acc[en.order.id])
                    acc[en.order.id] = []
                acc[en.order.id].push(en)
                return acc
            }, {})
        },
        activeOrders() {
            return this.orders.filter(o => {
                // active subscribe are included
                if(o.status === 'active')
                    return true
                // cancelled subscribe or refunded are excluded
                if(o.status === 'refund' || o.status === 'canceled')
                    return false
                // after 2 conditions above subscriptions are completely processed
                // include orders which not have full enrollments
                if(!this.orderEnrollments[o.id] || o.num_lessons > this.orderEnrollments[o.id].length)
                    return true
                // include if any of the enrollments is in the future
                return this.orderEnrollments[o.id].some(en => new Date() < moment(`${en.date} ${en.time_from}`).toDate())
            })
        },
        pastOrders() {
            return this.orders.filter(o => {
                // active subscribe are excluded
                if(o.status === 'active')
                    return false
                // cancelled subscribe included
                if(o.status === 'canceled' && o.is_subscription)
                    return true
                // after 2 conditions above subscriptions are completely processed
                // exclude orders which not have full enrollments
                if(!this.orderEnrollments[o.id] || o.num_lessons > this.orderEnrollments[o.id].length)
                    return false
                // exclude if any of the enrollments is in the future
                return !this.orderEnrollments[o.id].some(en => {
                    const current = new Date()
                    const lesson = moment(`${en.date} ${en.time_from}`).toDate()
                    // if lesson in the future
                    return current < lesson
                })
            })
        },
        classList() {
            const orderDict = this.orders.reduce((acc, o) => {
                if(!acc[o.klass])
                    acc[o.klass] = []
                acc[o.klass].push(o)
                return acc
            }, {})
            let checkExpired = classHelper.checkExpired

            return _.sortBy(_.map(this.classes, v => {
                const students = [
                    ...this.activeOrders.map(o => ({isActive: true, ...o})),
                    ...this.pastOrders.map(o => ({isActive: false, ...o})),
                ].filter(o => o.klass === v.pk)
                    .map(v => ({order_id: v.id, isActive: v.isActive, ...v.student}));
                const isBoosted = v.is_boosted
                const isExpired = checkExpired(v)
                return {
                    key: v.pk,
                    id: v.pk,
                    totalAmount: v.total_amount || 0,
                    type: v.is_private ? 'Private' : 'Group',
                    chipColor: v.is_private ? 'indigo' : 'primary',
                    avatar: v.master_media,
                    name: `${v.is_private ? v.private_className : v.name}`,
                    title: `${v.is_private ? v.private_className : v.name} ${v.teacher.user.is_company ? v.teacher.first_name+' '+v.teacher.last_name : ''}`,
                    description: v.groupClassSummary || '',
                    editEnabled: !isExpired,
                    deleteEnabled: !v.num_enrolled || isExpired,
                    isPrivate: v.is_private,
                    isExpired: isExpired,
                    isDeactivated: v.is_deactivated,
                    isBoostAvailable: !isBoosted,
                    isBoosted: isBoosted,
                    isEmailAvailable: !v.is_email_boosted,
                    isEmailBoosted: v.is_email_boosted,
                    isLoadidngActivation: this.loadingActivations[v.pk],
                    isEnrollStudentsAvailable: !isExpired
                        && !v.is_deactivated
                        //&& !v.is_private
                        && orderDict[v.pk]
                        && orderDict[v.pk].some(o => o.reserved_lessons < o.num_lessons),
                    processActivation: this.processActivation,
                    showAddStudentForm: this.showAddStudentForm,
                    showEnrollStudentsForm: this.showEnrollStudentsForm,
                    openSendMessageForm: this.openSendMessageForm,
                    deleteClass: this.deleteClass,
                    openBoostForm: this.openBoostForm,
                    openEmailBoostForm: this.openEmailBoostForm,
                    students,
                }
            }), v => (-v.id * (v.isDeactivated || v.isExpired ? 1 : 1000000)))
        },
        enrollStudentsFormItems() {
            if(!this.enrollStudentsFormClass)
                return []
            return this.orders.filter(v => v.klass === this.enrollStudentsFormClass.pk).map(o => ({
                id: o.id,
                key: o.id,
                name: `${o.student.first_name} ${o.student.last_name}`,
                num_lessons: o.num_lessons,
                reserved_lessons: o.reserved_lessons,
                order: o,
                class: this.enrollStudentsFormClass,
                plannedEnroll: o.plannedEnroll,
                isEnrollAvailable: o.reserved_lessons < o.num_lessons,
                chipColor: o.reserved_lessons === o.num_lessons ? 'success' : '',
            }))
        },
        availableDates() {
            //console.log(this.enrollStudentsFormClass)
            if(!this.enrollStudentsFormClass)
                return []
            if(this.enrollStudentsFormClass.is_private) {
                // should know order to calc dates available
                return []
            }
            return classHelper.getAvailableSchedule(this.enrollStudentsFormClass, 100)

        },
        enrollStudentsFormDateBtnTitle() {
            return this.enrollStudentsFormDate
                ? moment(this.enrollStudentsFormDate).toDate().toLocaleString('en-us', {day: 'numeric', month: 'long'})
                : 'Select Date'
        },
        enrollStudentsFormCalendarDate: {
            set(v) {
                this.enrollStudentsFormCalendarDateValue = v
            },
            get() {
                if(this.enrollStudentsFormCalendarDateValue) {
                    return
                }
                if (this.availableDates && Object.keys(this.availableDates).length) {
                    return Object.keys(this.availableDates)
                        .filter(d => this.availableDates[d].some(slot => slot.isAvailable))
                        .sort((a, b) => {
                            return moment(a) - moment(b)
                        })[0]
                }
                return undefined
            }
        }
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        removeNewOrder(id) {
            console.log(id)
            axios.post(`/api/orders/${id}/`, {data: {isRemovedNotification: true}}).then(res => {
                if(res.data.status) {
                    this.new_orders = this.new_orders.filter(no => no.id !== id)
                }
            })
        },
        isDateAvailable(date) {
            //console.log(date, this.availableDates)
            return this.availableDates && this.availableDates[date] && this.availableDates[date].length
        },
        removePrivateEnroll(id) {
            this.private_enroll = this.private_enroll.filter(pe => pe.id !== id)
        },
        showAddStudentForm(classData) {
            const classFull = this.classes.find(c => c.pk === classData.id)
            this.addStudentFormItem = {...classData, ...classFull}
            //this.updateAddStudentMessageUrl()
            this.addStudentForm = true
        },

        editClass(id) {
            console.log('editClass', id)
        },
        reloadData() {
            this.isLoading = true
            return axios.get('/api/teacher_classes/').then(res => {
                //console.log(res)
                this.isLoading = false
                this.classes = res.data.classes
                this.private_enroll = res.data.private_enroll
                this.group_enroll = res.data.group_enroll
                this.new_orders = res.data.new_orders
                this.orders = res.data.orders
                this.bankMessage = res.data.bank_message
                this.boostClassesNum = res.data.boost_classes_num
                // for quick test
                //this.privateEnrollsConfirmed[148] = res.data.private_enroll.find(v => v.id === 148)
                return axios.get('/api/payment_cards/')
            }).then(res => {
                this.pendingCardNotice = res.data.default && this.classes.some(c => c.is_deactivated)
            })
        },
        deleteClass(id) {
            if(this.deleteClassForm && this.deleteClassId) {
                this.isLoading = true
                axios.delete(`/api/classes/${id}/`).then(res => {
                    // this.reloadData()
                    this.classes = this.classes.filter(c => c.pk !== id);
                }).catch(e => {
                    this.isLoading = false
                    this.deleteClassForm = false
                }).then(() => {
                    this.isLoading = false
                    this.deleteClassForm = false
                })
            } else {
                this.deleteClassId = id
                this.deleteClassForm = true
                this.deleteClassName = _.find(this.classList, {id: id}).title.replace(/\(\d+\)/, '')
            }
        },
        processActivation(id, data) {
            if(!data.success && data.error_message) {
                // hide snack for now, just redirect to checkout (add card page)
                this.setGlobalError(data.error_message)
                return this.$router.push(`/teacher_check/${id}?n=tc`)
            }
            const i = this.classes.findIndex(c => c.pk === id)
            const is_deactivated = data.is_deactivated
            if(i !== -1) {
                this.$set(this.classes, i, {...this.classes[i], is_deactivated})
            }
        },
        pauseClass(id) {
            this.$set(this.loadingActivations, id, true)
            axios.post(`/api/deactivate_class/`, {
                id,
                deactivate: true,
            }).then(res => {
                this.processActivation(id, res.data)
            }).catch((e) => console.log(e)).finally(() => {
                this.$set(this.loadingActivations, id, false)
            })
        },
        resumeClass(id) {
            this.$set(this.loadingActivations, id, true)
            axios.post(`/api/deactivate_class/`, {
                id,
                deactivate: false,
            }).then(res => {
                this.processActivation(id, res.data)
            }).catch((e) => console.log(e)).finally(() => {
                this.$set(this.loadingActivations, id, false)
            })
        },
        downloadCSVReport() {
            axios.get(`/api/csv_export/`, {
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
        sendMessageToClassStudents() {
            this.$v.$touch()
            //console.log('submit', this, arguments)
            if (this.$v.classMessage.$anyError)
                return
            this.isMessageLoading = true
            axios.post(`/api/teacher_class/${this.sendMessageFormId}/message/`, {
                message: this.classMessage,
                copyMe: this.sendMessageFormCopyMe,
            }).then(res => {
                this.isMessageLoading = false
                this.isMessageSent = true
                this.classMessage = ''
            })
        },
        openSendMessageForm(id) {
            this.sendMessageFormId = id
            this.sendMessageForm = true
            this.sendMessageFormTitle = _.find(this.classList, {id}).title
        },
        openBoostForm(id) {
            const classToBoost = this.classes.find(v => v.pk === id)
            if(classToBoost.is_boosted) {
                this.boostFormId = id
                this.boostFormTitle = classHelper.title(classToBoost)
                this.boostClass = classToBoost
                this.isBoostFormSent = true
                this.boostFormPrivateWeekday = null
                this.boostForm = true
            } else {
                this.$router.push(`/calendar_upsell/${id}`)
            }

        },
        openEmailBoostForm(id) {
            this.$router.push(`/email_upsell/${id}`)
        },
        sendBoostForm() {
            this.isBoostLoading = true
            axios.post(`/api/boost_class/${this.boostFormId}/`, {
                weekday: this.boostFormPrivateWeekday,
            }).then(res => {
                if(res.data.status) {
                    this.isBoostLoading = false
                    this.isBoostFormSent = true
                    this.reloadData()
                } else if(res.data.limit_reached) {
                    this.boostClassesNum = 0
                } else {
                    this.isBoostLoading = false
                    console.warn(res.data)
                }
            })
        },
        notificationAction(action) {
            console.log(action)
            if(action.id === 'collectMoney')
                this.$router.push("/dashboard/teach/account_take")
        },
        weekdayName(index) {
            return utils.getWeekday(index)
        },
        helpHintExpand(isExpand) {
            console.log('check')
            if(isExpand) {
                this.helpHintExpanded = true
                this.helpHintBgcolor = 'white'
            } else {
                this.helpHintExpanded = false
                this.helpHintBgcolor = '#eee'
                api.updateUserSettings({collapsedHints: {dashboardTeacherClasses: true}})
                    .catch(e => console.log(e))
            }
        },
        showEnrollStudentsForm(item) {
            //console.log('students list')
            this.enrollStudentsFormCalendarDateValue = undefined
            this.enrollStudentsFormClass = this.classes.find(c => c.pk === item.id)

            this.enrollStudentsFormStudents = this.orders.filter(v => v.klass === this.enrollStudentsFormClass.pk).map(o => ({
                id: o.id,
                first_name: o.student.first_name,
                last_name: o.student.last_name,
                num_lessons: o.num_lessons,
                reserved_lessons: o.reserved_lessons,
                order: o,
            }))

            this.enrollStudentsFormValue = {
                step: 1,
                student: null,
                date: null,
                time: null,
            }
            this.enrollStudentsFormDate = null
            if(this.enrollStudentsFormClass.is_private)
                this.enrollStudentsFormPrivate = true
            else
                this.enrollStudentsFormGroup = true
        },
        submitEnrollStudentsFormGroup(order) {
            const timeslot = this.classes.find(c => c.pk === order.klass).schedule_dates.find(d => d.date === this.enrollStudentsFormDate)
            return this.submitEnrollStudent({
                date: this.enrollStudentsFormDate,
                time: timeslot.start,
                student: order,
            })
        },
        submitEnrollStudentsForm(v) {
            return this.submitEnrollStudent(v)
                .then(() => {
                    this.enrollStudentsFormPrivate = false
                    this.enrollStudentsFormGroup = false
                })
                .catch(e => {
                    this.setGlobalError(e)
                })
        },
        submitEnrollStudent(v) {
            //console.log(v)
            if(!v.date || !v.time || !v.student)
                return
            const index = this.orders.findIndex(o => o.id === v.student.id)
            const o = this.orders[index]
            return axios.post(`/api/teacher_sign_student`, {
                order_id: v.student.id,
                date: v.date,
                time: v.time,
            }).then(res => {
                if(!res.data.success) {
                    // show error
                    return Promise.reject(res.data.message)
                }
                const cIndex = this.classes.findIndex(c => o.klass === c.pk)
                o.reserved_lessons ++
                this.$set(this.orders, index, o)
                this.classes[cIndex].num_enrolled++
                this.classes[cIndex].enrolled.push({order_id: res.data.enr.order, ...res.data.enr})
                this.$set(this.classes, cIndex, this.classes[cIndex])
            })
        },
        enrollStudentsFormSelected({date, order}) {
            //console.log(date, order)
            const index = this.orders.findIndex(o => o.id === order.id)
            const o = this.orders[index]
            o.plannedEnroll = date
            this.$set(this.orders, index, o)
        },
        submitPlannedEnroll(order) {
            const o = this.orders.find(v => v.id === order.id)
            if(!o)
                return Promise.reject('order not found')
            return axios.post(`/api/teacher_sign_student`, {
                order_id: order.id,
                date: o.plannedEnroll,
            }).then(res => {
                o.plannedEnroll = null
                o.reserved_lessons ++
                const index = this.orders.findIndex(o => o.id === order.id)
                this.$set(this.orders, index, o)
            })
        },
        removePlannedEnroll(order) {
            const index = this.orders.findIndex(o => o.id === order.id)
            const o = this.orders[index]
            o.plannedEnroll = null
            this.$set(this.orders, index, o)
        },
        updateAddStudentMessageUrl() {
            this.addStudentFormMessage = this.addStudentFormMessage.replaceAll(/\/3\/\?name=([^&]+|)&phone=([^&]+|)&email=(\S+|)/g, () => {
                return `/3/?name=${encodeURIComponent(this.addStudentFormName)}&phone=${encodeURIComponent(this.addStudentFormPhone)}&email=${encodeURIComponent(this.addStudentFormEmail)}`
            })
        },
        async copyClass(id) {
            const cl = (await axios.get(`/api/classes/${id}/`)).data;
            delete cl.enrolled;
            delete cl.id;
            delete cl.logged_in_user_orders;
            delete cl.orders;
            delete cl.schedule_dates;
            delete cl.schedule_excluded;
            delete cl.schedule_from;
            delete cl.schedule_to;
            delete cl.start_date;
            delete cl.until_date;
            delete cl.weekdays_schedule;
            await axios.post('/api/draft/', {
                class_data: {
                    teacherGroupClass: fbmap.bf.teachingClass(cl),
                    teacherLessonType: cl.is_private ? 'private' : 'group',
                    categoriesSelected: cl.subcategories,
                }
            });
            this.$router.push('/teachers/start');
        },
        tmpMet() {
            this.$refs.dateMenu.value=false
        },

    },

    watch: {
        sendMessageForm(val) {
            if(!val) {
                this.sendMessageFormId = null;
                this.sendMessageFormTitle = '';
                this.isMessageSent = false;
                this.sendMessageFormCopyMe = false;
            }
        },
        boostForm(val) {
            if(!val) {
                this.isBoostFormSent = false
            }
        },
        addStudentFormName(v) {
            // do it on backend
            //this.updateAddStudentMessageUrl()
        },
        addStudentFormEmail(v) {
            // do it on backend
            //this.updateAddStudentMessageUrl()
        },
        addStudentFormPhone(v) {
            // do it on backend
            //this.updateAddStudentMessageUrl()
        },
    }
}
</script>
<style lang="scss">
    .dashboard-teacher-classes {
        .paused-chip > span {
            cursor: pointer;
        }
    }

</style>
<style lang="scss" scoped>
.no-notifications {
    min-height: 60px;
    width: 100%;
}
.notification {
    font-size: 22px;
}
.classes-hint {
    cursor: pointer;
}
.scale-collapse-enter-active {
    transition: all .15s ease;
    max-height: 300px;
    transform: scale(1);
    opacity: 1;
}
.scale-collapse-leave-active {
    transition: all .15s ease;
    max-height: 300px;
    transform: scale(1);
    opacity: 1;
}
.scale-collapse-enter, .scale-collapse-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
    max-height: 0;
    transform: scale(0);
    opacity: 0;
}
</style>
