<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 md10 class="inline-content">
            <v-select
                v-model="studentFilter"
                :items="studentFilterItems"
                label="Membership"
            ></v-select>
            <v-select
                v-model="interestFilter"
                :items="interestFilterItems"
                label="Interest"
            ></v-select>
            <v-select
                v-model="skillFilter"
                :items="skillFilterItems"
                label="Skill"
            ></v-select>
            <v-select
                v-model="levelFilter"
                :items="levelFilterItems"
                label="Level"
            ></v-select>
            <!--div v-if="studentList && studentList.length" class="button-container">
                <SendEmailsToStudents 
                    :studentFilter="studentFilter"
                    :students="filteredStudentIds"
                ></SendEmailsToStudents>
            </div-->
        </v-flex>
        <v-flex xs12 md10 class="inline-content">
            <v-text-field
                label="Search in text"
                v-model="textSearch"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md10 v-if="pagedStudentList && pagedStudentList.length">
            <v-list two-line class="full-height-list">
                <template v-for="(item, index) in pagedStudentList">
                    <StudentListItem
                        v-bind="item"
                    ></StudentListItem>
                  <v-divider
                      v-if="index + 1 < pagedStudentList.length"
                  ></v-divider>
                </template>
            </v-list>

        </v-flex>
        <v-flex xs12 v-else>

            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="grey"
            ></v-progress-circular>
        </v-flex>
        <v-flex v-if="totalPages > 1" xs12>
            <v-pagination
                v-model="page"
                :length="totalPages"
                :total-visible="7"
            ></v-pagination>
        </v-flex>
        <v-dialog
            v-model="enrollOrderDialog"
            lazy
            full-width
            width="290px"
        >
            <v-date-picker
                @input="enrollOrderDialog=false"
                v-model="enrollOrderDialogDate"
                :allowed-dates="allowedDates"
                scrollable
            >

            </v-date-picker>
        </v-dialog>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import SendEmailsToStudents from './Components/SendEmailsToStudents'
import StudentListItem from './Components/StudentListItem'
import ActionableOnClick from '@/components/basic/ActionableOnClick'
import utils from '@/lib/utils.js'

export default {
    name: 'dashboard_teach_classes',
    data: () => ({
        isLoading: false,
        all: [],
        orders: [],
        classes: [],
        members: [],
        confirmRefundForm: false,
        refundStudent: '',
        refundClass: '',
        refundOrderId: null,
        refundCost: '',
        learnerNeedsLimit: 50,

        expandedStudents: {},
        enrollOrderDialog: false,
        enrollOrderDialogOrder: null,
        enrollOrderDialogAllowed: new Map(),
        studentFilter: 'all',
        studentFilterItems: [
            { value: 'all', text: 'All' },
            { value: 'members', text: 'Members' },
            { value: 'prospects', text: 'Prospects' },
            { value: 'students', text: 'Students' },
            { value: 'registered', text: 'Registered' },
        ],
        interestFilter: '',
        skillFilter: '',
        levelFilter: '',
        textSearch: '',
        itemsPerPage: 10,
        page: 1,
    }),
    props: [],
    components: {
        SendEmailsToStudents,
        ActionableOnClick,
        StudentListItem,
    },
    created() {
        this.reloadData()
    },
    computed: {
        interestFilterItems() {
            return [{text: 'All', value: ''}, ...[...new Set(this.studentList.map(s => s.interest))]
                .filter(Boolean)
                .map(v => ({text: v, value: v}))];
        },
        skillFilterItems() {
            return [{text: 'All', value: ''}, ...[...new Set(this.studentList.map(s => s.skill))]
                .filter(Boolean)
                .map(v => ({text: v, value: v}))];
        },
        levelFilterItems() {
            return [{text: 'All', value: ''}, ...[...new Set(this.studentList.map(s => s.level))]
                .filter(Boolean)
                .map(v => ({text: v, value: v}))];
        },
        enrollOrderDialogDate: {
            get() {
                if(this.enrollOrderDialogOrder) {
                    return this.orders.find(o => o.id === this.enrollOrderDialogOrder.id).plannedEnroll
                }
            },
            set(v) {
                if(this.enrollOrderDialogOrder) {
                    const index = this.orders.findIndex(o => o.id === this.enrollOrderDialogOrder.id)
                    const o = this.orders[index]
                    o.plannedEnroll = v
                    this.$set(this.orders, index, o)
                }
            }
        },
        classDict() {
            return new Map(this.classes.map(c => [c.pk, c]))
        },
        memberDict() {
            return new Map(this.members.map(c => [c.student, c]))
        },
        first_name() {
            //console.log(this.$store.state)
            return this.$store.state.user.first_name
        },
        ordersDict() {
            return _.groupBy(this.orders, 'user');
        },
        studentList() {
            const res = _.map(_.sortBy(this.all, v => `${v.first_name} ${v.last_name}`), v => ({
                key: v.id,
                id: v.id,
                isMember: v.isMember,
                isRegistered: v.isRegistered,
                email: v.email,
                first_name: v.first_name,
                last_name: v.last_name,
                phone: v.phone,
                media: v.media,
                title: (this.memberDict.get(v.id) || {}).title,
                city: (this.memberDict.get(v.id)  || {}).city,
                document: (this.memberDict.get(v.id)  || {}).document,
                social: (this.memberDict.get(v.id)  || {}).social,
                website: (this.memberDict.get(v.id)  || {}).website,
                description: (this.memberDict.get(v.id)  || {}).description,
                level: (this.memberDict.get(v.id)  || {}).level,
                skill: (this.memberDict.get(v.id)  || {}).skill,
                interest: (this.memberDict.get(v.id)  || {}).interest,
                expanded: this.expandedStudents[v.id],
                cost: this.ordersDict[v.id] ?
                    utils.formatPrice(_.sumBy(this.ordersDict[v.id], o => Number(o.status !== 'refund' ? o.amount : 0)), this.ordersDict[v.id][0].data.package ? this.ordersDict[v.id][0].data.package.currency : 'usd').replace('Free', '$0') :
                    '',
                classTitles: this.ordersDict[v.id] ?
                    _.map(this.ordersDict[v.id], v => v.data.name).join(', ') :
                    '',
                orders: this.ordersDict[v.id] ? this.ordersDict[v.id].map(o => Object.assign({
                    chipColor: o.reserved_lessons === o.num_lessons ? 'success' : '',
                    isEnrollAavailable: o.reserved_lessons < o.num_lessons && (this.classDict.has(o.klass) && !this.classDict.get(o.klass).is_private)
                }, o)) : [],
            }));
            return res;
        },
        filteredStudentList() {
            const filterFunc = v => {
                if (this.studentFilter === 'students') return this.ordersDict[v.id];
                if (this.studentFilter === 'prospects') return !this.ordersDict[v.id];
                if (this.studentFilter === 'members') return v.isMember;
                if (this.studentFilter === 'registered') return v.isRegistered;
                return true;
            };
            const filterByProp = (v) => {
                if (this.interestFilter && v.interest !== this.interestFilter) return false;
                if (this.skillFilter && v.skill !== this.skillFilter) return false;
                if (this.levelFilter && v.level !== this.levelFilter) return false;
                return true;
            }
            const textSearch = (v) => {
                const fields = ['first_name', 'last_name', 'description', 'city', 'document',
                    'social', 'website', 'phone', 'emaol',
                ];
                return fields.some(f => v[f] && v[f].includes(this.textSearch));
            }
            let rows = this.studentList.filter(filterFunc).filter(filterByProp);
            if (this.textSearch && this.textSearch.length >= 3) {
                rows = rows.filter(textSearch);
            }
            return rows;
        },
        pagedStudentList() {
            return this.filteredStudentList.slice((this.page - 1) * this.itemsPerPage, this.page * this.itemsPerPage);
        },
        filteredStudentIds() {
            return this.filteredStudentList.map(v => v.id);
        },
        totalPages() {
            return Math.ceil(this.filteredStudentList.length / this.itemsPerPage);
        },
    },
    methods: {
        reloadData() {
            this.isLoading = true
            axios.get('/api/teacher_students/').then(res => {
                //console.log(res)
                this.all = res.data.all || []
                this.orders = res.data.orders || []
                this.classes = res.data.classes || []
                this.members = res.data.members || []
            }).catch(e => console.log(e)).then(() => {
                this.isLoading = false
            })
        },
        openDateSelect(order) {
            this.enrollOrderDialogOrder = order
            this.enrollOrderDialogAllowed = new Map(this.classDict.has(order.klass) && this.classDict.get(order.klass).schedule_dates ? this.classDict.get(order.klass).schedule_dates.map(sd => [sd.date, true]) : [])
            this.enrollOrderDialog = true
        },
        allowedDates(date) {
            return this.enrollOrderDialogAllowed.has(date)
        },
        removePlannedEnroll(order) {
            const index = this.orders.findIndex(o => o.id === order.id)
            const o = this.orders[index]
            o.plannedEnroll = null
            this.$set(this.orders, index, o)
        },
        submitPlannedEnroll(order) {
            //return new Promise((resolve) => setTimeout(() => resolve(true), 10000))
            const o = this.orders.find(v => v.id === order.id)
            if(!o)
                return Promise.reject('order not found')
            return axios.post(`/api/teacher_sign_student`, {
                order_id: order.id,
                date: o.plannedEnroll,
            })
        }
    },

    watch: {

    }
}
</script>
<style lang="scss" scoped>
    .inline-content {
        display: flex;
        flex-flow: row;

        &> .radio-container {
            flex: 1 0 auto;
        }

        &> .button-container {
            flex: 0 1 auto;
        }
    }
</style>
<style lang="scss">
.expandable-text {
    margin-left: 10px;
}
.containered-collapsable-text {
    position: absolute;
    white-space: normal;
    background: rgb(250,250,250);
    margin-right: 120px;
    margin-left: 5px;
    padding: 0 5px;
    z-index: 1;
    box-shadow: 1px 3px 1px -2px rgba(0,0,0,0.2);
}
</style>