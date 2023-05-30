<template>
  <div class="teacher-private-package">
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
        <v-layout align-top justify-center row wrap>
            <v-flex xs12 class="text-xs-center" >
                  <h1>Create class prices</h1>
                  <h3> We recommend offering a low cost trial, short term package for projects and long term subscription for  your best students with the lowest rate, charged automatically.</h3>
            </v-flex>
            <v-flex xs12 class="text-xs-left" >
                <v-list one-line>
                  <template v-for="(p, index) in customPackageList">
                    <v-list-tile
                       v-if="index < customPackageList.length-1"
                      :key="p.key"
                      avatar
                      ripple
                    >
                      <v-list-tile-action>
                        <div :disabled="isEditDisabled" class="v-chip__close remove-weekday" @click.stop="removeCustomPackage(index)"><i aria-hidden="true" class="v-icon material-icons theme--light">cancel</i></div>
                      </v-list-tile-action>
                      <v-list-tile-content>
                        <v-list-tile-title v-if="!p.isSubscription">{{ p.numberOfLessons}} time{{p.numberOfLessons == 1 ? '' : 's'}} for {{p.formattedPrice}},
                            <span v-if="p.isPricePerPerson">
                                <v-icon color="primary">check_circle</v-icon>Price per person,
                            </span>
                            <span v-if="p.isTrial">
                                <v-icon color="success">check_circle</v-icon>Trial,
                            </span>
                             {{personsText(p)}}
                        </v-list-tile-title>
                        <v-list-tile-title v-else v-html="subscriptionHtml(p)">

                        </v-list-tile-title>
                        <v-list-tile-sub-title>{{p.description}}</v-list-tile-sub-title>
                      </v-list-tile-content>

                    </v-list-tile>
                    <v-divider
                      v-if="index + 1 < customPackageList.length"
                      :key="index"
                    ></v-divider>
                  </template>

                </v-list>
            </v-flex>
            <v-flex xs8 class="text-xs-left" >
                <v-radio-group v-model="rateType">
                  <v-radio
                    label="Trial rate - One time only  time offer such as free or $1"
                    value="trial"
                  ></v-radio>
                  <v-radio
                    label="Package rate  - One or more lessons paid up front"
                    value="package"
                  ></v-radio>
                  <v-radio
                    label="Subscription  - ongoing payments"
                    value="subscription"
                  ></v-radio>
                </v-radio-group>
            </v-flex>
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

            <v-layout align-top justify-center row wrap v-if="!showSubsriptionForm">

                <v-flex xs4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.totalPrice"
                        label="Total Price"
                        v-on:input="lastCustomPackage={totalPrice: $event}"
                        :error-messages="customTotalPriceError"
                      ></v-text-field>
                </v-flex>
                <v-flex xs4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.numberOfLessons"
                        label="# of days"
                        v-on:input="lastCustomPackage={numberOfLessons: $event}"
                        :error-messages="customNumberOfLessonsError"
                        type="number"
                      ></v-text-field>
                </v-flex>
                <v-flex xs4 class="text-xs-left" >
                      <v-text-field
                            :disabled="isEditDisabled"
                            :value="formatPerLessonPrice(lastCustomPackage.perLesson)"
                            label="$per lesson"
                            readonly
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
                            :value="formatMemberPerLessonPrice(lastCustomPackage.memberPerLesson)"
                            label="Member $per lesson"
                            readonly
                        ></v-text-field>
                </v-flex>
                <v-flex xs3 class="text-xs-left" >
                        <v-combobox
                          v-model="lastCustomPackage.lessonLength"
                          :items="lessonLengthAvailable"
                          label="lesson Length"
                          @change="lastCustomPackage={lessonLength: $event}"
                          @input.native="onLLInput"
                          :search-input.sync="lastLessonLength"
                          dense
                          placeholder="1 hour 30 minutes"
                          :error-messages="customLessonLengthError"
                        >
                        </v-combobox>
                </v-flex>
                <v-flex xs3 class="text-xs-left" >
                      <v-checkbox
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.isPricePerPerson"
                        label="Price per person"
                        v-on:input="lastCustomPackage={isPricePerPerson: $event}"
                      ></v-checkbox>
                </v-flex>
                <v-flex xs3 class="text-xs-left" >
                      <v-text-field

                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.minPersons"
                        label="Minimum persons"
                        v-on:input="lastCustomPackage={minPersons: $event}"
                        :error-messages="customMinPersonsError"
                        type="number"
                      ></v-text-field>
                </v-flex>
                <v-flex xs3 class="text-xs-left" >
                      <v-text-field

                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.maxPersons"
                        label="Maximum persons"
                        v-on:input="lastCustomPackage={maxPersons: $event}"
                        :error-messages="customMaxPersonsError"
                        type="number"
                      ></v-text-field>
                </v-flex>
                <v-flex xs4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.description"
                        v-on:input="lastCustomPackage={description: $event}"
                        label="Description (optional)"
                      ></v-text-field>
                </v-flex>
                <v-flex xs8 class="text-xs-left" >
                    <v-radio-group v-model="lastCustomPackage.charge" hide-details row v-on:change="lastCustomPackage={charge: $event}" >
                        <v-radio
                            :disabled="isEditDisabled"
                            label="Pay per class"
                            value="per_lesson"
                        ></v-radio>
                        <v-radio
                            :disabled="isEditDisabled"
                            label="Pay total upfront"
                            value="upfront"
                      ></v-radio>
                    </v-radio-group>
                </v-flex>

            </v-layout>
            <v-layout align-top justify-center row wrap v-else>
                <v-flex xs6 md4 class="text-xs-left" >
                    <v-select
                      v-model="lastCustomPackage.period"
                      :items="subscriptionPeriods"
                      label="Subscription (monthly, weekly,etc)"
                      v-on:change="lastCustomPackage={period: $event}"
                      placeholder="Select how often student pays"
                    ></v-select>
                </v-flex>
                <v-flex xs6 md4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.rateBilled"
                        label="Payment amount"
                        v-on:input="lastCustomPackage={rateBilled: $event}"
                        :error-messages="customTotalRateBilledError"
                        type="number"
                      ></v-text-field>
                </v-flex>
                <v-flex xs6 md4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.classesPerInterval"
                        label="Classes per payment"
                        v-on:input="lastCustomPackage={classesPerInterval: Number($event)}"
                        :error-messages="classesPerIntervalError"
                        type="number"
                      ></v-text-field>
                </v-flex>
                <v-flex xs6 md4 class="text-xs-left" >
                        <v-combobox
                          v-model="lastCustomPackage.lessonLength"
                          :items="lessonLengthAvailable"
                          label="Duration of lesson"
                          @change="lastCustomPackage={lessonLength: $event}"
                          @input.native="onLLInput"
                          :search-input.sync="lastLessonLength"
                          dense
                          placeholder="1 hour 30 minutes"
                          :error-messages="customLessonLengthError"
                        >
                        </v-combobox>
                </v-flex>
                <v-flex xs6 md4 class="text-xs-left" >
                    <v-select
                      v-model="lastCustomPackage.subscriptionLength"
                      :items="subscriptionLengths"
                      label="Length of subscription"
                      v-on:change="lastCustomPackage={subscriptionLength: $event}"
                      :error-messages="subscriptionLengthError"
                    ></v-select>
                      <!--v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.numberOfIntervals"
                        label="Length of subscription"
                        v-on:input="lastCustomPackage={numberOfIntervals: Number($event)}"
                        :error-messages="numberOfIntervalsError"
                        type="number"
                        placeholder="Type in number of payments"
                      ></v-text-field-->
                </v-flex>
                <v-flex xs6 md4 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.description"
                        v-on:input="lastCustomPackage={description: $event}"
                        label="Description (optional)"
                      ></v-text-field>
                </v-flex>
                <v-flex xs12 class="text-xs-left" >
                      <v-text-field
                        :disabled="isEditDisabled"
                        v-model="lastCustomPackage.memberTotalPrice"
                        label="Member rate for this package"
                        v-on:input="lastCustomPackage={memberTotalPrice: $event}"
                      ></v-text-field>
                </v-flex>
            </v-layout>

            <v-flex v-if="isCompany" xs12 md6 class="text-xs-left" >
                    <v-switch v-model="canBook" label="Students can book on this page"></v-switch>
            </v-flex>
            <v-flex v-if="isCompany" xs12 md6 class="text-xs-left" >
                    <v-switch v-if="canBook" v-model="canPay" label="Students can pay on this site"></v-switch>
                    <v-switch v-if="!canBook" v-model="isPriceHidden" label="Toggle on to hide price"></v-switch>
                    <v-text-field
                      v-model="canBookUrl"
                      label="URL where student can book this class (optional)"
                      v-if="!canBook"
                    ></v-text-field>
            </v-flex>
            <v-flex xs12 class="text-xs-center" >
                    <v-btn @click="addCustomPackage" :disabled="isEditDisabled"> Save & add next package rate</v-btn>
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
import classHelper from '@/lib/helpers/Class.js'
import { validationMixin } from 'vuelidate'
import { numeric, required, minValue } from 'vuelidate/lib/validators'
import _ from 'lodash'

import axios from 'axios'

export default {
    mixins: [validationMixin],
    validations: {
        lessonPricePerHour: {numeric},
    },
    props: {

    },

    components: {
        DateSelect,
    },

    data: () => ({
        isLoading: false,
        customPackages: [],
        currency: 'usd',
        currencies: [],
        currencyDict: {},
        lessonPricePerHour: null,
        activeNumberOfLessons: null,
        customTotalPriceError: [],
        customNumberOfLessonsError: [],
        customLessonLengthError: [],
        customMinPersonsError: [],
        customMaxPersonsError: [],
        customTotalRateBilledError: [],
        subscriptionLengthError: [],
        classesPerIntervalError: [],
        enrolled: [],
        lessonLengthAvailable: [
            {value: 15, text: '15 min'},
            {value: 20, text: '20 min'},
            {value: 30, text: '30 min'},
            {value: 40, text: '40 min'},
            {value: 45, text: '45 min'},
            {value: 60, text: '1 hour'},
            {value: 480, text: '8 hours'},
        ],
        lastLessonLength: null,
        canBook: null,
        canPay: null,
        canBookUrl: '',
        isPriceHidden: false,
        subscriptionPeriods: [
            {value: 'week|1', text: 'Weekly'},
            //{value: 'week|2', text: 'Every other week'},
            {value: 'month|1', text: 'Monthly'},
        ],
        subscriptionLengths: classHelper.subscriptionLengthsList(),
    }),

    created: function () {
        this.currencies = utils.getCurrencyList()
        this.currencyDict = _.keyBy(utils.getCurrencyList(), 'id')
        if (this.$store.state.teacherGroupClass) {
            this.enrolled = this.$store.state.teacherGroupClass.enrolled
            this.isPriceHidden = this.$store.state.teacherGroupClass.isPriceHidden
            this.customPackages = _.filter(this.$store.state.teacherGroupClass.customPackages || [], 'isPrivate')
            this.currency = this.$store.state.teacherGroupClass.currency || 'usd'
            this.lessonPricePerHour = isNaN(this.$store.state.teacherGroupClass.lessonPricePerHour) ? null : Math.round(this.$store.state.teacherGroupClass.lessonPricePerHour)
            this.canBook = typeof this.$store.state.teacherGroupClass.canBook == 'undefined' ? true : this.$store.state.teacherGroupClass.canBook
            this.canPay = typeof this.$store.state.teacherGroupClass.canPay == 'undefined' ? this.canBook : this.$store.state.teacherGroupClass.canPay
            this.canBookUrl = this.$store.state.teacherGroupClass.canBookUrl || ''
        }
    },

    mounted() {

    },

    computed: {
        numberOfIntervalsLabel() {
            const dict = {
                'week|1': 'weeks',
                'week|2': 'biweeks',
                'month|1': 'months',
            }
            return `Number of ${dict[this.lastCustomPackage.period]}`
        },
        classesPerIntervalPlaceholder() {
            return `Classes per ${classHelper.packagePeriodNameSingle(this.lastCustomPackage.period)}`
        },
        rateBilledPlaceholder() {
            return `Payment amount per ${classHelper.packagePeriodNameSingle(this.lastCustomPackage.period)}`
        },
        showSubsriptionForm() {
            return this.lastCustomPackage && this.lastCustomPackage.isSubscription
        },
        rateType: {
            get() {
                if(this.lastCustomPackage && this.lastCustomPackage.isTrial)
                    return 'trial'
                if(this.lastCustomPackage && this.lastCustomPackage.isSubscription)
                    return 'subscription'
                if(this.lastCustomPackage)
                    return 'package'
                return 'trial'
            },
            set(v) {
                if(!this.lastCustomPackage) {
                    this.lastCustomPackage = this.blankCustomPackage()
                }
                const p = {
                    isTrial: false,
                    isSubscription: false,
                }
                if(v === 'trial')
                    p.isTrial = true
                if(v === 'subscription')
                    p.isSubscription = true
                this.lastCustomPackage = p
            }
        },
        customDurationText: {
            get() {
                if(this.customDuration)
                    return this.customDuration
                return this.customDurationTextVal
            },
            set(val) {
                this.lastCustomPackage.lessonLength = this.val
            }
        },
        lessonPricePerHourErrors() {
            const errors = []
            if (!this.$v.lessonPricePerHour.$dirty) return errors
            !this.$v.lessonPricePerHour.numeric && errors.push('Please use numbers only')
            return errors
        },
        isEditDisabled() {
            return false // allow price edits even for enrolled
            return Boolean(this.enrolled && this.enrolled.length)
        },
        customPackageList() {
            return _.map(this.customPackages, v => _.assign({}, v, {
                formattedPrice: utils.formatPrice(v.totalPrice, v.currency),
                formattedMemberPrice: utils.formatPrice(v.memberTotalPrice, v.currency),
            }))
        },
        lastCustomPackage: {
            set(v) {
                //console.log(v)
                let numberOfLessons = ''
                let perLesson = ''
                if(!this.customPackages.length) {
                    this.customPackages.push(this.blankCustomPackage())
                }
                let last = _.last(this.customPackages)
                if(v.lessonLength && typeof v.lessonLength === 'string') {
                    let value = this.recognizeDuration(v.lessonLength)

                    v.lessonLength = _.find(this.lessonLengthAvailable, {value}) || {
                        value: value,
                        text: v.lessonLength
                    }
                    if(!_.find(this.lessonLengthAvailable, {value}))
                        this.lessonLengthAvailable.push(v.lessonLength)
                }
                if(v.totalPrice) {
                    v.totalPrice = String(v.totalPrice).replace(/[^\d]+/g, '')
                }
                if(v.memberTotalPrice) {
                    v.memberTotalPrice = String(v.memberTotalPrice).replace(/[^\d]+/g, '')
                }
                _.each(v, (newVal, k) => {
                    last[k] = newVal
                })
                if(last.subscriptionLength && last.period) {
                    last.numberOfIntervals = classHelper.subscriptionLengthMap[last.subscriptionLength][last.period]
                }
                if(last.totalPrice && last.numberOfLessons) {
                    last.perLesson = !String(last.totalPrice) || !Number(last.numberOfLessons) ? '' : Math.round(last.totalPrice / last.numberOfLessons)
                }
                if(last.memberTotalPrice && last.numberOfLessons) {
                    last.memberPerLesson = !String(last.memberTotalPrice) || !Number(last.numberOfLessons) ? '' : Math.round(last.memberTotalPrice / last.numberOfLessons)
                }
                this.$set(this.customPackages, this.customPackages.length-1, last)
            },
            get() {
                let perLesson = ''

                _.each(this.customPackages, v => {
                    const totalPrice = Number(String(v.totalPrice).replace(/[^\d]+/g, ''))
                    v.perLesson = totalPrice && v.numberOfLessons ? Math.round(totalPrice / v.numberOfLessons) : ''
                    if (v.memberTotalPrice) {
                        const memberTotalPrice = Number(String(v.memberTotalPrice).replace(/[^\d]+/g, ''))
                        v.memberPerLesson = memberTotalPrice && v.numberOfLessons ? Math.round(memberTotalPrice / v.numberOfLessons) : ''
                    }
                })
                if(!_.last(this.customPackages)) {
                    this.customPackages.push(this.blankCustomPackage())
                }
                return _.last(this.customPackages)
            },
        },
        isCompany() {
            return this.$store.state.user && this.$store.state.user.is_company
        }
    },

    methods: {
        blankCustomPackage() {
            return {
                isPrivate: true,
                description: '',
                currency: this.currency,
                totalPrice: '',
                numberOfLessons: '',
                perLesson: '',
                memberTotalPrice: '',
                memberPerLesson: '',
                lessonLength: {value: 60, text: '1 hour'},
                isPricePerPerson: true,
                minPersons: 1,
                maxPersons: 1,
                isTrial: this.customPackages.length === 0,
                isSubscription: this.customPackages.length > 1,
                key: Number(_.max(_.map(this.customPackages, v=>v.key))||0)+1,
                charge: 'upfront',
                period: 'week|1',
                classesPerInterval: 1,
                numberOfIntervals: 4,
            }
        },
        subscriptionHtml(p) {
            return classHelper.packageFormatter(p)
            /*
            if(p.period === 'week|2')
                return `${utils.formatPrice(p.rateBilled, this.currency)} every other week for ${p.classesPerInterval} classes`
            const perWord = {
                'week|1': 'week',
                'week|2': 'every other week',
                'month|1': 'month',
            }
            return `${utils.formatPrice(p.rateBilled, this.currency)} ${classHelper.packagePeriodName(p.period)} for ${p.classesPerInterval} class${p.classesPerInterval > 1 ? 'es' : ''} per ${perWord[p.period]}, ongoing for ${p.numberOfIntervals} ${perWord[p.period]}s`
            return `${p.classesPerInterval} class${p.classesPerInterval > 1 ? 'es' : ''} per ${p.numberOfIntervals} ${classHelper.packagePeriodName(p.period)} intervals for ${utils.formatPrice(p.rateBilled, this.currency)} each`
            */
        },
        personsText(p) {
            if (p.minPersons == p.maxPersons) {
                return `${p.minPersons} person${p.minPersons == 1 ? '' : 's'}`
            }
            return `minimum ${p.minPersons}, maximum ${p.maxPersons} persons`
        },
        recognizeDuration(val) {
            const pattern1 = /([\d]+):([\d]+)/
            const pattern2 = /(([0-9]*[.])?[0-9]+)\s*hour/i
            const pattern3 = /([\d]+)\s*min/i
            if (pattern1.test(val)) {
                let match = val.match(pattern1)
                return Number(match[1])*60 + Number(match[2])
                //return ('0'+match[1]).slice(-2)+':'+(('0'+match[2]).slice(-2))
            } else if (pattern2.test(val) || pattern3.test(val)) {
                let match1 = val.match(pattern2) || []
                let match2 = val.match(pattern3) || []
                return Number(match1[1] || '0')*60 + Number(match2[1] || '0')
                //return ('0'+(match1[1] || '0')).slice(-2)+':'+(('0'+(match2[1] || '0')).slice(-2))
            }
            return null
        },
        formatPrice(price) {
            if(!price || price-0 === 0)
                return ''
            return utils.formatPrice(price, this.currency)
        },
        formatPerLessonPrice(price) {
            if(!price || price-0 === 0)
                return this.lastCustomPackage.totalPrice === '0' ? 0 : ''
            return utils.formatPrice(price, this.currency)
        },
        formatMemberPerLessonPrice(price) {
            if(!price || price-0 === 0)
                return this.lastCustomPackage.memberTotalPrice === '0' ? 0 : ''
            return utils.formatPrice(price, this.currency)
        },
        resetErrors() {
            this.customTotalPriceError = []
            this.customLessonLengthError = []
            this.customNumberOfLessonsError = []
            this.customMinPersonsError = []
            this.customMaxPersonsError = []
            this.customTotalRateBilledError = []
            this.subscriptionLengthError = []
            this.classesPerIntervalError = []
        },
        checkPackageErrors(packageData) {
            let res = false
            if(packageData.isSubscription) {
                if(!packageData.numberOfIntervals || !classHelper.subscriptionLengthReverseMap[packageData.numberOfIntervals]) {
                    this.subscriptionLengthError = ['Please, fill in subscription length']
                    res = true
                }
                if(!packageData.classesPerInterval || packageData.classesPerInterval === '0') {
                    this.classesPerIntervalError = ['Please, fill in number of classes per interval']
                    res = true
                }
                if((!packageData.rateBilled || packageData.rateBilled === '0')) {
                    this.customTotalRateBilledError = ['Please type in rate billed']
                    res = true
                }
            } else {
                /*
                if (!packageData.isTrial && (!packageData.totalPrice || packageData.totalPrice === '0')) {
                    this.customTotalPriceError = ['Please, fill in Total price']
                    res = true
                }
                */
                if ((!packageData.lessonLength || !packageData.lessonLength.value)) {
                    this.customLessonLengthError = ['Please type in “minutes” or “hours”']
                    res = true
                }
                if ((!packageData.numberOfLessons || packageData.numberOfLessons === '0')) {
                    this.customNumberOfLessonsError = ['Number of lessons is required']
                    res = true
                } else if (packageData.numberOfLessons < 1) {
                    this.customNumberOfLessonsError = ['Number of lessons should be one or more']
                    res = true
                }
                if (true/*packageData.isPricePerPerson*/) {
                    if ((!packageData.minPersons || packageData.minPersons === '0')) {
                        this.customMinPersonsError = ['Minimum persons is required']
                        res = true
                    } else if (packageData.minPersons < 1) {
                        this.customMinPersonsError = ['Minimum persons should be one or more']
                        res = true
                    }
                    if ((!packageData.maxPersons || packageData.maxPersons === '0')) {
                        this.customMaxPersonsError = ['Maximum persons is required']
                        res = true
                    } else if (packageData.maxPersons < 1) {
                        this.customMaxPersonsError = ['Maximum persons should be one or more']
                        res = true
                    }
                    if (Number(packageData.maxPersons) < Number(packageData.minPersons)) {
                        this.customMinPersonsError = ['Minimum persons should be less than maximum']
                        this.customMaxPersonsError = ['Maximum persons should be more than minimum']
                        res = true
                    }
                }
            }
            return res
        },
        checkErrors() {
            this.resetErrors()
            if(this.checkPackageErrors(this.lastCustomPackage)) {
                // true means error
                if (this.customPackages.length > 1) {
                    if (Number(this.lastCustomPackage.totalPrice) || Number(this.lastCustomPackage.numberOfLessons)) {
                        return false
                    } else {
                        this.customPackages.splice(this.customPackages.length-1, 1)
                        return true
                    }
                } else {
                    return false
                }
            }
            return true
        },
        saveData() {
            /*
            _.each(this.customPackages, v => {
                if (!v.isPricePerPerson) {

                }
            })
            */
            this.$store.commit('setGroupClass', {
                currency: this.currency,
                customPackages: this.customPackages,
                lessonPricePerHour: this.lessonPricePerHour,
                canBook: this.canBook,
                canPay: this.canPay,
                canBookUrl: this.canBookUrl,
                isPriceHidden: this.isPriceHidden,
            })
        },
        back() {
            this.$nextTick(() => {
                this.saveData()
                this.$emit('prev:step')
            })
        },
        submit () {
            if(this.lastLessonLength && (!this.lastCustomPackage.lessonLength || this.lastCustomPackage.lessonLength.text != this.lastLessonLength)) {
                this.lastCustomPackage = {lessonLength: this.lastLessonLength}
            }
            if(!this.checkErrors())
                return
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.$nextTick(() => {
                this.saveData()
                this.$emit('next:step')
            })
        },
        clear () {

        },
        addCustomPackage() {
            this.resetErrors()
            if(this.checkPackageErrors(this.lastCustomPackage)) {
                return
            }
            this.customPackages.push(this.blankCustomPackage())
        },
        removeCustomPackage(i) {
            this.customPackages.splice(i, 1)
        },
        checkNumberOfDays(newVal) {
            this.standardNumOfLessonsError = []
            if(this.scheduleDates.length < Number(newVal)) {
                this.numberOfLessonsAlert = true
                this.standardNumOfLessonsError = [`Number of lessons exceeds ${this.scheduleDates.length} days selected`]
            }
        },
        onLLInput(event) {
            //console.log(event)
            const value = this.recognizeDuration(event.target.value)
            if(value) {
                const foundIndex = _.findIndex(this.lessonLengthAvailable, {value})
                if (foundIndex !== -1) {
                    this.lessonLengthAvailable.splice(foundIndex, 1, {
                        value,
                        text: event.target.value
                    })
                } else {
                    this.lessonLengthAvailable.push({
                        value,
                        text: event.target.value
                    })
                }
            }
        },
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

</style>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>