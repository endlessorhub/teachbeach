<template>
<v-layout align-top justify-left row wrap>
    <v-dialog
      v-model="isLoading"
      persistent
      width="300"
    >
      <v-card dark>
        <v-card-text>
          <v-progress-circular
            indeterminate
          ></v-progress-circular>
          Loading...
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-flex xs12 md6 class="text-xs-left">
        <SearchBox
                v-bind:category="category"
                v-bind:subcategory="subcategory"
                v-bind:city="city"
                v-bind:state="state"
                v-bind:venue="venue"
                v-bind:lessonType="lessonType"
                ref="searchbox"
        >
        </SearchBox>
    </v-flex>

    <v-flex xs6 md3 class="text-xs-left h-padded">
        <v-select
          :items="typeItems"
          label="Type"
          v-model="lessonTypeWrap"
        ></v-select>
    </v-flex>
    <v-flex xs6 md3 class="text-xs-left h-padded">
        <v-select
          :items="arrangeItems"
          label="Arrange by"
          v-model="arrange"
        ></v-select>
    </v-flex>
    <v-flex xs12 class="text-xs-left h-padded" v-if="sorting=='distance' && !geolocationAvailable">
        <div class="v-input v-text-field v-input--is-label-active v-input--is-dirty theme--light nearest-point-input">
            <div class="v-input__control">
              <div class="v-input__slot">
                <div class="v-text-field__slot">
                  <label aria-hidden="true" class="v-label v-label--active theme--light" style="left: 0px; right: auto; position: absolute;"></label>
                  <gmap-autocomplete
                    placeholder="Start typing address to set starting point"
                    @place_changed="setPlace"
                    :options="{fields: ['geometry']}"
                  >
                  </gmap-autocomplete>
                </div>
              </div>
            </div>
        </div>
    </v-flex>

    <v-flex v-if="classListType=='availability'" xs12 class="text-xs-left">
        <v-layout align-center>
          <v-flex class="text-xs-center" style="flex: 0 0 auto;">
            <v-btn
              fab
              outline
              small
              left
              color="primary"
              @click="prevMonth"
            >
              <v-icon dark>
                keyboard_arrow_left
              </v-icon>
            </v-btn>
          </v-flex>
          <v-flex class="text-xs-center" style="flex: 0 0 200px; margin: 0 20px;">
              <div>
                  <v-menu
                    v-model="calMenuOpened"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="curMonthStr"
                        label="Select month"
                        append-icon="event"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="curMonthCal" no-title scrollable type="month" @input="calMenuOpened = false">
                    </v-date-picker>
                  </v-menu>
              </div>
          </v-flex>
          <v-flex class="text-xs-center" style="flex: 0 0 auto;">
            <v-btn
              fab
              outline
              small
              right
              color="primary"
              @click="nextMonth"
            >
              <v-icon
                dark
              >
                keyboard_arrow_right
              </v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
    </v-flex>

  <v-flex v-if="classesPromo.length" xs12 class="text-xs-left">
    <h2>Master classes</h2>
      <div class="layout align-top justify-left row wrap slide-container">
      <v-flex v-if="!c.isShrinked" v-for="(c, i) in classesPromo" class="slide" :key="c.id" @click.stop.prevent="bookClass(c.id)">
          <v-img
              :aspect-ratio="1.25"
              width="150"
              v-if="c.imageUrl"
              :src="c.imageUrl"
          >
          </v-img>
          <div class="master-title">{{c.name}}</div>
      </v-flex>
      </div>
  </v-flex>
  <v-flex xs12 md8 class="text-xs-left">
    <v-layout align-top justify-center row wrap class="layout-classes-wrapper">
        <ul v-if="classListType=='teacher'" class="lessons">
            <template v-for="(item, index) in teachersListPrepared">
            <li v-if="item.isHeader" :key="item.key">
                <div class="image">
                    <v-img
                        v-if="item.avatar"
                        height="110"
                        width="137"
                        :src="item.avatar"
                    >
                    </v-img>
                </div>
                <div class="text">
                    <div class="title v-card__title">
                        <div><router-link :to="'/teacher_profile/'+item.id">{{item.title}}</router-link></div>
                        <Rating object-type="teacher" :object-id="item.id"></Rating>
                    </div>
                    <div class="description">
                        <div v-if="!item.expanded">{{ item.shortDescription }} <a v-if="item.expandable" @click="toggle(item.key)">more</a></div>
                        <div v-else>{{ item.description }} <a v-if="item.expandable" @click="toggle(item.key)">collapse</a></div>
                    </div>
                </div>
            </li>
            <li v-else :key="item.key" class="bottom-line">
                <div class="text">
                    <div class="title">
                        <router-link :to="'/class/'+item.id">{{ item.title }}</router-link>
                        <v-chip v-if="item.isMasterClass" label class="small-chip">MASTER CLASS</v-chip>
                        <v-chip v-if="item.isEditorPick" label class="small-chip">EDITOR PICK</v-chip>
                    </div>
                </div>
                <div class="cta">
                    <span v-if="item.isEnrollable">
                        <v-btn v-if="item.instantAvailable && item.isPrivate" fab small color="primary" @click.stop.prevent="bookClass(item.id)">
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                        <v-btn v-else fab small color="primary" @click.stop.prevent="item.isPrivate ? $router.push('/class/'+item.id) : bookClass(item.id)">
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                    </span>
                </div>
            </li>
            </template>
        </ul>
        <ul v-else-if="classListType=='venue'" class="lessons">
            <template v-for="(item, index) in companyListPrepared">
            <li v-if="item.isHeader" :key="item.key" class="company-header">
                <div class="image">
                    <v-img
                        v-if="item.avatar"
                        height="110"
                        width="137"
                        :src="item.avatar"
                    >
                    </v-img>
                </div>
                <div class="text">
                    <div class="title header-title">
                        <div><router-link :to="item.link">{{item.title}}</router-link></div>
                        <Rating object-type="company" :object-id="item.id"></Rating>
                    </div>
                    <div v-if="item.venue" class="venue">{{item.venue}}</div>
                    <div class="description">
                        <div v-if="!item.expanded">{{ item.shortDescription }} <a v-if="item.expandable" @click="toggle(item.key)">more</a></div>
                        <div v-else>{{ item.description }} <a v-if="item.expandable" @click="toggle(item.key)">collapse</a></div>
                    </div>
                </div>
            </li>
            <li v-else :key="item.key" class="bottom-line">
                <div class="text">
                    <div class="title">
                        <router-link :to="'/class/'+item.id">{{ item.title }}</router-link>
                        <v-chip v-if="item.isMasterClass" label class="small-chip">MASTER CLASS</v-chip>
                        <v-chip v-if="item.isEditorPick" label class="small-chip">EDITOR PICK</v-chip>
                    </div>
                    <div v-if="false" class="description">
                        <b v-if="item.venue">{{item.venue}}</b>
                        <div>{{ item.location }}</div>
                    </div>
                </div>
                <div class="cta">
                    <span v-if="item.isEnrollable">
                        <v-btn color="primary" v-if="item.instantAvailable && item.isPrivate" fab small @click.stop.prevent="bookClass(item.id)">
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                        <v-btn color="primary" v-else fab small @click.stop.prevent="item.isPrivate ? $router.push('/class/'+item.id) : bookClass(item.id)">
                            <v-icon>arrow_forward</v-icon>
                        </v-btn>
                    </span>
                </div>
            </li>
            </template>
        </ul>
        <ul v-else-if="classListType=='plain'" class="lessons">
            <template v-for="(item, index) in plainListPrepared">
                <class-item :key="item.key" v-bind="item" v-on:bookClass="bookClass"></class-item>
            </template>
        </ul>
        <ul v-else class="lessons">
            <template v-for="(item, index) in classesListPrepared">
            <li v-if="item.date" :key="item.key">
                <v-subheader>{{ item.date }}</v-subheader>
            </li>
            <class-item v-else :key="item.key" v-bind="item" v-on:bookClass="bookClass"></class-item>
            </template>
        </ul>
        <v-progress-circular
                v-if="pagerLoading"
          indeterminate
          color="platform-green"
        ></v-progress-circular>
    </v-layout>
  </v-flex>
  <v-flex xs12 md4 class="text-xs-right" order-xs3 order-md2>
    <v-layout align-top justify-center row wrap>
      <v-flex xs12 class="text-xs-left">
        <h3 v-if="calMapSwitch == 'calendar' && !(classListType=='teacher' && lessonType=='private')">When?</h3>
        <h3 v-if="calMapSwitch == 'map'">Where?</h3>
        <a href="javascript:void(0)" v-if="calMapSwitch == 'map' && !(classListType=='teacher' && lessonType=='private')" @click="calMapSwitch='calendar'">View Calendar</a>
        <a href="javascript:void(0)" v-if="calMapSwitch == 'calendar'" @click="calMapSwitch='map'">View Map</a>
        <v-date-picker v-if="calMapSwitch == 'calendar' && !(classListType=='teacher' && lessonType=='private')" v-model="datesInCalendar" readonly multiple no-title :picker-date.sync="pickerDate"></v-date-picker>
        <GeoMap v-if="calMapSwitch == 'map'" v-bind="mapData" height="300px"/>
      </v-flex>

    </v-layout>
  </v-flex>
</v-layout>
</template>

<script>
import moment from 'moment'
import _ from 'lodash'
import axios from 'axios'

import utils from '@/lib/utils.js'
import classHelper from '@/lib/helpers/Class.js'

import ClassItem from '@/components/Classes/ClassItem'
import Rating from '@/components/basic/Rating.vue'
import GeoMap from '@/components/basic/GeoMap.vue'
//import CategorySelect from '@/components/basic/CategorySelect.vue'
import SearchBox from '@/components/basic/Searchbox.vue'
import metadata from '@/mixins/metadata'
import companyService from '@/lib/services/company'

let scrollListener = null

export default {
    props: ['city', 'state', 'category', 'subcategory', 'venue', 'lessonType', 'teacher', 'classId'],
    mixins: [metadata],
    components: {
        GeoMap,
        //CategorySelect,
        Rating,
        SearchBox,
        ClassItem,
    },
    data () {
        return {
            isLoading: false,
            availableCategories: [],
            availableSubcategories: [],
            categoriesSelected: [],
            categoryRequest: false,
            newCategory: null,
            //lessonType: null,
            //city: null,
            timeInterval: 'today',
            items: [],
            curSlide: 0,
            slidesInRow: 1,
            pagination: false,
            paginationPerPage: 10,
            paginationCurrent: 1,
            paginationCount: 0,
            paginationSettings: {},
            zip: null,
            isMaster: false,
            calMapSwitch: 'map',
            pickerDate: null,
            sorting: null,

            weekDiff: 0,
            monthDiff: 0,
            doFirst10Request: true,

            autoNextWeekLimit: 16,
            autoNextWeekEnabled: true,

            classListType: 'plain',

            place: null,
            lat: null,
            lng: null,

            classListTypeList: [
                {text: 'Class', value: 'plain'},
                {text: 'Teacher', value: 'teacher'},
                {text: 'Date', value: 'availability'},
                {text: 'Venue', value: 'venue'},
            ],

            geolocationBrowserSupport: true,
            geolocationAvailable: true,

            expanded: {},
            typeItems: [
                {value: null, text: 'All'},
                {value: 'online', text: 'Online (all)'},
                {value: 'group', text: 'Group'},
                {value: 'private', text: 'Private'},
            ],
            arrangeItems: [
                {text: 'Class', value: 'plain-distance'},
                {text: 'Date', value: 'availability-date'},
                {text: 'By Price', value: 'plain-price'},
                {text: 'Teachers', value: 'teacher-distance'},
                {text: 'Venue', value: 'venue-distance'},
            ],
            arrange: null,
            calMenuOpened: false,
            curMonthCal: moment().format('YYYY-MM'),
            pagerCount: 0,
            pagerNext: null,
            pagerPrev: null,
            pagerLoading: false,
        }
    },
    created: function () {
        let _this = this
        const setParams = (params) => {
            _.each(params, (v, k) => {
                this[k] = v
            })
        }
        if (this.$store.state.learnerSearch) {
            let presetData = {}
            presetData.items = this.$store.state.learnerSearch.items || []
            presetData.categoriesSelected = this.$store.state.learnerSearch.categoriesSelected || []
            //presetData.lessonType = this.$store.state.learnerSearch.lessonType
            //presetData.city = this.$store.state.learnerSearch.city
            presetData.zip = this.$store.state.learnerSearch.zip
            presetData.timeInterval = this.$store.state.learnerSearch.timeInterval || []
            presetData.isMaster = this.$store.state.learnerSearch.isMaster || false
            setParams(presetData)
        } else {
            //load data thru ajax call

        }
        this.arrange = this.arrangeItems[0]
        // drop items saved from last home -> this page visit, due to redundant page composition
        this.items = []
        /*
        if(this.city && this.state) {
            this.reloadClasses()
        }
        */
        console.log('add scrollListener')
        scrollListener = _.bind(this.loadNextPage, this)
        document.documentElement.addEventListener('endOfPage', scrollListener, {passive: true})
    },
    beforeDestroy() {
        console.log('remove scrollListener')
        document.documentElement.removeEventListener('endOfPage', scrollListener)
    },
    computed: {
        lessonTypeWrap: {
            get() {
                if(this.state === 'none' && !this.lessonType && this.city === 'online') {
                    return 'online'
                }
                return this.lessonType
            },
            set(v) {
                let params = {}
                if(v === 'online') {
                    params.city = 'online'
                    params.state = 'none'
                    params.lessontype = '0'

                } else {
                    params.lessontype = !v ? '0' : v
                }
                params = _.assign({}, this.$route.params, params)
                if(!_.isEqual(this.$route.params, params)) {
                    this.$router.push({name: 'learners_search2', params})
                }
            }
        },
        sortingList() {
            const res = [
                {text: 'Price', value: 'price'},
                {text: 'Nearest', value: 'distance'}
            ]
            if(this.classListType != 'availability') {
                res.unshift({text: 'Date', value: 'date'})
            }
            return res
        },
        curMonthStr() {
            let date = new Date(this.startDate)
            date.setDate(date.getDate()+3)
            return date.toLocaleString('en-us', {month: 'long', year: 'numeric'})
        },
        curDatesArr() {
            let res = []
            for (let i=0;i<31;i++) {
                let date = new Date(this.startDate)
                date.setDate(date.getDate()+i)
                res.push(date)
            }
            return _.map(res, v => ({
                date: utils.dateToString(v),
                num: v.getDate(),
                day: v.toLocaleString('en-us', {weekday: 'short'}).substr(0, 1)
            }))
        },
        startDate() {
            let today = new Date()
            const days = today.getDate()
            let date = moment(this.curMonthCal, 'YYYY-MM').toDate()
            const dateCheck = new Date(date)
            date.setDate(days)
            if(date.getMonth() !== dateCheck.getMonth()) {
                date.setDate(1)
                date = new Date(date-1)
            }
            return date
        },
        categorySelects: function () {
            let res = []
            let subCats = _.groupBy(this.availableSubcategories, 'category')
            _.each(this.availableCategories, (c) => {
                const items = _.map(subCats[c.id] || [], (sc) => ({text: sc.name, value: sc.id}))
                res.push({
                    items: items,
                    label: c.name,
                    id: c.id,
                    selected: this.categoriesSelected ? _.filter(items, v => this.categoriesSelected.indexOf(v.value) != -1) : undefined
                })
            })
            /*
            res.push({
                items: _.map(this.availableSubcategories, (sc) => ({text: sc.name, value: sc.id})),
                label: 'Click to see topics in each category or enter your own.',
                id: 0,
                selected: this.categoriesSelected[0] || []
            })
            */
            return res
        },
        cityName() {
            return this.city && typeof this.city == 'object' ? this.city.address_city+', '+this.city.address_state : this.city
        },
        datesInCalendar() {
            let res = {}
            let y = new Date().getFullYear()
            let m = new Date().getMonth()
            if (this.pickerDate) {
                y = this.pickerDate.split('-')[0]
                m = this.pickerDate.split('-')[1]-1
            }
            _.each(this.items, (v) => {
                let dates
                if(v.day_select_type == 'weekly')
                    dates = utils.getCalendarDatesForMonth(y, m, v.weekdays_schedule, v.start_date, v.until_date, v.schedule_excluded || [])
                else
                    dates = _.map(v.schedule_dates, d => d.date)
                _.assign(res, _.keyBy(dates, v => v))
            })
            return _.map(res, v => v)
        },
        mapData() {
            return {
                center: {
                    lat: _.meanBy(_.filter(this.items, v => v.lat), v => v.lat),
                    lng: _.meanBy(_.filter(this.items, v => v.lng), v => v.lng),
                },

                markers: _.map(this.items, v => ({
                    position: {
                        lng: v.lng,
                        lat: v.lat
                    },
                    //label: 'name',
                }))

            }
        },
        complexData() {

            let res = {
                lessonType: this.lessonType,
                //newCategory: this.newCategory,
                zip: this.zip,
                city: this.city || 'all',
                state: this.state || 'all',
                //timeInterval: {from: this.curDatesArr[0].date, to: this.curDatesArr[this.curDatesArr.length-1].date},
                //categoriesSelected: this.categoriesSelected,
                category: this.category,
                subcategory: this.subcategory,
                classListType: this.classListType,
                sorting: this.sorting,
                venue: this.venue,
                classId: this.classId,
                teacher: this.teacher,
            }
            if (this.isMaster)
                res.isMaster = this.isMaster
            return res
        },
        plainListPrepared() {
            let resItems = []
            _.each(this.items, v => {
                let res = {
                    id: v.id,
                    key: v.id,
                    title: v.is_private ? v.private_className+' with '+v.teacher.first_name : v.name,
                    isMasterClass: v.is_master,
                    isEditorPick: false,
                    isPrivate: v.is_private ? true : false,
                    isEnrollable: this.isEnrollable(v),
                    instantAvailable: v.instant_booking,
                    freqDates: '',
                    location: '',
                    teacher: `${v.teacher.first_name} ${v.teacher.last_name}`,
                    price: '',
                    from: '',
                    to: '',
                    schedule: '',
                    avatar: classHelper.previewImageSrc(v.master_media),
                    description: v.groupClassSummary ? v.groupClassSummary : '',
                    venue: v.teaching_venue || '',
                    classItem: v,
                }

                if (v.class_type === "address") {
                    res.location = `${v.address} ${v.address_street}, ${v.address_zip}`
                } else if (v.class_type === "online") {
                    res.location = 'online'
                } else if (v.class_type === 'student_location') {
                    res.location = 'your location'
                }
                res.price = classHelper.price(v, this.is_private)
                /*
                if (v.is_private) {
                    res.price = utils.formatPrice(v.rate, v.currency)+' /hour'
                } else {
                    if (v.flexible_dates)
                        res.price = utils.formatPrice(v.drop_in_rate, v.currency)
                    else {
                        if (v.standard_packages.length) {
                            res.price = utils.formatPrice(v.standard_packages[0].totalPrice, v.currency)+', '+v.standard_packages[0].numberOfLessons+` class${v.standard_packages[0].numberOfLessons == 1 ? '' : 'es'}`
                        } else if (v.custom_packages.length) {
                            res.price = utils.formatPrice(v.custom_packages[0].totalPrice, v.currency)+', '+v.custom_packages[0].numberOfLessons+` class${v.custom_packages[0].numberOfLessons == 1 ? '' : 'es'}`
                        }
                    }
                }
                */
                resItems.push(res)
            })
            //resItems = _.sortBy(resItems, v => -v.isMasterClass)
            return resItems
        },
        companyListPrepared() {
            let resItems = []
            const items = _.sortBy(_.filter(this.items,  v => v.teacher.user.is_company), c => -c.id)
            let classGroups = _.groupBy(items,  v => v.teacher.user.company_profile.id)
            let companies = _.sortBy(_.uniqBy(_.map(items, v => v.teacher.user.company_profile), v => v.id), v => v.name)

            _.each(companies, t => {
                const key = `t${t.id}`
                const uniqVenues = _.uniq(_.map(classGroups[t.id], v => v.teaching_venue || ''))
                const description = t.description
                let expandable = description && description.length > 200
                resItems.push({
                    isHeader: true,
                    id: t.id,
                    title: `${t.name}`,
                    link: companyService.getLink(t),
                    venue: uniqVenues.length === 1 ? classHelper.location(classGroups[t.id][0]) : '',
                    description: description,
                    shortDescription: expandable ? description.substring(0, 200)+'...' : description,
                    avatar: classHelper.previewImageSrc(t.main_media || t.media),
                    expanded: this.expanded[key],
                    expandable: expandable,
                    key: key,
                })
                _.each(classGroups[t.id], v => {
                    let res = {
                        id: v.id,
                        key: v.id,
                        title: `${v.is_private ? v.private_className : v.name}`,
                        isMasterClass: v.is_master,
                        isEditorPick: false,
                        isPrivate: v.is_private ? true : false,
                        isEnrollable: this.isEnrollable(v),
                        instantAvailable: v.instant_booking,
                        freqDates: '',
                        location: '',
                        teacher: `${v.teacher.first_name} ${v.teacher.last_name}`,
                        price: '',
                        from: '',
                        to: '',
                        schedule: '',
                        avatar: classHelper.previewImageSrc(v.master_media),
                        description: v.groupClassSummary ? v.groupClassSummary : '',
                        venue: uniqVenues.length === 1 ? '' : v.teaching_venue || '',
                        classItem: v,
                    }
                    if (v.day_select_type === 'weekly' && v.weekdays_schedule.length) {
                        res.schedule = _.map(_.sortBy(v.weekdays_schedule, 'weekday'), v => utils.getWeekday(v.weekday)).join(', ')
                        let untilDate = new Date()
                        untilDate.setMonth(untilDate.getMonth()+1)
                        let dates = utils.getCalendarDatesForPeriod(utils.dateToString(new Date()), utils.dateToString(untilDate), v.weekdays_schedule, v.start_date, v.until_date, v.schedule_excluded)
                        res.nextDate = dates[0]
                    } else {
                        res.nextDate = _.filter(_.map(v.schedule_dates, 'date').sort(), v => {
                            return utils.stringToDate(v) > new Date()
                        })[0]
                    }
                    if(res.nextDate)
                        res.nextDate = utils.stringToDate(res.nextDate).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})
                    if (v.class_type === "address") {
                        res.location = `${v.address} ${v.address_street}, ${v.address_zip}`
                    } else if (v.class_type === "online") {
                        res.location = 'online'
                    } else if (v.class_type === 'student_location') {
                        res.location = 'your location'
                    }
                    resItems.push(res)
                })

            })
            //resItems = _.sortBy(resItems, v => -v.isMasterClass)
            return resItems
        },
        teachersListPrepared() {
            let resItems = []
            let classGroups = _.groupBy(_.sortBy(this.items, c => -c.id),  v => v.teacher.id)
            let teachers = _.sortBy(_.uniqBy(_.map(this.items, v => v.teacher), v => v.id), v => `${v.first_name} ${v.last_name}`)

            _.each(teachers, t => {
                let expandable = t.description && t.description.length > 200
                const key = `t${t.id}`
                resItems.push({
                    isHeader: true,
                    id: t.id,
                    title: `${t.first_name} ${t.last_name}`,
                    description: t.description,
                    shortDescription: expandable ? t.description.substring(0, 200)+'...' : t.description,
                    avatar: classHelper.previewImageSrc(t.media),
                    expanded: this.expanded[key],
                    expandable: expandable,
                    key: key,
                })
                _.each(classGroups[t.id], v => {
                    let res = {
                        id: v.id,
                        key: v.id,
                        title: `${v.is_private ? v.private_className : v.name}`,
                        isMasterClass: v.is_master,
                        isEditorPick: false,
                        isPrivate: v.is_private ? true : false,
                        isEnrollable: this.isEnrollable(v),
                        instantAvailable: v.instant_booking,
                        freqDates: '',
                        location: '',
                        teacher: `${v.teacher.first_name} ${v.teacher.last_name}`,
                        price: '',
                        from: '',
                        to: '',
                        schedule: '',
                        avatar: classHelper.previewImageSrc(v.master_media),
                        description: v.groupClassSummary ? v.groupClassSummary : '',
                        classItem: v,
                    }
                    if (v.day_select_type == 'weekly' && v.weekdays_schedule.length) {
                        res.schedule = _.map(_.sortBy(v.weekdays_schedule, 'weekday'), v => utils.getWeekday(v.weekday)).join(', ')
                        let untilDate = new Date()
                        untilDate.setMonth(untilDate.getMonth()+1)
                        let dates = utils.getCalendarDatesForPeriod(utils.dateToString(new Date()), utils.dateToString(untilDate), v.weekdays_schedule, v.start_date, v.until_date, v.schedule_excluded)
                        res.nextDate = dates[0]
                    } else {
                        res.nextDate = _.filter(_.map(v.schedule_dates, 'date').sort(), v => {
                            return utils.stringToDate(v) > new Date()
                        })[0]
                    }
                    if(res.nextDate)
                        res.nextDate = utils.stringToDate(res.nextDate).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})
                    if (v.class_type == "address") {
                        res.location = `${v.address} ${v.address_street}, ${v.address_zip}`
                    } else if (v.class_type == "online") {
                        res.location = 'online'
                    } else if (v.class_type == 'student_location') {
                        res.location = 'your location'
                    }
                    res.price = classHelper.price(v, this.is_private)
                    resItems.push(res)
                })

            })
            //resItems = _.sortBy(resItems, v => -v.isMasterClass)
            return resItems
        },
        classesListPrepared() {
            const curDates = _.keyBy(this.curDatesArr, v => v.date)
            let startDate = this.startDate
            let startDateStr = utils.dateToString(startDate)
            let endDateStr = this.curDatesArr[this.curDatesArr.length-1].date
            //let endDate = utils.stringToDate(endDateStr)
            let dateLessonDict = {}
            let lessonDict = _.keyBy(this.items, 'id')
            _.each(this.items, item => {
                if(item.day_select_type === 'weekly') {
                    let dates = utils.getCalendarDatesForPeriod(startDateStr, endDateStr, item.weekdays_schedule, item.start_date, item.until_date, item.schedule_excluded)
                    _.each(dates, date => {
                        if(!dateLessonDict[date]) {
                            dateLessonDict[date] = []
                        }
                        dateLessonDict[date].push(item.id)
                    })
                } else {
                    _.each(_.map(item.schedule_dates), v => {
                        if(!curDates[v.date])
                            return
                        if(!dateLessonDict[v.date]) {
                            dateLessonDict[v.date] = []
                        }
                        dateLessonDict[v.date].push(item.id)
                    })
                }
            })
            let resItems = []
            _.each(_.sortBy(Object.keys(dateLessonDict), v => v), (dateStr) => {
                let ids = dateLessonDict[dateStr]
                resItems.push({
                    date: utils.stringToDate(dateStr).toLocaleString('en-us', { month: 'long', day: 'numeric', weekday: 'long' }),
                    key: dateStr,
                })
                _.each(_.sortBy(ids, id => {
                    let item = lessonDict[id]
                    let weekday = utils.stringToDate(dateStr).getDay()
                    if(item.day_select_type == 'weekly') {
                        if (item.weekdays_schedule.length) {
                            return _.find(item.weekdays_schedule, {weekday}).start
                        } else
                            return Infinity
                    } else {
                        return _.find(item.schedule_dates, {date: dateStr}).start
                    }
                }), id => {
                    let v = lessonDict[id]
                    let res = {
                        id: v.id,
                        key: v.id+'_'+dateStr,
                        title: v.is_private ? v.private_className+' with '+v.teacher.first_name : v.name,
                        isMasterClass: v.is_master,
                        isEditorPick: false,
                        isPrivate: v.is_private ? true : false,
                        isEnrollable: this.isEnrollable(v),
                        freqDates: '',
                        location: '',
                        teacher: `${v.teacher.first_name} ${v.teacher.last_name}`,
                        price: '',
                        from: '',
                        to: '',
                        avatar: classHelper.previewImageSrc(v.master_media),
                        description: v.groupClassSummary ? v.groupClassSummary : '',
                        venue: v.teaching_venue || '',
                        classItem: v,
                    }
                    if (v.day_select_type == 'weekly') {
                        if (v.weekdays_schedule.length) {
                            let weekday = utils.stringToDate(dateStr).getDay()
                            let dayData = _.find(v.weekdays_schedule, {weekday})
                            res.from = utils.time24HtoAMPM(dayData.start)
                            res.to = utils.time24HtoAMPM(dayData.end)
                        }
                    } else {
                        let dayData = _.find(v.schedule_dates, {date: dateStr})
                        res.from = utils.time24HtoAMPM(dayData.start)
                        res.to = utils.time24HtoAMPM(dayData.end)
                    }
                    if (v.class_type == "address") {
                        res.location = `${v.address} ${v.address_street}, ${v.address_zip}`
                    } else if (v.class_type == "online") {
                        res.location = 'online'
                    } else if (v.class_type == 'student_location') {
                        res.location = 'your location'
                    }
                    res.price = classHelper.price(v, this.is_private)
                    //calc actual dates
                    let dates = []
                    const dateLimit = 5
                    let counter = 0
                    let month = new Date().getMonth()
                    const monthDict = [
                        'Jan',
                        'Feb',
                        'Mar',
                        'Apr',
                        'May',
                        'Jun',
                        'Jul',
                        'Aug',
                        'Sep',
                        'Oct',
                        'Nov',
                        'Dec',
                    ]
                    if (v.day_select_type == 'weekly' && v.weekdays_schedule && v.weekdays_schedule.length) {
                        for (let now = new Date(); counter<dateLimit; now.setDate(now.getDate() + 1)) {
                            if (_.find(v.weekdays_schedule, {weekday: now.getDay()})
                            && (!v.schedule_excluded || !v.schedule_excluded.length || v.schedule_excluded.indexOf(utils.dateToString(now)) == -1)) {
                                dates.push(!counter || now.getMonth() != month ? `${monthDict[now.getMonth()]} ${now.getDate()}` : now.getDate())
                                month = now.getMonth()
                                counter++
                            }
                        }
                    } else if (v.day_select_type == 'monthly' && v.schedule_dates && v.schedule_dates.length) {
                        _.each(v.schedule_dates, (d) => {
                            if (counter >= dateLimit)
                                return
                            let now = utils.stringToDate(d.date)
                            if(now.getTime()+86399000 > new Date().getTime()
                            && (!v.schedule_excluded || !v.schedule_excluded.length || v.schedule_excluded.indexOf(d.date) == -1)) {
                                //dates.push(utils.stringToDate(d))
                                dates.push(!counter || now.getMonth() != month ? `${monthDict[now.getMonth()]} ${now.getDate()}` : now.getDate())
                                month = now.getMonth()
                                counter++
                            }
                        })
                    }
                    res.freqDates = dates.join(', ')
                    resItems.push(res)
                })
            })
            if (!resItems.length && this.autoNextWeekLimit && this.autoNextWeekEnabled) {
                this.autoNextWeekLimit--
                this.nextWeek()
            } else {
                this.autoNextWeekEnabled = false
            }
            return resItems
        },
        classesPromo() {
            let res = _.map(_.filter(this.items, v => v.is_master), (c) => {
                return {
                    imageUrl: classHelper.previewImageSrc(c.master_media),
                    name: c.is_private ? c.private_className : c.name,
                    id: c.id,
                    dates: utils.stringToDate(c.start_date).toLocaleString('en-us', {month: 'long', day: 'numeric'})+' - '+(c.until_date ? utils.stringToDate(c.until_date).toLocaleString('en-us', {month: 'long', day: 'numeric'}) : 'ongoing'),
                    teacher_name: c.teacher.first_name+' '+c.teacher.last_name,
                    isShrinked: c.isShrinked,
                }
            })
            return res
        },
        carouselPrev() {
            return _.find(this.classesPromo, {isShrinked: true})
        },
        carouselNext() {
            return this.classesPromo.length > 2
        },
        carouselOptions() {
            return {
                perPage: this.slidesInRow,
                loop: true,

            }
        },
        catOrSub() {
            if(!this.$refs.searchbox)
                return null
            const subcategory = _.find(this.$refs.searchbox.availableSubcategories, {id: Number(this.subcategory)})
            const category = _.find(this.$refs.searchbox.availableCategories, {id: Number(this.category)})
            return subcategory ? subcategory.name : null || category ? category.name : null
        },
    },
    watch: {
        arrange(newVal) {
            if(newVal) {
                this.classListType = (newVal.value ? newVal.value : newVal).split('-')[0]
                this.sorting =  (newVal.value ? newVal.value : newVal).split('-')[1]
            }
        },
        classListType(newVal) {
            console.log('classListType', newVal)
        },
        lessonTypeWrap(newVal) {

        },
        complexData(cur, old) {
            if(_.some(cur, (v, i) => v != old[i] && (v || old[i])) || _.some(old, (v, i) => v != cur[i] && (v || cur[i])))
                this.reloadClasses()
        },
        place(val) {
            if(val) {
                this.lat = val.geometry.location.lat()
                this.lng = val.geometry.location.lng()
                this.sortItems()
            }
        },
        sorting(val) {
            this.sortItems()
            if(val === 'distance') {
                this.getGeolocation().then(res => {
                    console.log(res)
                    this.lat = res.coords.latitude
                    this.lng = res.coords.longitude
                    this.sortItems()
                }).catch(e => console.log(e))
            }
        },
    },
    methods: {
        loadNextPage() {
            console.log('loadNextPage')
            if(this.pagerNext && !this.pagerLoading) {
                this.pagerLoading = true
                this.reloadClasses(this.pagerNext, true)
            }
        },
        isEnrollable(item) {
            return !!(item.can_book || item.can_book_url)
        },
        toggle(key) {
            this.$set(this.expanded, key, !this.expanded[key])
        },
        getGeolocation() {
            return new Promise((resolve, reject) => {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(res => {
                        return resolve(res)
                    }, err => {
                        this.geolocationAvailable = false
                        return reject(err)
                    })
                } else {
                    this.geolocationBrowserSupport = false
                    this.geolocationAvailable = false
                    return reject(new Error('geolocation not supported by browser'))
                }
            })
        },
        setPlace(place) {
            this.place = place
        },
        reloadClasses(url, concatenate) {
            if(!this.sorting || !this.classListType) {
                return
            }
            if(!concatenate)
                this.isLoading = true
            let reqData = {...this.complexData}
            if(this.classListType === 'plain' && this.sorting === 'distance') {
                reqData.paginated = 1
                reqData.lat = this.lat
                reqData.lng = this.lng
            }

            /*
            if(this.doFirst10Request) {
                this.doFirst10Request = false
                reqData = {
                    //limit: 10,
                    city: this.complexData.city,
                }
            }
            */
            axios.post(url || '/api/filter_classes/', reqData).then((res) => {
                console.log('done', res)
                const items = res.data.results || res.data
                if(res.data) {
                    //_this.$emit('update:step', 11)
                    if(concatenate) {
                        this.items = [...this.items, ...items]
                    } else {
                        this.items = this.preFilterItems(items)
                        this.sortItems()
                    }
                    if(reqData.paginated) {
                        this.pagerCount = res.data.count
                        this.pagerNext = res.data.next
                        this.pagerPrev = res.data.previous
                    } else {
                        this.pagerCount = 0
                        this.pagerNext = null
                        this.pagerPrev = null
                    }
                    this.pagination = false
                    this.$store.commit('setLearnerSearch', _.assign({}, {
                        items: this.items,
                    }, this.complexData))

                } else {
                    //process errors

                }
            }).catch(function () {
                //console.log(arguments)
            }).then(() => {
                this.isLoading = false
                this.pagerLoading = false
            })
        },
        sortItems() {
            if(this.sorting === 'price') {
                this.items = _.sortBy(this.items, [v => -this.isEnrollable(v), v => classHelper.sortByPriceValue(v)])
                //console.log(_.map(this.items, c => [-this.isEnrollable(c), classHelper.sortByPriceValue(c)]))
            }
            if(this.sorting === 'distance' && this.lat && this.lng) {
                this.items = _.sortBy(this.items, [v => -this.isEnrollable(v), v => (v.lat && v.lng ? Math.sqrt(Math.pow(this.lat-v.lat, 2) + Math.pow(this.lng-v.lng, 2)) : 1000000)])
            }
            if(this.sorting === 'date') {
                this.items = _.sortBy(this.items, [v => -this.isEnrollable(v), v => -v.id])
            }
        },
        preFilterItems(items) {
            let res = _.filter(items, v => {
                return classHelper.canEnroll(v)
            })
            _.each(res, v => {
                v.schedule_dates = v.schedule_dates ? _.uniqBy(v.schedule_dates, 'date') : []
            })
            return res
        },
        nextMonth() {
            this.curMonthCal = moment(this.curMonthCal, 'YYYY-MM').add(1, 'M').format('YYYY-MM')
        },
        prevMonth() {
            this.curMonthCal = moment(this.curMonthCal, 'YYYY-MM').subtract(1, 'M').format('YYYY-MM')
        },
        nextWeek() {
            this.weekDiff ++
        },
        prevWeek() {
            this.weekDiff --
        },
        getCurrencyLogo(id) {
            return utils.getCurrencyLogo(id)
        },
        bookClass(id) {
            console.log(_.find(this.items, {id: id}))
            const foundClass = _.find(this.items, {id: id})
            if(!foundClass)
                return
            if(!foundClass.can_book) {
                if(!foundClass.can_book_url) {

                } else {
                    window.open(utils.prepareUrl(foundClass.can_book_url), '_blank')
                    return
                }
            }
            //this.$store.commit('setLearnerChoice', _.find(this.items, {id: id}))
            //this.$emit('next:step')
            this.$router.push(`/learners/${id}/2`)
        },
        changeCarouselFunc () {
            console.log(arguments)
        },
        prevClick() {
            let classesPromo = _.filter(this.items, v => v.is_master)
            for (let i=classesPromo.length-3; i>= 0 ;i--) {
                if (classesPromo[i].isShrinked) {
                    this.$set(classesPromo[i], 'isShrinked', false)
                    break
                }
            }
        },
        nextClick() {
            let classesPromo = _.filter(this.items, v => v.is_master)
            for (let i=0;i<=classesPromo.length-3;i++) {
                if (!classesPromo[i].isShrinked) {
                    this.$set(classesPromo[i], 'isShrinked', true)
                    break
                }
            }
        },
        changePage(page) {

        },
        getMetaTitle() {
            if(!this.$refs.searchbox || !this.metadataTemplate.title)
                return
            let location = this.$refs.searchbox.locationText
            let lessontype = this.lessonType
            return this.metadataTemplate.title
                .replace('${location}', location || '')
                .replace('${category}', this.catOrSub || '')
                .replace('${lessontype}', lessontype || '')
                .replace(/^:[ ]*/, '')
        },
        getMetaDescription() {
            if(!this.$refs.searchbox || !this.metadataTemplate.metatag)
                return
            let location = this.$refs.searchbox.locationText
            let lessontype = this.lessonType
            return this.metadataTemplate.metatag
                .replace('${location}', location || '')
                .replace('${category}', this.catOrSub || '')
                .replace('${lessontype}', lessontype || '')
                .replace(/^:[ ]*/, '')
        },
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.slide-container {
    overflow: hidden;
    height: 204px;
    justify-content: space-between;
    > div {
        cursor: pointer;
    }

    .master-title {
        font-family: Roboto, sans-serif;
        font-weight: 700;
        font-size: 14px;
        color: #000000;
        letter-spacing: 0;
        margin-bottom: 100px;
    }
}
.slide {
    /*height: 200px;*/
    flex: 0 1 150px;
}
.small-chip {
    font-size: 12px;
    height: 20px;

}
.carousel-container {
    width: 100%;
    position: relative;
    top: 0;
    height: 200px;
}
.weekday {
    padding: 3px;
}
.padded {
    padding: 0 10px;
}


.filters {
    width: 100%;
    text-align: left;
    margin-bottom: 10px;
    &:last-child {
        margin-bottom: 40px;
    }
    .check-container {
        display: inline-block;
        margin: 0;
        position: relative;
        cursor: pointer;
        font-family: Montserrat, sans-serif;
        font-weight: 500;
        font-size: 16px;
        line-height: 33px;
        color: #666;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;

        &.separator {
            width: 20px;
        }

        &.selector {
            width: 200px;
        }
    }
    .check-container.group {
        border: solid 2px #999;
        border-left-width:1px;
    }
    .check-container.private {
        border: solid 2px #999;
        border-right-width:1px;
    }
    .check-container.date {
        border: solid 2px #999;
        border-right-width:1px;
        margin-left: 30px;
    }
    .check-container.price {
        border: solid 2px #999;
        border-right-width:1px;
    }
    .check-container.nearest {
        border: solid 2px #999;
        border-right-width:1px;
    }
    .check-container input {
        position: absolute;
        opacity: 0;
        cursor: pointer;
        height: 0;
        width: 0;
    }
    .checkmark {
        display: block;
        text-align: center;
        width: 150px;
        background-color: #fff;
    }
    .check-container input:checked ~ .checkmark {
      background-color: #C3C3C3;
      color: #fff;
    }
    .sorting {
        display: inline-block;
    }

}

.lessons {
	list-style-type: none;
	padding: 0;
    width: 100%;

    li {
        display: flex;
        flex-direction: row;
        margin-top: 40px;

        &.company-header {
            border-bottom: 1px solid silver;
        }
        &.bottom-line {
            border-bottom: 1px solid silver;
            margin-top: 0;
            min-height: 53px;
            .text {
                display: flex;
                .title {
                    flex: 1 1 50%;
                    height: 1rem;
                    align-self: center;
                    font-size: 1em !important;
                    margin: 0;
                }
                .description {
                    flex: 1 1 50%;
                }
            }
        }
        .image {
            margin-right: 20px;
            flex: 0 0 137px;
        }
        .text {
            flex: 1 1 auto;
        }
        .text .title {
            font-family: Roboto, sans-serif;
            font-weight: 700;
            font-size: 18px;
            color: #000000;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        .text .header-title {
            font-size: 1.6em !important;
        }
        .text .venue {
            font-size: 1em;
        }
        .text .description {
            font-family: Roboto, sans-serif;
            font-weight: 400;
            font-size: 14px;
            line-height: 18px;
            color: #000000;
            letter-spacing: 0;
        }
        .cta {
            align-self: center;
            //margin: -5px 5px -5px 5px;
            flex: 0 0 190px;

            .v-icon {
                display: inline-flex;
            }
        }
        .cta button.more-filters {
            background: rgb(31, 190, 215);
            box-shadow: 0 5px 10px 0 rgba(0,0,0,0.33);
            border-radius: 49px;
            padding: 10px;
            font-weight: 500;
            font-size: 14px;
            color: #FFFFFF;
            text-align: center;
            cursor: pointer;
        }
        .cta button.more-filters:hover {
            background: #fff;
            color: #268390;
        }
    }
}
.nearest-point-input {
    display: inline-block;
    width: 100%;
    //margin: -10px 0 -10px 10px;
    padding-top: 0;
}
.layout-classes-wrapper ul {
    margin-top: -36px;
}

</style>