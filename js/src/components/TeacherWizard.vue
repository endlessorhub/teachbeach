<template>
  <v-stepper v-model="step" alt-labels style="box-shadow: none;">
    <v-stepper-header style="display: none;">
      <v-stepper-step :complete="step > 1" step="1"><div class="text-xs-center">Choose<br/>a category</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 2" step="2"><div class="text-xs-center">Create<br/>account</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 3" step="3"><div class="text-xs-center">Create<br/>Profile</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 4" step="4"><div class="text-xs-center">Create<br/>a location</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 5" step="5"><div class="text-xs-center">Give<br/>your schedule</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 6" step="6"><div class="text-xs-center">Set<br/>your pricing</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 7" step="7"><div class="text-xs-center">something</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 8" step="8"><div class="text-xs-center">something</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 9" step="9"><div class="text-xs-center">something</div></v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">
        <h1>Select or create a topic</h1>
        <TeacherCategoryForm v-if="step==1" v-on:update:step="updateStep" v-bind:alreadyRegistered="alreadyRegistered" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>

      <v-stepper-content step="2">
        <h1>Please register to post classes <a href="javascript:void(0);" @click="openLoginForm">or login</a></h1>
        <!-- not using next:step here, handled by watching isLoggedIn -->
        <TeacherForm
                v-if="step==2"
                v-on:update:step="updateStep"
                v-on:prev:step="prevStep"
                v-on:openLoginForm="openLoginForm"
                v-on:register:done="registerDone"
        />
      </v-stepper-content>

      <v-stepper-content step="3">
        <h1 v-if="isCompany">Please tell students a little about your organization</h1>
        <h1 v-else>Create your profile</h1>
        <TeacherCompanyProfile v-if="step==3 && isCompany" v-on:update:step="updateStep" v-bind:alreadyRegistered="alreadyRegistered" v-bind:hasAvatar="hasAvatar" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        <TeacherProfileForm v-if="step==3 && !isCompany" v-on:update:step="updateStep" v-bind:alreadyRegistered="alreadyRegistered" v-bind:hasAvatar="hasAvatar" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>

      <v-stepper-content step="4">
        <h1>Say Cheese!</h1>
        <TeacherLoadAvatar v-if="step==4" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="5">
        <h1>What kind of session are these?</h1>
        <TeacherGroupOrPrivate v-if="step==5" v-on:update:step="updateStep" v-bind:hasAvatar="hasAvatar" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="6">
        <h1>Create Membership</h1>
        <TeacherMembership v-if="step === 6" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="7">
        <div v-if="groupClassBranch">
            <TeacherGroupClass v-if="step === 7" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-if="privateClassBranch">
            <h1>Great!  Now create a promotional summary of the private class.</h1>
            <TeacherPrivateClass v-if="step === 7" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
      </v-stepper-content>
      <v-stepper-content step="8">
        <div v-if="groupClassBranch">
            <TeacherGroupSupport v-if="step === 8" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-if="privateClassBranch">
            <h1>a private class step</h1>
        </div>
      </v-stepper-content>

      <v-stepper-content step="9" v-if="step === 9">
        <TeacherMultipleProfiles v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>

      <v-stepper-content step="10" v-if="step === 10">
        <TeacherGroupPrice v-if="classType == 'group'" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        <TeacherPrivatePackages v-else v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="11">
        <TeacherGroupPackages v-if="step === 11" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind="classData" v-bind:isWorkshop="isWorkshop"/>
      </v-stepper-content>
      <v-stepper-content step="12">
        <TeacherWhereChoice v-if="step === 12" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="13" v-if="step === 13">
        <div v-if="locationBranch == 'address'">
            <h1>Please give the address for the class</h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-else-if="locationBranch == 'student_location'">
            <h1>Please tell us your address so we can display your information to students near you. </h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-else-if="locationBranch == 'online'">
            <h1>Online</h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-else-if="locationBranch == 'custom'">
            <h1>Please tell us your address so we can display your information to students near you.</h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-else-if="locationBranch == 'other'">
            <h1>Please type in zip code or city name</h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
        <div v-else>
            <h1>Please give the address for the class</h1>
            <TeacherAddress v-bind:isCompany="isCompany" v-on:update:step="updateStep" v-bind:classType="classType" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
      </v-stepper-content>
      <v-stepper-content step="14" v-if="step === 14">
        <div v-if="groupClassBranch">

        </div>
        <div v-else>
            <h1>When are you available to teach?</h1>
            <TeacherPrivateSchedule v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
        </div>
      </v-stepper-content>
      <v-stepper-content step="15" v-if="step === 15">
        <h1>Edit dates</h1>
        <TeacherScheduleExclude v-on:update:step="updateStep" v-bind:weekdaysScheduled="weekdaysScheduled" v-bind:untilDate="untilDate" v-bind:startDate="startDate" v-on:next:step="nextStep" v-on:prev:step="prevStep"/>
      </v-stepper-content>
      <v-stepper-content step="16" v-if="step === 16">
        <TeacherAllDone v-on:update:step="updateStep" v-bind:daySelectType="daySelectType" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:isEditMode="isEditMode"/>
      </v-stepper-content>
      <v-stepper-content step="17" v-if="step === 17">
        <TeacherPreview v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:isEditMode="isEditMode"/>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script>
import axios from 'axios'
import _ from 'lodash'

import fbmap from '@/lib/fbmap'

import TeacherCategoryForm from '@/components/TeacherCategoryForm.vue'
import TeacherProfileForm from '@/components/TeacherProfileForm.vue'
import TeacherForm from '@/components/TeacherForm.vue'
import TeacherLoadAvatar from '@/components/TeacherLoadAvatar.vue'
import TeacherGroupOrPrivate from '@/components/TeacherGroupOrPrivate.vue'
import TeacherGroupClass from '@/components/TeacherGroupClass.vue'
import TeacherPrivateClass from '@/components/TeacherPrivateClass.vue'
import TeacherGroupSupport from '@/components/TeacherGroupSupport.vue'
import TeacherPrivatePackages from '@/components/TeacherPrivatePackages.vue'
import TeacherGroupPrice from '@/components/TeacherGroupPrice.vue'
import TeacherGroupPackages from '@/components/TeacherGroupPackages.vue'
import TeacherWhereChoice from '@/components/TeacherWhereChoice.vue'
import TeacherAddress from '@/components/TeacherAddress.vue'
import TeacherPrivateSchedule from '@/components/TeacherPrivateSchedule.vue'
import TeacherScheduleExclude from '@/components/TeacherScheduleExclude.vue'
import TeacherAllDone from '@/components/TeacherAllDone.vue'
import TeacherPreview from '@/components/TeacherPreview.vue'
import TeacherCompanyProfile from '@/components/TeacherCompanyProfile.vue'
import TeacherMultipleProfiles from '@/components/TeacherMultipleProfiles.vue'
import { mapGetters, mapState } from 'vuex'
import TeacherMembership from "@/components/Teacher/Membership";

export default {
    components: {
        TeacherMembership,
        TeacherCategoryForm,
        TeacherProfileForm,
        TeacherForm,
        TeacherLoadAvatar,
        TeacherGroupOrPrivate,
        TeacherGroupClass,
        TeacherPrivateClass,
        TeacherGroupSupport,
        TeacherPrivatePackages,
        TeacherWhereChoice,
        TeacherAddress,
        TeacherAllDone,
        TeacherPrivateSchedule,
        TeacherScheduleExclude,
        TeacherPreview,
        TeacherGroupPrice,
        TeacherGroupPackages,
        TeacherCompanyProfile,
        TeacherMultipleProfiles,
    },
    data () {
        return {
            step: 100,
            locationBranch: 'address',
            classType: null,
            weekdaysScheduled: [],
            startDate: null,
            untilDate: null,
            daySelectType: null,
            alreadyRegistered: false,
            hasAvatar: false,
            hasProfile: false,
            isWorkshop: false,
            classData: {},
            isEditMode: false,
            isCompany: false,
            subcategories: [],
            isCreditCardExists: false,
        }
    },
    created() {
        //console.log(this.$route)
        if(this.$route.params.id && this.isLoggedIn) {
            if(this.$route.name === 'teachers_copy_class') {
                //copy class
                axios.get(`/api/classes/${this.$route.params.id}/`).then(res => {
                    console.log(res.data)
                    delete res.data.schedule_dates
                    delete res.data.start_date
                    delete res.data.until_date
                    delete res.data.weekdays_schedule
                    delete res.data.schedule_excluded
                    delete res.data.day_select_type
                    delete res.data.enrolled
                    delete res.data.logged_in_user_orders
                    delete res.data.orders
                    this.$store.commit('setTeacherLessonType', res.data.is_private ? 'private' : 'group')
                    this.$store.commit('setGroupClassForce', fbmap.bf.teachingClass(res.data))
                    this.$store.commit('setTeacherCategory', res.data.subcategories)
                    this.$store.commit('setTeacherProfile', res.data.teacher)
                    this.$store.commit('setTeacher', res.data.teacher)
                    return axios.post('/api/draft/', {
                        class_data: {
                            teacherGroupClass: this.$store.state.teacherGroupClass,
                            teacherLessonType: this.$store.state.teacherLessonType,
                            categoriesSelected: this.$store.state.categoriesSelected,
                        }
                    })
                }).then(v => {
                    //this.isEditMode = true
                    this.updateStepValues()
                    this.step = 0
                    this.nextStep()
                })
            } else {
                axios.get(`/api/classes/${this.$route.params.id}/`).then(res => {
                    //console.log(`/api/classes/${this.$route.params.id}/`, res)
                    this.$store.commit('setTeacherLessonType', res.data.is_private ? 'private' : 'group')
                    this.$store.commit('setGroupClassForce', fbmap.bf.teachingClass(res.data))
                    this.$store.commit('setTeacherCategory', res.data.subcategories)
                    this.$store.commit('setTeacherProfile', res.data.teacher)
                    this.$store.commit('setTeacher', res.data.teacher)
                    this.isEditMode = true
                    this.updateStepValues()
                    this.step = 0
                    this.nextStep()
                })
            }
        } else {
            if(this.$store.state.teacherGroupClass && this.$store.state.teacherGroupClass.id) {
                this.$store.commit('setGroupClassForce', {})
                this.$store.commit('setTeacherLessonType', null)
            }
            //this.$store.commit('setTeacherLessonType', null)
            //this.$store.commit('setGroupClassForce', {})
            this.isEditMode = false
            this.step = 1
            this.updateStepValues()
        }
    },
    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        ...mapState([
            'teacherCreateMembership',
        ]),
        groupClassBranch: function () {
            return this.classType === 'group'
        },
        privateClassBranch: function () {
            return this.classType === 'private'
        },
        hasCompanyProfile() {
            return this.$store.state.companyProfile && this.$store.state.companyProfile.id && this.isCompany
        }
    },
    watch: {
        step() {
            this.updateStepValues()
        },
        async isLoggedIn(v) {
            if(v) {
                await this.$store.dispatch('loadDraft')
                if(this.step === 2) {
                    this.nextStep()
                    return
                }
            }
            this.step = 0
            this.nextStep()
        }
    },
    methods: {
        registerDone() {
            this.$emit('register:done')
        },
        openLoginForm() {
            this.$emit('openLoginForm')
        },
        updateStepValues() {
            this.classType = this.$store.state.teacherLessonType
            this.alreadyRegistered = this.$store.state.user && Object.keys(this.$store.state.user).length ? true : false
            this.hasAvatar = !!(this.$store.state.teacher && this.$store.state.teacher.id && this.$store.state.avatar && this.$store.state.avatar.uploadPhoto && this.$store.state.avatar.uploadPhoto.imageUrl)
            this.hasProfile = this.$store.state.teacher && this.$store.state.teacher.description && this.$store.state.teacher.areasOfSpeciality ? true : false
            this.isCompany = this.$store.state.user && this.$store.state.user.is_company
            if(this.$store.state.teacherGroupClass) {
                this.locationBranch = this.$store.state.teacherGroupClass.whereTeach || 'address'
                this.weekdaysScheduled = this.$store.state.teacherGroupClass.weekdaysScheduled
                this.untilDate = this.$store.state.teacherGroupClass.untilDate
                this.startDate = this.$store.state.teacherGroupClass.startDate
                this.daySelectType = this.$store.state.teacherGroupClass.daySelectType
                if('flexibleDates' in this.$store.state.teacherGroupClass) {
                    this.isWorkshop = !this.$store.state.teacherGroupClass.flexibleDates
                }
                this.classData = this.$store.state.teacherGroupClass
            }
        },
        updateStep: function (num, additional = {}) {
            _.each(additional, (v, k) => {
                this[k] = v
            })
            this.updateStepValues()
            this.step = num
        },
        nextStep: function () {
            this.updateStepValues()
            if(this.isLoggedIn && this.$store.state.teacherGroupClass && !this.$store.state.teacherGroupClass.id) {
                axios.post('/api/draft/', {
                    class_data: {
                        teacherGroupClass: this.$store.state.teacherGroupClass,
                        teacherLessonType: this.$store.state.teacherLessonType,
                        categoriesSelected: this.$store.state.categoriesSelected,
                    }
                })
            }
            let add = 0
            this.step = Number(this.step)
            /* removed by Alisa's request
            if(this.step+add == 0 && this.isEditMode && this.privateClassBranch) {
                add++
            }
            */
            if(this.step+add === 1 && this.alreadyRegistered) {
                add++
            }
            if(this.step+add === 2 && (this.hasCompanyProfile || !this.isCompany && this.hasProfile || this.isEditMode)) {
                add++
            }
            if(this.step+add === 3 && (this.hasAvatar || this.isEditMode || this.isCompany)) {
                add++
            }
            if(this.step+add === 4 && this.isEditMode) {
                add++
            }
            if(this.step+add === 5 && !this.teacherCreateMembership) {
                add++
            }
            if(this.step+add === 7 && this.privateClassBranch) {
                add++
            }

            if(this.step+add === 8 && !this.isCompany) {
                add++
            }

            if(this.step+add === 10 && this.privateClassBranch) {
                add++
            }
            if(this.step+add === 12 && (this.locationBranch === 'online' || this.locationBranch === 'custom')) {
                add++
            }
            if(this.step+add === 13 && this.groupClassBranch) {
                add++
            }
            if(this.step+add === 14 && (this.$store.state.teacherGroupClass.daySelectType !== 'weekly' || this.groupClassBranch)) {
                add++
            }
            this.step = Number(this.step) + (add+1)
        },
        prevStep: function () {
            this.updateStepValues()
            let add = 0
            this.step = Number(this.step)
            if(this.step-add === 16 && (this.$store.state.teacherGroupClass.daySelectType !== 'weekly' || this.groupClassBranch)) {
                add++
            }
            if(this.step-add === 15 && this.groupClassBranch) {
                add++
            }
            if(this.step-add === 14 && (this.locationBranch === 'online' || this.locationBranch === 'custom')) {
                add++
            }
            if(this.step-add === 12 && this.privateClassBranch) {
                add++
            }

            if(this.step-add === 10 && !this.isCompany) {
                add++
            }
            if(this.step-add === 9 && this.privateClassBranch) {
                add++
            }
            if(this.step-add === 7 && !this.teacherCreateMembership) {
                add++
            }
            if(this.step-add === 6 && this.isEditMode) {
                add++
            }
            if(this.step-add === 5 && (this.hasAvatar || this.isEditMode || this.isCompany)) {
                add++
            }
            if(this.step-add === 4 && (this.hasCompanyProfile || !this.isCompany && this.hasProfile || this.isEditMode)) {
                add++
            }
            if(this.step-add === 3 && this.alreadyRegistered) {
                add++
            }
            /* removed by Alisa's request
            if(this.step-add == 2 && this.isEditMode && this.privateClassBranch) {
                add++
            }
            */
            this.step -= (add+1)
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>