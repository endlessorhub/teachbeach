<template>
      <v-layout align-top justify-start row wrap>
        <v-flex xs12  class="text-xs-left">
            <v-layout align-top justify-start row nowrap>
                <v-flex v-if="mediaUrl" xs12 md6 lg3  class="text-xs-left">
                    <gallery
                        :items="galleryItems"
                    >
                    </gallery>
                </v-flex>
                <v-flex xs12 md6 lg6 class="text-xs-left" style="padding-left: 1rem;">
                    <LocationPartial
                        :class-data="$props"
                    />
                    <v-divider ></v-divider>
                    <div v-if="!is_price_hidden && dropInRate"><b>Drop-in:</b> {{currencyLogo}}{{ dropInRate }}</div>
                    <div v-if="!is_price_hidden && trialLesson"><b>Trial:</b> {{ trialLesson }}</div>
                    <div v-if="!is_price_hidden && !flexible_dates"><b>Workshop price:</b> {{ workshopPrice }} for {{workshopDuration}}<span v-if="workshopMemberPrice">, <a @click="buyMembership">Premium Member price {{workshopMemberPrice}}</a></span></div>
                    <div v-if="!is_price_hidden && flexible_dates"><b>Price: </b>
                        <span v-for="(item,i) in packages" :key="i">
                            {{item.text}}
                            <span v-if="item.memberPrice">, <a @click="buyMembership">Premium Member price {{item.memberPrice}}</a></span>
                            <span v-if="i<packages.length-1">, </span>
                        </span>
                    </div>
                        <div v-if="!is_price_hidden && flexible_dates && subscriptionLowest"><b>Subscription: </b>
                            From ${{ subscriptionLowest }}/hour
                            <a v-if="memberSubscriptionLowest || memberSubscriptionLowest === 0" @click="buyMembership">Premium Member Price From ${{ memberSubscriptionLowest }}/hour</a>
                        </div>
                    <v-divider v-if="!is_price_hidden"></v-divider>
                    <div v-if="levelOfExperience"><b>Level of experience:</b> {{levelOfExperience}}</div>
                    <v-divider v-if="levelOfExperience"></v-divider>
                    <div>
                        <b>Schedule</b>
                        (Timezone: {{timezone}})
                        <v-btn icon @click="teacher.group_count > 1" :to="isCompany ? `/company_group_calendar/${companyProfile.id}` : `/teacher_group_calendar/${teacher.id}`" >
                            <v-icon color="platform-green">event</v-icon>
                        </v-btn>
                    </div>
                    <div v-if="day_select_type == 'weekly'">
                        <div v-if="fromDate">From {{fromDate}} <span v-if="until_date"> to {{toDate}}</span><span v-else> ongoing</span></div>
                        <div v-else><span v-if="until_date"> Until {{toDate}}</span><span v-else> Ongoing</span></div>
                    </div>
                    <div class="schedule-list-item" v-for="(item,i) in schedule" :key="i">{{item}}</div>
                </v-flex>
            </v-layout>
            <v-divider style="margin: 3px;"></v-divider>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-left">
            
            <v-flex xs12  class="text-xs-left" style="display: flex; align-items: center;">
                <a
                    v-if="canEnroll"
                    @click.stop.prevent="bookClass()"
                    :loading="isLoading"
                    :disabled="isLoading"
                >
                    {{ lowestPricePackage ? '$'+lowestPricePackage.totalPrice : 'Book now' }}
                </a>
                <v-btn
                    v-if="isFreeMemberPackage && !isMemberOfCurrentCompany"
                    class="btn__round-animated"
                    :loading="isLoading"
                    :disabled="isLoading"
                    large
                    @click.stop.prevent="buyMembership"
                >
                    Free to members JOIN
                </v-btn>
                <v-btn
                    v-if="isFreeMemberPackage && isMemberOfCurrentCompany"
                    class="btn__round-animated"
                    :loading="isLoading"
                    :disabled="isLoading"
                    large
                    @click.stop.prevent="bookClass()"
                >
                    Free to members! Sign up
                </v-btn>
                <v-btn
                    v-if="!isFreeMemberPackage"
                    class="btn__round-animated"
                    :loading="isLoading"
                    :disabled="isLoading"
                    large
                    @click.stop.prevent="bookClass()"
                >
                    Sign Up
                </v-btn>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
              <h1>{{classTitle}}
                <Rating object-type="class" :object-id="id"></Rating>
              </h1>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
              <div v-if="wedo"><b>What we'll do</b>: <span v-html="wedo"></span></div>
              <v-divider v-if="youLearn"></v-divider>

              <div v-if="bring"><b>Includes</b>: <span v-html="bring"></span></div>
              <v-divider v-if="supply"></v-divider>
              <div v-if="supply"><b>What we'll supply</b>: {{supply}}</div>
              <v-divider ></v-divider>
                <div v-if="youLearn"><b>Meeting instructions</b>: <span v-html="youLearnFormatted"></span></div>
              <v-divider v-if="bring"></v-divider>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
                <h2>Meet <span>{{teacher.first_name}}</span> </h2>
                <div v-if="show_email && email">
                    Email: <a :href="`mailto:${email}`">{{email}}</a>
                </div>
                <div v-if="show_phone && phone">
                    Phone: <a :href="`tel:${phone}`">{{phone}}</a>
                </div>
              <router-link v-if="teacher.private_count" :to="'/classes/private/teacher/'+teacher.id">Private  availability</router-link>&nbsp;
              <router-link v-if="teacher.group_count" :to="'/classes/group/teacher/'+teacher.id">Group  availability</router-link>&nbsp;
              <router-link v-if="teacher.group_count || teacher.private_count" :to="'/classes/all/teacher/'+teacher.id">All classes</router-link>&nbsp;
              <div class="bio" >
                  <v-flex xs12  class="text-xs-left" style="margin-right: 5px; width: 50%;">
                    <v-img v-if="avatarUrl" :src="avatarUrl" width="100%" :aspect-ratio="1.25"/>
                  </v-flex>
                <div v-html="bio"></div>
              </div>

              <v-flex xs12  class="text-xs-left">
                  <v-btn
                      v-if="canEnroll"
                      class="platform-green"
                      @click.stop.prevent="bookClass()"
                      :loading="isLoading"
                      :disabled="isLoading"
                      large
                  >
                      Book now
                  </v-btn>
              </v-flex>
              <v-flex xs12 v-if="isCompany" class="text-xs-left">
                  <div style="width: 50%;">
                      <v-img v-if="companyImgUrl" :src="companyImgUrl" width="100%" :aspect-ratio="1.25"/>
                  </div>
                  <h4 class="company-title">About {{companyName}}</h4>
                  <div v-html="companyDescription"></div>
              </v-flex>
            </v-flex>
        </v-flex>
        <v-flex v-if="isMapVisible" xs12 md6 class="text-xs-left">
            <v-flex xs12  class="text-xs-left">
              <GeoMap v-bind="mapData" height="300px" v-if="lat && lng"/>
            </v-flex>
        </v-flex>
        <RegMinPopup
            v-model="registerDialog"
            :registrationTitle="registrationTitle"
            v-bind="regMinFormData"
            v-on:done="registerDone"
        />
      </v-layout>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import DateWithTimePicker from '@/components/basic/DateWithTimePicker.vue'
import GeoMap from '@/components/basic/GeoMap.vue'
import RegMinPopup from './RegMinPopup'
import Gallery from '@/components/basic/Gallery.vue'
import LocationPartial from './LocationPartial'
import Rating from '@/components/basic/Rating.vue'

import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'
import metadata from '@/mixins/metadata'
import { mapGetters } from 'vuex'

const weekDays = [
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
]

export default {
    props: [
        'address',
        'address_city',
        'address_street',
        'address_zip',
        'can_book',
        'can_book_url',
        'can_pay',
        'class_media',
        'class_type',
        'currency',
        'custom_packages',
        'day_select_type',
        'drop_in_rate',
        'experience',
        'flexible_dates',
        'group_description',
        'group_lesson_length',
        'group_number_of_lessons',
        'group_package_type',
        'groupClassSummary',
        'id',
        'instant_booking',
        'is_master',
        'is_premium_community',
        'is_private',
        'lat',
        'lng',
        'logged_in_user_orders',
        'master_media',
        'maxSize',
        'name',
        'orders',
        'private_className',
        'private_lesson_length',
        'private_number_of_lessons',
        'rate',
        'schedule_dates',
        'schedule_excluded',
        'schedule_from',
        'schedule_to',
        'show_email',
        'show_phone',
        'show_phone_rule',
        'standard_packages',
        'start_date',
        'students_bring',
        'teacher',
        'teacher_supplies',
        'teaching_country',
        'teaching_venue',
        'timezone',
        'until_date',
        'user_category',
        'user_subcategory',
        'venue',
        'weekdays_schedule',
        'what_else',

        //optional, dynamic
        'supportFiles',
        'avatar',

        //show enroll button
        'show_enroll',
        'is_price_hidden',
    ],

    mixins: [metadata],

    data: () => ({
        isLoading: false,
        pickerDate: null,
        datesSelected: [],
        packageSelected: null,
        utils: utils,
        weekDayNames: [
            'S',
            'M',
            'T',
            'W',
            'T',
            'F',
            'S',
        ],
        startCal: null,
        endCal: null,
        modelCal: null,
        cachedDates: [],
        calAlertText: '',
        calAlertActive: false,
        calPackages: [],
        carouselHeight: 300,
        mapDialog: false,
        contactDialog: false,
        registerDialog: false,
        registrationTitle: '',
        initAction: '',
    }),

    components: {
        GeoMap,
        DateWithTimePicker,
        RegMinPopup,
        Gallery,
        LocationPartial,
        Rating,
    },

    created: function () {

    },

    mounted() {
        /*
        const update = _.bind(() => {
            if(this.$refs.carouselEl && this.$refs.carouselEl.$el && this.$refs.carouselEl.$el.clientWidth)
                this.carouselHeight = this.$refs.carouselEl.$el.clientWidth
        }, this)
        this.$nextTick(() => {
            update()
            window.addEventListener('resize', update);
            //console.log(this.carouselHeight)
        })
        */
    },

    computed: {
        ...mapGetters([
            'isLoggedIn',
            'isMember',
        ]),
        isMapVisible() {
            return this.lat && this.long && this.class_type !== 'online';
        },
        galleryItems() {
            const createItem = (url, isRaw) => {
                const type = /^data:image/.test(url) || /\.(png|jpg|jpeg|gif)/i.test(url) ? 'image' : 'video'
                return {
                    src: type === 'image' && !isRaw ? classHelper.previewImageSrc(url) : url,
                    type: type,
                }
            }
            const res = []
            if(this.class_media && this.class_media.length) {
                _.each(this.class_media, v => {
                    res.push(createItem(v.class_media, v.isRaw))
                })
            } else if(this.master_media) {
                res.push(createItem(this.master_media))
            }
            return res
        },
        regMinFormData() {
            return {
                isPrivate: this.is_private,
                class_id: this.id,
                alertText: "You may receive SMS alerts about teacher's first response and lesson reminders",
                teacherPhone: this.show_phone ? this.phone : '',
            }
        },
        trialLesson() {
            const trial = _.find(classHelper.classPackages(this), 'isTrial')
            if(!trial)
                return ''
            return Number(trial.totalPrice) ?
                `${utils.formatPrice(trial.totalPrice, this.currency || 'usd')} for ${trial.numberOfLessons} lesson${trial.numberOfLessons > 1 ? 's' : ''}` :
                `${trial.numberOfLessons} free trial lesson${trial.numberOfLessons > 1 ? 's' : ''}`
        },
        canEnroll() {
            return (this.can_book || this.can_book_url) && this.show_enroll && classHelper.canEnroll(this)
        },
        dropInRate() {
            return Math.round(this.drop_in_rate)
        },
        groupClassSummaryFormatted() {
            return utils.formatTextToHtml(this.groupClassSummary)
        },
        groupClassDescriptionFormatted() {
            return utils.formatTextToHtml(this.group_description)
        },
        levelOfExperience() {
            return this.experience && this.experience.join(', ') || ''
        },
        calSheetHeight() {
            return Math.min(this.intervalCount*this.intervalHeight, 240)
        },
        firstInterval() {
            if(this.calPackages && this.calPackages.length) {
                return _.min(_.map(this.calPackages, v => Number(v.start.split(':')[0])))-1
            }
            return 6
        },
        intervalCount() {
            if(this.calPackages && this.calPackages.length) {
                let end = _.max(_.map(this.calPackages, v => Number(v.end.split(':')[0])))+2
                return Math.max(end-this.firstInterval, 4)
            }
            return 15
        },
        intervalHeight() {
            if(this.calPackages && this.calPackages.length) {
                return Math.round(Math.max(200/this.intervalCount, 32))
            }
            return 32
        },
        classTitle() {
            return this.name
        },
        location() {
            return classHelper.location(this)
        },
        packages() {
            return classHelper.priceDescription(this)
            // the rest is old format (could be recovered)
            const dateFormat = (dateStr) => utils.stringToDate(dateStr).toLocaleString('en-us', { month: 'long', day: 'numeric' })
            return !this.flexible_dates ?
                _.map(this.custom_packages, v => `${dateFormat(this.start_date)} to ${dateFormat(this.until_date)} for ${utils.formatPrice(v.totalPrice, this.currency)}`) :
                _.map(this.standard_packages, v => `${utils.formatPrice(v.totalPrice, this.currency)} for ${v.numberOfLessons} lesson${v.numberOfLessons == 1 ? '' : 's'}`)
        },
        price() {
            return utils.formatPrice(this.rate || this.drop_in_rate, this.currency || 'usd')
            //return this.currencyLogo+Number(this.rate || this.drop_in_rate || 0).toFixed(2)
        },
        workshop() {
            return _.find(classHelper.classPackages(this), p => !p.isTrial);
        },
        workshopDuration() {
            return this.workshop && `${this.workshop.numberOfLessons} lesson/s` || ''
        },
        currencyLogo() {
            return utils.getCurrencyLogo(this.currency || 'usd')
        },
        workshopPrice() {
            return this.workshop && utils.formatPrice(this.workshop.totalPrice, this.currency) || ''
        },
        workshopMemberPrice() {
            if (this.workshop.memberTotalPrice === '')
                return '';
            return this.workshop && utils.formatPrice(this.workshop.memberTotalPrice, this.currency) || ''
        },
        schedule() {
            if(this.day_select_type === 'weekly') {
                return _.map(this.weekdays_schedule, (v) => weekDays[v.weekday]+` ${utils.time24HtoAMPM(v.start)}-${utils.time24HtoAMPM(v.end)}`)
            } else {
                return _.map(utils.formatDatesSchedule(this.schedule_dates.filter(d => (utils.isTimeInFuture(`${d.date} ${d.start}:00`, this.timezone))), true), v => v.dateStr)
                // return _.map(this.schedule_dates, (v) => utils.stringToDate(v.date).toLocaleString('en-us', { month: 'long', day: 'numeric' }))
            }
        },
        wedo() {
            return utils.formatTextToHtml(this.group_description)
        },
        youLearn() {
            return this.what_else
        },
        youLearnFormatted() {
            return utils.formatTextToHtml(this.what_else)
        },
        bring() {
            return utils.formatTextToHtml(this.students_bring)
        },
        supply() {
            return this.teacher_supplies
        },
        teacherName() {
            return this.teacher.first_name + ' '+this.teacher.last_name
        },
        avatarUrl() {
            if(this.avatar && this.avatar.uploadPhoto && this.avatar.uploadPhoto.imageUrl)
                return this.avatar.uploadPhoto.imageUrl
            else
                return this.teacher && this.teacher.media ? classHelper.previewImageSrc(this.teacher.media) : null
        },
        bio() {
            return utils.formatTextToHtml(this.teacher.description)
        },
        mediaUrl() {
            if(this.class_media && this.class_media.length)
                return this.class_media[0].class_media
            else
                return  this.master_media ? this.master_media : null
        },
        datesInCalendar() {
            return this.calcDates()
        },

        mapData() {
            return this.lat && this.lng ? {
                marker: {
                    lat: this.lat,
                    lng: this.lng,
                },
                center: {
                    lat: this.lat,
                    lng: this.lng,
                },
            } : {}
        },
        today() {
            return utils.dateToString(new Date())
        },
        dateTimeDict() {
            let res = {}
            _.each(this.datesInCalendar, d => {
                const date = utils.stringToDate(d)
                const scheduleDay = _.find(this.weekdays_schedule, {weekday: date.getDay()})
                if(scheduleDay) {
                    res[d] = scheduleDay
                }
            })
            return res
        },
        currentPackage() {
            if(this.packageSelected == 'drop_in_package') {
                return {
                    numberOfLessons: 1,
                    totalPrice: this.drop_in_rate,
                    perLesson: this.drop_in_rate,
                    currency: this.currency ? this.currency : this.standard_packages.length ? this.standard_packages[0].currency : 'usd'
                }
            }
            if (this.group_package_type == 'standard') {
                return _.find(this.standard_packages, {key: this.packageSelected})
            }
            return _.find(this.custom_packages, {key: this.packageSelected})
        },

        showChipSelectPackage() {
            return !this.currentPackage
        },
        showChip() {
            return this.currentPackage
        },
        chipDone() {
            return this.currentPackage && this.datesSelected.length == this.currentPackage.numberOfLessons
        },
        fromDate() {
            if(!this.start_date)
                return ''
            const today = new Date()
            const date = utils.stringToDate(this.start_date)
            if(today > date)
                return ''
            return date.toLocaleString('en-us', { month: 'long' }) + ' ' + (date.getDate()-0)+', '+date.getFullYear()
        },
        toDate() {
            if(!this.until_date)
                return ''
            const date = utils.stringToDate(this.until_date)
            return date.toLocaleString('en-us', { month: 'long' }) + ' ' + (date.getDate()-0)+', '+date.getFullYear()
        },
        isCompany() {
            return this.teacher.user.is_company
        },
        companyImgUrl() {
            return this.teacher.user.company_profile && classHelper.previewImageSrc(this.teacher.user.company_profile.main_media)
        },
        companyName() {
            return this.teacher.user.company_profile && this.teacher.user.company_profile.name
        },
        companyDescription() {
            return utils.formatTextToHtml(this.teacher.user.company_profile && this.teacher.user.company_profile.description)
        },
        companyProfile() {
            return this.teacher.user.company_profile
        },
        isOnline() {

        },
        alreadyBought() {
            return _.intersection(this.logged_in_user_orders , _.map(this.orders, v => v.id)).length
        },
        alreadyBoughtTrial() {
            return _.intersection(this.logged_in_user_orders , _.map(_.filter(this.orders, o => (o.data.package && o.data.package.isTrial)), v => v.id)).length
        },
        trialExists() {
            return _.find(this.flexible_dates ? this.standard_packages : this.custom_packages, p => (!p.isPrivate && p.isTrial))
        },
        email() {
            return this.teacher.email || this.teacher.user.email
        },
        phone() {
            return this.teacher.phone || this.teacher.user.phone
        },
        lowestPricePackage() {
            return (this.flexible_dates ? this.standard_packages : this.custom_packages)
                .filter(v => (v.totalPrice && v.type !== 'limitedSubscription'))
                .sort((a, b) => a.totalPrice - b.totalPrice)[0];
        },
        subscriptionLowest() {
            const sorted = this.custom_packages.filter(p => p.type === 'limitedSubscription').sort((a, b) => (a.pricePerInterval - b.pricePerInterval));
            return sorted.length ? sorted[0].pricePerInterval : null;
        },
        memberSubscriptionLowest() {
            const sorted = this.custom_packages
                .filter(p => (p.type === 'limitedSubscription' && (p.memberPricePerInterval || p.memberPricePerInterval === 0)))
                .sort((a, b) => (a.memberPricePerInterval - b.memberPricePerInterval));
            return sorted.length ? sorted[0].memberPricePerInterval : null;
        },
        isFreeMemberPackage() {
            return classHelper.classPackages(this).find(p => p.memberPricePerInterval === 0 || p.memberTotalPrice === '0')
        },
        isMemberOfCurrentCompany() {
            return this.teacher && this.teacher.user && this.teacher.user.membership && this.isMember(this.teacher.user.membership);
        },
    },

    methods: {
        openSchedule() {
            // not implemented in group class
        },
        openMessageForm() {
            // not implemented in group class
        },
        buyMembership() {
            const showRegForm = () => {
                this.initAction = 'membership'
                this.registrationTitle = 'Looks like you’re new here!'
                this.registerDialog = true
            }
            if(this.isLoggedIn) {
                this.$router.push(`/buy-membership/${this.teacher.user.membership}?return=${this.$route.path}`)
            } else {
                showRegForm()
            }
        },
        bookClass() {
            if (this.canEnroll) {
                const showRegForm = () => {
                    this.initAction = 'book'
                    this.registrationTitle = 'Looks like you’re new here!'
                    this.registerDialog = true
                }
                if(this.can_book) {
                    if(this.isLoggedIn) {
                        this.$router.push(`/learners/new_enroll/${this.id}/4/0`)
                    } else {
                        showRegForm()
                    }
                } else if (this.can_book_url) {
                    // do not show reg form, redirect right away
                    window.open(utils.prepareUrl(this.can_book_url), '_blank')
                    /*
                    if(this.isLoggedIn) {
                        window.open(utils.prepareUrl(this.can_book_url), '_blank')
                    } else {
                        showRegForm()
                    }
                    */
                }
            }
        },
        showMap() {
            this.mapDialog = true
        },
        choosePackage() {
            this.$emit('choose:package', this.id)
        },
        calcDates() {
            let y = new Date().getFullYear()
            let m = new Date().getMonth()
            if (this.pickerDate) {
                y = this.pickerDate.split('-')[0]
                m = this.pickerDate.split('-')[1]-1
            }
            return utils.getCalendarDatesForMonth(y, m, this.weekdays_schedule, this.start_date, this.until_date, this.schedule_excluded || [])
        },
        allowedDates(date) {
            return this.datesInCalendar.indexOf(date) > -1
        },
        dayFormat() {
            return ''
        },
        weekdayFormat() {
            return ''
        },
        clickDay(event) {
            console.log('clickDay', event)
            this.calAlertActive = false
            if(this.datesSelected.indexOf(event.date)  > -1) {
                if(!this.flexible_dates && !utils.checkSequence(this.cachedDates, _.difference(this.datesSelected, [event.date]))) {
                    //show warning about dates selected should be only one after another
                    this.calAlertText = 'Please deselect earliest or latest day'
                    this.calAlertActive = true
                    return
                }
                this.datesSelected.splice(this.datesSelected.indexOf(event.date), 1)
            } else {
                if(this.cachedDates.indexOf(event.date) == -1)
                    return
                if(!this.flexible_dates && !utils.checkSequence(this.cachedDates, _.concat(this.datesSelected, [event.date]))) {
                    //show warning about dates selected should be only one after another
                    this.calAlertText = 'Please select dates consistently'
                    this.calAlertActive = true
                    return
                }
                this.datesSelected.push(event.date)
            }
        },
        calChanged(event) {
            console.log(event)
            this.calPackages = _.map(utils.getCalendarDatesForPeriod(event.start.date, event.end.date, this.weekdays_schedule, this.start_date, this.until_date, this.schedule_excluded || []), v => {
                return _.find(this.weekdays_schedule, {weekday: utils.stringToDate(v).getDay()})
            })
            const start = utils.stringToDate(event.start.date)
            const end = utils.stringToDate(event.end.date)
            this.startCal = start.toLocaleString('en-us', { month: 'short' }) + ' ' + (start.getDate()-0)
            this.endCal = end.toLocaleString('en-us', { month: 'short' }) + ' ' + (end.getDate()-0)
        },
        getEvent(date) {
            let nextDay = utils.stringToDate(date)
            nextDay.setDate(nextDay.getDate()+1)
            const events = _.map(utils.getCalendarDatesForPeriod(date, utils.dateToString(nextDay), this.weekdays_schedule, this.start_date, this.until_date, this.schedule_excluded || []), curDate => {
                const date = '2019-01-01'
                const v = _.find(this.weekdays_schedule, {weekday: utils.stringToDate(curDate).getDay()})
                return {
                    active: this.datesSelected.indexOf(curDate) > -1 ? true : false,
                    busy: true,
                    title: utils.time24HtoAMPM(v.start).replace(' ', '')+' '+utils.time24HtoAMPM(v.end).replace(' ', ''),
                    weekday: v.weekday,
                    time: v.start,
                    start: v.start,
                    end: v.end,
                    date: curDate,
                    duration: Math.round(((new Date(date+' '+v.end+':00').getTime()) - (new Date(date+' '+v.start+':00').getTime()))/60000)
                }
            })
            if (events.length && this.cachedDates.indexOf(events[0].date) == -1 ) {
                this.cachedDates.push(events[0].date)
                this.cachedDates = _.sortBy(this.cachedDates, v => utils.stringToDate(v))
            }
            return events.length ? events[0] : null
        },
        intervalStyle(event) {
            //console.log(arguments)
            if(_.find(this.calPackages, {weekday: event.weekday+1})) {
                return {backgroundColor: '#eee'}
            }
            return
        },
        getMetaTitle() {
            return this.metadataTemplate.title ? this.metadataTemplate.title.replace('${class.name}', this.name) : ''
        },
        getMetaDescription() {
            return this.metadataTemplate.metatag ? this.metadataTemplate.metatag.replace('${class.description}', this.group_description) : ''
        },
        registerDone(res) {
            this.registerDialog = false
            switch (this.initAction) {
                case 'schedule':
                    this.openSchedule()
                    break;
                case 'book':
                    this.bookClass()
                    break;
                case 'message':
                    this.openMessageForm()
                    break;
                case 'membership':
                    this.buyMembership()
                    break;
            }
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.bio {
    overflow: auto;
}
.margined {
    margin: 2px 0;
}
.my-event {
    overflow: visible;
    text-overflow: ellipsis;
    border-radius: 2px;
    background-color: gray;
    color: #ffffff;
    border: 1px solid gray;
    font-size: 8px;
    padding: 1px;
    cursor: pointer;
    margin-bottom: 1px;
    left: 2px;
    margin-right: 2px;
    position: relative;

    &.with-time {
        position: absolute;
        right: 2px;
        margin-right: 0px;

        &.active {
            background-color: yellow;
            color: black;
        }
    }
}
.custom-head-weekday {
    text-align: center;
    color: #424242;

    .title-weekday {
        font-size: 12px;
    }
    .title-day {
        font-size: 20px;
    }

    &.is-future {
        color: #000;
    }
    &.is-present {
        color: #1867c0;
    }
    &.is-past {
        color: rgba(0,0,0,0.38);
    }
}
.schedule-list-item:last-child {
    margin-bottom: 10px;
}
.timezone {
  display: inline-block;
  margin: 0 10px;
}
.company-title {
    font-size: 24px;
}
.free-to-premium {
    font-size: 20px;
}
</style>