<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 md10 v-if="studentList && studentList.length" class="inline-content">
            <div class="radio-container">
                <v-radio-group v-model="studentFilter" row>
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
                    <v-list-group
                        :key="item.id"
                        v-model="expandedStudents[item.id]"
                    >
                        <template v-slot:activator>
                          <v-list-tile
                            :key="item.key"
                            avatar
                          >
                            <v-list-tile-avatar :tile="true">
                              <v-avatar>
                                  <v-icon color="primary">account_circle</v-icon>
                              </v-avatar>
                            </v-list-tile-avatar>

                            <v-list-tile-content>
                                <v-list-tile-title>
                                    {{item.first_name}}
                                    {{item.last_name}}
                                    <a :href="'tel:'+item.phone">{{item.phone}}</a>,
                                    <a :href="'mailto:'+item.email">{{item.email}}</a>
                                </v-list-tile-title>
                                <v-list-tile-sub-title v-if="item.classTitles && item.cost">
                                    <span>{{item.classTitles}}</span>,&nbsp;
                                    <b>{{item.cost}}</b>&nbsp;
                                </v-list-tile-sub-title>
                            </v-list-tile-content>

                            <v-list-tile-action>

                            </v-list-tile-action>
                          </v-list-tile>
                        </template>
                        <v-list-tile
                            v-for="order in item.orders"
                            :key="order.id"
                          >
                            <v-list-tile-avatar :tile="true">
                                <v-tooltip top content-class="teachbeach-tooltip">
                                  <template v-slot:activator="{ on }">
                                      <v-chip small v-on="on" :color="order.chipColor" :dark="!!order.chipColor">
                                         {{order.reserved_lessons}}/{{order.num_lessons}}
                                      </v-chip>
                                  </template>
                                    <span>Signed in to {{order.reserved_lessons}} lesson{{order.reserved_lessons === 1 ? '' : 's'}} out of {{order.num_lessons}} available</span>
                                </v-tooltip>
                            </v-list-tile-avatar>
                            <v-list-tile-content>
                                <v-list-tile-title>
                                    {{order.data.name}}
                                </v-list-tile-title>
                                <v-list-tile-sub-title >
                                    <span v-if="order.plannedEnroll">
                                        Sign in: {{order.plannedEnroll}}
                                        <ActionableOnClick
                                            :action="() => submitPlannedEnroll(order)"
                                            @success="reloadData"
                                            v-slot="{loading, click}"
                                        >
                                            <v-btn color="platform-green" :loading="loading" @click="click">
                                              Save
                                            </v-btn>
                                        </ActionableOnClick>
                                        <v-btn icon @click="removePlannedEnroll(order)">
                                          <v-icon color="error">cancel</v-icon>
                                        </v-btn>
                                    </span>
                                </v-list-tile-sub-title>
                            </v-list-tile-content>

                            <v-list-tile-action v-if="!order.plannedEnroll">
                                <v-btn v-if="order.isEnrollAavailable" class="platform-green" @click="openDateSelect(order)">Sign in</v-btn>
                            </v-list-tile-action>
                          </v-list-tile>

                    </v-list-group>
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
import ActionableOnClick from '@/components/basic/ActionableOnClick'
import utils from '@/lib/utils.js'

export default {
    name: 'dashboard_teach_classes',
    data: () => ({
        isLoading: false,
        all: [],
        orders: [],
        classes: [],
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
        studentFilter: 'students',
    }),
    props: [],
    components: {
        SendEmailsToStudents,
        ActionableOnClick,
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
        first_name() {
            //console.log(this.$store.state)
            return this.$store.state.user.first_name
        },
        studentList() {
            let ordersDict = _.groupBy(this.orders, 'user')
            let filterFunc = v => this.studentFilter === 'all'
                ? true
                : this.studentFilter === 'students' ? ordersDict[v.id] : !ordersDict[v.id]
            return _.map(_.sortBy(this.all.filter(filterFunc), v => `${v.first_name} ${v.last_name}`), v => ({
                key: v.id,
                id: v.id,
                email: v.email,
                first_name: v.first_name,
                last_name: v.last_name,
                phone: v.phone,
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
            }))
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