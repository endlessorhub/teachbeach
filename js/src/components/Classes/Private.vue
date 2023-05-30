<template>

      <v-layout align-top justify-center row wrap>
        <v-flex xs12 md6 class="text-xs-left">
            <v-flex xs12 class="text-xs-left">
                <div style="width: 50%;">
                  <gallery
                    :items="galleryItems"
                  >
                  </gallery>
                </div>
              <v-divider v-if="mediaUrl" style="margin: 3px;"></v-divider>
            </v-flex>
          <v-flex xs12  class="text-xs-left">
              <LocationPartial
                :class-data="$props"
              />
              <div v-if="lowestPrice && !is_price_hidden">From ${{lowestPrice}}/hour</div>
              <div v-if="memberLowestPrice && !is_price_hidden"><a @click="buyMembership">Premium Member Price From ${{memberLowestPrice}}/hour</a></div>
            <!--v-btn v-if="canEnroll" color="primary" @click.stop.prevent="bookClass()" :loading="isLoading" :disabled="isLoading">Make appointment</v-btn-->
          </v-flex>
          <h1>{{private_className}}
            <Rating object-type="class" :object-id="id"></Rating>
          </h1>
          <div v-html="groupClassDescriptionFormatted"></div>

          <v-flex xs12  class="text-xs-left">
            <v-divider v-if="bio || specialties" ></v-divider>
            <p v-if="bio" v-html="bio"></p>
            <div v-if="specialties"><b>Specialties: </b>{{specialties}}</div>
          </v-flex>

          <v-flex v-if="teacher.group_count || teacher.private_count" xs12 class="text-xs-left">
            <v-divider ></v-divider>
            <router-link v-if="teacher.private_count" :to="'/classes/private/teacher/'+teacher.id">Private  Classes</router-link>&nbsp;
            <router-link v-if="teacher.group_count" :to="'/classes/group/teacher/'+teacher.id">Group  Classes</router-link>&nbsp;
            <router-link v-if="teacher.group_count || teacher.private_count" :to="'/classes/all/teacher/'+teacher.id">All classes</router-link>
          </v-flex>
          <v-flex v-if="reviews && reviews.length" xs12 md12 class="text-xs-left">
            <v-divider ></v-divider>
            <h3>Reviews</h3>
            <ReviewItem v-for="gc in reviews" v-bind="gc" :key="gc.id"/>
          </v-flex>

          <v-flex xs12 v-if="isCompany" class="text-xs-left">
              <div style="width: 50%;">
                  <v-img v-if="companyImgUrl" :src="companyImgUrl" width="100%" :aspect-ratio="1.25"/>
              </div>
              <h4 class="company-title">About {{companyName}}</h4>
              <div v-html="companyDescription"></div>
          </v-flex>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-center">
          <v-layout align-top justify-left row wrap class="bio">
            <v-flex xs4  class="text-xs-left">
              <v-img v-if="avatarUrl" :src="avatarUrl" width="100%" :aspect-ratio="1.25"/>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
              <h2>with <span>{{teacher.first_name}} {{teacherLastNameFL}}.</span></h2>
            </v-flex>
            <v-flex xs8  class="text-xs-left">
                <div v-if="alreadyBought || show_phone"><b>Phone:</b> <a :href="`tel:${phone}`">{{phone}}</a></div>
                <div v-if="alreadyBought || show_email"><b>Email:</b> <a :href="`mailto:${email}`">{{email}}</a></div>
            </v-flex>

            <v-flex xs12  class="text-xs-left">
              <v-divider ></v-divider>
              <h3>Private availability</h3>
              <div>{{availablePeriod}}</div>
              <div>
              <v-btn-toggle v-model="curWeekday" mandatory>
                <v-btn v-for="(v, i) in weekdaysAvailable" :key="i" small :disabled="!v.isAvailable">
                  {{v.name}}
                </v-btn>
              </v-btn-toggle>
              </div>
              <div>&nbsp;{{weekdayTime}} Timezone: {{timezone}}</div>
            </v-flex>
            <v-flex xs12 class="text-xs-left" v-if="false">
              <v-btn @click.stop.prevent="openSchedule()" :loading="isLoading" :disabled="isLoading" style="margin: 0;">View full schedule</v-btn>
            </v-flex>
            <v-flex xs12 class="text-xs-left">
              <v-btn class="platform-green" v-if="canEnroll" @click.stop.prevent="bookClass()" :loading="isLoading" :disabled="isLoading" style="margin: 0;">{{!trialExists || alreadyBoughtTrial ? 'Book now' : 'Book a '+(trialPrice ? `$${trialPrice}` : 'free')+' trial'}}</v-btn>
            </v-flex>
            <v-flex xs12 class="text-xs-left">
              <v-btn @click.stop.prevent="openMessageForm()" :loading="isLoading" :disabled="isLoading" style="margin: 0;">Contact {{teacher.first_name}}</v-btn>
            </v-flex>
          </v-layout>
          <v-divider ></v-divider>

          <!--GeoMap v-bind="mapData" height="300px" v-if="lat && lng"/-->
        </v-flex>

        <v-dialog
          v-model="mapDialog"
          width="600"
        >
          <v-card>
            <v-card-text>
              <GeoMap v-bind="mapData" height="500px"/>
            </v-card-text>
          </v-card>
        </v-dialog>

        <v-dialog
          v-model="contactDialog"
          persistent
          width="400"
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
import RegMinPopup from './RegMinPopup'
import SendMessageForm from '@/components/basic/forms/SendMessage'
import ClassGroup from '@/components/Classes/Group.vue'
import ReviewItem from '@/components/Classes/ReviewItem.vue'
import ClassItem from '@/components/Classes/ClassItem.vue'
import utils from '@/lib/utils.js'
import Gallery from '@/components/basic/Gallery.vue'
import classHelper from '@/lib/helpers/Class.js'
import LocationPartial from './LocationPartial'
import Rating from '@/components/basic/Rating.vue'

export default {
    extends: ClassGroup,
    data: () => ({
        weekdays: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        _curWeekday: undefined,
        contactDialog: false,
        sendMessageFormData: {},
    }),
    components: {
        ReviewItem,
        ClassItem,
        RegMinPopup,
        SendMessageForm,
        Gallery,
        LocationPartial,
        Rating,
    },
    computed: {
        teacherLastNameFL() {
            return String(this.teacher.last_name || ' ')[0].toUpperCase()
        },
        price() {
            return classHelper.priceDescription(this)
        },
        prices() {
            return classHelper.price(this, true)
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
        specialties() {
            return (this.teacher.areas_of_specialty || []).join(', ')
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
            if(this.day_select_type == 'weekly') {
                return `From ${utils.stringToDate(this.start_date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})}
                ${this.until_date ? 'to '+utils.stringToDate(this.until_date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'}) : 'ongoing'}`
            } else {
                return ''
            }
        },
        lowestPrice() {
            return Math.round(_.min(_.map(_.filter(this.custom_packages, p => (p.isPrivate && !p.isTrial)), p => (p.totalPrice/(p.lessonLength.value/60*(p.isSubscription ? p.classesPerInterval : p.numberOfLessons))))))
        },
        memberLowestPrice() {
            return Math.round(_.min(_.map(_.filter(this.custom_packages, p => (p.isPrivate && !p.isTrial && p.memberTotalPrice)), p => (p.memberTotalPrice/(p.lessonLength.value/60*(p.isSubscription ? p.classesPerInterval : p.numberOfLessons))))))
        },
        trialPrice() {
            return Number((_.find(this.custom_packages, p => (p.isPrivate && p.isTrial)) || {}).totalPrice)
        },
        trialExists() {
            return _.find(this.custom_packages, p => (p.isPrivate && p.isTrial))
        }
    },
    methods: {
        closeDialogs() {
            this.contactDialog = false
            this.registerDialog = false
        },
        openSchedule() {
            if(!this.can_book && this.can_book_url) {
                return window.open(utils.prepareUrl(this.can_book_url), '_blank')
            }
            if(this.isLoggedIn) {
                //console.log('schedule open')
                this.$router.push(`/learners/new_enroll/${this.id}/2/0`)
            } else {
                this.initAction = 'schedule'
                this.registrationTitle = 'Sign up to see schedule'
                this.registerDialog = true
            }
        },
        bookClass() {
            if (this.canEnroll) {
                if(this.can_book) {
                    if(this.isLoggedIn) {
                        this.$router.push(`/learners/new_enroll/${this.id}/4/0`)
                    } else {
                        this.initAction = 'book'
                        this.registrationTitle = 'Please create account'
                        this.registerDialog = true
                    }
                } else if (this.can_book_url) {
                    window.open(utils.prepareUrl(this.can_book_url), '_blank')
                }
            }
        },
        openMessageForm() {
            if(!this.can_book && this.can_book_url) {
                return window.open(utils.prepareUrl(this.can_book_url), '_blank')
            }
            if(this.isLoggedIn) {
                this.sendMessageFormData = {
                    contact: _.assign({entity: 'teacher'}, this.teacher),
                    avatar: this.avatarUrl,
                    additional: {classId: this.id},
                    showBookBtn: this.canEnroll,
                    phone: this.show_phone_rule === 'call' ? this.phone : '',
                    includeAllowOther: false,
                }
                this.contactDialog = true
            } else {
                this.initAction = 'message'
                this.registrationTitle = `Sign up to send ${this.teacher.first_name} a message`
                this.registerDialog = true
            }
        },
        getMetaTitle() {
            return this.metadataTemplate.title.replace('${class.name}', this.private_className)
        },
        getMetaDescription() {
            return this.metadataTemplate.metatag.replace('${class.description}', this.group_description)
        },
        messageDone(res) {
            /*
            if(res.status) {
                this.contactDialog = false
            }
            */
        },
        closeSendMessage() {
            this.contactDialog = false
            this.sendMessageFormData = {}
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.price-item {
    margin-left: 10px;
}
.company-title {
    font-size: 24px;
}
</style>