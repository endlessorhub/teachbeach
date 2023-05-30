<template>
<div class="teacher-checkout-page">
    <v-container grid-list-md text-xs-center>
        <template v-if="isEmailBoost">
            <div class="title"><v-icon >email</v-icon> Add my class to the TeachBeach "What we do this week" newsletter</div>
        </template>
        <template v-else-if="isFreeForNow">
            <h3 class="headline">Let’s do this!</h3>
            <div class="title">On your dashboard, click on the green rocket <v-icon color="platform-green">fas fa-rocket</v-icon> after any class to submit it to 40 online event calendars.
            </div>
        </template>
        <template v-else>
            <h3 class="headline">Let’s do this!</h3>
            <div class="title"><v-icon >fas fa-rocket</v-icon> Yes!  Submit my {{classNumber}} class{{classNumber == 1 ? '' : 'es'}} to 42 local media and online event listings {{isFreeForNow ? '' : `for ${cost} ${monthly}`}}</div>
        </template>
        <v-layout align-top justify-center row wrap v-if="isFreeForNow">
            <v-flex xs12 class="text-xs-center">
                <v-btn :color="btnColor" class='pay-with-stripe' @click="submit" :loading="isLoading" :disabled="!complete || isLoading">
                    <v-icon v-if="done" left>check_circle</v-icon>
                    {{btnText}}
                </v-btn>
            </v-flex>
        </v-layout>

        <v-layout align-top justify-center row wrap v-else>

            <v-flex xs12 class="text-xs-left" v-if="!isSkipping">
              Please choose card or add payment information
            </v-flex>
            <v-flex xs12 class="text-xs-left" v-if="!isSkipping">
                <credit-cards
                    ref="creditCardEl"
                    :btn-text="btnText"
                    :url="url"
                    :payment-options="paymentOptions"
                    :btn-color="btnColor"
                    @cardAdded="onSuccess"
                    @cardError="onError"
                />
            </v-flex>
          </v-layout>
    </v-container>
</div>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import CreditCards from '@/components/basic/CreditCards';
import axios from 'axios'
import config from '@/config.js'
import moment from 'moment'
import metadata from '@/mixins/metadata'

export default {
    mixins: [metadata],
    props: {
        'option': Number,
        'class_id': Number,
    },

    components: { CreditCards },

    data: () => ({
        btnText: '',
        btnColor: '',
        done: false,
        isLoading: false,
        package: null,
        complete: false,
        defaultCard: null,
        sourceCards: [],
        cardError: '',
        disabledDeletes: {},
        isEmailBoost: false,
        isFreeForNow: true,
    }),

    created: function () {
        this.btnText = this.isFreeForNow ? 'Got it' : 'Pay'
        this.complete = this.isFreeForNow ? true : false
        this.isLoading = true
        if(this.option > 100) {
            this.isEmailBoost = true
        } else {
            this.isEmailBoost = false
        }
        const init = () => (this.isEmailBoost ? axios.get('/api/buy_email_boost') : axios.get('/api/buy_membership'));
        init().then(res => {
            this.package = _.find(res.data.available_options, {id: Number(this.isEmailBoost ? this.option-100 : this.option)})
            this.isLoading = false
        })
    },

    computed: {
        url() {
            if(this.isEmailBoost && this.class_id) {
                return '/api/buy_email_boost';
            } else if (!this.isEmailBoost) {
                return '/api/buy_membership';
            } else {
                return '/api/stripe/add_card';
            }
        },
        paymentOptions() {
            if(this.isEmailBoost && this.class_id) {
                return {
                    'class_id': this.class_id,
                };
            } else if (!this.isEmailBoost) {
                return {
                    'option_id': this.option,
                };
            } else {
                return {
                    no_pay: true,
                };
            }
        },
        cost() {
            return utils.formatPrice(this.costNumber, 'usd')
        },
        costNumber() {
            return this.package ? this.package.amount : 0
        },
        classNumber() {
            return this.package ? this.package.num_classes : 0
        },
        monthly() {
            return this.package && this.package.is_monthly ? 'per month' : ''
        }
    },

    methods: {
        submit () {
            if(this.done) {
                this.$router.push('/dashboard/teach/classes')
                return
            }
            this.isLoading = true;
            this.cardError = '';
            // createToken returns a Promise which resolves in a result object with
            // either a token or an error key.
            // See https://stripe.com/docs/api#tokens for the token object.
            // See https://stripe.com/docs/api#errors for the error object.
            // More general https://stripe.com/docs/stripe.js#stripe-create-token.
            if (!this.isFreeForNow) {
                this.$refs.creditCardEl.submit();
                return;
            }
            const action = () => {
                if(this.isEmailBoost && this.class_id) {
                    return axios.post('/api/buy_email_boost', {
                        'class_id': this.class_id,
                    })
                } else if (!this.isEmailBoost) {
                    return axios.post('/api/buy_membership', {
                        'option_id': this.option,
                    })
                } else {
                    return Promise.reject({msg: 'final action not recognized'})
                }
            }

            action().then(res => {
                if(res.data.success && this.class_id && !this.isEmailBoost && this.package && this.package.num_classes === 1) {
                    // todo: automatically boost that class
                    return res
                } else {
                    return res
                }
            }).then((res) => {
                this.isLoading = false
                console.log(res)
                if(res.data.success) {
                    this.done = true
                    this.btnColor = 'success'
                    this.btnText = this.isFreeForNow ? 'It’s done' : 'Congrats, you’re enrolled!'
                    setTimeout(() => {
                        // console.log('go to next')
                        this.$router.push('/dashboard/teach/classes')
                    }, 1000)
                } else {
                    this.cardError = res.data.error_message
                }
            }).catch(err => {
                this.isLoading = false
                console.log(err)
            })
        },
        cancel() {
            console.log('cancel checkout')
        },
        onSuccess() {
            this.done = true
            this.btnColor = 'success'
            this.btnText = this.isFreeForNow ? 'It’s done' : 'Congrats, you’re enrolled!'
            setTimeout(() => {
                // console.log('go to next')
                this.$router.push('/dashboard/teach/classes')
            }, 1000);
        },
        onError(err) {
            this.cardError = err.error_message;
        }
    }
}
</script>

<style scoped lang="scss">
.teacher-checkout-page {
    .shrinked {
        padding: 0 !important;
    }
    .expanded{
        padding: 20px 0 !important;
        margin: 20px 0 !important;
    }
}
</style>