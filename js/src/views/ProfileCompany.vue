<template>
<div class="teacher-profile-page">
    <div class="teacher-profile-container flex xs12">
      <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 md8 class="text-xs-left">
            <v-card class="general-card">
                <v-card-text>
                  <div class="bio">
                    <v-flex xs12 v-if="avatarUrl" class="text-xs-left">
                      <v-img v-if="avatarUrl" :src="avatarUrl" :aspect-ratio="1.25" width="50%"/>
                    </v-flex>
                    <h1 class="headline">{{title}}</h1>
                    <div v-if="address"><v-icon>location_on</v-icon> <b v-if="teaching_venue">{{teaching_venue}}, </b>  {{address}}</div>
                      <p v-if="bio" v-html="bio"></p>
                    <div><b>Phone:</b> {{phone}}</div>
                    <div><b>Email:</b> {{email}}</div>
                  </div>
                    <v-divider ></v-divider>
                    <div class="headline text-xs-left">
                        Meet your mentor{{teachers.length > 1 ? 's' : ''}}
                    </div>
                    <div v-for="(t, i) in teachersFromatted" :key="t.id" :class="{'teacher-container': true, 'is-hidden': t.isHidden}">
                        <div class="teacher-header">
                            <div class="teacher-avatar"><v-img :src="t.media" :aspect-ratio="1.25"/></div>
                            <div class="teacher-name title">{{t.first_name}} {{t.last_name}}</div>
                        </div>
                        <div class="teacher-description">
                            {{t.description}}
                        </div>
                    </div>
                    <a v-if="showExpandLink" @click="isTeachersExpanded = !isTeachersExpanded">{{ isTeachersExpanded ? '...less' : '...more'}}</a>
                  <v-flex v-if="reviews && reviews.length" xs12 md12 class="text-xs-left">
                    <v-divider ></v-divider>
                    <h3>Reviews</h3>
                    <ReviewItem v-for="gc in reviews" v-bind="gc" :key="gc.id"/>
                  </v-flex>
                </v-card-text>
            </v-card>

        </v-flex>
        <v-flex xs12 md4 class="text-xs-center">
            <div class="text-xs-left">
                <v-btn-toggle v-model="rightSwitch" mandatory class="right-switch">
                    <v-btn flat value="classes">
                        Classes
                    </v-btn>
                    <v-btn flat value="calendar" @click="$router.push(`/company_group_calendar/${id}`)">
                        Calendar
                    </v-btn>
                    <v-btn v-if="memberCenterUrl" flat value="member_center" @click="onClickMemberCenter" style="width: auto;">
                        Member Center
                    </v-btn>
                </v-btn-toggle>
            </div>
            <bound-membership-info v-if="!isMemberOfCompany && membershipId"
                :id="membershipId"
            />
            <v-card v-for="(item, index) in classesSorted" :key="item.id" class="general-card">
                <v-card-title>
                    <div class="headline text-xs-left class-title">
                        <router-link class="class-link" :to="'/class/'+item.id">{{item.is_private ? item.private_className : item.name}}</router-link>
                    </div>
                    <div class="text-xs-left font-weight-bold">{{item.is_private ? 'Private' : 'Group'}}</div>
                </v-card-title>
                <v-card-text>
                    <router-link :to="'/class/'+item.id">
                        <v-img
                          v-if="item.master_media"
                          :src="item.master_media"
                          width="60%"
                        >
                        </v-img>
                    </router-link>
                    <div style="text-align: left;">
                        <v-btn class="platform-green" v-if="canEnrollByClass(item)" large @click="bookClassById(item.id)">Enroll</v-btn>
                    </div>
                    <div v-if="!address" class="text-xs-left">
                        <span v-if="item.class_type !== 'address'"><b>Location: </b></span>
                        <v-icon v-else>location_on</v-icon> {{location(item)}}
                    </div>
                  <div class="text-xs-left">
                    {{item.groupClassSummary}}
                    <router-link :to="'/class/'+item.id">More</router-link>
                  </div>
                </v-card-text>
            </v-card>
          <GeoMap v-bind="mapData" height="300px" v-if="lat && lng"/>
        </v-flex>
      </v-layout>
      </v-container>
    </div>
    <v-dialog
      v-model="contactDialog"
      persistent
      width="400"
      lazy
    >
      <v-card>
        <v-card-title>
            <v-spacer></v-spacer>
            <v-btn icon @click="closeSendMessage">
              <v-icon>close</v-icon>
            </v-btn>
        </v-card-title>
        <v-card-text>
          <SendMessageForm v-if="sendMessageFormData && sendMessageFormData.contact" v-bind="sendMessageFormData" v-on:done="messageDone" v-on:bookLesson="bookClass"/>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="registerDialog"
      width="400"
      persistent
      lazy
    >
      <v-card>
        <v-card-title>
            {{registrationTitle}}
            <v-spacer></v-spacer>
            <v-btn icon @click="registerDialog = false">
              <v-icon>close</v-icon>
            </v-btn>
        </v-card-title>
        <v-card-text>
          <RegMinForm v-bind="regMinFormData" v-on:done="registerDone"/>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-dialog
      v-model="membershipDialog"
      width="400"
      persistent
      lazy
    >
      <v-card>
        <v-card-title>
            Premium Membership
            <v-spacer></v-spacer>
            <v-btn icon @click="membershipDialog = false">
              <v-icon>close</v-icon>
            </v-btn>
        </v-card-title>
        <v-card-text>
            <div>Join as a premium member to access this area</div>
            <div><v-btn @click="buyMembership">GO</v-btn></div>
        </v-card-text>
      </v-card>
    </v-dialog>
</div>
</template>

<script>

import _ from 'lodash'
import { mapGetters, mapActions, mapState } from 'vuex'
import ClassGroup from '@/components/Classes/Group.vue'
import ReviewItem from '@/components/Classes/ReviewItem.vue'
import ClassItem from '@/components/Classes/ClassItem.vue'
import SendMessageForm from '@/components/basic/forms/SendMessage'
import RegMinForm from '@/components/basic/forms/RegMin'
import BoundMembershipInfo from '@/components/bound/BoundMembershipInfo';
import utils from '@/lib/utils.js'
import axios from 'axios'
import classHelper from '@/lib/helpers/Class.js'
import metadata from '@/mixins/metadata'
import classItemMixin from '@/mixins/classItem'
import moment from 'moment'
let untilDate = new Date()
untilDate.setMonth(untilDate.getMonth()+1)


export default {
    mixins: [
        metadata,
        classItemMixin,
    ],
    data: () => ({
        id: null,
        isLoading: false,
        weekdays: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        _curWeekday: null,
        carouselHeight: 300,
        title: '',
        description: '',
        name: '',
        address: '',
        teaching_venue: '',
        media: null,
        main_media: null,
        user: {},
        classes: [],
        rightSwitch: 'classes',
        teachersThreshold: 5,
        isTeachersExpanded: false,
        selectedClass: null,
        memberCenterUrl: '',
        membershipDialog: false,
    }),
    created() {
        this.isLoading = true
        const id = this.$route.params.id
        const slug = this.$route.params.slug
        this.loadCompany(id || slug);
        this.$store.dispatch('syncLogoCompanyProfile', id || slug);
        axios.get('/api/company_profile/'+(id || slug)+'/').then((res) => {
            //console.log('done', res)
            this.id = res.data.id
            this.title = res.data.title || `Welcome to ${res.data.name}`
            this.description = res.data.description
            this.name = res.data.name
            this.media = res.data.media
            this.main_media = res.data.main_media
            this.user = res.data.user || {}
            this.classes = res.data.classes || []
            this.memberCenterUrl = res.data.member_center_url
            let venues = _.uniq(_.map(res.data.classes, classHelper.location))
            if(venues.length === 1) {
                this.address = venues[0]
                this.teaching_venue = res.data.classes[0].teaching_venue
            }
        }).catch(() => {
            //console.log(arguments)

        }).then(() => {
            this.isLoading = false
        })
    },
    components: {
        ReviewItem,
        ClassItem,
        SendMessageForm,
        RegMinForm,
        BoundMembershipInfo,
    },
    computed: {
        ...mapGetters([
            'isMember',
        ]),
        ...mapState('viewingCompany', [
            'company',
        ]),
        classesSorted() {
            const getClosestDate = (dates) => {
                const now = new Date()
                let res = new Date()
                res.setFullYear(2112)
                dates.forEach((d) => {
                    const cur = moment(d).toDate()
                    if (cur > now && cur < res)
                        res = cur
                })
                return res
            }
            return this.classes.sort((a, b) => {
                if(!a.is_private && !b.is_private) {
                    return getClosestDate(a.schedule_dates.map(d => d.date)) - getClosestDate(b.schedule_dates.map(d => d.date))
                }
                if(a.is_private !== b.is_private) {
                    return a.is_private - b.is_private
                }
                return moment(b.created_at).format('x') - moment(a.created_at).format('x')
            })
        },
        showExpandLink() {
            return this.teachers.length > this.teachersThreshold
        },
        teachersFromatted() {
            return this.teachers.map((v, i) => ({
                ...v,
                isHidden: this.showExpandLink && !this.isTeachersExpanded && i >= this.teachersThreshold,
            }))
        },
        teachers() {
            const teacherMap = new Map()
            this.classes.forEach(c => {
                if(!teacherMap.has(c.teacher.id)) {
                    teacherMap.set(c.teacher.id, c.teacher)
                }
            })
            return [...teacherMap.values()]
        },
        privateClasses() {
            return _.filter(this.classes, 'is_private')
        },
        groupClasses() {
            return _.filter(this.classes, {'is_private': false})
        },
        weekdays_schedule() {
            return []
        },
        curWeekday: {
            get() {
                if(typeof this._curWeekday !== 'undefined')
                    return this._curWeekday
                return _.min(_.map(this.weekdays_schedule || [], v => v.weekday))
            },
            set(v) {
                this._curWeekday = v
            }
        },
        email() {
            return this.user ? this.user.email : ''
        },
        phone() {
            return this.user ? this.user.phone : ''
        },
        weekdayTime() {
            const curItem = _.find(this.weekdays_schedule, {weekday: this.curWeekday})
            if(!curItem)
                return ''
            return `${utils.time24HtoAMPM(curItem.start)} - ${utils.time24HtoAMPM(curItem.end)}`
        },
        weekdaysAvailable() {
            return _.map(this.weekdays, (v, i) => ({
                name: v,
                isAvailable: _.find(this.weekdays_schedule, {weekday: i}) ? true : false,
            }))
        },
        availablePeriod() {
            return ''
        },
        teacherName() {
            return this.first_name + ' '+this.last_name
        },
        avatarUrl() {
            const oldest = this.classes.filter(c => c.master_media).sort((a, b) => b.id-a.id)[0]
            return this.main_media ? this.main_media : oldest ? oldest.master_media : this.media
        },
        bio() {
            return utils.formatTextToHtml(this.description)
        },
        currentClass() {
            return this.selectedClass || {}
        },
        membershipId() {
            return this.user && this.user.membership
        },
        isMemberOfCompany() {
            return this.isMember(this.membershipId)
        },
        hasMembership() {
            return !!this.membershipId
        },
    },
    methods: {
        ...mapActions('viewingCompany', [
            'loadCompany',
        ]),
        location(cl) {
            return classHelper.location(cl)
        },
        bookClassById(id) {
            const found = _.find(this.classes, {id})
            if(!found)
                return
            this.selectedClass = found
            this.bookClass()
        },
        onClickMemberCenter() {
            if(!this.hasMembership || this.isMemberOfCompany)
                this.openExternalLink(this.memberCenterUrl)
            else {
                this.membershipDialog = true
            }
        },
        buyMembership() {
            this.$router.push(`/company/membership/${this.id}?return=${this.$route.path}`)
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.teacher-profile-page {
    background-color: rgb(231, 231, 231);
    text-align: center;
    .teacher-profile-container {
        //width: 800px;
        margin: 0 auto;
    }
}
    .class-link {
        text-decoration: none;
        color: #000;
    }
    .class-title {
        flex: 1 0 100%;
    }
    .general-card {
        margin: 0 10px 20px 10px;
    }
    .teacher-container {
        margin: 1.5em 0 1.5em;
        &.is-hidden {
            display: none;
        }
    }
    .teacher-header {
        display: flex;
        .teacher-name {
            flex: 0 1 25%;
            padding-left: 10px;
        }
        .teacher-avatar {
            flex: 0 1 25%;
        }
    }
    .teacher-description {
        text-indent: 1em;
    }
    .right-switch {
        background-color: transparent;
        box-shadow: none;
        margin-left: 10px;
        &> button {
            width: 100px;
        }
    }
</style>