<template>
    <v-card class="student-info__card">
        <div v-if="onclose" class="student-info__close-container">
            <v-spacer></v-spacer>
            <v-btn icon @click="onclose">
                  <v-icon>close</v-icon>
            </v-btn>
        </div>
        <v-card-title
          class="headline"
          primary-title
        >
            <div v-if="!isUpdatable" class="student-info__title">{{first_name}} {{last_name}}</div>
        </v-card-title>
        <v-card-text>
            <v-layout align-start justify-center row wrap class="student-info__fields-container">
                <v-flex v-if="isUpdatable" sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedFirstName"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">First name</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex v-if="isUpdatable" sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedLastName"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Last name</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedPhone"
                      :readonly="!isUpdatable"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Phone</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      :value="email"
                      readonly
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Email</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedSource"
                      :readonly="!isUpdatable"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Source</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex sm6 xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedNotes"
                      :readonly="!isUpdatable"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Notes</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <v-flex xs12 class="text-xs-center">
                    <v-text-field
                      label=""
                      v-model="updatedNotes2"
                      :readonly="!isUpdatable"
                      class="student-info_text_right"
                    >
                        <template v-slot:prepend-inner>
                            <b class="student-info__field-prefix">Notes2</b>
                        </template>
                    </v-text-field>
                </v-flex>
                <template v-for="(o) in currentOrders">
                    <v-flex xs4 class="text-xs-center" :key="`cc_${o.id}`">
                        <v-text-field
                          label="Current"
                          :value="o.name"
                          readonly
                        >
                        </v-text-field>
                    </v-flex>
                    <v-flex xs4 class="text-xs-center" :key="`cr_${o.id}`">
                        <v-text-field
                          label=""
                          :value="`${o.num_lessons-o.reserved_lessons}/${o.num_lessons} Credits Left`"
                          readonly
                          class="student-info_text_center"
                        >
                        </v-text-field>
                    </v-flex>
                    <v-flex xs4 class="text-xs-center" :key="`si_${o.id}`">
                        <v-btn class="platform-green" @click="signIn(o.id)">Sign in</v-btn>
                    </v-flex>
                </template>
                <v-flex xs12 class="text-xs-center">
                    <v-btn :disabled="!isUserChanged" class="platform-green student-info__btn-update" large @click="updateStudent">UPDATE DATA</v-btn>
                    <v-btn class="platform-green student-info__btn-invite" large @click="inviteToNewClass">INVITE TO A NEW CLASS</v-btn>
                </v-flex>
                <v-flex xs12 class="text-xs-center">
                    <v-textarea
                      name="student-info-textarea"
                      label="History"
                      outline
                      readonly
                      :value="historyText"
                    ></v-textarea>
                </v-flex>
            </v-layout>
            <v-dialog v-model="signInDialog" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Add another date</span>
              </v-card-title>
              <v-card-text>
                  <div class="text-xs-left">The customer will also receive a confirmation</div>
                  <v-window v-model="signInStep">
                  <v-window-item :value="1">
                      <v-date-picker
                        v-model="signInDate"
                        :allowedDates="isSignInAvailable"
                        no-title
                      ></v-date-picker>
                  </v-window-item>
                  <v-window-item :value="2">
                    <v-radio-group v-model="signInTime" class="full-width">
                        <v-list
                          two-line
                        >
                          <v-list-tile v-for="item in signInTimeSlots" :key="item.start" @click.prevent="item.isAvailable && (signInTime = item.start)">
                            <v-list-tile-action>
                              <v-radio
                                :value="item.start"
                                :disabled="!item.isAvailable"
                              ></v-radio>
                            </v-list-tile-action>

                            <v-list-tile-content>
                              <v-list-tile-title>{{item.title}}</v-list-tile-title>
                              <v-list-tile-sub-title></v-list-tile-sub-title>
                            </v-list-tile-content>
                          </v-list-tile>
                        </v-list>
                      </v-radio-group>
                  </v-window-item>
                </v-window>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        color="blue darken-1"
                        flat
                        @click="signInBack"
                >{{signInBackBtn}}</v-btn>
                <v-btn
                        color="primary"
                        :disabled="!signInDate || signInStep === 2 && !signInTime"
                        @click="signInNext"
                >{{signInNextBtn}}</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="inviteToNewClassDialog" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Invite {{currentStudentName}} to a new class</span>
              </v-card-title>
              <v-card-text>
                  <v-layout align-start justify-center row wrap>
                      <v-flex xs12>
                          <v-combobox
                              v-model="selectedClassItem"
                              :items="availableClassItems"
                              label="Type in class name"
                              :error-messages="selectedClassErrors"
                          ></v-combobox>
                      </v-flex>
                      <v-flex xs12>
                        <AddStudentForm
                            v-model="addStudentFormData"
                            :item="selectedClass"
                            :students="[currentStudent]"
                        />
                      </v-flex>
                  </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                        color="blue darken-1"
                        flat
                        @click="inviteToNewClassDialog=false"
                >Cancel</v-btn>
                <v-btn
                        color="primary"
                        @click="confirmInviteToNewClass"
                >Send</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>

        </v-card-text>
    </v-card>
</template>
<script>
import axios from 'axios';
import { mapState } from 'vuex';
import utils from "@/lib/utils";
import classHelper from '@/lib/helpers/Class'
import AddStudentForm from './AddStudentForm'

const formatTime = (time) => utils.time24HtoAMPM(time)

export default {
    name: 'dashboard_teach_studentinfo',
    components: {
        AddStudentForm,
    },
    data: function () {
        return {
            signInDialog: false,
            selectedOrderId: null,
            addStudentFormData: undefined,
            inviteToNewClassDialog: false,
            selectedClassItem: null,

            signInStep: 1,
            signInDate: null,
            signInTime: null,

            updatedFirstName: this.first_name,
            updatedLastName: this.last_name,
            updatedPhone: this.phone,
            updatedSource: this.source,
            updatedNotes: this.notes,
            updatedNotes2: this.notes2,
        }
    },
    props: {
        onclose: Function,
        email: String,
        first_name: String,
        id: Number,
        last_name: String,
        phone: String,
        source: String,
        notes: String,
        notes2: String,
        orders: Array,
        classes: Array,
        managed_by: Array,
        memberships: Array,
    },
    computed: {
        ...mapState(['user']),
        isUpdatable() {
            return this.managed_by && this.managed_by.includes(this.user.id);
        },
        isUserChanged() {
            return this.first_name !== this.updatedFirstName ||
                this.last_name !== this.updatedLastName ||
                this.phone !== this.updatedPhone ||
                this.source !== this.updatedSource ||
                this.notes !== this.updatedNotes ||
                this.notes2 !== this.updatedNotes2;
        },
        signInBackBtn() {
            return this.signInStep === 1 ? 'Cancel' : 'Back'
        },
        signInNextBtn() {
            if(!this.signInClass)
                return ''
            return this.signInStep < 2 ? 'Next' : 'Sign In'
        },
        signInClass() {
            return this.selectedOrder ? this.classes.find(c => c.id === this.selectedOrder.klass): null
        },
        availableSignInDates() {
            if(!this.selectedOrder || !this.signInClass)
                return {}
            if(this.signInClass.is_private) {
                const duration = this.selectedOrder.data.package.lessonLength && this.selectedOrder.data.package.lessonLength.value
                return classHelper.getAvailableSchedule(this.signInClass, 100, duration)
            }
            return classHelper.getAvailableSchedule(this.signInClass, 100)
        },
        signInTimeSlots() {
            return (this.availableSignInDates && this.availableSignInDates[this.signInDate] || []).map(v => ({
                ...v,
                title: `${formatTime(v.start)} - ${formatTime(v.end)}`
            }))
        },
        orderGroups() {
            return classHelper.groupOrdersByStatus(this.orders.filter(o => o.class))
        },
        currentOrders() {
            console.log(this.orders)
            return this.orderGroups.current.map(v => ({
                ...v,
                name: v.data.name,
            }))
        },
        selectedOrder() {
            return this.orders.find(o => o.id === this.selectedOrderId)
        },
        selectedClass() {
            return this.selectedClassItem && this.classes.find(c => c.pk === this.selectedClassItem.value)
        },
        currentCalassName() {
            return this.selectedOrder && this.selectedOrder.data.name
        },
        currentStudent() {
            return {
                email: this.email,
                first_name: this.first_name,
                id: this.id,
                last_name: this.last_name,
                phone: this.phone,
            }
        },
        currentStudentName() {
            return this.first_name +' '+ this.last_name
        },
        historyText() {
            return [
                ...this.orderGroups.current,
                ...this.orderGroups.past,
            ].map(o => `${classHelper.title(o.class)}, Created: ${(new Date(o.created_at)).toLocaleDateString('en-US')}, $${o.amount}`)
            .concat(this.memberships.map(m => `Member of ${m.name} since ${new Date(m.created_at).toLocaleDateString('en-US')}, paid ${utils.formatPrice(m.total_paid, 'usd')}`)).join('\n')
        },
        availableClasses() {
            return classHelper.groupClassesByAvailability(this.classes).current
        },
        availableClassItems() {
            return this.availableClasses.map(v => ({
                value: v.pk,
                text: classHelper.title(v),
            }))
        },
    },
    watch: {
        first_name(v) {
            this.updatedFirstName = v;
        },
        last_name(v) {
            this.updatedLastName = v;
        },
        phone(v) {
            this.updatedPhone = v;
        },
        source(v) {
            this.updatedSource = v;
        },
        notes(v) {
            this.updatedNotes = v;
        },
        notes2(v) {
            this.updatedNotes2 = v;
        },
    },
    methods: {
        signInNext() {
            if(!this.signInClass)
                return ''
            if(this.signInStep < 2) {
                this.signInStep++
                return
            }
            this.signInFormConfirm()
        },
        signInBack() {
            if(this.signInStep > 1)
                this.signInStep--
            else
                this.signInDialog = false
        },
        isSignInAvailable(date) {
            return this.availableSignInDates && this.availableSignInDates[date] && this.availableSignInDates[date].length
        },
        signIn(orderId) {
            this.selectedOrderId = orderId
            this.signInStep = 1
            this.signInDate = null
            this.signInTime = null
            this.signInDialog = true
            //console.log(this.selectedOrder)
        },
        signInFormConfirm() {
            this.submitEnrollStudent()
                .then(() => {
                    this.signInDialog = false
                })
                .catch(e => {
                    this.setGlobalError(e)
                })
        },
        submitEnrollStudent() {
            //console.log(v)
            if(!this.signInDate || !this.signInTime || !this.signInClass || !this.selectedOrder)
                return
            return axios.post(`/api/teacher_sign_student`, {
                order_id: this.selectedOrder.id,
                date: this.signInDate,
                time: this.signInTime,
            }).then(res => {
                if(!res.data.success) {
                    // show error
                    return Promise.reject(res.data.message)
                }
                const order = this.orders.find(v => v.id === this.selectedOrder.id)
                const cl = this.classes.find(v => v.id === this.signInClass.id)
                order.reserved_lessons ++
                cl.num_enrolled++
                cl.enrolled.push({order_id: res.data.enr.order, ...res.data.enr})
                this.$emit('update-class', cl)
                this.$emit('update-order', order)
            })
        },
        inviteToNewClass() {
            this.addStudentFormData = {
                addStudentFormType: 'registered',
                addStudentFormAutocompleteEmail: this.currentStudent,
            }
            this.inviteToNewClassDialog = true
        },
        confirmInviteToNewClass() {
            if(!this.addStudentFormData.isValid)
                return
            axios.post(`/api/send_add_student_request/`, {
                class_id: this.selectedClass.id,
                name: this.addStudentFormData.addStudentFormName,
                email: this.addStudentFormData.addStudentFormType === 'new' ? this.addStudentFormData.addStudentFormEmail : this.addStudentFormData.addStudentFormAutocompleteEmail.email,
                phone: this.addStudentFormData.addStudentFormPhone,
                message: this.addStudentFormData.addStudentFormMessage,
                type: this.addStudentFormData.addStudentFormType,
                copyMe: this.addStudentFormData.addStudentFormCopyMe,
            }).then(res => {
                if(res.data.success)
                    this.inviteToNewClassDialog = false
                else {
                    this.setGlobalError(res.data.error_message)
                }
            }).catch(e => console.error(e)).then(() => {
                this.isLoading = false
            })
        },
        updateStudent() {
            axios.post(`/api/update_managed_student/`, {
                id: this.id,
                first_name: this.updatedFirstName,
                last_name: this.updatedLastName,
                phone: this.updatedPhone,
                source: this.updatedSource,
                notes: this.updatedNotes,
                notes2: this.updatedNotes2,
            }).then(res => {
                this.$emit('update-student', res.data.student)
            }).catch(console.error).finally(() => {
                this.isLoading = false
            })
        },
    },
}
</script>
<style lang="scss" scoped>
.student-info__close-container {
    height: 0;
    display: flex;
}
.student-info__title {
    text-align: center;
    flex: 1 0 auto;
}
.student-info__card {
    background-color: #F1F1F1;
}
.student-info__field-prefix {
    margin-top: 4px;
}
.student-info_text_right >>> input[type=text] {
    text-align: right;
}
.student-info_text_center >>> input[type=text] {
    text-align: center;
}
.student-info__btn-invite {
    margin-bottom: 20px;
    padding: 30px 30px;
    width: 250px;
}
.student-info__btn-update {
    margin-bottom: 20px;
    padding: 30px 30px;
    width: 250px;
}
.student-info__fields-container {
    margin: 0 -3px;
    div {
        padding: 0 3px;
    }
}
.pad-right {
    padding-right: 12px;
}
.pad-left {
    padding-left: 12px;
}
</style>