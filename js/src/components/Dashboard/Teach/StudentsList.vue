<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 md10 v-if="studentList && studentList.length" class="inline-content">
            <div class="title">Membership Directory</div>
            <div class="radio-container">
                <v-radio-group v-model="studentFilter" row>
                    <v-radio
                        label="Members"
                        value="members"
                    ></v-radio>
                    <v-radio
                        label="Prospects"
                        value="prospects"
                    ></v-radio>
                    <v-radio
                        label="Students"
                        value="students"
                    ></v-radio>
                    <v-radio
                        label="All"
                        value="all"
                    ></v-radio>
                </v-radio-group>
            </div>
            <div class="button-container">
                <SendEmailsToStudents :studentFilter="studentFilter"></SendEmailsToStudents>
            </div>
        </v-flex>
        <v-flex xs12 md10 v-if="studentList && studentList.length">
            <v-list two-line class="full-height-list">
                <template v-for="(item, index) in studentList">
                    <StudentListItem
                        v-bind="item"
                    ></StudentListItem>
                  <v-divider
                      v-if="index + 1 < studentList.length"
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
        studentFilter: 'members',
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
        studentList() {
            let ordersDict = _.groupBy(this.orders, 'user')
            let filterFunc = v => {
                if (this.studentFilter === 'students') return ordersDict[v.id];
                if (this.studentFilter === 'prospects') return !ordersDict[v.id];
                if (this.studentFilter === 'members') return v.isMember;
                return true;
            };
            const res = _.map(_.sortBy(this.all.filter(filterFunc), v => `${v.first_name} ${v.last_name}`), v => ({
                key: v.id,
                id: v.id,
                email: v.email,
                first_name: v.first_name,
                last_name: v.last_name,
                phone: v.phone,
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
                cost: ordersDict[v.id] ?
                    utils.formatPrice(_.sumBy(ordersDict[v.id], o => Number(o.status !== 'refund' ? o.amount : 0)), ordersDict[v.id][0].data.package ? ordersDict[v.id][0].data.package.currency : 'usd').replace('Free', '$0') :
                    '',
                classTitles: ordersDict[v.id] ?
                    _.map(ordersDict[v.id], v => v.data.name).join(', ') :
                    '',
                orders: ordersDict[v.id] ? ordersDict[v.id].map(o => Object.assign({
                    chipColor: o.reserved_lessons === o.num_lessons ? 'success' : '',
                    isEnrollAavailable: o.reserved_lessons < o.num_lessons && (this.classDict.has(o.klass) && !this.classDict.get(o.klass).is_private)
                }, o)) : [],
            }));
            console.log(res);
            return res;
        }
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