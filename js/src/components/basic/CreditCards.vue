<template>
<div>
    <v-list two-line>
      <v-list-tile v-for="item in cards" :key="item.id">
        <v-list-tile-action>
            <v-btn
                    v-if="!item.isExpired"
                    flat
                    icon
                    @click="setCardActive(item.id)"
                    :loading="cardPending === item.id"
                    :disabled="cardPending === item.id"
            >
                <v-icon
                  v-if="item.isActive"
                  color="yellow darken-2"
                >
                  check_circle
                </v-icon>
                <v-icon
                  v-else
                  color="grey lighten-1"
                >
                  done
                </v-icon>
            </v-btn>

        </v-list-tile-action>

        <v-list-tile-content>
            <v-list-tile-title>
                <b>{{item.brand}}</b>
                <span>...{{item.last4}}</span>
            </v-list-tile-title>
          <v-list-tile-sub-title><span :class="expirationColor(item)">{{item.exp_month}} / {{item.exp_year}}</span></v-list-tile-sub-title>
        </v-list-tile-content>
        <v-list-tile-action>
          <v-btn flat icon @click="deleteCard(item.id)" :disabled="isDeleteDisabled(item.id)">
            <v-icon
              color="darken-2"
            >
              delete_outline
            </v-icon>
          </v-btn>
        </v-list-tile-action>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-action>
            <v-btn flat icon @click="setCardActive('new_card')">
                <v-icon
                  v-if="defaultCard == 'new_card'"
                  color="yellow darken-2"
                >
                  check_circle
                </v-icon>
                <v-icon
                  v-else
                  color="grey lighten-1"
                >
                  done
                </v-icon>
            </v-btn>
        </v-list-tile-action>

        <v-list-tile-content>
            <StripeElements
                :stripe-key="stripeKey"
                :instance-options="stripeInstanceOptions"
                :elements-options="stripeElementsOptions"
                style="width: 100%; min-width: 300px;"
                #default="{ elements }"
                ref="elms"
            >
                <StripeElement
                    type="card"
                    :elements="elements"
                    :options="stripeCardOptions"
                    ref="card"
                    @change='onCardChange'  
                    @focus="defaultCard='new_card'"
                />
            </StripeElements>
        </v-list-tile-content>

        <v-list-tile-action>

        </v-list-tile-action>
      </v-list-tile>
    </v-list>
    <v-alert
      :value="!!cardError"
      type="error"
      :color="cardErrorColor"
    >
      {{cardError}}
    </v-alert>
    <v-btn v-if="cancelBtn" @click="cancel" :disabled="isLoading">No, thanks</v-btn>
    <v-btn :color="curBtnColor" class='pay-with-stripe' @click="submit" :loading="isLoading" :disabled="!complete && defaultCard === 'new_card'">
        <v-icon v-if="done" left>check_circle</v-icon>
        {{curBtnText}}
    </v-btn>
</div>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import { StripeElements, StripeElement } from 'vue-stripe-elements-plus'
import axios from 'axios'
import config from '@/config.js'
import moment from 'moment'
import { mapGetters } from 'vuex'

export default {
    props: {
        cancelBtn: {
            type: Boolean,
            default: false,
        },
        btnText: {
            type: String,
            default: 'Add',
        },
        successBtnText: {
            type: String,
            default: 'Card Added',
        },
        btnColor: {
            type: String,
            default: '',
        },
        paymentOptions: {
            type: Object,
            default: {
                no_pay: true
            },
        },
        url: {
            type: String,
            default: '/api/stripe/add_card',
        },
    },

    components: {
        StripeElements,
        StripeElement,
    },

    data: () => ({
        done: false,
        isLoading: false,
        stripeInstanceOptions: {
            // https://stripe.com/docs/js/initializing#init_stripe_js-options
        },
        stripeeElementsOptions: {
            // https://stripe.com/docs/js/elements_object/create#stripe_elements-options
        },
        stripeCardOptions: {
            // https://stripe.com/docs/stripe.js#element-options
            value: {
                postalCode: '',
            },
            style: {
                base: {
                    width: '100%',
                    fontWeight: '500',
                    fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
                    fontSize: '16px',
                    fontSmoothing: 'antialiased',
                    '::placeholder': {
                        color: '#877675',
                    },
                },
                invalid: {
                    color: '#fa755a',
                    iconColor: '#fa755a'
                },
                empty: {
                    '::placeholder': {
                        color: '#FF0000',
                    },
                },
            },
        },
        complete: false,
        stripeKey: null,
        defaultCard: null,
        cardError: '',
        cardErrorColor: 'platform-error',
        disabledDeletes: {},
        sourceCards: [],
        curBtnColor: 'success',
        curBtnText: '',
        addCardParams: {
            url: '/api/stripe/add_card',
            options: {
                no_pay: true
            }
        },
        cardPending: null,
        showPayBtnTooltip: false,
    }),

    created: function () {
        this.stripeKey = this.$store.state.globals['stripe-key']
        this.isLoading = true
        this.curBtnText = this.btnText
        this.curBtnColor = '#4caf50 !important'
        if (this.isLoggedIn) {
            axios.get('/api/payment_cards/').then(res => {
                this.defaultCard = res.data.default || 'new_card'
                this.sourceCards = res.data.sources || []
            }).finally(res => {
                this.isLoading = false
            })
        }
    },

    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        isPaymentDisaled() {
            return !this.complete && this.defaultCard == 'new_card'
        },
        payBtnTooltip() {
            if (this.complete) return 'Confirm payment';
            return 'Please fill in correct credit card information (including postal code if required)';
        },
        cards() {
            const now = moment()
            return _.map(this.sourceCards, c => _.assign({
                isActive: this.defaultCard == c.id,
                isExpired: c.exp_year < now.year() || c.exp_year == now.year() && c.exp_month < (now.month()+1),
            }, c))
        },
    },

    methods: {
        onCardChange(event) {
            this.complete = event.complete;
        },
        setCardActive(id) {
            //this.defaultCard = id
            this.cardPending = id
            axios.post(`/api/stripe/set_default_card/${id}/`).then(res => {
                if(res.data.success) {
                    this.defaultCard = id
                }
            }).finally(() => {
                this.cardPending = null
            })
        },
        deleteCard(id) {
            this.isLoading = true
            this.disabledDeletes[id] = true
            axios.post(`/api/stripe/delete_card/${id}/`).then(res => {
                let ind = _.findIndex(this.sourceCards, {id: id})
                this.sourceCards.splice(ind, 1)
                this.disabledDeletes[id] = false
                this.isLoading = false
            })
        },
        isDeleteDisabled(id) {
            return this.disabledDeletes[id]
        },
        expirationColor(item) {
            return item.isExpired ? 'red--text text--darken-2' : ''
        },
        submit () {
            if (this.isPaymentDisaled) return;
            if(this.done) {
                this.$emit('doneSubmit')
                return
            }
            this.isLoading = true
            this.cardError = ''
            this.cardErrorColor = 'platform-error'
            let processTokenError = (data) => {
                if(data && data.error) {
                    this.cardError = data.error.message
                    return false
                }
                return true
            }
            const createToken = () => {
                const groupComponent = this.$refs.elms
                const cardComponent = this.$refs.card
                const cardElement = cardComponent.stripeElement
                return groupComponent.instance.createToken(cardElement);
            }
            // createToken returns a Promise which resolves in a result object with
            // either a token or an error key.
            // See https://stripe.com/docs/api#tokens for the token object.
            // See https://stripe.com/docs/api#errors for the error object.
            // More general https://stripe.com/docs/stripe.js#stripe-create-token.
            let initialStep = this.defaultCard !== 'new_card'
                ? Promise.resolve({})
                : createToken()
            if(this.addCardParams.url !== this.url && this.defaultCard === 'new_card') {
                // add card if component used for payment
                initialStep = initialStep.then(data => {
                    if(!processTokenError(data))
                        return Promise.reject(data)
                    if(!data.token)
                        return Promise.reject({strypeTokenError: data})
                    this.defaultCard = data.token.card.id
                    return axios.post(this.addCardParams.url, {
                        card_id: 'new_card',
                        token: data.token,
                        ...this.addCardParams.options
                    })
                }).then(res => {
                    if(!res.data.success) {
                        this.cardError = res.data.error_message
                        this.cardErrorColor = 'error'
                        this.$emit('cardError', res.data)
                        return Promise.reject(res.data)
                    }
                })
            }
            initialStep.then((data) => {
                if(!processTokenError(data))
                    return Promise.reject(data)
                const addToken = data && data.token ? {token: data.token} : {}
                return axios.post(this.url, {
                    card_id: this.defaultCard,
                    ...this.paymentOptions,
                    ...addToken
                })
            }).then((res) => {
                this.isLoading = false
                console.log(res)
                if(res.data.success || res.data.status) {
                    this.done = true
                    this.curBtnColor = 'success'
                    this.curBtnText = this.successBtnText
                    this.$emit('cardAdded', res.data)
                } else {
                    this.cardError = res.data.error_message
                    this.cardErrorColor = 'error'
                    this.$emit('cardError', res.data)
                }

            }).catch(err => {
                this.isLoading = false
                console.log(err)
            })
        },
        cancel() {
            this.$emit('cancel')
        }
    }
}
</script>

<style lang="scss">

</style>