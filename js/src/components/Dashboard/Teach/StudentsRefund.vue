<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 md10 v-if="studentList && studentList.length">
            <v-list two-line class="full-height-list">
                <template v-for="(item, index) in studentList">
                  <v-list-tile
                    :key="item.key"
                    avatar
                  >
                    <v-list-tile-avatar :tile="true">
                      <img v-if="item.avatar" :src="item.avatar">
                    </v-list-tile-avatar>

                    <v-list-tile-content>
                        <v-list-tile-title>
                            {{item.first_name}}
                            {{item.last_name}}
                            <a :href="'tel:'+item.phone">{{item.phone}}</a>,
                            <a :href="'mailto:'+item.email">{{item.email}}</a>
                        </v-list-tile-title>
                        <v-list-tile-sub-title>
                            <span>{{item.classTitle}}</span>,&nbsp;
                            <b>{{item.cost}}</b>,
                            <span>Reserved: {{ item.reservedLessons }}</span>
                            <span v-if="!item.learnerNeeds.short">{{item.learnerNeeds.full}}</span>
                            <span v-else-if="!item.learnerNeeds.isExpanded" class="expandable-text">{{item.learnerNeeds.short}}
                                <a @click="toggleLN(item.id)">more</a>
                            </span>
                            <span v-else class="containered-collapsable-text">{{item.learnerNeeds.full}}
                                <a @click="toggleLN(item.id)">less</a>
                            </span>
                        </v-list-tile-sub-title>
                    </v-list-tile-content>

                    <v-list-tile-action>
                        <v-btn v-if="item.isRefundable" @click.stop.prevent="openRefundConfirmation(item.id)">
                            Refund
                        </v-btn>
                        <v-chip v-if="item.isRefunded" color="red" text-color="white">
                          <v-avatar>
                            <v-icon>check_circle</v-icon>
                          </v-avatar>
                          Refunded
                        </v-chip>
                    </v-list-tile-action>
                  </v-list-tile>
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
          v-model="confirmRefundForm"
          max-width="390"
        >
          <v-card>
            <v-card-title class="headline">
                Refund
              <v-spacer></v-spacer>
              <v-btn icon @click.native="confirmRefundForm = false" color="gray darken-1">
                <v-icon>close</v-icon>
              </v-btn>
            </v-card-title>

            <v-card-text>
              You are going to refund {{refundCost}} the class {{refundClass}} for {{refundStudent}}, continue?
            </v-card-text>

            <v-card-actions>
              <v-btn
                flat="flat"
                @click="confirmRefundForm = false"
              >
                No
              </v-btn>
              <v-spacer></v-spacer>

              <v-btn
                :loading="isLoading"
                :disabled="isLoading"
                color="primary"
                @click="refundOrder(refundOrderId)"
              >
                Yes
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'

import utils from '@/lib/utils.js'

export default {
    name: 'dashboard_teach_classes',
    data: () => ({
        isLoading: false,
        all: [],
        orders: [],
        confirmRefundForm: false,
        refundStudent: '',
        refundClass: '',
        refundOrderId: null,
        refundCost: '',
        learnerNeedsLimit: 50,
        expanded: {},
    }),
    props: [],
    components: {

    },
    created() {
        this.reloadData()
    },
    computed: {
        first_name() {
            //console.log(this.$store.state)
            return this.$store.state.user.first_name
        },
        studentList() {
            let studentDict = _.keyBy(this.all, 'id')
            return _.map(_.sortBy(this.orders, v => -v.id), v => ({
                key: v.id,
                id: v.id,
                email: studentDict[v.user].email,
                first_name: studentDict[v.user].first_name,
                last_name: studentDict[v.user].last_name,
                phone: studentDict[v.user].phone,
                cost: utils.formatPrice(v.amount, v.data.package ? v.data.package.currency : 'usd'),
                isRefundable: v.status === 'succeeded',
                isRefunded: v.status === 'refund',
                classTitle: v.data.name,
                reservedLessons: v.reserved_lessons,
                learnerNeeds: {
                    isExpanded: this.expanded[v.id],
                    full: v.learnerNeeds,
                    short: v.learnerNeeds && v.learnerNeeds.length > this.learnerNeedsLimit ? v.learnerNeeds.substr(0, this.learnerNeedsLimit-3)+'...' : null
                }
            }))
        }
    },
    methods: {

        reloadData() {
            this.isLoading = true
            axios.get('/api/teacher_students/').then(res => {
                //console.log(res)
                this.all = res.data.all
                this.orders = res.data.orders
            }).catch(e => console.log(e)).then(() => {
                this.isLoading = false
            })
        },
        openRefundConfirmation(id) {
            const order = _.find(this.orders, {id})
            const student = _.find(this.all, {id: order.user})

            this.refundOrderId = id
            this.refundClass = order.data.name
            this.refundStudent = `${student.first_name} ${student.last_name}`
            this.refundCost = utils.formatPrice(order.amount, order.data.package.currency)
            this.confirmRefundForm = true
        },
        refundOrder(id) {
            this.isLoading = true
            axios.post(`/api/orders/${id}/refund/`).then(res => {
                this.reloadData()
            }).catch(e => console.log(e)).then(() => {
                this.isLoading = false
                this.confirmRefundForm = false
            })
        },
        toggleLN(id) {
            this.$set(this.expanded, id, !this.expanded[id])
        },
    },

    watch: {

    }
}
</script>
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