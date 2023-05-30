<template>
    <div v-resize="onResize" class="company-profile-page">
        <section class="main-info">
            <v-container grid-list-md text-xs-center>
            <v-layout>
                <v-flex lg8 class="content">
                    <div class="caption">
                        <h1>{{title}}</h1>
                    </div>
                    <div class="description">
                    <p>{{ description }}</p>
                    </div>
                    <div class="join_btn">
                        <button class="btn_btn" @click="buyMembership">Join</button>
                    </div>
                </v-flex>
                <v-flex lg4>
                    <img v-if="avatarUrl" class="f_image" :src="avatarUrl" alt="">
                </v-flex> 
            </v-layout>
        </v-container>
    </section>
    <section class="classes">
        <div class="container">
            <!-- <div class="row justify-content-center"> -->
            <div class="row">
                <div class="col-lg-6">
                    <div class="caption">
                        <h2><router-link :to="'/company_classes/group/'+currentSlug" style="font-size: 28px;">Courses & events</router-link></h2>
                        <!-- <p>Nunc consectetur ex nunc, id porttitor leo semper eget. Vivamus interdum, mauris quis cursus sodales, urn</p> -->
                    </div>                
                </div>
                <!-- <div class="col-lg-6">
                    <button class="btn_btn join-classes">Free and discounted classes</button>
                </div> -->
            </div>
            <v-container grid-list-md text-xs-center style="padding: 0;">
                <v-layout>
                    <v-flex lg12 class="content classes-carousel">
                        <tiny-slider
                            v-if="groupClassesSorted.length"
                            :controls-container="classesControlsContainer"
                            :nav="false"
                            :mouse-drag="true"
                            :loop="false"
                            :items="itemsPerPage"
                            gutter="20"
                            class="classes-carousel-container owl-carousel owl-theme"
                        >
                            <div v-for="(item, index) in groupClassesSorted" :key="item.id">
                                <div class="item">
                                    <router-link :to="'/class/'+item.id">
                                        <v-img
                                            v-if="item.master_media"
                                            :src="item.master_media"
                                            width="100%"
                                            class="img class-image"
                                        >
                                        </v-img>
                                        <div v-else class="class-image"></div>
                                    </router-link>
                                    <div class="border-blue"></div>
                                    <div class="text-content">
                                        <h4>{{ item.name }} with {{ item.teacher.first_name }}</h4>
                                        <label>{{ availablePeriod(item) }}</label>
                                        <label>Timezone: {{ item.timezone }}</label>
                                        <p class="class-desc">{{ item.description }}</p>
                                        <router-link :to="'/class/'+item.id">SEE MORE <img src="@/assets/profile-company2/see_more.svg" class="img"> </router-link>
                                    </div>
                                </div>
                            </div>
                        </tiny-slider>
                        <div ref="classes-carousel-controls" class="owl-nav classes-carousel-controls">
                            <button type="button" role="presentation" class="owl-prev">
                                <div class="left"></div>
                            </button>
                            <button type="button" role="presentation" class="owl-next">
                                <div class="right"></div>
                            </button>
                        </div>
                    </v-flex>
                </v-layout> 
            </v-container>
        </div>
    </section>
    <section class="mentors">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="caption">
                        <h2 style="font-size: 28px;">Knowledge exchange</h2>
                    </div>
                </div>
            </div>
            <v-container grid-list-md text-xs-center style="padding: 0;">
                <v-layout>
                    <v-flex lg12 class="content mentors-carousel">
                        <tiny-slider
                            v-if="privateClassesSorted.length"
                            :controls-container="$refs['privateClassesControls']"
                            :nav="false"
                            :mouse-drag="true"
                            :loop="false"
                            :items="itemsPerPage"
                            gutter="20"
                            class="mentors-carousel-container owl-carousel owl-theme"
                        >
                            <div v-for="(t, i) in privateClassesSorted" :key="t.id">
                                <div :class="{'teacher-container': true, 'item': true, 'is-hidden': t.isHidden}">
                                    <v-img :src="t.teacher.media" :aspect-ratio="0.9" class="img" width="50%"/>
                                    <div class="text-content">
                                        <router-link :to="`/class/${t.id}`"><img src="@/assets/profile-company2/plus.svg"></router-link>
                                        <h4>{{t.teacher.first_name}} {{t.teacher.last_name}}</h4>
                                        <p><router-link class="teacher-container__link" :to="'/class/'+t.id">{{ t.name }}</router-link></p>
                                        <span v-for="(cat, catIndex) in categoryNames(t.subcategories)">{{ cat }}<template v-if="catIndex < t.subcategories.length - 1">, </template></span>
                                    </div>
                                </div>
                            </div>
                        </tiny-slider>
                        <div ref="privateClassesControls" class="owl-nav mentors-carousel-controls">
                            <button type="button" role="presentation" class="owl-prev">
                                <div class="left"></div>
                            </button>
                            <button type="button" role="presentation" class="owl-next">
                                <div class="right"></div>
                            </button>
                        </div>
                    </v-flex>
                </v-layout> 
            </v-container>
        </div>
    </section>

    <company-profile-join
        :company-slug="id"
        :company-profile="profile"
    />
    <company-profile-footer
        :company-slug="id"
        :company-profile="profile"
    />
    </div>
</template>

<script>

import _ from 'lodash'
import { mapGetters, mapActions, mapState } from 'vuex'
import VueTinySlider from 'vue-tiny-slider';
import CompanyProfileFooter from '@/components/basic/CompanyProfileFooter.vue'
import CompanyProfileJoin from '@/components/basic/CompanyProfileJoin.vue';
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
import config from '@/config.js'

let untilDate = new Date()
untilDate.setMonth(untilDate.getMonth()+1)
let slider = null;
let sliderTeachers = null;

export default {
    mixins: [
        metadata,
        classItemMixin,
    ],
    data: () => ({
        id: null,
        profile: null,
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
        subcategories: {},
        windowSize: {
            x: 0,
            y: 0
        },
    }),
    mounted() {
        this.onResize();
    },
    created() {
        this.isLoading = true
        const id = this.$route.params.id || config.companySlug;
        const slug = this.$route.params.slug || config.companySlug;
        this.loadCompany(id || slug);
        this.$store.dispatch('syncLogoCompanyProfile', id || slug);
        axios.get('/api/company_profile/'+(id || slug)+'/').then((res) => {
            //console.log('done', res)
            this.profile = res.data
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
        });
        axios.get('/api/subcategories/').then((res) => {
            this.subcategories = res.data.reduce((acc, s) => ({...acc, [s.id]: s.name }));
        });
    },
    watch: {
        
    },
    components: {
        CompanyProfileJoin,
        CompanyProfileFooter,
        ReviewItem,
        ClassItem,
        SendMessageForm,
        RegMinForm,
        BoundMembershipInfo,
        'tiny-slider': VueTinySlider,
    },
    computed: {
        ...mapGetters([
            'isMember',
        ]),
        ...mapState('viewingCompany', [
            'company',
        ]),
        itemsPerPage() {
            if (this.windowSize.x < 410) return 1;
            if (this.windowSize.x < 820) return 2;
            if (this.windowSize.x < 1240) return 3;
            return 4;
        },
        categoryNames() {
            return (ids) => ids.map(id => this.subcategories[id])
        },
        classesControlsContainer() {
            return this.$refs['classes-carousel-controls'];
        },
        currentSlug() {
            return this.$route.params.slug || this.$route.params.id || config.companySlug;
        },
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
        groupClassesSorted() {
            return this.classesSorted.filter(v => !v.is_private)
        },
        privateClassesSorted() {
            return this.classesSorted.filter(v => v.is_private)
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
                if (c.is_deactivated || classHelper.checkExpired(c))
                    return;
                if(!teacherMap.has(c.teacher.id)) {
                    teacherMap.set(c.teacher.id, {...c.teacher, className: c.name, classId: c.id, categories: c.subcategories.map(s => this.subcategories[s])})
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
            return c => {
                if(c.day_select_type == 'weekly') {
                    return `From ${utils.stringToDate(c.start_date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})}
                    ${c.until_date ? 'to '+utils.stringToDate(c.until_date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'}) : 'ongoing'}`
                } else {
                    return utils.formatDatesSchedule((c.schedule_dates || []).filter(d => (utils.isTimeInFuture(`${d.date} ${d.start}:00`, c.timezone))), true).map(v => v.dateStr).join(', ');
                }
            }
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
        onResize() {
            this.windowSize = { x: window.innerWidth, y: window.innerHeight }
        },
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
@import 'tiny-slider/src/tiny-slider';

body .company-profile-page {
    background: #FFFFFF;
    font-family: 'Poppins', sans-serif;
}

.collapse{
    display: flex;
    justify-content: flex-end;
}
.join_btn {
    float: right;
}
.main-info .join_btn {
    float: left;
}
a.logo_img{
    margin-right: 146px;
}
section.header{
    height: 140px;
}
.main-info {
    background-color: #F8F8F8;
    padding-top: 20px;
    padding-bottom: 20px;
}
.main-info .content {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.main-info .caption h1{
    font-size: 55px;
    color: #2B2B2B;
    font-weight: 600;
    line-height: 60px;
    margin-bottom: 23px;
}
.main-info .caption h1 span{
    color: #4EA42F;
    text-decoration: underline;
}
.main-info .description p{
    margin-bottom: 23px;
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 18px;
    line-height: 28px;
    color: #575757;
}
.btn_btn{
    position: relative;
    width: 192px;
    height: 39px;
    border: none;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #FFFFFF;
    background: #4EA42F;
    border-radius: 27px;
    justify-content: center;
    align-items: center;
    display: flex;
}
.btn_btn::after{
    content: '';
    position: absolute;
    top: 6px;
    left: 6px;
    background-image: url('../assets/profile-company2/btnIcon.svg');
    background-repeat: no-repeat;
    height: 27px;
    width: 27px;
}
.f_image{
    width: 75%;
    height: auto;
    float: right;
}
.classes {
    padding-top: 10px;
}
.classes .caption{
    margin-bottom: 15px;
}
.classes .caption h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 38px;
    line-height: 38px;
    text-align: left;
    color: #999999;
}
.classes .caption p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 22.53px;
    line-height: 26px;
    text-align: center;
    color: #575757;
}
.classes .classes-carousel .item {
    overflow: hidden;
    border-radius: 12px;
    border: 1.18438px solid #F2EFEF;

    .class-desc {
        max-height: 1.3em;
        overflow: hidden;
        text-overflow: ellipsis;
        font-size: 1em;
        padding: 0;
        text-align: left;
    }
}
.classes .classes-carousel{
    position: relative;
}
.classes .classes-carousel .owl-prev{
    position: absolute;
    top: 45%;
    left: -50px;
}
.classes .classes-carousel .owl-next{
    position: absolute;
    top: 45%;
    right: -50px;
}
.classes .classes-carousel .owl-prev .left{
    width: 47px;
    height: 47px;
    /* background-image: url('../assets/profile-company2/left.svg'); */
    background-image: url('../assets/profile-company2/darkLeft.svg');
    background-repeat: no-repeat;
}
.classes .classes-carousel .owl-next .right{
    width: 47px;
    height: 47px;
    /* background-image: url('../assets/profile-company2/right.svg'); */
    background-image: url('../assets/profile-company2/darkRight.svg');
    background-repeat: no-repeat;
}
.classes .classes-carousel .item .img{
    width: 100%;
    height: 180px;
}
.classes .classes-carousel .item .border-blue{
    width: 100%;
    height: 5px;
    background: linear-gradient(175.6deg, #0E6BA8 -25.14%, #155799 107.01%);
}
.classes .classes-carousel .item .text-content{
    padding: 20px 0 0 18px;
}
.classes .classes-carousel .item .text-content h4{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #2B2B2B;
    margin-bottom: 13px;
}
.classes .classes-carousel .item .text-content label{
    font-family: 'Open Sans';
    font-style: italic;
    font-weight: 400;
    font-size: 14px;
    line-height: 14px;
    color: #575757;
    width: 100%;
    margin-bottom: 20px;
    display: inline-block;
    box-sizing: border-box;
    text-align: left;
}
.classes .classes-carousel .item .text-content a{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 16.5813px;
    line-height: 21px;
    color: #2B2B2B;
    display: flex;
    margin-bottom: 20px;
}
.classes .classes-carousel .item .text-content a .img{
    width: 16px;
    height: auto;
    padding-left: 8px;
}
.classes .join-classes {
    float: right;
    width: 402px;
    background: #797979;
}
.classes .join-classes::after {
    background-image: url(../assets/profile-company2/darkbtnicon.svg);
}
.mentors {
    padding-top: 83px;
}
.mentors .caption{
    margin-bottom: 65px;
}
.mentors .caption h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 38px;
    line-height: 38px;
    text-align: left;
    color: #999999;
    margin-bottom: 20px;
}
.mentors .caption h2 span{
    color: #4EA42F;
}
.mentors .caption p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 16px;
    line-height: 16px;
    text-align: left;
    color: #575757;
}
.mentors  .mentors-carousel .owl-nav{
    margin-top: 19px;
}
.mentors  .mentors-carousel .owl-prev{
    position: absolute;
    left: 46%;
}
.mentors  .mentors-carousel .owl-next{
    position: absolute;
    right: 46%;
}
.mentors  .mentors-carousel .owl-prev .left{
    width: 47px;
    height: 47px;
    background-image: url('../assets/profile-company2/darkLeft.svg');
    /* background-image: url('../assets/profile-company2/mentorLeft.svg'); */
    background-repeat: no-repeat;
}
.mentors  .mentors-carousel .owl-next .right{
    width: 47px;
    height: 47px;
    background-image: url('../assets/profile-company2/darkRight.svg');
    /* background-image: url('../assets/profile-company2/mentorRight.svg'); */
    background-repeat: no-repeat;
}
.mentors .mentors-carousel .item .img{
    border-radius: 50%;
}
.mentors .mentors-carousel .item .text-content{
    padding: 15px 0;
    position: relative;
}
.mentors .mentors-carousel .item .text-content img{
    position: absolute;
    top: -200px;
    right: -10px;
    width: 40px;
    height: 40px;
}
.mentors .mentors-carousel .item .text-content h4{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 22px;
    color: #2B2B2B;
    text-align: center;
}
.mentors .mentors-carousel .item .text-content p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #155799;
    text-align: center;
}
.mentors .joinButton {
    padding-top: 90px;
    width: 192px;
    margin: 0 auto;
}
.join-us {
    padding-top: 65px;
}
.join-us .join-us-bg {
    position: relative;
    background: #797979;
    border-radius: 40px;
    padding: 53px 98px 69px 98px;
}
.join-us .join-us-bg:after {
    content: '';
    position: absolute;
    bottom: 50px;
    left: -40px;
    width: 97px;
    height: 115px;
    background-image: url('../assets/profile-company2/joinUsLeft.svg');
    background-repeat: no-repeat;
}
.join-us .join-us-bg:before {
    content: '';
    position: absolute;
    top: 30px;
    right: -50px;
    width: 197px;
    height: 230px;
    background-image: url('../assets/profile-company2/joinUsRight.svg');
    background-repeat: no-repeat;
}
.join-us .join-us-bg h2{
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 700;
    font-size: 36px;
    line-height: 44px;
    color: #FFFFFF;    
}
.join-us .join-us-bg .joinusbtn{
    display: none;
}
.inputText, .inputEmail, .selectClass{
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    border: none;
    width: 100%;
    height: 39px;
    padding: 10px 15px;
    margin-bottom: 20px;
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #575757;    
    z-index: 1111;
    position: relative;
}
.inputText:focus-visible, .inputEmail:focus-visible, .selectClass:focus-visible, .inputMessage:focus-visible{
    outline: none;
}
.inputText::placeholder, .inputEmail::placeholder, .selectClass::placeholder, .inputMessage::placeholder{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #575757;
}
.selectClass {
    appearance: none;
    background-image: url(../assets/profile-company2/selectArrow.svg);
    background-repeat: no-repeat;
    background-position: right 15px center;
}
.inputMessage{
    background: rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    border: none;
    width: 100%;
    height: 70px;
    padding: 10px 15px;
}

@media only screen and (max-width: 1280px){
    .main-info .caption h1 {
        font-size: 50px;
        line-height: 80px;
    }
    .main-info .description p {
        font-size: 17px;
    }
    .f_image {
        width: 80%;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 50px;
    }
    .classes .caption p, .mentors .caption p{
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content h4 {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content label {
        font-size: 14px;
    }
    .classes .classes-carousel .item .text-content a {
        font-size: 13px;
    }
    .join-us .join-us-bg h2 {
        font-size: 34px;
    }
}
@media only screen and (max-width: 1024px) {
    a.logo_img {
        margin-right: 0px;
    }
    .main-info .caption h1 {
        font-size: 50px;
        line-height: 70px;
    }
    .main-info .description p {
        font-size: 17px;
    }
    .f_image {
        width: 100%;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 40px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content h4 {
        font-size: 16px;
    }
    .classes .classes-carousel .item .text-content label {
        font-size: 13px;
    }
    .classes .classes-carousel .item .text-content a {
        font-size: 12px;
    }
    .classes .joinButton {
        padding-top: 45px;
    }
    .mentors .mentors-carousel .item .text-content {
        padding: 15px 0 0 15px;
        position: relative;
    }
    .mentors .mentors-carousel .item .text-content h4 {
        font-size: 15px;
    }
    .mentors .mentors-carousel .item .text-content p {
        font-size: 12px;
    }
    .mentors .mentors-carousel .owl-prev {
        position: absolute;
        left: 44%;
    }
    .mentors .mentors-carousel .owl-next {
        position: absolute;
        right: 44%;
    }
    .mentors .joinButton {
        padding-top: 70px;
    }
    .join-us .join-us-bg {
        padding: 53px 50px 69px 50px;
    }
    .join-us .join-us-bg h2 {
        font-size: 30px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after{
        display: none;
    }
   
}

@media only screen and (max-width: 992px) {   
    section.header {
        height: 100px;
    }

    a.logo_img {
        margin-right: 60px;
    }
    .logo_img img {
        width: 100%;
    }

    .main-info .caption h1 {
        font-size: 40px;
        line-height: 50px;
    }
    .main-info .description p {
        font-size: 16px;
        line-height: 25px;
    }
    .f_image {
        width: 100%;
        height: auto;
        margin-top: 40px;
    }
    .main-info {
        // height: 100%;
    }
    .classes {
        padding-top: 30px;
    }
    .classes .caption {
        margin-bottom: 40px;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 35px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 16px;
    }    
    .classes .joinButton {
        padding-top: 25px;
    }
    .owl-nav {
        display: none;
    }
    .owl-dots {
        text-align: center;
    }
    .no-js .owl-carousel, .owl-carousel.owl-loaded .owl-dots {
        margin-top: 30px;
    }
    .owl-dots .owl-dot {
        margin: 5px;
    }
    button.owl-dot span {
        height: 15px;
        width: 15px;
        background-color: transparent;
        border: 1px solid #4ea42f;
        display: block;
        border-radius: 10px;
    }
    button.owl-dot.active span {
        background-color: #4ea42f;
    }
    .mentors .joinButton {
        padding-top: 45px;
    }
    .join-us .join-us-bg {
        border-radius: 20px;
        padding: 25px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after {
        display: none;
    }
    .join-us .join-us-bg h2 {
        font-size: 35px;
        line-height: 40px;
        margin-bottom: 30px;
    }
    .join-us .join-us-bg .joinusbtn{
        display: flex;
        margin-top: 20px;
        justify-content: center;
    }
    .join-us .join-us-bg .join-us-btn{
        display: none;
    }
    .mentors .mentors-carousel .item .text-content img {
        top: -310px;
        right: 10px;
    }
    footer {
        margin-top: -174px;
        padding: 229px 0 20px 0;
    }
    footer h4 {
        padding-top: 20px;
    }
    button:focus:not(:focus-visible){
        box-shadow: none;
    }
}

@media only screen and (max-width: 767px) {
    section.header {
        height: 70px;
    }
    a.logo_img {
        margin-right: 60px;
    }
    .logo_img img {
        width: 100%;
    }
    .main-info .caption h1 {
        font-size: 35px;
        line-height: 40px;
    }
    .main-info .caption h1 br{
        display: none;
    }
    .main-info .description p {
        font-size: 14px;
        line-height: 20px;
    }
    .f_image {
        width: 100%;
        height: auto;
        margin-top: 40px;
    }
    .main-info {
        // height: 100%;
    }
    .classes {
        padding-top: 30px;
    }
    .classes .caption {
        margin-bottom: 40px;
    }
    .classes .caption h2, .mentors .caption h2 {
        font-size: 30px;
    }
    .classes .caption p, .mentors .caption p {
        font-size: 14px;
    }    
    .classes .joinButton {
        padding-top: 25px;
    }
    .owl-nav {
        display: none;
    }
    .owl-dots {
        text-align: center;
    }
    .no-js .owl-carousel, .owl-carousel.owl-loaded .owl-dots {
        margin-top: 30px;
    }
    .owl-dots .owl-dot {
        margin: 5px;
    }
    button.owl-dot span {
        height: 15px;
        width: 15px;
        background-color: transparent;
        border: 1px solid #4ea42f;
        display: block;
        border-radius: 10px;
    }
    button.owl-dot.active span {
        background-color: #4ea42f;
    }
    .mentors .joinButton {
        padding-top: 45px;
    }
    .join-us .join-us-bg {
        border-radius: 20px;
        padding: 25px;
    }
    .join-us .join-us-bg:before, .join-us .join-us-bg:after {
        display: none;
    }
    .join-us .join-us-bg h2 {
        font-size: 30px;
        line-height: 35px;
        margin-bottom: 30px;
    }
    .join-us .join-us-bg .joinusbtn{
        display: flex;
        margin-top: 20px;
        justify-content: center;
    }
    .join-us .join-us-bg .join-us-btn{
        display: none;
    }
    .mentors .mentors-carousel .item .text-content img {
        top: -240px;
        right: 10px;
    }
    footer {
        margin-top: -174px;
        padding: 229px 0 20px 0;
    }
    footer h4 {
        padding-top: 20px;
    }
}

@media only screen and (min-width: 531px) and (max-width: 766px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -460px;
        right: 10px;
    }
}

@media only screen and (min-width: 481px) and (max-width: 530px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -443px;
        right: 10px;
    }
}

@media only screen and (min-width: 461px) and (max-width: 480px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -413px;
        right: 10px;
    }
}

@media only screen and (min-width: 401px) and (max-width: 460px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -380px;
        right: 10px;
    }
}

@media only screen and (min-width: 360px) and (max-width: 400px) {
    .mentors .mentors-carousel .item .text-content img {
        top: -330px;
        right: 10px;
    }
}
.class-image {
    width: 100%;
    height: 180px;
}
.owl-carousel .owl-nav button.owl-next, .owl-carousel .owl-nav button.owl-prev, .owl-carousel button.owl-dot {
    background: 0 0;
    color: inherit;
    border: none;
    padding: 0!important;
    font: inherit;
}
.owl-carousel .owl-dot, .owl-carousel .owl-nav .owl-next, .owl-carousel .owl-nav .owl-prev {
    cursor: pointer;
    user-select: none;
}
.classes .owl-prev {
    position: absolute;
    top: 45%;
    left: -50px;
}
.classes .owl-next {
    position: absolute;
    top: 45%;
    right: -50px;
}
.teacher-container {
    align-items: center;
    display: flex;
    flex-flow: column;
    padding: 10px;

    &__link {
        font-size: 22px;
    }
}
</style>