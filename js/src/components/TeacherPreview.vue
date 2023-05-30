<template>
  <form>
    <v-container grid-list-md text-xs-center>
      <ClassGroup v-if="classData && !classData.is_private" v-bind="classData" v-bind:show_enroll="false"/>
      <ClassPrivate v-if="classData && classData.is_private" v-bind="classData" v-bind:show_enroll="false"/>
    </v-container>

    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">{{publishBtnText}}</v-btn>
    <v-alert
      :value="published"
      color="grey"
      transition="scale-transition"
      dismissible
    >
        {{publishedMessage}}
        <v-btn v-if="isEditMode" to="/dashboard/teach/classes" color="primary">back to dashboard</v-btn>
        <v-btn v-else @click="another" color="primary">Add another one?</v-btn>
    </v-alert>
    <v-alert
      :value="notPublished"
      type="error"
      color="platform-error"
      icon="warning"
      transition="scale-transition"
      dismissible
    >
        {{notPublishedError}}
    </v-alert>
    <div v-if="!published"><a href="javascript:void(0);" @click="back">Edit this page</a></div>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import ClassGroup from '@/components/Classes/Group.vue'
import ClassPrivate from '@/components/Classes/Private.vue'

import utils from '@/lib/utils.js'
import fbmap from '@/lib/fbmap.js'

const weekDays = [
    'Sun',
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
]

export default {
    props: {
        classType: {
            type: String,
            default: 'group'
        },
        isEditMode: Boolean,
    },

    data: () => ({
        isLoading: false,
        published: false,
        notPublishedError: '',
        notPublished: false,
        classTitle: '',
        profile: null,
        categories: null,
        avatar: null,
        teacherLessonType: null,
        teacherGroupClass: null,
        publishBtnText: 'Publish',
        publishedMessage: 'Your Class was published',
    }),

    components: {
        ClassGroup,
        ClassPrivate,
    },

    created: function () {
        this.user = this.$store.state.user
        this.teacher = this.$store.state.teacher
        this.profile = this.$store.state.profile
        this.avatar = this.$store.state.avatar
        this.categories = this.$store.state.categoriesSelected
        this.teacherLessonType = this.$store.state.teacherLessonType
        this.teacherGroupClass = this.$store.state.teacherGroupClass
        this.classTitle = this.teacherLessonType == 'group' ? this.$store.state.teacherGroupClass.groupClassName : 'Private lessons'
        if(this.isEditMode) {
            this.publishBtnText = 'Save edits'
            this.publishedMessage = 'Your Class was updated'
        }
        console.log(this)
    },

    computed: {
        classData() {
            let res = fbmap.fb.teachingClass(this.teacherGroupClass)
            res.is_private = this.teacherLessonType == 'group' ? false : true
            res.avatar = this.avatar
            res.teacher = this.teacher || {}
            res.teacher.user = this.user
            if (this.$store.state.profile) {
                res.teacher.description = this.$store.state.profile.description
                res.teacher.areas_of_specialty = this.$store.state.profile.areasOfSpeciality
            }
            return res
        },
    },

    methods: {
        another() {
            this.$store.commit('setGroupClassForce', {})
            this.$store.commit('setTeacherLessonType', null)
            this.$emit('update:step', 1, {isEditMode: false})
        },
        back() {
            this.$emit('update:step', 1)
        },
        submit () {
            this.isLoading = true
            let _this = this
            axios.post('/api/classes/', {
                //user: _this.$store.state.user,
                profile: _this.$store.state.profile,
                avatar: _this.$store.state.avatar,
                categories: _this.$store.state.categoriesSelected,
                teacherLessonType: _this.$store.state.teacherLessonType,
                teacherGroupClass: _this.$store.state.teacherGroupClass
            }).then((res) => {
                console.log('done', res)
                if(res.data && res.data.success) {
                    //_this.$emit('update:step', 11)
                    fbq('trackCustom', 'teacherClassPublish')
                    this.published = true
                    const isEditing = this.$store.state.teacherGroupClass.id
                    const isDeactivated = this.$store.state.teacherGroupClass.is_deactivated
                    this.$store.commit('setGroupClassForce', {

                    })
                    if(res.data.isFreeMember || (isEditing && !isDeactivated))
                        return this.$router.push(`/teachers/finish/${res.data.id}`)
                    else
                        return this.$router.push(`/teacher_check/${res.data.id}`)
                    /*
                    if(res.data.isBankAccount) {
                        if(res.data.isFirstClass) {
                            this.$router.push('/dashboard/teach/classes/first')
                        } else {
                            this.$router.push('/dashboard/teach/classes')
                        }
                    } else {
                        if(res.data.isFirstClass) {
                            this.$router.push('/dashboard/teach/account_take')
                        } else {
                            this.$router.push('/dashboard/teach/account_take')
                        }
                    }
                    */
                } else {
                    //process errors
                    this.notPublished = true
                    this.notPublishedError = res.data.error_message
                }
            }).catch(() => {
                //console.log(arguments)
                this.notPublished = true
                this.notPublishedError = JSON.stringify(e.data || e.errors)//'server error, try again later'
            }).then(() => {
                _this.isLoading = false
            })
        },
        clear () {

        },
        calcDates() {
            let dates = []
            const dateLimit = 30
            let counter = 0
            let month = new Date().getMonth()
            let v = this.teacherGroupClass
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
            let excluded = v.scheduleDatesExcluded && Object.keys(v.scheduleDatesExcluded).length ? _.flatten(_.map(v.scheduleDatesExcluded, v => v)) : []
            if (v.daySelectType == 'weekly' && v.weekdaysScheduled && v.weekdaysScheduled.length) {
                for (let now = new Date(); counter<dateLimit; now.setDate(now.getDate() + 1)) {
                    if (_.find(v.weekdaysScheduled, {weekday: now.getDay()})
                    && (!excluded.length || excluded.indexOf(utils.dateToString(now)) == -1)) {
                        dates.push(utils.dateToString(now))
                        month = now.getMonth()
                        counter++
                    }
                }
            } else if (v.daySelectType == 'monthly' && v.scheduleDates && v.scheduleDates.length) {
                _.each(v.scheduleDates, (d) => {
                    if (counter >= dateLimit)
                        return
                    let now = utils.stringToDate(d.date)
                    if(now.getTime()+86399000 > new Date().getTime()
                    && (!excluded.length || excluded.indexOf(d.date) == -1)) {
                        //dates.push(utils.stringToDate(d))
                        dates.push(utils.dateToString(now))
                        month = now.getMonth()
                        counter++
                    }
                })
            }
            return _.reverse(dates)
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>