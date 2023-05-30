<template>
<v-flex xs12 md10>
    <template v-if="notifications && notifications.length">
    <v-dialog v-model="rescheduleForm" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="headline">Reschedule</span>
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
            <v-btn color="primary" @click="rescheduleFormConfirm">Send</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog
      v-model="declineSubmitForm"
      max-width="390"
    >
      <v-card>
        <v-card-title class="headline">
            Add a reason
          <v-spacer></v-spacer>
          <v-btn icon @click.native="declineSubmitForm = false" color="gray darken-1">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-text-field
              v-model.trim="declineReason"
              label="Decline reason"
              :error-messages="declineReasonErrors"
              required
              @input="$v.declineReason.$touch()"
              @blur="$v.declineReason.$touch()"
          ></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-btn
            flat="flat"
            @click="declineSubmitForm = false"
          >
            Decide later
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn
            :loading="isLoading"
            :disabled="isLoading"
            class="platform-green"
            flat="flat"
            @click="submitDecline"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="newOrderMessageForm"
      max-width="390"
    >
      <v-card>
        <v-card-title class="headline">
            Schedule a time to meet
          <v-spacer></v-spacer>
          <v-btn icon @click.native="newOrderMessageForm = false" color="gray darken-1">
            <v-icon>close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
            <a :href="`tel:${newOrderMessagePhone}`">{{newOrderMessagePhone}}</a>,
            <a :href="`mailto:${newOrderMessageEmail}`">{{newOrderMessageEmail}}</a>
            <v-textarea
                v-model="newOrderMessageMessage"
                auto-grow
                box
                label="Message"
                rows="2"
            ></v-textarea>
        </v-card-text>

        <v-card-actions>
          <v-btn
            flat="flat"
            @click="newOrderMessageForm = false"
          >
            Later
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn
            :loading="isLoading"
            :disabled="isLoading"
            class="platform-green"
            flat="flat"
            @click="submitNewOrderMessage"
          >
            Send
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="confirmEnrollForm"
      max-width="390"
    >
      <v-card>
        <v-card-title class="headline">
            {{confirmEnrollTitle}}
        </v-card-title>

        <v-card-text>
            <v-textarea
                v-model="confirmEnrollMessage"
                auto-grow
                box
                label="Send message or other instructions"
                rows="2"
            ></v-textarea>
        </v-card-text>

        <v-card-actions>
          <v-btn
            flat="flat"
            @click="confirmEnrollForm = false"
          >
            Cancel
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn
            :loading="confirmEnrollLoading"
            :disabled="confirmEnrollLoading"
            class="platform-green"
            flat="flat"
            @click="confirmEnrollSend"
          >
            Send
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
                      <v-list-tile-title v-if="item.isCreditNotice">
                          {{item.creditAmount}} credit{{item.creditAmount > 1 ? 's' : ''}} to launch classes in 42 local online event listings. Click <v-icon color="platform-green">fas fa-rocket</v-icon> below to launch.
                      </v-list-tile-title>
                      <v-list-tile-title v-else-if="item.isNewOrder">
                          {{item.text}} <a @click="openNewOrderMessage(item)">here</a>.
                      </v-list-tile-title>
                      <v-list-tile-title v-else v-html="item.title">
                          <v-icon v-if="item.iconAfter">{{item.iconAfter}}</v-icon>
                      </v-list-tile-title>
                    </v-list-tile-content>
                    <v-list-tile-action style="min-width: 90px;">
                      <router-link v-if="item.type === 'linkAfter'" :to="item.linkUrl">{{ item.linkName }}</router-link>
                        <template  v-else-if="item.customActions && item.customActions.length">
                            <v-btn @click="notificationAction(action)" v-for="action in item.customActions" :key="action.id">{{action.title}}</v-btn>
                        </template>
                        <PrivateLessonCalendarImport
                                v-else-if="item.isRegular && item.confirmedEnroll"
                                :isPopupOpened="true"
                                :privateClass="item.class"
                                :enrollment="item.confirmedEnroll"
                                @downloaded="removePrivateEnroll(item.id)"
                        />
                        <v-menu v-else-if="item.isRegular" offset-y>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              v-on="on"
                            >
                              Respond
                            </v-btn>
                          </template>
                          <v-list>
                            <v-list-tile
                              v-if="item.isConfirmable"
                              @click="confirmEnroll(item.id)"
                            >
                                <v-list-tile-title>Confirm</v-list-tile-title>
                            </v-list-tile>
                            <v-list-tile
                              @click="rejectEnroll(item.id)"
                            >
                              <v-list-tile-title>Decline</v-list-tile-title>
                            </v-list-tile>
                            <v-list-tile
                              @click="editEnroll(item.id)"
                            >
                              <v-list-tile-title>Reschedule</v-list-tile-title>
                            </v-list-tile>
                          </v-list>
                        </v-menu>
                        <v-btn v-else="item.isNewOrder" flat icon @click="$emit('removeNewOrder', item.id);">
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
    </template>
    <slot v-else name="empty">

    </slot>


</v-flex>
</template>
<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import moment from 'moment'

import Reschedule from '@/components/basic/Reschedule'
import utils from '@/lib/utils.js'
import classHelpers from '@/lib/helpers/Class.js'
import PrivateLessonCalendarImport from './PrivateLessonCalendarImport'


import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
import { mapMutations } from 'vuex'

export default {
    name: 'dashboard_teach_notifications',
    mixins: [validationMixin],
    data: () => ({
        isLoading: false,
        declineSubmitForm: false,
        declineReason: '',
        currentDeclineEnrollmentId: null,

        rescheduleForm: false,
        rescheduleFormItem: {},
        rescheduleFormDate: null,
        rescheduleFormDuration: 1,
        rescheduleFormNotice: '',

        confirmEnrollId: null,
        confirmEnrollForm: false,
        confirmEnrollMessage: '',
        confirmEnrollLoading: false,
        confirmEnrollTitle: '',

        newOrderMessageItem: {},
        newOrderMessageForm: '',
        newOrderMessageMessage: '',
        newOrderMessageMail: '',
        newOrderMessagePhone: '',

        privateEnrollsConfirmed: {},
        removedPrivateEnrolls: {},
        removedNewOrders: {},
    }),
    props: {
        classes: {
            type: Array,
            default: [],
        },
        private_enroll: {
            type: Array,
            default: [],
        },
        new_orders: {
            type: Array,
            default: [],
        },
        bank_message: {
            type: String,
            default: '',
        },
    },
    validations: {
        declineReason: { required },
    },
    components: {
        Reschedule,
        PrivateLessonCalendarImport,
    },
    created() {
        console.log(this.private_enroll)
    },
    computed: {

        declineReasonErrors() {
            const errors = []
            if (!this.$v.declineReason.$dirty) return errors
            !this.$v.declineReason.required && errors.push('Reason is required.')
            return errors
        },
        notifications() {
            const classDict = _.keyBy(this.classes, 'pk')
            const res = this.private_enroll
                .filter(v => (v.status === 'requested' && !this.removedPrivateEnrolls[v.id] && !classHelpers.checkExpired(classDict[v.class_id])))
                .map(v => ({
                    key: v.id,
                    id: v.id,
                    isRegular: true,
                    isConfirmable: moment(`${v.date} ${v.time_from}`).toDate() > new Date(),
                    confirmedEnroll: this.privateEnrollsConfirmed[v.id],
                    class: classDict[v.class_id],
                    avatar: v.student.media,
                    title: `${v.student.first_name} (<a href="mailto:${v.student.email}">${v.student.email}</a>,
<a href="tel:${v.student.phone}">${v.student.phone}</a>) has requested "${classDict[v.class_id].name}"
${utils.time24HtoAMPM(v.time_from)} - ${utils.time24HtoAMPM(v.time_to)} ${classDict[v.class_id].timezone}
on ${utils.stringToDate(v.date).toLocaleString('en-us', {month: 'long', day: 'numeric', weekday: 'long'})}`,
            }))
            if(this.bank_message) {
                res.unshift({
                    key: 'bm',
                    id: 'bm',
                    avatar: null,
                    title: this.bank_message,
                    customActions: [
                        {
                            id: 'collectMoney',
                            title: 'Collect',
                            icon: 'monetization'
                        }
                    ]
                })
            }

            if(this.new_orders)
                _.each(this.new_orders, (o, i) => {
                    if(this.removedNewOrders[o.id] || classHelpers.checkExpired(classDict[o.klass]))
                        return
                    res.push({
                        key: `new_${o.id}`,
                        id: o.id,
                        isNewOrder: true,
                        text: `${o.student.first_name} ${o.student.last_name} has enrolled in "${o.class_name}" and is added to the CRM. Send a personal note`,
                        order: o,
                    })
                })
            this.classes.forEach(v => {
              if (v.class_type === 'online' && !v.zoom_link && !v.is_deactivated && !classHelpers.checkExpired(v)) {
                res.push({
                      key: `zoom_link_invalid_${v.pk}`,
                      id: v.id,
                      title: `Please add a zoom link for ${v.name}. Click on Edit class and go to "Where will the lessons be held"`,
                      type: 'linkAfter',
                      linkName: 'Edit',
                      linkUrl: `/teachers/class/${v.pk}`,
                  })
              }
            });
            return res
        },

    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        removePrivateEnroll(id) {
            this.removedPrivateEnrolls[id] = true
        },

        submitNewOrderMessage() {
            //console.log(this.newOrderMessageItem)
            axios.post(`/api/send_email_to_student/`, {
                order_id: this.newOrderMessageItem.id,
                message: this.newOrderMessageMessage,
            }).then(res => {
                if(!res.data.status) {
                    this.setGlobalError(res.data.err);
                    return new Error(res.data.err)
                }
                this.newOrderMessageForm = false
                this.removedNewOrders[this.newOrderMessageItem.id] = true
            }).catch(e => console.error(e)).then(() => {
                this.isLoading = false
            })
        },
        openNewOrderMessage(item) {
            //console.log(item)
            const cl = this.classes.find(c => c.pk === item.order.klass)
            const phone = cl.teacher.phone || cl.teacher.user.phone
            const email = cl.teacher.email || cl.teacher.user.email
            this.newOrderMessageItem = item
            this.newOrderMessagePhone = item.order.student.phone
            this.newOrderMessageEmail = item.order.student.email
            this.newOrderMessageMessage = `Hi ${item.order.student.first_name}, Thanks for enrolling in ${cl.name}, we are glad you can make it. Let me know if you have any questions.

Kindly,
${cl.teacher.first_name}
${phone}
${email}
`
            this.newOrderMessageForm = true
        },
        editEnroll(id) {
            this.rescheduleFormItem = _.find(this.private_enroll, {id: id})
            this.rescheduleFormItem.studentName = `${this.rescheduleFormItem.student.first_name} ${this.rescheduleFormItem.student.last_name}`
            this.rescheduleFormItem.phone = this.rescheduleFormItem.student.phone
            this.rescheduleFormItem.email = this.rescheduleFormItem.student.email
            this.rescheduleFormDate = moment(`${this.rescheduleFormItem.date} ${this.rescheduleFormItem.time_from}`, 'YYYY-MM-DD HH:mm').toDate()
            const durHours = this.rescheduleFormItem.time_to.split(':')[0] - this.rescheduleFormItem.time_from.split(':')[0]
            const durMinutes = this.rescheduleFormItem.time_to.split(':')[1] - this.rescheduleFormItem.time_from.split(':')[1]
            this.rescheduleFormDuration = 60*durHours+durMinutes
            this.rescheduleFormNotice = ''
            this.rescheduleForm = true
        },
        rescheduleFormConfirm() {
            //console.log(this.rescheduleFormItem, this.rescheduleFormDate, this.rescheduleFormNotice)
            axios.post('/api/teacher_reschedule', {
                notice: this.rescheduleFormNotice,
                datetime: moment(this.rescheduleFormDate).format('YYYY-MM-DD HH:mm'),
                enrollment_id: this.rescheduleFormItem.id,
                enrollment_type: 'private'
            }).then(res => {
                if(!res.data.status) {
                    this.setGlobalError(res.data.err)
                } else {
                    const {student, order} = this.private_enroll.find(pe => pe.id === this.rescheduleFormItem.id)
                    const enrollment = Object.assign({}, res.data.enrollment, {student, order})
                    this.rescheduleForm = false
                    this.$set(this.privateEnrollsConfirmed, this.rescheduleFormItem.id, enrollment)
                    //return this.reloadData()
                }
            })
        },
        confirmEnroll(id) {
            const enrollment = this.private_enroll.find(v => v.id === id)
            const date = moment(enrollment.date).toDate().toLocaleString('en-us', {weekday: 'long', month: 'short', day: 'numeric'})
            const timeStart = utils.time24HtoAMPM(enrollment.time_from)
            const timeEnd = utils.time24HtoAMPM(enrollment.time_to)
            this.confirmEnrollId = id
            this.confirmEnrollTitle = `Confirm ${timeStart} to ${timeEnd} on ${date}`
            this.confirmEnrollForm = true
        },
        confirmEnrollSend() {
            this.confirmEnrollLoading = true
            axios.post(`/api/private_enroll/${this.confirmEnrollId}/confirm/`, {
                message: this.confirmEnrollMessage,
            }).then(res => {
                this.$set(this.privateEnrollsConfirmed, this.confirmEnrollId, _.find(this.private_enroll, {id: this.confirmEnrollId}))
                this.confirmEnrollForm = false
                this.confirmEnrollMessage = ''
                this.confirmEnrollTitle = ''
                this.confirmEnrollId = null
                this.confirmEnrollLoading = false
            })
        },
        rejectEnroll(id) {
            this.currentDeclineEnrollmentId = id
            this.declineSubmitForm = true
            this.declineReason = ''
        },
        submitDecline() {
            this.$v.$touch()
            //console.log('submit', this, arguments)
            if (this.$v.declineReason.$anyError)
                return
            //this.isLoading = true
            axios.post(`/api/private_enroll/${this.currentDeclineEnrollmentId}/reject/`, {reason: this.declineReason}).then(res => {
                this.removePrivateEnroll(this.currentDeclineEnrollmentId)
                this.declineReason = ''
                this.currentDeclineEnrollmentId = null
                this.declineSubmitForm = false
            })
        },
        notificationAction(action) {
            console.log(action)
            if(action.id === 'collectMoney')
                this.$router.push("/dashboard/teach/account_take")
        },


    },

    watch: {

    }
}
</script>

<style lang="scss" scoped>

</style>
