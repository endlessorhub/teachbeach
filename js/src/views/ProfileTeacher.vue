<template>
<div class="teacher-profile-page">
    <div class="teacher-profile-container flex xs12">
      <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 md6 class="text-xs-left">
          <div class="bio">
            <v-flex xs6 md12 v-if="avatarUrl" class="text-xs-left">
              <v-img :src="avatarUrl" width="50%" :aspect-ratio="1.25"/>
            </v-flex>
            <h2>Meet <span>{{first_name}}</span></h2>
              <p v-if="bio" v-html="bio"></p>
            <div><b>Phone:</b> {{phone}}</div>
            <div><b>Email:</b> {{email}}</div>
            <v-divider v-if="specialties" ></v-divider>
            <div v-if="specialties"><b>Specialties: </b>{{specialties}}</div>
          </div>
          <v-flex v-if="privateClasses.length" xs12 class="text-xs-left">
            <h3>Private Sessions</h3>
            <v-divider ></v-divider>
            <v-list two-line>
              <template v-for="(item, index) in privateClasses">
                <v-list-tile
                  :key="item.id"
                  avatar
                  ripple
                >

                  <v-list-tile-content>
                    <v-list-tile-title>
                        <router-link :to="'/class/'+item.id">{{ item.private_className }}</router-link>
                    </v-list-tile-title>

                    <v-list-tile-sub-title>
                        {{item.groupClassSummary}}
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                  <v-list-tile-action style="min-width: 90px;">
                      <v-btn v-if="canEnroll(item)" @click="bookClass(item.id)">Enroll</v-btn>
                  </v-list-tile-action>
                </v-list-tile>
                <v-divider
                  v-if="index + 1 < privateClasses.length"
                ></v-divider>
              </template>
            </v-list>
          </v-flex>
          <v-flex v-if="groupClasses.length" xs12 class="text-xs-left">
            <v-divider ></v-divider>
            <h3>Group Events</h3>
            <v-list two-line>
              <template v-for="(item, index) in groupClasses">
                <v-list-tile
                  :key="item.id"
                  avatar
                  ripple
                >

                  <v-list-tile-content>
                    <v-list-tile-title>
                        <router-link :to="'/class/'+item.id">{{ item.name }}</router-link>
                    </v-list-tile-title>

                    <v-list-tile-sub-title>
                        {{item.groupClassSummary}}
                    </v-list-tile-sub-title>
                  </v-list-tile-content>
                  <v-list-tile-action style="min-width: 90px;">
                      <v-btn v-if="canEnroll(item)" @click="bookClass(item.id)">Enroll</v-btn>
                  </v-list-tile-action>
                </v-list-tile>
                <v-divider
                  v-if="index + 1 < groupClasses.length"
                ></v-divider>
              </template>
            </v-list>
          </v-flex>
          <v-flex v-if="group_count" xs12 class="text-xs-left">
            <v-divider ></v-divider>
            <router-link :to="'/classes/group/teacher/'+id">Group Events</router-link>
          </v-flex>
          <v-flex v-if="reviews && reviews.length" xs12 md12 class="text-xs-left">
            <v-divider ></v-divider>
            <h3>Reviews</h3>
            <ReviewItem v-for="gc in reviews" v-bind="gc" :key="gc.id"/>
          </v-flex>


        </v-flex>
        <v-flex xs12 md6 class="text-xs-center">

          <GeoMap v-bind="mapData" height="300px" v-if="lat && lng"/>
        </v-flex>
      </v-layout>
      </v-container>
    </div>
</div>
</template>

<script>

import _ from 'lodash'
import ClassGroup from '@/components/Classes/Group.vue'
import ReviewItem from '@/components/Classes/ReviewItem.vue'
import ClassItem from '@/components/Classes/ClassItem.vue'
import utils from '@/lib/utils.js'
import axios from 'axios'
import metadata from '@/mixins/metadata'

let untilDate = new Date()
untilDate.setMonth(untilDate.getMonth()+1)


export default {
    mixins: [metadata],
    data: () => ({
        id: null,
        isLoading: false,
        weekdays: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        _curWeekday: null,
        carouselHeight: 300,
        alerts: false,
        areas_of_specialty: [],
        description: '',
        first_name: '',
        last_name: '',
        media: null,
        user: {},
        classes: [],
    }),
    created() {
        this.isLoading = true
        this.id = this.$route.params.id
        axios.get('/api/teacher_profile/'+this.$route.params.id+'/').then((res) => {
            console.log('done', res)
            this.alerts = res.data.alerts
            this.areas_of_specialty = res.data.areas_of_specialty || []
            this.description = res.data.description
            this.first_name = res.data.first_name
            this.last_name = res.data.last_name
            this.media = res.data.media
            this.user = res.data.user || {}
            this.classes = res.data.classes || []
        }).catch(() => {
            //console.log(arguments)

        }).then(() => {
            this.isLoading = false
        })
    },
    components: {
        ReviewItem,
        ClassItem,
    },
    computed: {
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
        specialties() {
            return (this.areas_of_specialty || []).join(', ')
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
            return this.media
        },
        bio() {
            return utils.formatTextToHtml(this.description)
        },
    },
    methods: {
        canEnroll(classData) {
            if(classData.can_book || classData.can_book_url) {
                if(classData.day_select_type == 'weekly') {
                    let dates = utils.getCalendarDatesForPeriod(utils.dateToString(new Date()), utils.dateToString(untilDate), classData.weekdays_schedule, classData.start_date, classData.until_date, classData.schedule_excluded)
                    return dates.length > 0
                } else {
                    return !!_.find(_.map(classData.schedule_dates, 'date'), v => {
                        return utils.stringToDate(v) > new Date()
                    })
                }
            }
            return false
        },
        bookClass(id) {
            const found = _.find(this.classes, {id})
            if(!found)
                return
            if (this.canEnroll(found)) {
                if(found.can_book) {
                    this.$router.push(`/learners/new_enroll/${id}/4/0`)
                } else if (found.can_book_url) {
                    window.open(utils.prepareUrl(found.can_book_url), '_blank')
                }
            }
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.teacher-profile-page {
    text-align: center;
    .teacher-profile-container {
        //width: 800px;
        margin: 0 auto;
    }
}
</style>