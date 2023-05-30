<template>
    <div v-resize="onResize" class="company-group-classes">
        <section class="innerpage_header">
            <v-container>
                <v-layout class="row align-items-center header_row">
                    <v-flex lg6 md6>
                        <div class="page_title">
                            <h2>Group Classes & Events</h2>
                        </div>
                    </v-flex>
                    <v-flex lg6 md6 style="text-align: right;">
                        <div class="filter_btn">
                            <v-select
                                v-model="filterCategory"
                                :items="activeCategories"
                                prepend-icon="mdi-filter"
                                menu-props="auto"
                                hide-details
                                label="Filter"
                                single-line
                            ></v-select>
                        </div>
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
                            <h2>{{ currentCategoryTitle }}</h2>
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
                            <div  ref="classes-carousel-controls" class="owl-nav classes-carousel-controls">
                                <button type="button" role="presentation" class="owl-prev">
                                    <div class="left"></div>
                                </button>
                                <button type="button" role="presentation" class="owl-next">
                                    <div class="right"></div>
                                </button>
                            </div>
                            <tiny-slider
                                v-if="subcategoryNotEventsClasses.length"
                                :controls-container="classesControlsContainer"
                                :nav="false"
                                :mouse-drag="true"
                                :loop="false"
                                :items="itemsPerPage"
                                gutter="20"
                                class="classes-carousel-container owl-carousel owl-theme"
                            >
                                <div v-for="(item, index) in subcategoryNotEventsClasses" :key="item.id">
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
                                            <h4>{{ item.name }}</h4>
                                            <p>
                                                {{ availablePeriod(item) }}
                                                <label>Timezone: {{ item.timezone }}</label>
                                            </p>
                                            <p>{{ item.teacher.first_name }} {{ item.teacher.last_name }}</p>
                                            <p class="class-desc">{{ item.description }}</p>
                                            <p>{{ item.class_type === 'online' ? 'Online' : item.address_city }}</p>
                                            <div class="button_price">
                                                <div class="price_box me-auto">
                                                    <h4>{{ priceDescription(item).text }}</h4>
                                                    <h3>{{ priceDescription(item).memberPrice }}</h3>
                                                </div>
                                                <div class="go_button">
                                                    <button class="btn_btn" @click="$router.push('/class/'+item.id)">Go</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </tiny-slider>
                        </v-flex>
                    </v-layout> 
                </v-container>
            </div>
        </section>
    
        <section class="classes">
            <div class="container">
                <!-- <div class="row justify-content-center"> -->
                <div class="row">
                    <div class="col-lg-6">
                        <div class="caption">
                            <h2>Upcoming Events</h2>
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
                            <div ref="events-carousel-controls" class="owl-nav events-carousel-controls">
                                <button type="button" role="presentation" class="owl-prev">
                                    <div class="left"></div>
                                </button>
                                <button type="button" role="presentation" class="owl-next">
                                    <div class="right"></div>
                                </button>
                            </div>
                            <tiny-slider
                                v-if="upcomingEventsClasses.length"
                                :controls-container="classesControlsContainer"
                                :nav="false"
                                :mouse-drag="true"
                                :loop="false"
                                items="4"
                                gutter="20"
                                class="events-carousel-container owl-carousel owl-theme"
                            >
                                <div v-for="(item, index) in upcomingEventsClasses" :key="item.id">
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
                                            <h4>{{ item.name }}</h4>
                                            <p>
                                                {{ availablePeriod(item) }}
                                                <label>Timezone: {{ item.timezone }}</label>
                                            </p>
                                            <p>{{ item.teacher.first_name }} {{ item.teacher.last_name }}</p>
                                            <p class="class-desc">{{ item.description }}</p>
                                            <p>{{ item.class_type === 'online' ? 'Online' : item.address_city }}</p>
                                            <div class="button_price">
                                                <div class="price_box me-auto">
                                                    <h4>{{ priceDescription(item).text }}</h4>
                                                    <h3>{{ priceDescription(item).memberPrice }}</h3>
                                                </div>
                                                <div class="go_button">
                                                    <button class="btn_btn" @click="$router.push('/class/'+item.id)">Go</button>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </tiny-slider>
                        </v-flex>
                    </v-layout> 
                </v-container>
            </div>
        </section>

    <company-profile-join
        :company-slug="id"
        :company-profile="company"
    />
    <company-profile-footer
        :company-slug="id"
        :company-profile="company"
    />
    </div>
</template>

<script>

import _ from 'lodash'
import { mapGetters, mapActions, mapState } from 'vuex'
import VueTinySlider from 'vue-tiny-slider';
import ClassGroup from '@/components/Classes/Group.vue'
import ReviewItem from '@/components/Classes/ReviewItem.vue'
import ClassItem from '@/components/Classes/ClassItem.vue'
import SendMessageForm from '@/components/basic/forms/SendMessage'
import RegMinForm from '@/components/basic/forms/RegMin'
import BoundMembershipInfo from '@/components/bound/BoundMembershipInfo';
import CompanyProfileFooter from '@/components/basic/CompanyProfileFooter.vue';
import CompanyProfileJoin from '@/components/basic/CompanyProfileJoin.vue';
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


const eventsCategoryId = 10;

export default {
    mixins: [
        metadata,
        classItemMixin,
    ],
    data: () => ({
        weekdays: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        _curWeekday: null,
        carouselHeight: 300,
        rightSwitch: 'classes',
        teachersThreshold: 5,
        isTeachersExpanded: false,
        selectedClass: null,
        membershipDialog: false,
        subcategories: [],
        filterCategory: null,
        windowSize: {
            x: 0,
            y: 0
        },
    }),
    mounted() {
        this.onResize();
    },
    created() {
        const id = this.$route.params.id || config.companySlug;
        const slug = this.$route.params.slug || config.companySlug;
        this.loadCompany(id || slug);
        this.$store.dispatch('syncLogoCompanyProfile', id || slug);
        axios.get('/api/subcategories/').then((res) => {
            this.subcategories = res.data;
        });
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
        ...mapGetters('viewingCompany', [
            'isLoading',
        ]),
        itemsPerPage() {
            if (this.windowSize.x < 410) return 1;
            if (this.windowSize.x < 820) return 2;
            if (this.windowSize.x < 1240) return 3;
            return 4;
        },
        categoryDict() {
            return this.subcategories.reduce((acc, s) => ({...acc, [s.id]: s.name }), {});
        },
        eventsSubcategoryIds() {
            return this.subcategories.filter(v => v.category === eventsCategoryId).map(v => v.id)
        },
        activeCategories() {
            return [...new Set(this.groupClasses.reduce((acc, v) => ([...acc, ...v.subcategories]), []))].filter(v => v && v !== eventsCategoryId).map((sc) => ({
                value: sc,
                text: this.categoryDict[sc],
            }))
        },
        currentCategoryTitle () {
            return this.filterCategory && this.categoryDict[this.filterCategory] ? this.categoryDict[this.filterCategory] : 'Classes';
        },
        id () {
            return this.company && this.company.id;
        },
        title () {
            return this.company && (this.company.title || `Welcome to ${this.company.name}`);
        },
        description () {
            return this.company && this.company.description;
        },
        name () {
            return this.company && this.company.name;
        },
        media () {
            return this.company && this.company.media;
        },
        main_media () {
            return this.company && this.company.main_media;
        },
        user () {
            return this.company && this.company.user || {};
        },
        classes () {
            return this.company && this.company.classes || [];
        },
        memberCenterUrl () {
            return this.company && this.company.member_center_url;
        },
        address () {
            if (!this.company) return '';
            const venues = _.uniq(_.map(this.classes, classHelper.location))
            if(venues.length === 1) return venues[0];
            return '';
        },
        teaching_venue () {
            if (!this.company) return '';
            const venues = _.uniq(_.map(this.classes, classHelper.location))
            if(venues.length === 1) return this.classes[0].teaching_venue;
            return '';
        },
        classesAvailable() {
            return this.classes.filter(c => !classHelper.checkExpired(c));
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
            return this.classesAvailable.sort((a, b) => {
                if(!a.is_private && !b.is_private) {
                    return getClosestDate(a.schedule_dates.map(d => d.date)) - getClosestDate(b.schedule_dates.map(d => d.date))
                }
                if(a.is_private !== b.is_private) {
                    return a.is_private - b.is_private
                }
                return moment(b.created_at).format('x') - moment(a.created_at).format('x')
            })
        },
        groupClasses() {
            return this.classesSorted.filter(c => !c.is_private);
        },
        eventsClassesIds() {
            return this.groupClasses
                .filter(c => c.subcategories.some(s => this.eventsSubcategoryIds.includes(s)))
                .map(v => v.id);
        },
        subcategoryClasses() {
            return this.groupClasses.filter(c => (!this.filterCategory || c.subcategories.includes(this.filterCategory)))
        },
        subcategoryNotEventsClasses() {
            return this.subcategoryClasses.filter(v => !this.eventsClassesIds.includes(v.id));
        },
        upcomingClasses() {
            return this.groupClasses.filter(c => classHelper.isUpcoming(c));
        },
        upcomingEventsClasses() {
            return this.upcomingClasses.filter(v => this.eventsClassesIds.includes(v.id));
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
                    teacherMap.set(c.teacher.id, {...c.teacher, className: c.name, classId: c.id, categories: c.subcategories.map(s => this.categoryDict[s])})
                }
            })
            return [...teacherMap.values()]
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
        priceDescription() {
            return c => classHelper.priceDescription(c);
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
        classesControlsContainer() {
            return this.$refs['classes-carousel-controls'];
        },
        eventsControlsContainer() {
            return this.$refs['events-carousel-controls'];
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
body .company-profile-page {
    background: #FFFFFF;
    font-family: 'Poppins', sans-serif;
}
.innerpage_header {
    background-color: #F8F8F8;
    min-height: 130px;
    display: flex;
}
.filter_btn {
    max-width: 350px;
    display: inline-block;
}
.page_title h2 {
    font-size: 40px;
    font-weight: 500;
    line-height: 40px;
    color: #2B2B2B;
    margin-bottom: 0px;
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
.owl-nav {
    position: absolute;
    top: -75px;
    right: 0;
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
    padding: 20px 15px;

    p {
        text-align: left;
    }
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
footer {
    background-color: #383838;
    margin-top: -134px;
    padding: 229px 0 64px 0;
}
footer img.footerLogo{
    width: 50%;
    padding-bottom: 30px;
}
footer p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #FFFFFF;
}
footer h4 {
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #FFFFFF;
    padding-bottom: 20px;
}
footer ul {
    padding: 0;
}
footer ul li {
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 14px;
    line-height: 18px;
    color: #FFFFFF;
    padding-bottom: 10px;
    list-style: none;
}
footer .hrdiv {
    border-bottom: 1px solid #BBBBBB;
    padding-top: 29px;
}
footer .footer_copyright p{
    font-family: 'Open Sans';
    font-style: normal;
    font-weight: 400;
    font-size: 14px;
    line-height: 19px;
    color: #FFFFFF;
    padding-top: 30px;
}
footer .footer_copyright ul {
    padding-top: 30px;
    float: right;
    margin-bottom: 0;
}
footer .footer_copyright ul li {
    display: inline-block;
    padding-left: 20px;
    padding-bottom: 0;
}
footer .footer_copyright ul li img {
    padding-bottom: 0;
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
    footer {
        margin-top: -174px;
        padding: 229px 0 20px 0;
    }
    footer h4 {
        padding-top: 20px;
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
    padding: 10px;
}
.footer-container {
    display: flex;
    flex: row wrap;
}
.go_button .btn_btn{
    position: relative;
    width: 102px;
    height: 39px;
    border: none;
    font-family: 'Poppins';
    font-style: normal;
    font-weight: 500;
    font-size: 18px;
    line-height: 20px;
    color: #4EA42F;
    background: transparent;
    border: 2px solid #4EA42F;
    border-radius: 27px;
    justify-content: center;
    align-items: center;
    display: flex;
    transition: all ease 0.5s 0s;
}
.go_button .btn_btn::after{
    content: none;
    top: 4px;
}
.go_button .btn_btn:hover::after{
    content: '';
}
.go_button .btn_btn:hover{
    background: #4EA42F;
    color: #fff;
    padding: 0px 30px 0px 55px;
    transition: all ease 0.5s 0s;
}
.events-carousel-container, .classes-carousel-container {
    display: flex;
    flex-wrap: nowrap;
}
</style>