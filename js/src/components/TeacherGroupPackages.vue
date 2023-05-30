<template>
  <div class="teacher-group-package">
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-snackbar
      v-model="snackbar"
      color="platform-error"
      timeout="500000"
      :top="snackbarTop"
      :bottom="snackbarBottom"
    >
      {{ error }}
      <v-btn
        dark
        flat
        @click="error = ''"
      >
        Close
      </v-btn>
    </v-snackbar>
    <v-container grid-list-md text-xs-center>

        <v-dialog
          v-model="numberOfLessonsAlert"
          max-width="290"
        >
          <v-card>
            <v-card-title class="headline">
                  <v-spacer></v-spacer>
                  <v-btn icon @click.native="numberOfLessonsAlert = false" color="gray darken-1">
                    <v-icon>close</v-icon>
                  </v-btn>
            </v-card-title>

            <v-card-text>
              Whoops! The number of lessons in your package exceeds the {{scheduleDates ? scheduleDates.length : ''}} number of days selected.
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>

              <v-btn
                color="green darken-1"
                flat="flat"
                @click="back(); numberOfLessonsAlert=false"
              >
                Add available Days
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-layout v-if="isWorkshop" align-top justify-center row wrap>
              <v-flex xs12 class="text-xs-center" ><h1>{{ title }}</h1></v-flex>
              <v-flex xs4 class="text-xs-center" >
                <v-select
                    :disabled="isEditDisabled"
                    v-model="currency"
                    :items="currencies"
                    label="Currency"
                    item-text="label"
                    item-value="id"
                ></v-select>
              </v-flex>
              <v-flex xs8 class="text-xs-left" >
                <div style="width: 200px;">
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="dropInRate"
                    label="Drop in rate (optional)"
                    hide-details
                    outline
                    :error-messages="dropInRateErrors"
                    @input="$v.dropInRate.$touch()"
                    @blur="$v.dropInRate.$touch()"
                  ></v-text-field>
                </div>
              </v-flex>
              <v-flex xs12 class="text-xs-left" >
                <v-list one-line>
                  <template v-for="(p, index) in customPackagesList">
                    <v-list-tile
                       v-if="index < customPackagesList.length-1"
                      :key="p.key"
                      avatar
                      ripple
                    >
                      <v-list-tile-action>
                        <div :disabled="isEditDisabled" class="v-chip__close remove-weekday" @click.stop="removeCustomPackage(index)"><i aria-hidden="true" class="v-icon material-icons theme--light">cancel</i></div>
                      </v-list-tile-action>
                      <v-list-tile-content>
                        <v-list-tile-title>Package{{ p.key }} - {{ p.numberOfLessons}} time{{p.numberOfLessons == 1 ? '' : 's'}} for {{p.formattedPrice}}
                            <span v-if="p.isTrial">
                                <v-icon color="success">check_circle</v-icon>Trial,
                            </span>
                        </v-list-tile-title>
                        <v-list-tile-sub-title>{{p.isGlobalPackage ? 'Students can use this package for any class ' : ''}} {{p.description}}</v-list-tile-sub-title>
                      </v-list-tile-content>

                    </v-list-tile>
                    <v-divider
                      v-if="index + 1 < customPackagesList.length"
                      :key="index"
                    ></v-divider>
                  </template>

                </v-list>
                </v-flex>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastCustomPackage.totalPrice"
                    label="Total Price"
                    v-on:input="lastCustomPackage={totalPrice: $event}"
                    :error-messages="customTotalPriceError"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastCustomPackage.numberOfLessons"
                    v-on:input="lastCustomPackage={numberOfLessons: $event}"
                    label="# of days"
                    :readonly="!lastCustomPackage.isTrial"
                    :class="lastCustomPackage.isTrial ? 'platform-green' : ''"
                    :outline="lastCustomPackage.isTrial"
                  >
                      <template v-slot:append>
                          <v-tooltip
                            content-class="teachbeach-tooltip"
                            top
                            v-model="tooltipNumLessons"
                          >
                            <template v-slot:activator="{on}">
                              <v-icon @click="tooltipNumLessons = !tooltipNumLessons">help_outline</v-icon>
                            </template>
                              All classes are required (unless this is trial package). <a @click="back">Change?</a>
                          </v-tooltip>
                      </template>
                  </v-text-field>
                </v-flex>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    :value="formatPrice(lastCustomPackage.perLesson)"
                    label="$per lesson"
                    readonly
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastCustomPackage.description"
                    v-on:input="lastCustomPackage={description: $event}"
                    label="Description (optional)"
                  ></v-text-field>
                </v-flex>
                <v-flex xs6 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastCustomPackage.memberTotalPrice"
                    label="Member rate for this package"
                    v-on:input="lastCustomPackage={memberTotalPrice: $event}"
                  ></v-text-field>
                </v-flex>
                <v-flex xs6 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    :value="formatPrice(lastCustomPackage.memberPerLesson)"
                    label="Member $per lesson"
                    readonly
                  ></v-text-field>
                </v-flex>

                <v-flex xs12 class="text-xs-left" >
                  <v-checkbox
                    :disabled="isEditDisabled"
                    v-model="lastCustomPackage.isTrial"
                    v-on:change="lastCustomPackage={isTrial: $event}"
                  >
                      <template v-slot:label>
                        <div>
                          This is a one time trial rate
                          <v-tooltip top>
                            <template v-slot:activator="{ on }">
                              <v-icon v-on="on">help_outline</v-icon>
                            </template>
                              <span>User can book it only once, lesson is free if total price is empty</span>
                          </v-tooltip>
                        </div>
                      </template>
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 class="text-xs-center" >
                    <v-btn @click="addCustomPackage" :disabled="isEditDisabled">+ Pricing Option</v-btn>
                </v-flex>
                <v-flex xs12 md6 class="text-xs-left" >
                    <v-switch v-if="canBook" v-model="canPay" label="Students can pay on this site"></v-switch>
                    <v-text-field
                      v-model="canBookUrl"
                      label="URL where student can book this class"
                      v-if="!canBook"
                    ></v-text-field>
                </v-flex>
</v-layout>
        <v-layout v-else align-top justify-center row wrap>
              <v-flex xs12 class="text-xs-center" ><h1>{{ title }}</h1></v-flex>
              <v-flex xs4 class="text-xs-center" >
                <v-select
                    :disabled="isEditDisabled"
                    v-model="currency"
                    :items="currencies"
                    label="Currency"
                    item-text="label"
                    item-value="id"
                ></v-select>
              </v-flex>
              <v-flex xs8 class="text-xs-left" >
                <div style="width: 200px;">
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="dropInRate"
                    label="Drop in rate (optional)"
                    outline
                    :error-messages="dropInRateErrors"
                    @input="$v.dropInRate.$touch()"
                    @blur="$v.dropInRate.$touch()"
                  ></v-text-field>
                </div>
              </v-flex>
              <v-flex v-if="standardPackagesList.length" xs12 class="text-xs-left" >
                  <h3>Package rate</h3>
                <v-list one-line>
                  <template v-for="(p, index) in standardPackagesList">
                    <v-list-tile
                       v-if="index < standardPackagesList.length-1 || isSubscriptionCreating"
                      :key="p.key"
                      avatar
                      ripple
                    >
                      <v-list-tile-action>
                        <div :disabled="isEditDisabled" class="v-chip__close remove-weekday" @click.stop="removeStandardPackage(index)"><i aria-hidden="true" class="v-icon material-icons theme--light">cancel</i></div>
                      </v-list-tile-action>
                      <v-list-tile-content>
                        <v-list-tile-title>Package{{ p.key }} - {{ p.numberOfLessons}} time{{p.numberOfLessons == 1 ? '' : 's'}} for {{p.formattedPrice}}
                            <span v-if="p.isTrial">
                                <v-icon color="success">check_circle</v-icon>Trial,
                            </span>
                        </v-list-tile-title>
                        <v-list-tile-sub-title>{{p.isGlobalPackage ? 'Students can use this package for any class ' : ''}} {{p.description}}</v-list-tile-sub-title>
                      </v-list-tile-content>

                    </v-list-tile>
                    <v-divider
                      v-if="index + 1 < standardPackagesList.length"
                      :key="index"
                    ></v-divider>
                  </template>

                </v-list>
              </v-flex>
              <v-flex v-if="subscriptionPackagesList.length" xs12 class="text-xs-left" >
                <h3>{{ isPremiumCommunity ? 'Premium community rate' : '' }}</h3>
                <v-list one-line>
                  <template v-for="(p, index) in subscriptionPackagesList">
                    <v-list-tile
                       v-if="index < subscriptionPackagesList.length-1 || !isSubscriptionCreating"
                      :key="p.key"
                      avatar
                      ripple
                    >
                      <v-list-tile-action>
                        <div :disabled="isEditDisabled" class="v-chip__close remove-weekday" @click.stop="removeCustomPackage(index)"><i aria-hidden="true" class="v-icon material-icons theme--light">cancel</i></div>
                      </v-list-tile-action>
                      <v-list-tile-content>
                        <v-list-tile-title>{{ p.formattedPrice }} {{ p.intervalDisplay }} - {{ p.numberOfIntervals}} time{{p.numberOfIntervals == 1 ? '' : 's'}}
                            <span v-if="p.isTrial">
                                <v-icon color="success">check_circle</v-icon>Trial,
                            </span>
                        </v-list-tile-title>
                        <v-list-tile-sub-title>{{p.description}}</v-list-tile-sub-title>
                      </v-list-tile-content>

                    </v-list-tile>
                    <v-divider
                      v-if="index + 1 < subscriptionPackagesList.length"
                      :key="index"
                    ></v-divider>
                  </template>

                </v-list>
              </v-flex>
              <v-flex v-if="!isPremiumCommunity" xs12 class="text-xs-left" >
                <v-radio-group v-model="creatingPackageType">
                  <v-radio
                    :disabled="isEditDisabled"
                    label="Standard"
                    value="standard"
                  ></v-radio>
                  <v-radio
                    :disabled="isEditDisabled"
                    label="Subscription"
                    value="subscription"
                  ></v-radio>
                </v-radio-group>
              </v-flex>
              <template v-if="isSubscriptionCreating">
                  <v-flex xs6 md4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.pricePerInterval"
                        :label="'Price per '+(lastCustomPackage.interval || 'month')"
                        v-on:input="lastCustomPackage={pricePerInterval: $event, type: 'limitedSubscription'}"
                        :error-messages="lastCustomPackagePricePerIntervalError"
                      ></v-text-field>
                  </v-flex>
                  <v-flex xs6 md4 class="text-xs-left" >
                      <v-select
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.interval"
                        :items="[{text: 'Monthly', value: 'month'}, {text: 'Weekly', value: 'week'}]"
                        label="Interval"
                        v-on:change="lastCustomPackage={interval: $event, type: 'limitedSubscription'}"
                      ></v-select>
                  </v-flex>
                  <v-flex xs6 md4 class="text-xs-left" >
                    <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.memberPricePerInterval"
                        label="Member rate for this package"
                        v-on:input="lastCustomPackage={memberPricePerInterval: Number.isNaN($event) || $event === '' ? '' : Number($event), type: 'limitedSubscription'}"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs6 md4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.numberOfIntervals"
                        :label="'Number of '+(lastCustomPackage.interval || 'month')+'s'"
                        v-on:input="lastCustomPackage={numberOfIntervals: $event, type: 'limitedSubscription'}"
                        :error-messages="lastCustomPackageNumberOfIntervalsError"
                      ></v-text-field>
                  </v-flex>
              </template>
              <template v-else>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.totalPrice"
                    label="Total Price"
                    v-on:input="lastStandardPackage={totalPrice: $event}"
                    :error-messages="standardTotalPriceError"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.numberOfLessons"
                    label="# of days"
                    v-on:input="standardNumOfLessonsInput"
                    :error-messages="standardNumOfLessonsError"
                  ></v-text-field>
                </v-flex>
                <v-flex xs4 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.perLesson"
                    label="$per lesson"
                    v-on:input="standardPerLessonInput"
                    readonly
                    :error-messages="standardPerLessonError"
                  ></v-text-field>
                </v-flex>
                <v-flex xs6 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.memberTotalPrice"
                    label="Member rate for this package"
                    v-on:input="lastStandardPackage={memberTotalPrice: $event}"
                  ></v-text-field>
                </v-flex>
                <v-flex xs6 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.memberPerLesson"
                    label="Member $per lesson"
                    readonly
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 md3 class="text-xs-left" >
                  <v-text-field
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.description"
                    v-on:input="lastStandardPackage={description: $event}"
                    label="Description (optional)"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12 class="text-xs-left" >
                  <v-checkbox
                    :disabled="isEditDisabled"
                    v-model="lastStandardPackage.isTrial"
                    v-on:change="lastStandardPackage={isTrial: $event}"
                  >
                      <template v-slot:label>
                        <div>
                          This is a one time trial rate
                          <v-tooltip top>
                            <template v-slot:activator="{ on }">
                              <v-icon v-on="on">help_outline</v-icon>
                            </template>
                              <span>User can book it only once, lesson is free if total price is empty</span>
                          </v-tooltip>
                        </div>
                      </template>
                  </v-checkbox>
                </v-flex>
                <v-flex xs12 md6 class="text-xs-left" >
                    <v-radio-group v-model="lastStandardPackage.charge" hide-details row v-on:change="lastStandardPackage={charge: $event}" >
                      <v-radio
                              :disabled="isEditDisabled"
                        label="Charge upfront"
                        value="upfront"
                      ></v-radio>
                      <v-radio
                              :disabled="isEditDisabled"
                        label="Charge monthly"
                        value="monthly"
                      ></v-radio>
                      <v-radio
                              :disabled="isEditDisabled"
                        label="Charge per lesson"
                        value="per_lesson"
                      ></v-radio>
                    </v-radio-group>

                    <v-checkbox
                        :disabled="isEditDisabled"
                        v-model="lastStandardPackage.isGlobalPackage"
                        label="Students can use this package for any class"
                        hide-details
                        v-on:change="lastStandardPackage={isGlobalPackage: $event}"
                    ></v-checkbox>
                </v-flex>
              </template>
              <v-flex xs12 md6 class="text-xs-left" >
                <v-switch v-if="!canBook" v-model="isPriceHidden" label="Toggle on to hide price"></v-switch>
                <v-switch v-if="canBook" v-model="canPay" label="Students can pay on this site"></v-switch>
                <v-text-field
                  v-model="canBookUrl"
                  label="URL where student can book this class (optional)"
                  v-if="!canBook"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 class="text-xs-center" >
                <v-btn @click="addPackage" :disabled="isEditDisabled">+ Pricing Option</v-btn>
              </v-flex>
        </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </div>
</template>

<script>
import DateSelect from '@/components/basic/DateSelect.vue'
import utils from '@/lib/utils'
import { validationMixin } from 'vuelidate'
import { numeric, required, minValue } from 'vuelidate/lib/validators'
import _ from 'lodash'

import axios from 'axios'

export default {
    mixins: [validationMixin],
    validations: {
        dropInRate: {numeric},
    },
    props: {
        //isWorkshop: false,
        untilDate: null,
        startDate: null,
        weekdaysScheduled: [],
        scheduleDatesExcluded: [],
        daySelectType: null,
    },

    components: {
        DateSelect,
    },

    data: () => ({
        isLoading: false,
        isWorkshop: false,
        standardPackages: [],
        customPackages: [],
        currency: 'usd',
        currencies: [],
        currencyDict: {},
        dropInRate: null,
        numberOfLessonsAlert: false,
        activeNumberOfLessons: null,
        scheduleDates: [],
        standardTotalPriceError: [],
        standardNumOfLessonsError: [],
        standardPerLessonError: [],
        customTotalPriceError: [],
        enrolled: null,
        canBook: null,
        canPay: null,
        canBookUrl: '',
        isPriceHidden: false,
        tooltipNumLessons: false,
        error: '',
        errorPosition: 'top',
        isPremiumCommunity: false,
        lastCustomPackageIntervals: [],
        lastCustomPackagePricePerIntervalError: [],
        lastCustomPackageNumberOfIntervalsError: [],
        creatingPackageType: 'standard',
    }),

    created: function () {
        let _this = this
        this.currencies = utils.getCurrencyList()
        this.currencyDict = _.keyBy(utils.getCurrencyList(), 'id')
        if (this.$store.state.teacherGroupClass) {
            this.enrolled = _this.$store.state.teacherGroupClass.enrolled
            this.standardPackages = _.uniqBy(_this.$store.state.teacherGroupClass.standardPackages || [], p => {
                return p.numberOfLessons+'_'+p.totalPrice+'_'+p.isTrial
            })
            this.customPackages = _.filter(_this.$store.state.teacherGroupClass.customPackages || [], v => !v.isPrivate)
            this.currency = _this.$store.state.teacherGroupClass.currency || 'usd'
            this.dropInRate = isNaN(_this.$store.state.teacherGroupClass.dropInRate) ? null : Math.round(_this.$store.state.teacherGroupClass.dropInRate)
            this.isPriceHidden = this.$store.state.teacherGroupClass.isPriceHidden
            this.canBook = _this.$store.state.teacherGroupClass.canBook
            this.canPay = typeof this.$store.state.teacherGroupClass.canPay == 'undefined' ? this.canBook : this.$store.state.teacherGroupClass.canPay
            this.canBookUrl = this.$store.state.teacherGroupClass.canBookUrl || ''
            this.isWorkshop = !this.$store.state.teacherGroupClass.flexibleDates
            this.scheduleDates = this.$store.state.teacherGroupClass.scheduleDates
            if (this.isWorkshop) {
                _.each(this.customPackages, p => p.numberOfLessons = this.scheduleDates.length)
            }
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
        }
    },

    mounted() {

    },

    computed: {
        isSubscriptionCreating() {
          return this.isPremiumCommunity || this.creatingPackageType === 'subscription'
        },
        title() {
            return this.isPremiumCommunity ? 'Create a rate for your premium community' : 'Create package rates';
        },
        snackbarTop() {
            return this.errorPosition === 'top'
        },
        snackbarBottom() {
            return this.errorPosition === 'bottom'
        },
        snackbar: {
            get() {
                return !!this.error
            },
            set(v) {
                if(!v)
                    this.error = ''
            },
        },
        standardPackagesList() {
            return _.map(this.standardPackages, v => _.assign({}, v, {
                formattedPrice: utils.formatPrice(v.totalPrice, v.currency),
                formattedMemberPrice: utils.formatPrice(v.memberTotalPrice, v.currency),
            }))
        },
        subscriptionPackages() {
            return this.customPackages.filter(p => p.type === 'limitedSubscription');
        },
        subscriptionPackagesList() {
            const intervalsDisplay = {
                month: 'monthly',
                week: 'weekly',
            };
            return this.subscriptionPackages.map(p => ({
                formattedPrice: utils.formatPrice(p.pricePerInterval, p.currency),
                formattedMemberPrice: utils.formatPrice(p.memberPricePerInterval, p.currency),
                intervalDisplay: intervalsDisplay[p.interval],
                ...p,
            }));
        },
        customPackagesList() {
            return this.customPackages.filter(p => p.type !== 'limitedSubscription').map(p => ({
                ...p,
                formattedPrice: utils.formatPrice(p.totalPrice, p.currency),
                formattedMemberPrice: utils.formatPrice(p.memberTotalPrice, p.currency),
            }))
        },
        dropInRateErrors() {
            const errors = []
            if (!this.$v.dropInRate.$dirty) return errors
            !this.$v.dropInRate.numeric && errors.push('Please use numbers only')
            return errors
        },
        isEditDisabled() {
            // enabled by Alisa's request
            return false
            //return Boolean(this.isWorkshop && this.enrolled && this.enrolled.length)
        },

        lastStandardPackage: {
            set(v) {
                if(!this.standardPackages.length) {
                    this.standardPackages.push({
                        numberOfLessons: '',
                        perLesson: '',
                        currency: this.currency,
                        totalPrice: '',
                        memberTotalPrice: '',
                        memberPerLesson: '',
                        charge: 'upfront',
                        isGlobalPackage: false,
                        description: '',
                        isTrial: false,
                        key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
                    })
                }

                let last = _.last(this.standardPackages)
                if(v.totalPrice) {
                    v.totalPrice = String(v.totalPrice).replace(/[^\d]+/g, '')
                    v.perLesson = !v.totalPrice || !Number(last.numberOfLessons) ? '' : Math.round(v.totalPrice / last.numberOfLessons)
                }
                if(v.memberTotalPrice) {
                    v.memberTotalPrice = String(v.memberTotalPrice).replace(/[^\d]+/g, '')
                    v.memberPerLesson = !v.memberTotalPrice || !Number(last.numberOfLessons) ? '' : Math.round(v.memberTotalPrice / last.numberOfLessons)
                }
                _.each(v, (newVal, k) => {
                    last[k] = newVal
                })
                if(last.numberOfLessons) {
                    this.activeNumberOfLessons = last.numberOfLessons
                }
                if(last.totalPrice && last.numberOfLessons && last.currency) {
                    last.totalPrice = String(last.totalPrice).replace(/[^\d]+/g, '')
                    last.numberOfLessons = String(last.numberOfLessons).replace(/[^\d]+/g, '')
                    last.perLesson = !String(last.totalPrice) || !Number(last.numberOfLessons) ? '' : Math.round(last.totalPrice / last.numberOfLessons)
                }
                if(last.memberTotalPrice && last.numberOfLessons && last.currency) {
                    last.memberTotalPrice = String(last.memberTotalPrice).replace(/[^\d]+/g, '')
                    last.numberOfLessons = String(last.numberOfLessons).replace(/[^\d]+/g, '')
                    last.memberPerLesson = !String(last.memberTotalPrice) || !Number(last.numberOfLessons) ? '' : Math.round(last.memberTotalPrice / last.numberOfLessons)
                }
            },
            get() {
                return _.last(this.standardPackages) || {
                    numberOfLessons: '',
                    perLesson: '',
                    currency: this.currency,
                    totalPrice: '',
                    memberTotalPrice: '',
                    memberPerLesson: '',
                    charge: 'upfront',
                    isGlobalPackage: false,
                    description: '',
                    isTrial: false,
                    key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
                }
            },
        },
        lastCustomPackage: {
            set(v) {
                if (v.type === 'limitedSubscription') {
                    const last = this.getLastLimitedSubscriptionItem();
                    if (!this.customPackages.includes(last))
                        this.customPackages.push(last);
                    Object.keys(v).forEach(k => { last[k] = v[k] })
                    return;
                }
                let numberOfLessons = ''
                let perLesson = ''
                let memberPerLesson = ''
                if (this.daySelectType == 'monthly') {
                    numberOfLessons = this.scheduleDates.length
                } else {
                    numberOfLessons = utils.getCalendarDatesForPeriod(this.startDate, this.untilDate, this.weekdaysScheduled, this.startDate, this.untilDate, this.scheduleDatesExcluded).length
                }
                if(!this.customPackages.length) {
                    this.customPackages.push({
                        description: '',
                        currency: this.currency,
                        totalPrice: '',
                        key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                        numberOfLessons: numberOfLessons,
                        perLesson: perLesson,
                        memberTotalPrice: '',
                        memberPerLesson,
                        isTrial: false,
                    })
                }
                let last = _.last(this.customPackages)
                if(v.totalPrice) {
                    last.numberOfLessons = numberOfLessons
                    v.totalPrice = String(v.totalPrice).replace(/[^\d]+/g, '')
                    v.perLesson = !v.totalPrice || !Number(last.numberOfLessons) ? '' : Math.round(v.totalPrice / last.numberOfLessons)
                }
                if(v.memberTotalPrice && numberOfLessons) {
                    last.numberOfLessons = numberOfLessons
                    v.memberTotalPrice = String(v.memberTotalPrice).replace(/[^\d]+/g, '')
                    v.memberPerLesson = !v.memberTotalPrice || !Number(last.numberOfLessons) ? '' : Math.round(v.memberTotalPrice / last.numberOfLessons)
                }
                if(!v.totalPrice && 'totalPrice' in v) {
                    // drop package for fixed dates because it is only one variable meaningful - totalPrice
                    v.perLesson = ''
                    v.numberOfLessons = ''
                }
                if(!v.memberTotalPrice && 'memberTotalPrice' in v) {
                    v.memberPerLesson = ''
                }
                if (v.numberOfLessons) {
                    v.numberOfLessons = Number(v.numberOfLessons)
                    last.totalPrice = String(last.totalPrice).replace(/[^\d]+/g, '')
                    last.perLesson = !Number(last.totalPrice) || !Number(v.numberOfLessons) ? '' : Math.round(last.totalPrice / v.numberOfLessons)
                    last.memberTotalPrice = String(last.memberTotalPrice).replace(/[^\d]+/g, '')
                    last.memberPerLesson = !Number(last.memberTotalPrice) || !Number(v.numberOfLessons) ? '' : Math.round(last.memberTotalPrice / v.numberOfLessons)
                }
                _.each(v, (newVal, k) => {
                    last[k] = newVal
                })
            },
            get() {
                if (this.isPremiumCommunity) {
                    return this.getLastLimitedSubscriptionItem();
                }
                let numberOfLessons = ''
                let perLesson = ''
                let memberPerLesson = ''
                /*
                if (this.daySelectType == 'monthly') {
                    numberOfLessons = this.scheduleDates.length
                } else {
                    numberOfLessons = utils.getCalendarDatesForPeriod(this.startDate, this.untilDate, this.weekdaysScheduled, this.startDate, this.untilDate, this.scheduleDatesExcluded).length
                }
                _.each(this.customPackages, v => {
                    const totalPrice = String(v.totalPrice).replace(/[^\d]+/g, '')
                    v.numberOfLessons = numberOfLessons
                    v.perLesson = totalPrice && numberOfLessons ? Math.round(totalPrice / numberOfLessons) : ''
                })
                if(!_.last(this.customPackages) || !_.last(this.customPackages).isTrial && !_.last(this.customPackages).totalPrice) {
                    return {
                        description: '',
                        currency: '',
                        totalPrice: '',
                        key: _.uniqueId('empt_cust_pack'),
                        numberOfLessons: '',
                        perLesson: '',
                        isTrial: false,
                    }
                }
                */
                return _.last(this.customPackages) || {
                    description: '',
                    currency: this.currency,
                    totalPrice: '',
                    key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                    numberOfLessons: numberOfLessons,
                    perLesson: perLesson,
                    memberTotalPrice: '',
                    memberPerLesson,
                    isTrial: false,
                }
            },
        },
    },

    methods: {
        getLastLimitedSubscriptionItem() {
            return [...this.customPackages].reverse().find(p => p.type === 'limitedSubscription') || {
                description: '',
                currency: this.currency,
                key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                interval: 'month',
                numberOfIntervals: '',
                pricePerInterval: '',
                isTrial: false,
            };
        },
        formatPrice(price) {
            if(!price || price-0 === 0)
                return ''
            return utils.formatPrice(price, this.currency)
        },
        resetErrors() {
            this.customTotalPriceError = []
            this.standardNumOfLessonsError = []
            this.standardPerLessonError = []
            this.standardTotalPriceError = []
            this.lastCustomPackagePricePerIntervalError = []
            this.lastCustomPackageNumberOfIntervalsError = []
        },
        checkPackageErrors(packageData) {
            let res = false
            if(!String(packageData.totalPrice)) {
                this.customTotalPriceError = ['Please enter the package rate first (zero for free)']
                res = true
            }
            if(!this.isWorkshop && !packageData.numberOfLessons) {
                this.standardNumOfLessonsError = ["Number of lessons can't be empty"]
                res = true
            }
            /*
            if(!packageData.isTrial && !this.isWorkshop && !packageData.perLesson) {
                this.standardPerLessonError = ["Per lesson can't be empty"]
                res = true
            }
            */
            if (!this.isWorkshop && packageData && packageData.numberOfLessons) {
                this.checkNumberOfDays(packageData.numberOfLessons)
                res = res || this.numberOfLessonsAlert
            }
            return res
        },
        checkErrors() {
            this.resetErrors()
            if (!this.isWorkshop && (this.isPremiumCommunity || this.creatingPackageType === 'subscription')) {
                if (!this.checkLimitedSubscriptionErrors(this.lastCustomPackage)) {
                    if (this.subscriptionPackagesList.length > 1) {
                        this.customPackages = this.subscriptionPackages.slice(0, -1);
                        return this.checkLimitedSubscriptionErrors(this.lastCustomPackage);
                    }
                    return false
                }
                return true
            }
            let checkPackage = this.isWorkshop ? this.lastCustomPackage : this.lastStandardPackage
            let packagesArr = this.isWorkshop ? this.customPackages : this.standardPackages
            const meaningPackages = _.filter(packagesArr, p => (String(p.totalPrice) || Number(p.numberOfLessons) || p.isTrial))
            if(_.some(meaningPackages, 'isTrial') && !_.some(meaningPackages, p => !p.isTrial)) {
                this.errorPosition = 'bottom'
                this.error = "Great! Now you have a trial lesson. Please add a regular class package that students can buy after the trial."
                return false
            }
            if(this.checkPackageErrors(checkPackage)) {
                // true means error
                if (packagesArr.length > 1) {
                    if (String(checkPackage.totalPrice) || Number(checkPackage.numberOfLessons) || checkPackage.isTrial) {
                        return false
                    } else {
                        packagesArr.splice(packagesArr.length-1, 1)
                        return true
                    }
                } else {
                    return false
                }
            }
            return true
        },
        saveData() {
            this.$store.commit('setGroupClass', {
                currency: this.currency,
                standardPackages: _.filter(this.standardPackages, v => v.numberOfLessons),
                customPackages: this.subscriptionPackages.concat(_.filter(this.customPackages, v => v.numberOfLessons)),
                dropInRate: this.dropInRate,
                canPay: this.canPay,
                canBookUrl: this.canBookUrl,
                isPriceHidden: this.isPriceHidden,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            if(!this.checkErrors())
                return
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.saveData()
            this.$emit('next:step')
        },
        clear () {

        },
        addPackage() {
            if (!this.isPremiumCommunity && this.creatingPackageType !== 'subscription') {
                return this.addStandardPackage();
            }
            if(!this.checkLimitedSubscriptionErrors(this.lastCustomPackage))
                return;
            this.customPackages.push({
                ...Object.keys(this.lastCustomPackage).reduce((acc, k) => ({...acc, [k]: ''}), {}),
                key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                type: 'limitedSubscription',
                isGlobalPackage: false,
                currency: this.currency,
                isTrial: false,
            })
        },
        checkLimitedSubscriptionErrors(packageData) {
            let res = true
            this.lastCustomPackagePricePerIntervalError = []
            if(!packageData.pricePerInterval) {
                this.lastCustomPackagePricePerIntervalError = ['Please enter the price per interval']
                res = false
            }
            this.lastCustomPackageNumberOfIntervalsError = []
            if(!packageData.numberOfIntervals) {
                this.lastCustomPackageNumberOfIntervalsError = ["Number of intervals can't be empty"]
                res = false
            }
            this.lastCustomPackageInterval = []
            if (!packageData.interval) {
                this.lastCustomPackageInterval = ["Select Interval please"]
            }
            return res
        },
        addStandardPackage() {
            /*
            this.standardNumOfLessonsError = []
            if(!this.lastStandardPackage.numberOfLessons) {
                this.standardNumOfLessonsError = ["Number of lessons can't be empty"]
            } else {
                this.checkNumberOfDays(this.lastStandardPackage.numberOfLessons)
            }
            this.standardPerLessonError = []
            if(!this.lastStandardPackage.isTrial && !this.lastStandardPackage.perLesson) {
                this.standardPerLessonError = ["Per lesson can't be empty"]
            }
            this.standardTotalPriceError = []
            if(!this.lastStandardPackage.isTrial && !this.lastStandardPackage.totalPrice) {
                this.standardTotalPriceError = ["Total price can't be empty"]
            }
            if(this.standardNumOfLessonsError.length || this.standardPerLessonError.length || this.standardTotalPriceError.length) {
                return
            }
            */
            this.resetErrors()
            if(this.checkPackageErrors(this.lastStandardPackage)) {
                return
            }
            this.standardPackages.push({
                numberOfLessons: '',
                perLesson: '',
                totalPrice: '',
                memberTotalPrice: '',
                memberPerLesson: '',
                charge: 'upfront',
                isGlobalPackage: false,
                currency: this.currency,
                key: Number(_.max(_.map(this.standardPackages, v=>v.key))||0)+1,
                isTrial: false,
            })
        },
        removeStandardPackage(i) {
            if(!this.isEditDisabled)
                this.standardPackages.splice(i, 1)
        },
        addCustomPackage() {
            /*
            this.customTotalPriceError = []
            if(!this.lastCustomPackage.isTrial && !this.lastCustomPackage.totalPrice) {
                this.customTotalPriceError = ["Total price can't be empty"]
                return
            }
            */
            this.resetErrors()
            if(this.checkPackageErrors(this.lastCustomPackage)) {
                return
            }
            this.customPackages.push({
                description: '',
                totalPrice: '',
                numberOfLessons: '',
                perLesson: '',
                memberTotalPrice: '',
                memberPerLesson: '',
                currency: this.currency,
                key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                isTrial: false,
            })
        },
        removeCustomPackage(i) {
            if(!this.isEditDisabled)
                this.customPackages.splice(i, 1)
        },
        standardNumOfLessonsInput(event) {
            if(isNaN(event)) {
                this.standardNumOfLessonsError = ['Please use numbers only']
                return
            }
            this.standardNumOfLessonsError = []
            this.lastStandardPackage = {
                numberOfLessons: event
            }
        },
        standardPerLessonInput(event) {
            if(isNaN(event)) {
                this.standardPerLessonError = ['Please use numbers only']
                return
            }
            this.standardPerLessonError = []
            this.lastStandardPackage = {
                perLesson: event
            }
        },
        standardDescriptionInput(event) {
            this.lastStandardPackage = {
                description: event
            }
        },
        checkNumberOfDays(newVal) {
            this.standardNumOfLessonsError = []
            if(this.scheduleDates.length < Number(newVal)) {
                this.numberOfLessonsAlert = true
                this.standardNumOfLessonsError = [`Number of lessons exceeds ${this.scheduleDates.length} days selected`]
            }
        }
    },
    watch: {

        currency(newVal, oldVal) {

            _.each(this.standardPackages, (p) => {
                p.currency = newVal
            })
            _.each(this.customPackages, (p) => {
                p.currency = newVal
            })
        },
        activeNumberOfLessons(newVal, oldVal) {
            this.checkNumberOfDays(newVal)
        }
    }
}
</script>
<style lang="scss">
.teacher-group-price {
    a.v-tabs__item--active {
        font-weight: bold;
        background-color: yellow;
    }
}
</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>