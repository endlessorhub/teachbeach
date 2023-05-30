<template>
<v-container grid-list-md text-xs-center>
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 lg6 class="text-xs-left">
          <v-layout align-top justify-center row wrap>
            <v-flex xs12 class="text-xs-left">
              <h3>{{ name }}</h3>
            </v-flex>
            <v-flex xs12 class="text-xs-left">
              {{classData && classData.groupClassSummary}}
            </v-flex>
            <v-flex v-if="datesToShow" xs12 class="text-xs-left">
              {{datesToShow}}
            </v-flex>
            <v-flex xs12 class="text-xs-left">
                <div class="product-title">
                    <b>{{productTitle}}</b>
                    <div v-if="serviceFee">{{productFee}}</div>
                    <div v-if="serviceFee">{{productTotal}}</div>
                </div>
                <div class="product-description">{{productDescription}}</div>
            </v-flex>
              <v-flex xs12 headline v-if="isSkipping">
                  Enrolling, please wait
                  <v-progress-circular
                      indeterminate
                      color="primary"
                  ></v-progress-circular>
              </v-flex>
            <v-flex xs12 class="text-xs-left" v-if="!isSkipping">
              Please choose card or add payment information
            </v-flex>
            <v-flex xs12 class="text-xs-left" v-if="!isSkipping">
                <v-list two-line>
                  <v-list-tile v-for="item in cards" :key="item.id">
                    <v-list-tile-action>
                        <v-btn v-if="!item.isExpired" flat icon @click="setCardActive(item.id)">
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
                        <v-btn v-else flat icon @click="deleteCard(item.id)" :disabled="isDeleteDisabled(item.id)">
                            <v-icon
                              color="red darken-2"
                            >
                              delete_outline
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

                  </v-list-tile>
                    <v-list-tile>
                    <v-list-tile-action>
                        OR
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <paypal />
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
                <v-alert
                  :value="!!cardError"
                  type="error"
                  color="platform-error"
                >
                  {{cardError}}
                </v-alert>
                <v-tooltip v-model="showPayBtnTooltip" top>
                    <template v-slot:activator="{ on }">
                        <v-btn 
                            :color="btnColor" 
                            :class='{"pay-with-stripe": true, "v-btn--disabled": isPaymentDisaled}'
                            @click="submit" 
                            :loading="isLoading" 
                            v-on="on"
                        >
                            <v-icon v-if="done" left>check_circle</v-icon>
                            {{btnText}}
                        </v-btn>
                    </template>
                    <span>{{ payBtnTooltip }}</span>
                </v-tooltip>
            </v-flex>
          </v-layout>
        </v-flex>
        <v-flex xs12 lg6 class="text-xs-left">
          <v-layout align-top justify-center row wrap>
            <v-flex xs12 class="text-xs-center">
                <v-card>
                  <v-layout row wrap>
                    <v-flex xs12 v-if="!isPrivate">
                      <v-img
                        width="50%"
                        v-if="classMedia"
                        :src="classMedia"
                        :aspect-ratio="1.25"
                        contain
                      ></v-img>
                    </v-flex>
                    <v-flex xs5>
                      <v-img
                        v-if="avatarUrl"
                        :src="avatarUrl"
                        height="125px"
                        :aspect-ratio="1.25"
                        contain
                      ></v-img>
                    </v-flex>
                    <v-flex xs7>
                      <v-card-title primary-title>
                        <div>
                          <div><b>{{teacherName}}</b></div>
                          <div>
                            <Rating object-type="teacher" :object-id="teacherId"></Rating>
                          </div>
                        </div>
                      </v-card-title>
                    </v-flex>
                  </v-layout>

                </v-card>

            </v-flex>
          </v-layout>
        </v-flex>
    </v-layout>

    <v-btn @click="back">Back</v-btn>
</v-container>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'
import { StripeElements, StripeElement } from 'vue-stripe-elements-plus'
import axios from 'axios'
import config from '@/config.js'
import moment from 'moment'
import { mapGetters } from 'vuex'
import Rating from '@/components/basic/Rating.vue'

export default {
    components: {
        StripeElements,
        StripeElement,
        Rating,
        Paypal: () => import('@/components/Paypal.vue'),
    },
    props: [
        'classData',
    ],

    data: () => ({
        btnText: 'Pay',
        btnColor: '',
        done: false,
        isLoading: false,
        persons: 1,
        numLessons: 0,
        lessonDuration: 0,
        duration: 0,
        package: null,
        selectedLessons: null,
        learnerNeeds: null,
        alerts: false,
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
        sourceCards: [],
        isSkipping: false,
        cardError: '',
        disabledDeletes: {},
        serviceFee: 0,
        showPayBtnTooltip: false,
    }),

    created: function () {
        this.stripeKey = this.$store.state.globals['stripe-key']
        if (this.$store.state.learnerData && this.$store.state.learnerData.package) {
            this.lessonDuration = this.$store.state.learnerData.lessonDuration
            this.duration = this.$store.state.learnerData.duration
            this.package = this.$store.state.learnerData.package
            this.selectedLessons = this.$store.state.learnerData.selectedLessons
            this.numLessons = this.$store.state.learnerData.numLessons
            this.learnerNeeds = this.$store.state.learnerData.learnerNeeds
            this.alerts = this.$store.state.learnerData.alerts
            this.persons = this.$store.state.learnerData.persons
            if(!this.costNumber && !this.$store.state.learnerData.id) {

                //create order skip to next step
                this.isSkipping = true
                axios.post('/api/enroll_class', {
                    'class': this.classData,
                    'package': this.package,
                    'name': this.name,
                    'cost': this.costNumber,
                    'learnerNeeds': '', //this.learnerNeeds, disabled due incorrect restoring from backend
                    'persons': this.persons,
                    'alerts': this.alerts,
                }).then(res => {
                    if(res.data.success) {
                        this.done = true
                        this.btnColor = 'success'
                        this.btnText = 'Congrats, you’re enrolled!'
                        setTimeout(() => {
                            this.$emit('next:step', {order_id: res.data.order_id})
                        }, 1000)
                    }
                }).catch(e => console.log(e))
                return
            }
        } else
            return this.$emit('prev:step')
        axios.post('/api/service_fee/', {
            amount: this.costNumber,
            class_id: this.classData.id,
        }).then((res) => {
            this.serviceFee = res.data.fee
            return axios.get('/api/payment_cards/')
        }).then(res => {
            this.defaultCard = res.data.default
            this.sourceCards = res.data.sources || []
            // hardcode expired
            /*
            _.each(this.sourceCards, (v, i) => {
                if (i === 0) {
                    v.exp_month = 12
                    v.exp_year = 2019
                }
                if (i === 1) {
                    v.exp_month = 1
                    v.exp_year = 2020
                }
                if (i === 2) {
                    v.exp_month = 2
                    v.exp_year = 2020
                }
            })
            */
        })
    },

    computed: {
        ...mapGetters([
            'isMember',
        ]),
        isPaymentDisaled() {
            return !this.complete && this.defaultCard == 'new_card'
        },
        payBtnTooltip() {
            if (this.complete) return 'Confirm payment';
            return 'Please fill in correct credit card information (including postal code if required)';
        },
        membershipMode() {
            return this.isMemberOfClass ? 'isMember' : 'regular';
        },
        classMembershipId() {
            return this.classData ? this.classData.teacher.user.membership : null
        },
        isMemberOfClass() {
            return this.isMember(this.classMembershipId)
        },
        datesToShow() {
            if(!this.classData.flexible_dates) {
                return this.classData.schedule_dates.map(v => utils.stringToDate(v.date).toLocaleString('en-us', {
                    day: 'numeric',
                    month: 'short',
                })).join(', ');
            }
            return '';
        },
        cards() {
            const now = moment()
            return _.map(this.sourceCards, c => _.assign({
                isActive: this.defaultCard == c.id,
                isExpired: c.exp_year < now.year() || c.exp_year == now.year() && c.exp_month < (now.month()+1),
            }, c))
        },
        isPrivate() {
            if(!this.classData)
                return null
            return this.classData.is_private
        },
        teacherName() {
            if(!this.classData)
                return ''
            return this.classData.teacher ? this.classData.teacher.first_name+' '+this.classData.teacher.last_name : ''
        },
        teacherId() {
            if(!this.classData)
                return ''
            return this.classData.teacher ? this.classData.teacher.id : ''
        },
        name() {
            if(!this.classData)
                return ''
            return this.classData.is_private ? this.classData.private_className : this.classData.name
        },
        cost() {
            return utils.formatPrice(this.costNumber, this.package.currency)
        },
        costNumber() {
            const useMemberPrice = utils.useMemberPrice(this.isMemberOfClass ? 'isMember' : '', this.package); //this.isMemberOfClass && (this.package.memberTotalPrice === '0' || this.package.memberTotalPrice)
            if(this.classData.is_private && this.package.isSubscription) {
                return Number(useMemberPrice ? this.package.memberTotalPrice : this.package.rateBilled)
            }
            if (this.package && this.package.type === 'limitedSubscription') {
                return Number(useMemberPrice ? this.package.memberPricePerInterval : this.package.pricePerInterval);
            }
            return Number(this.classData.is_private
                ? (useMemberPrice ? this.package.memberTotalPrice : this.package.totalPrice)*(this.package.isPricePerPerson ? this.persons : 1)
                : (useMemberPrice ? this.package.memberTotalPrice : this.package.totalPrice)*(this.persons || 1))
        },
        avatarUrl() {
            if(!this.classData)
                return ''
            return this.classData.teacher && this.classData.teacher.media ? this.classData.teacher.media : ''
        },
        classMedia() {
            if(!this.classData)
                return ''
            return this.classData.master_media ? this.classData.master_media : ''
        },
        lessonsText() {
            if(!this.package)
                return ''
            return this.package.numberOfLessons
        },
        productTitle() {
            if(this.package && this.package.type === 'limitedSubscription') {
                return classHelper.packageFormatter(this.package, this.membershipMode);
            }
            if(this.package && this.package.isPrivate) {
                if(this.package.isSubscription)
                    return classHelper.packageFormatter(this.package, this.membershipMode)
                return `${this.serviceFee ? '' : 'Total '}${this.cost} ${this.persons > 1 ? `for ${this.persons} people` : ''} for ${this.package.lessonLength.text.replace('hours', 'hour')} class${this.lessonsText == 1 ? '' : 'es'} ${this.lessonsText} time${this.lessonsText == 1 ? '' : 's'}`
            } else if(this.package) {
                return `${this.serviceFee ? '' : 'Total '}${this.cost} ${this.persons > 1 ? `for ${this.persons} people` : ''} for ${this.lessonsText} class${this.lessonsText == 1 ? '' : 'es'}`
            }
        },
        productFee() {
            return `Service fee ${utils.formatPrice(this.serviceFee, this.package.currency)}`
        },
        productTotal() {
            return `Total ${utils.formatPrice(this.costNumber + this.serviceFee, this.package.currency)}`
        },
        productDescription() {
            if(this.package && this.package.description)
                return this.package.description
            return ''
        }
    },

    methods: {
        onCardChange(event) {
            this.complete = event.complete;
        },
        back() {
            this.$emit('prev:step')
        },
        setCardActive(id) {
            this.defaultCard = id
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
            if(this.done || this.isPaymentDisaled)
                return
            this.isLoading = true;
            this.cardError = '';
            // createToken returns a Promise which resolves in a result object with
            // either a token or an error key.
            // See https://stripe.com/docs/api#tokens for the token object.
            // See https://stripe.com/docs/api#errors for the error object.
            // More general https://stripe.com/docs/stripe.js#stripe-create-token.
            const createToken = () => {
                const groupComponent = this.$refs.elms
                const cardComponent = this.$refs.card
                const cardElement = cardComponent.stripeElement
                return groupComponent.instance.createToken(cardElement);
            }
            (() => this.defaultCard != 'new_card' ? Promise.resolve({}) : createToken())().then(data => {
                console.log(data)
                return axios.post('/api/stripe/add_card', {
                    'class': this.classData,
                    'lessonDuration': this.lessonDuration,
                    'duration': this.duration,
                    'package': this.package,
                    'selectedLessons': this.selectedLessons,
                    'numLessons': this.numLessons,
                    'name': this.name,
                    'rate': this.classData.rate,
                    'cost': this.costNumber,
                    'serviceFee': this.serviceFee,
                    'learnerNeeds': '', //this.learnerNeeds, disabled due to errors from incorrectly restored data
                    'alerts': this.alerts,
                    'token': data.token,
                    'card_id': this.defaultCard,
                    'persons': this.persons,
                })
            }).then((res) => {
                this.isLoading = false
                console.log(res)
                if(res.data.success) {
                    //checkout tracking
                    fbq('trackCustom', 'studentCheckout')
                    gtag('event', 'conversion', { 'send_to': 'AW-964524864/q9rOCI6b2NcBEMD29csD', 'event_callback': () => {} });
                    this.done = true
                    this.btnColor = 'success'
                    this.btnText = 'Congrats, you’re enrolled!'
                    setTimeout(() => {
                        this.$emit('next:step', {order_id: res.data.order_id})
                    }, 1000)
                } else {
                    this.cardError = res.data.error_message
                }
            }).catch(err => {
                this.isLoading = false
                console.log(err)
            })
            //this.$emit('next:step')
        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">

.StripeElement {
  box-sizing: border-box;

  height: 40px;

  padding: 10px 12px;

  border: 1px solid transparent;
  border-radius: 4px;
  background-color: white;

  box-shadow: 0 1px 3px 0 #e6ebf1;
  -webkit-transition: box-shadow 150ms ease;
  transition: box-shadow 150ms ease;
}

.StripeElement--focus {
  box-shadow: 0 1px 3px 0 #cfd7df;
}

.StripeElement--complete {
  border-color: green;
}

.StripeElement--invalid {
  border-color: #fa755a;
}

.StripeElement--webkit-autofill {
  background-color: #fefde5 !important;
}
.v-btn--disabled.pay-with-stripe {
    pointer-events: auto;
}
</style>