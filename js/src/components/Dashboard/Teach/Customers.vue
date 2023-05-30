<template>
    <v-layout align-start justify-center row wrap class="customers">
        <v-flex xs12 md6 class="text-xs-left customers__controls-left">
            <v-btn class="customers__add-contact" @click="addContactFormOpen">Add Contact</v-btn>
            <v-text-field
                class="customers__search"
                label="Search Customers"
                append-icon="search"
                hide-details
                solo
                v-model="customersFilterField"
          ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-right customers__controls-right">
            <div class="customers__controls-right-title">Bulk Action: </div>
            <upload-popup
                url="/api/upload_students/"
                accept="text/csv"
                popup-description="File in csv format (first name, last name, email, phone, source, notes, notes2)"
                @uploaded="reloadData"
            >
                <template v-slot:popup-open-btn="{on, loading}">
                    <v-btn
                      :loading="loading"
                      :disabled="loading"
                      v-on="on"
                    >
                      Add
                    </v-btn>
                </template>
            </upload-popup>
            <v-menu offset-y>
              <template v-slot:activator="{ on }">
                <v-btn class="customers__bulk-email" v-on="on">Email</v-btn>
              </template>
              <v-list>
                <v-list-tile
                  key="selected"
                  @click="bulkEmail('selected')"
                >
                  <v-list-tile-title>Selected</v-list-tile-title>
                </v-list-tile>
                <v-list-tile
                  key="all"
                  @click="bulkEmail('all')"
                >
                  <v-list-tile-title>All</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
            <v-menu offset-y>
              <template v-slot:activator="{ on }">
                <v-btn class="customers__bulk-email" v-on="on">Invite</v-btn>
              </template>
              <v-list>
                <v-list-tile
                  key="selected"
                  @click="bulkInvite('selected')"
                >
                  <v-list-tile-title>Selected</v-list-tile-title>
                </v-list-tile>
                <v-list-tile
                  key="all"
                  @click="bulkInvite('all')"
                >
                  <v-list-tile-title>All</v-list-tile-title>
                </v-list-tile>
              </v-list>
            </v-menu>
            <v-btn class="customers__bulk-delete" @click="openBulkDeleteStudentForm">Delete</v-btn>
        </v-flex>
        <v-flex xs12 class="text-xs-center customers__spacer">

        </v-flex>
        <template>
            <v-flex xs12 sm5>
                <v-select
                  :items="sortStudentsItems"
                  label="Sort by:"
                  v-model="sortStudentsBy"
                ></v-select>
                <v-select
                  :items="filterStudentsItems"
                  :menu-props="{closeOnClick:false, closeOnContentClick:false, openOnClick:false, maxHeight:'auto'}"
                  label="Filter by:"
                  v-model="filterStudentsBy"
                ></v-select>
                <div>
                    <v-checkbox
                      @change="onSelectAll"
                      label="Select all"
                    ></v-checkbox>
                </div>
                <v-list  v-if="studentListFiltered && studentListFiltered.length" two-line class="customers__student-list">
                    <template v-for="(item, index) in studentListFiltered">
                        <v-list-tile :key="item.id" @click.stop="(event) => selectSingleStudent(item.id, event)">
                            <v-list-tile-action>
                              <v-checkbox
                                  :value="item.selected"
                                   @click.stop="setSelected(item.id)"
                                  hide-details
                              ></v-checkbox>
                            </v-list-tile-action>

                            <v-list-tile-content>
                              <v-list-tile-title>
                                <v-tooltip bottom>
                                  <template v-slot:activator="{ on }">
                                    <v-icon color="secondary" dark v-on="on">person-off</v-icon>
                                  </template>
                                  <span>Teacher of the company (can't login)</span>
                                </v-tooltip>
                                {{item.first_name}} {{item.last_name}}
                              </v-list-tile-title>
                              <v-list-tile-sub-title>
                                  <a :href="`tel:${item.phone}`">{{item.phone}}</a>,
                                  <a :href="`mailto:${item.email}`">{{item.email}}</a>
                              </v-list-tile-sub-title>
                            </v-list-tile-content>
                            <v-list-tile-action>
                              <v-icon class="customers__student-arrow">arrow_forward</v-icon>
                            </v-list-tile-action>
                        </v-list-tile>
                      <v-divider
                          v-if="index + 1 < studentList.length"
                      ></v-divider>
                    </template>
                </v-list>
            </v-flex>
            <v-flex sm7 v-if="!isXs" :style="{'padding-left': '10px', position: 'relative'}">
                <student-info
                    v-if="selectedSingleStudent && studentInfo"
                    v-bind="studentInfo"
                    :onclose="() => selectedSingleStudent=null"
                    :style="studentInfoFormStyle"
                    @update-class="updateClass"
                    @update-order="updateOrder"
                    @update-student="updateStudent"
                />
            </v-flex>
            <v-dialog
              v-else
              :value="selectedSingleStudent"
              width="500"
            >
                <student-info
                    v-if="selectedSingleStudent && studentInfo"
                    v-bind="studentInfo"
                    :onclose="() => selectedSingleStudent=null"
                    @update-class="updateClass"
                    @update-order="updateOrder"
                    @update-student="updateStudent"
                />
            </v-dialog>
        </template>
        <v-flex v-if="(!studentList || !studentList.length) && isLoading">
            <v-progress-circular
              indeterminate
              color="grey"
            ></v-progress-circular>
        </v-flex>

        <v-dialog v-model="emailStudentForm" persistent max-width="800px">
            <bulk-email-send-form
                :student-filter="emailStudentFilter"
                :student-list="emailStudentList"
                @cancel="emailStudentForm = false"
            />
        </v-dialog>
        <v-dialog v-model="bulkInviteStudentForm" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Invite students to a session or class</span>
              </v-card-title>
              <v-card-text>
                  <v-layout align-start justify-center row wrap>
                      <v-flex xs12 class="text-xs-left">
                        selected students: {{inviteStudentFilter === 'selected' ? selectedStudentsText : inviteStudentFilterTitle}}
                      </v-flex>
                      <v-flex xs12>
                          <v-combobox
                              v-model="selectedClass"
                              :items="availableClassItems"
                              label="Select a class"
                              :error-messages="selectedClassErrors"
                          ></v-combobox>
                          <v-checkbox
                            v-model="bulkInviteStudentCopyMe"
                            label="Copy me on this message"
                          ></v-checkbox>
                      </v-flex>
                      <v-flex xs12>
                        <v-textarea
                          name="bulk-invite-message"
                          label="Message"
                          outline
                          v-model="bulkInviteStudentMessage"
                        ></v-textarea>
                      </v-flex>
                  </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="bulkInviteStudentForm=false">Cancel</v-btn>
                <v-btn :loading="isLoading" :disabled="isLoading" :color="bulkInviteStudentFormState === 'done' ? 'platform-green' : 'primary'" @click="addBulkStudentFormConfirm">{{ bulkInviteStudentFormState === 'done' ? 'Done' : 'Send' }}</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="bulkDeleteStudentForm" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Delete students</span>
              </v-card-title>
              <v-card-text>
                  <v-layout align-start justify-center row wrap>
                      <v-flex xs12>
                        {{selectedStudentsText}}
                      </v-flex>
                      <v-flex xs12>
                          <b>You are going to delete selected students from your list, are you sure?</b>
                      </v-flex>

                  </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="bulkDeleteStudentForm=false">Cancel</v-btn>
                <v-btn :loading="isLoading" :disabled="isLoading" color="error" @click="bulkDeleteStudentFormConfirm">Delete</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="inviteToNewClassForm" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Invite student to new class</span>
              </v-card-title>
              <v-card-text>
                  <v-layout align-start justify-center row wrap>
                      <v-flex xs12>
                          <v-combobox
                              v-model="selectedClass"
                              :items="availableClassItems"
                              label="Select a class"
                              :error-messages="selectedClassErrors"
                          ></v-combobox>
                      </v-flex>
                      <v-flex xs12>
                        Invite form
                      </v-flex>
                  </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="bulkInviteStudentForm=false">Cancel</v-btn>
                <v-btn :loading="isLoading" :disabled="isLoading" :color="inviteToNewClassFormState === 'done' ? 'platform-green' : 'primary'" @click="addBulkStudentFormConfirm">{{ inviteToNewClassFormState === 'done' ? 'Done' : 'Send' }}</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="addContactForm" max-width="500px">
            <v-card>
              <v-card-title>
                <span class="headline">Add contact</span>
              </v-card-title>
              <v-card-text>
                  <v-layout align-start justify-center row wrap>
                      <v-flex xs12>
                          <v-text-field
                            label="First Name"
                            v-model="addContactFirstName"
                            :error-messages="addContactFirstNameErrors"
                            required
                            @input="$v.addContactFirstName.$touch()"
                            @blur="$v.addContactFirstName.$touch()"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Last Name"
                            v-model="addContactLastName"
                            :error-messages="addContactLastNameErrors"
                            required
                            @input="$v.addContactLastName.$touch()"
                            @blur="$v.addContactLastName.$touch()"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Phone"
                            v-model="addContactPhone"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Email"
                            v-model="addContactEmail"
                            :error-messages="addContactEmailErrors"
                            required
                            @input="$v.addContactEmail.$touch()"
                            @blur="$v.addContactEmail.$touch()"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Source"
                            v-model="addContactSource"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Notes"
                            v-model="addContactNotes"
                          ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                          <v-text-field
                            label="Notes2"
                            v-model="addContactNotes2"
                          ></v-text-field>
                      </v-flex>
                  </v-layout>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click="addContactForm=false">Cancel</v-btn>
                <v-btn :loading="isLoading" :disabled="isLoading" color="primary" @click="addContactFormSubmit">Send</v-btn>
              </v-card-actions>
            </v-card>
        </v-dialog>
    </v-layout>
</template>

<script>
import {sortBy, sumBy, groupBy, debounce} from 'lodash';
import { mapMutations } from 'vuex'
import { validationMixin } from 'vuelidate'
import { required, email, requiredIf } from 'vuelidate/lib/validators'
import axios from 'axios';
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class'
import StudentInfo from './Components/StudentInfo';
import BulkEmailSendForm from './Components/BulkEmailSendForm'
import UploadPopup from '@/components/basic/UploadPopup'

export default {
    name: 'dashboard_teach_customers',
    mixins: [validationMixin],
    components: {
        StudentInfo,
        BulkEmailSendForm,
        UploadPopup,
    },
    validations: {
        selectedClass: { required: requiredIf(function() {return this.bulkInviteStudentForm}) },
        addContactEmail: {email, required: requiredIf(function() {return this.addContactForm})},
        addContactFirstName: {required: requiredIf(function() {return this.addContactForm})},
        addContactLastName: {required: requiredIf(function() {return this.addContactForm})},
    },
    data: () => ({
        isLoading: false,
        all: [],
        orders: [],
        classes: [],
        deleted: [],
        instructors: [],
        selectedSingleStudent: null,
        selectedStudents: {},
        expandedStudents: {},
        customersFilterField: '',
        customersFilterValue: '',

        // dialogs
        emailStudentForm: false,
        emailStudentFilter: 'all',
        emailStudentList: [],

        bulkInviteStudentForm: false,
        bulkInviteStudentCopyMe: true,
        inviteToNewClassForm: false,
        inviteToNewClassFormState: 'initial',
        inviteStudentFilter: '',
        bulkInviteStudentMessage: '',
        bulkInviteStudentFormState: 'initial',

        bulkDeleteStudentForm: false,

        selectedClass: null,

        addContactForm: false,
        addContactServerErrors: {},
        addContactFirstName: '',
        addContactLastName: '',
        addContactPhone: '',
        addContactEmail: '',
        addContactSource: '',
        addContactNotes: '',
        addContactNotes2: '',

        studentInfoFormStyle: {},

        sortStudentsItems: [
            { text: 'Name', value: 'name' },
            { text: 'Date joined', value: 'date' },
            { text: 'Source', value: 'source' },
            { text: 'Notes', value: 'notes' },
            { text: 'Notes2', value: 'notes2' },
        ],
        sortStudentsBy: 'name',
        filterStudentsBy: '',
        membership: null,
    }),
    computed: {
        filterStudentsItems() {
            const notesOptions = Object.keys(this.all.filter(v => v.notes).reduce((acc, v) => ({...acc, [v.notes]: true}), {}))
                .map(value => ({text: `Notes: ${value}`, value: `notes-${value}`}));
            const notes2Options = Object.keys(this.all.filter(v => v.notes2).reduce((acc, v) => ({...acc, [v.notes2]: true}), {}))
                .map(value => ({text: `Notes2: ${value}`, value: `notes2-${value}`}));
            return [
                { text: 'All', value: '' },
                { text: 'Prospects', value: 'prospects' },
                { text: 'Members', value: 'members' },
                { text: 'Canceled Members', value: 'canceledMembers' },
                { text: 'Customers', value: 'customers' },
                { text: 'Registered only', value: 'registered' },
                { text: 'Unregistered prospects', value: 'unregistered' },
                { text: 'Instructors', value: 'instructors' },
                { text: 'Added Teachers', value: 'companyTeachers' },
                { text: 'Notes', disabled: true },
                ...notesOptions,
                { text: 'Notes2', disabled: true },
                ...notes2Options,
            ];
        },
        inviteStudentFilterTitle() {
            if(this.inviteStudentFilter)
                return this.inviteStudentFilter.charAt(0).toUpperCase()+this.inviteStudentFilter.substring(1)
            return ''
        },
        studentInfo() {
            if(!this.selectedSingleStudent)
                return null
            const orders = this.ordersDict[this.selectedSingleStudent] ? this.ordersDict[this.selectedSingleStudent].map(v => ({
                ...v,
                'class': this.classDict.get(v.klass),
            })) : []
            const student = this.all.find(v => v.id === this.selectedSingleStudent);
            if (!student) return null;
            const membershipName = this.membership ? this.membership.owner.company_profile ? this.membership.owner.company_profile.name : `${this.membership.owner.first_name} ${this.membership.owner.last_name}` : '';
            return {
                ...student,
                orders,
                classes: this.classes.map(c => ({...c, id: c.pk})),
                memberships: this.membership ? student.memberships.filter(v => (v.membership === this.membership.id && v.is_active)).map(v => ({...v, name: membershipName})) : [],
            };
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
        selectClassMenuTitle() {
            return this.selectedClass && this.availableClassItems.find(v => v.id === this.selectedClass).title || 'Select Class'
        },
        isXs() {
            return this.$vuetify.breakpoint.xs;
        },
        ordersDict() {
            return groupBy(this.orders, 'user');
        },
        selectedStudentsText() {
            return this.studentList.filter(s => this.selectedStudents[s.id]).map(s => `${s.first_name} ${s.last_name}`).join(', ')
        },
        studentList() {
            const sorters = {
                name: v => `${v.first_name} ${v.last_name}`,
                date: v => -(new Date(v.date_joined).getTime()),
                source: v => v.source,
                notes: v => v.notes,
                notes2: v => v.notes2,
            };
            const dupls = {};
            const exitingInstructorEmail = this.instructors.reduce((acc, v) => ({
                ...acc,
                [v.email]: true,
            }), {});
            const teachers = this.classesTeachers.filter(v => v.email && !exitingInstructorEmail[v.email])
            return sortBy([
                ...this.all, 
                ...this.instructors.map(v => ({...v, isInstructor: true})),
                ...teachers.map(v => ({...v, isInstructor: true, isCompanyAccount: true, id: `t${v.id}`})),
            ], sorters[this.sortStudentsBy])
                .filter(s => !this.deletedDict[s.id])
                .filter(v => {
                    if (dupls[v.id]) return false;
                    dupls[v.id] = true;
                    return true;
                })
                .filter(s => {
                    if (!this.filterStudentsBy) return true;
                    if (this.filterStudentsBy.startsWith('notes-') && s.notes === this.filterStudentsBy.substr(6)) return true;
                    if (this.filterStudentsBy.startsWith('notes2-') && s.notes2 === this.filterStudentsBy.substr(7)) return true;
                    if (this.filterStudentsBy === 'prospects' && s.isProspect) return true;
                    if (this.filterStudentsBy === 'members' && s.isMember) return true;
                    if (this.filterStudentsBy === 'canceledMembers' && s.isCanceledMember) return true;
                    if (this.filterStudentsBy === 'customers' && s.isCustomer) return true;
                    if (this.filterStudentsBy === 'registered' && s.isRegistered) return true;
                    if (this.filterStudentsBy === 'unregistered' && s.isUnregistered) return true;
                    if (this.filterStudentsBy === 'instructors' && s.isInstructor) return true;
                    if (this.filterStudentsBy === 'companyTeachers' && s.isCompanyAccount) return true;
                    return false;
                }).map(v => ({
                    key: v.id,
                    id: v.id,
                    email: v.email,
                    first_name: v.first_name,
                    last_name: v.last_name,
                    phone: v.phone,
                    expanded: this.expandedStudents[v.id],
                    selected: this.selectedStudents[v.id],
                    selectedSingle: this.selectedSingleStudent === v.id,
                    notes: v.notes,
                    notes2: v.notes2,
                    cost: this.ordersDict[v.id] ?
                        utils.formatPrice(sumBy(this.ordersDict[v.id], o => Number(o.status !== 'refund' ? o.amount : 0)), this.ordersDict[v.id][0].data.package ? this.ordersDict[v.id][0].data.package.currency : 'usd').replace('Free', '$0') :
                        '',
                    classTitles: this.ordersDict[v.id] ?
                        this.ordersDict[v.id].map(v => v.data.name).join(', ') :
                        '',
                    orders: this.ordersDict[v.id] ? this.ordersDict[v.id].map(o => Object.assign({
                        chipColor: o.reserved_lessons === o.num_lessons ? 'success' : '',
                        isEnrollAavailable: o.reserved_lessons < o.num_lessons && (this.classDict.has(o.klass) && !this.classDict.get(o.klass).is_private)
                    }, o)) : [],
            }))
        },
        studentListFiltered() {
            return this.studentList.filter(v => (
                v.first_name.toLowerCase().indexOf(this.customersFilterValue.toLowerCase()) !== -1
                || v.last_name.toLowerCase().indexOf(this.customersFilterValue.toLowerCase()) !== -1))
        },
        classDict() {
            return new Map(this.classes.map(c => [c.pk, c]))
        },
        deletedDict() {
            return this.deleted.reduce((acc, d) => ({...acc, [d]: true}), {})
        },
        selectedClassErrors() {
            const errors = []
            if (!this.$v.selectedClass.$dirty) return errors
            !this.$v.selectedClass.required && errors.push('Class is required.')
            return errors
        },
        addContactFirstNameErrors() {
            const errors = this.addContactServerErrors['first_name'] ? [...this.addContactServerErrors['first_name']] : []
            if (!this.$v.addContactFirstName.$dirty) return errors
            !this.$v.addContactFirstName.required && errors.push('First name is required.')
            return errors
        },
        addContactLastNameErrors() {
            const errors = this.addContactServerErrors['last_name'] ? [...this.addContactServerErrors['last_name']] : []
            if (!this.$v.addContactLastName.$dirty) return errors
            !this.$v.addContactLastName.required && errors.push('Last name is required.')
            return errors
        },
        addContactEmailErrors() {
            const errors = this.addContactServerErrors['email'] ? [...this.addContactServerErrors['email']] : []
            if (!this.$v.addContactEmail.$dirty) return errors
            !this.$v.addContactEmail.required && errors.push('Email is required.')
            !this.$v.addContactEmail.email && errors.push('Must be valid e-mail')
            return errors
        },
        classesTeachers() {
            return Object.values(this.classes.reduce((acc, v) => ({
                ...acc,
                [v.teacher.id]: v.teacher,
            }), {}));
        },
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        onSelectAll(selected) {
            const selectedDict = {};
            if (selected && this.studentListFiltered) {
                this.studentListFiltered.forEach(s => { selectedDict[s.id] = selected});
            }
            this.selectedStudents = selectedDict;
        },
        reloadData() {
            this.isLoading = true;
            axios.get('/api/teacher_students/').then(res => {
                //console.log(res)
                this.all = res.data.all || [];
                this.orders = res.data.orders || [];
                this.classes = res.data.classes || [];
                this.deleted = res.data.deleted || [];
                this.membership = res.data.membership;
            })
            .then(() => axios.get('/api/company_instructors/'))
            .then((res) => {
                this.instructors = res.data;
            })
            .catch(e => console.log(e)).then(() => {
                this.isLoading = false;
            })
        },
        setSelected(id) {
            this.$set(this.selectedStudents, id, !this.selectedStudents[id]);
        },
        selectSingleStudent(id, event) {
            this.selectedSingleStudent = id
            this.studentInfoFormStyle = { marginTop: event.currentTarget.offsetTop + 'px' };
        },
        bulkEmail(type) {
            this.emailStudentFilter = type;
            this.emailStudentList = type === 'selected'
                ? this.studentListFiltered.filter(v => v.selected).map(v => v.id)
                : null;
            this.emailStudentForm = true;
        },
        bulkInvite(type) {
            this.inviteStudentFilter = type;
            if(type === 'selected')
                return this.openBulkInviteStudentForm()
            this.bulkInviteStudentForm = true
        },
        addBulkStudentFormConfirm() {
            if (this.bulkInviteStudentFormState === 'done') {
                this.bulkInviteStudentForm = false;
                this.bulkInviteStudentFormState = 'initial'
                return;
            }
            this.$v.$touch()
            if (this.$v.selectedClass.$anyError)
                return
            this.isLoading = true;
            axios.post(`/api/send_add_student_request/`, {
                class_id: this.selectedClass.value,
                emails: this.studentList.filter(s => this.selectedStudents[s.id]).map(s => s.email),
                type: 'registered',
                filter: this.inviteStudentFilter,
                message: this.bulkInviteStudentMessage,
                copyMe: this.bulkInviteStudentCopyMe,
            }).then(res => {
                if(res.data.success)
                    this.bulkInviteStudentFormState = 'done'
                else {
                    this.setGlobalError(res.data.error_message)
                }
            }).catch(e => console.error(e)).then(() => {
                this.isLoading = false
            })
        },
        openBulkInviteStudentForm() {
            if(!Object.keys(this.selectedStudents).length)
                return
            this.bulkInviteStudentForm = true
        },
        openBulkDeleteStudentForm() {
            if(!Object.keys(this.selectedStudents).length)
                return
            this.bulkDeleteStudentForm = true
        },
        bulkDeleteStudentFormConfirm() {
            const ids = this.studentList.filter(s => this.selectedStudents[s.id]).map(s => s.id)
            this.isLoading = true
            axios.post(`/api/delete_student/`, {
                ids,
            }).then(res => {
                if(res.data.success) {
                    this.bulkDeleteStudentForm = false
                    this.deleted = [...this.deleted, ...ids]
                } else {
                    this.setGlobalError(res.data.error_message)
                }
            }).catch(e => console.error(e)).then(() => {
                this.isLoading = false
            })
        },
        updateClass(c) {
            const index = this.classes.findIndex(v => v.pk === c.id)
            this.$set(this.classes, index, c)
        },
        updateOrder(o) {
            const index = this.orders.findIndex(v => v.id === o.id)
            this.$set(this.orders, index, o)
        },
        addContactFormOpen() {
            this.addContactForm = true
        },
        addContactFormSubmit() {
            if(this.$v.$anyError) {
                return
            }
            this.isLoading = true;
            axios.post('/api/add_managed_student/', {
                first_name: this.addContactFirstName,
                last_name: this.addContactLastName,
                phone: this.addContactPhone,
                email: this.addContactEmail,
                source: this.addContactSource,
                notes: this.addContactNotes,
                notes2: this.addContactNotes2,
            }).then((res) => {
                this.addContactFirstName = ''
                this.addContactLastName = ''
                this.addContactPhone = ''
                this.addContactEmail = ''
                this.all = [...this.all, res.data.student]
                this.addContactForm = false
            }).catch(e => {
                console.log(e)
                this.addContactServerErrors = {...e.response.data}
            }).then(() => {
                this.isLoading = false
            })
        },
        companyName(item) {
            return item.teacher.user.is_company && item.teacher.user.company_profile ? `
${item.teacher.user.company_profile.name}` : '';
        },
        updateStudent(student) {
            const index = this.all.findIndex(v => v.id === student.id);
            if (index !== -1) {
                this.$set(this.all, index, {...this.all[index], ...student})
            }
        },
    },
    watch: {
        customersFilterField: debounce(function (val, oldVal) {
            this.customersFilterValue = val
        }, 100),
        selectedClass(val, old) {
            if (val && val.value && (!old || old.value !== val.value)) {
                const item = this.classes.find(v => v.pk === Number(val.value))
                if(!item) return;
                this.bulkInviteStudentMessage = `You’re invited to "${this.selectedClass.text}".
Book here: ${window.location.origin}/learners/${this.selectedClass.value}/3/?name=&phone=&email=

All the best,
${item.teacher.first_name} ${item.teacher.last_name}${this.companyName(item)}
${item.teacher.phone || item.teacher.user.phone}
${item.teacher.email || item.teacher.user.email}

Powered by TeachBeach.com`
                }
        }
    },
    created() {
        this.reloadData()
    },
}
</script>
<style lang="scss" scoped>
.customers__controls-left {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-start;
    align-items: flex-end;
}
.customers__search {

}
.customers__add-contact {
    margin-right: 20px;
}
.customers__controls-right {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-end;
    align-items: center;
}
.customers__controls-right-title {
    font-weight: bold;
}
.customers__spacer {
    height: 40px;
}
.customers__student-arrow {
    font-weight: bold;
    color: black;
    font-size: 30px;
}
.customers__student-list {
    position: relative;
}
.customers__search >>> .v-input__slot {
    margin-top: 6px;
    min-height: 36px;
}
.class-name-overflow {
    max-width: 160px;
    text-overflow: ellipsis;
}
</style>