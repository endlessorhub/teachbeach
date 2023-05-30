<template>
    <v-layout v-if="!isForTeacherPath || showForm" align-top justify-center row wrap fill-height>
        <snack v-model="msg"></snack>
        <h3 v-if="!isForTeacherPath" style="text-align: left; width: 100%;font-size: 20pt;">Please enter the bank account you would like to use to take payments online.</h3>
        <div v-if="!isForTeacherPath" style="text-align: left; font-size: 12pt;">Payments will be deposited in 24 hours.
            <a @click="moreInfo=true">More info</a>
            <v-dialog v-model="moreInfo" content-class="flex xs12 md8 lg6 faq-container">
              <v-card>
                <v-card-title class="headline grey lighten-2" primary-title>
                    <span>FAQ</span>
                  <v-spacer></v-spacer>
                  <v-btn icon @click.native="moreInfo=false" color="gray darken-1">
                    <v-icon>close</v-icon>
                  </v-btn>
                </v-card-title>
                <v-card-text >

                    <h4>What does this cost?</h4>
                    <p class="align-left">No fees will be charged to teachers until July 20. Students will be charged the Card processing fee. After July 20, the charge is $10% of sales. Stay free if you licence the marketing model from $5 per class per month.</p>
                    <h4>When will I be paid?</h4>
                    <p class="align-left">Student pay upfront. You will receive funds on the next business day. For private classes, you must have confirmed the date to receive funds. Just check notifications under “classes” on this dashboard. If you have any requests pending, please respond,  confirm and edit date, to release funds.</p>
                    <h4>What about security?</h4>
                    <p class="align-left">Account information is never saved on this site; it is transferred automatically into Stripe, a secure, encrypted third party processor, that serves as an escrow account. </p>
                    <v-btn @click="moreInfo=false">Thanks</v-btn>

                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="primary"
                    flat
                    @click="terms = false">
                    I accept
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
        </div>
        <v-flex xs12 class="text-xs-left">
            <v-radio-group v-model="accountType" row>
              <v-radio label="Bank account" value="bank"></v-radio>
            </v-radio-group>
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <v-alert
              :value="!!bankMessage"
              type="success"
              transition="scale-transition"
            >
              {{bankMessage}}
            </v-alert>
        </v-flex>
        <v-flex xs12 md6 v-if="accountType == 'bank'" class="text-xs-left">
            <v-text-field
                v-model="bankAccountNumber"
                label="Pay to account #"
            ></v-text-field>
            <v-text-field
                v-model="accountName"
                label="Name on account"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 v-if="accountType == 'bank'" class="text-xs-left">
            <v-text-field
                v-model="routingNumber"
                label="Routing number"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 v-if="error">
            <v-alert
              :value="error"
              type="error"
              color="platform-error"
              icon="warning"
              outline
              transition="scale-transition"
            >
              {{error}}
            </v-alert>
        </v-flex>
        <v-flex v-if="!isForTeacherPath" xs12 class="text-xs-left">
            <v-radio-group v-model="enablePayOnline">
              <v-radio label="Enable students to book and pay online" :value="true"></v-radio>
              <v-radio label="No thanks." :value="false"></v-radio>
            </v-radio-group>
        </v-flex>
        <v-flex v-if="!isForTeacherPath" xs12 class="text-xs-left">
            <v-btn @click="save" :disabled="isSaveDisabled" :loading="isLoading">Save</v-btn>
        </v-flex>
    </v-layout>
    <v-layout v-else-if="isLoading" align-center justify-center row wrap>
        <v-progress-circular
          indeterminate
          color="indigo darken-2"
        ></v-progress-circular>
    </v-layout>
</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'
import Snack from '@/components/basic/Snack'

export default {
    name: 'dashboard_account',
    data: () => ({
        isLoading: false,
        accountType: 'bank',
        bankAccountNumber: null,
        routingNumber: '',
        accountName: '',
        enablePayOnline: true,
        moreInfo: false,
        showForm: false,
        error: '',
        bankMessage: '',
        msg: '',
    }),
    props: {
        isForTeacherPath: {
            type: Boolean,
            default: false,
        }
    },
    components: {

    },
    created() {
        this.isLoading = true
        axios.get('/api/teacher/create_stripe_account/').then((res) => {
            // console.log(res)
            if(res.data.account && res.data.account.external_accounts && res.data.account.external_accounts.data && res.data.account.external_accounts.data.length) {
                const saved = res.data.account.external_accounts.data[0]
                this.bankAccountNumber = `********${saved.last4}`
                this.routingNumber = saved.routing_number
                this.accountName = saved.account_holder_name
                this.showForm = false
            } else {
                this.showForm = true
            }
            this.bankMessage = res.data.bank_message
            this.isLoading = false
            this.$emit('data:loaded', {
                isShowForm: this.showForm,
            })
        })
    },
    computed: {
        isSaveDisabled() {
            return this.isLoading || !this.bankAccountNumber || /[\*]+/.test(this.bankAccountNumber)
        }
    },
    methods: {
        save() {
            if(!this.routingNumber && !this.accountName && !this.bankAccountNumber)
                return Promise.resolve(true)
            this.isLoading = true
            this.error = ''
            return axios.post('/api/teacher/create_stripe_account/', {
                accountType: this.accountType,
                routingNumber: this.routingNumber,
                accountName: this.accountName,
                enablePayOnline: this.enablePayOnline,
                bankAccountNumber: this.bankAccountNumber,
            }).then((res) => {
                this.isLoading = false
                if(!res.data.status) {
                    this.error = res.data.err
                    return false
                }
                if(this.enablePayOnline && !this.isForTeacherPath) {
                    this.$router.push(`/dashboard/teach/classes`)
                }
                this.msg = 'Thanks! Payments will appear in your bank account in the next 24 hours'
                return true
            }).catch(e => {
                this.isLoading = false
                console.log('err', e)
                return e
            })
        }
    },

    watch: {

    }
}
</script>
<style lang="scss">
p.align-left {
    text-align: left;
}
    .faq-container {
        p {
            font-size: 1.2em;
            text-indent: 1em;
        }
    }
</style>