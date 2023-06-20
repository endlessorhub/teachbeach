<template>

  <form>
      <v-layout v-if="showAccountForm && !isAccountFormPrepared" align-center justify-center row wrap fill-height>
          <v-flex xs12 headline>
              Processing class, please wait
              <v-progress-circular
                  indeterminate
                  color="primary"
              ></v-progress-circular>
          </v-flex>
      </v-layout>
      <div :style="formStyle">
        <h1 v-if="showAccountForm">Where would you like to receive funds?</h1>
        <h1 v-else>All done</h1>
        <v-container grid-list-md text-xs-center>
          <v-layout align-top justify-center row wrap>
            <v-flex xs12 class="text-xs-center" v-if="showAccountForm">
              <TeacherAccount ref="accountForm" v-bind:isForTeacherPath="true" v-on:data:loaded="onAccountDataLoaded"></TeacherAccount>
            </v-flex>
            <v-flex xs12 class="text-xs-center title" v-else>
                Thanks!
            </v-flex>
            <v-flex xs12 md6 class="text-xs-center">
              <v-btn v-if="!published" @click="preview" color="primary" :disabled="isLoading" :loading="isLoading">Preview</v-btn>
            </v-flex>
            <v-flex xs12 md6 class="text-xs-center">
              <v-btn v-if="isPublishAvailable" color="success" @click="submit" :disabled="isLoading" :loading="isLoading">{{publishBtnText}}</v-btn>
            </v-flex>
            <v-flex v-if="published && isGroupClass" xs12 class="text-xs-center">
              <h4>Share  this class to your social media feed</h4>
              <social-share-class
                :class-id="classId"
                :class-name="className"
              />
              <v-btn v-if="published" @click="goAway" color="primary" :disabled="isLoading" :loading="isLoading">No, thanks</v-btn>
            </v-flex>
          </v-layout>
        </v-container>
        <v-btn v-if="isBackAvailable" @click="back" :disabled="isLoading" :loading="isLoading">Back</v-btn>
        <v-alert
          v-model="published"
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
      </div>
  </form>
</template>

<script>

import _ from 'lodash'
import TeacherAccount from '@/components/Dashboard/Teach/AccountTake.vue'
import AddToCalendar from '@/components/basic/AddToCalendar'
import SocialShareClass from '@/components/basic/SocialShareClass'
import datamap from '@/lib/fbmap'
import axios from 'axios'

export default {
    props: {
        isEditMode: Boolean,
        isSuccess: Boolean,
        classId: Number,
    },
    components: {
        TeacherAccount,
        AddToCalendar,
        SocialShareClass,
    },
    data: () => ({
        isLoading: false,
        published: false,
        notPublishedError: '',
        notPublished: false,
        addAnother: false,
        publishBtnText: 'Save draft',
        publishedMessage: 'Your Class was published',
        isBackAvailable: true,
        isPublishAvailable: true,
        showAccountForm: false,
        isAccountFormPrepared: false,
        canBook: true,
        canPay: true,
        isBankAccount: false,
        isFirstClass: false,
        schedule: {},
        isGroupClass: false,
        className: '',
    }),

    created: function () {
        let _this = this
        if (this.$store.state.teacherGroupClass) {
            // account form temporary disabled
            //this.showAccountForm = this.$store.state.teacherGroupClass.canPay && this.$store.state.teacherGroupClass.canBook
        }
        if(this.isEditMode) {
            this.publishBtnText = 'Save edits'
            this.publishedMessage = 'Your Class was updated'
        }
        if(this.isSuccess && this.classId) {
            // already published, this is /teachers/finish'
            this.isLoading = true
            this.published = true
            this.loadClass(this.classId).then((res) => {
                if(!res.data)
                    return
                this.isLoading = false
                this.setSchedule(res.data)
                this.addAnother = true
                this.isBackAvailable = false
                this.isPublishAvailable = false
                this.canBook = res.data.can_book
                this.canPay = res.data.can_pay
                this.isFirstClass = (res.data.teacher.group_count + res.data.teacher.private_count) <= 1
                this.isBankAccount = true
                this.className = res.data.is_private ? res.data.private_className : res.data.name;
            })
        }
    },

    computed: {
        eventsFilename() {
            return `${(new Date()).getTime()}.ics`
        },
        formStyle() {
            return !this.showAccountForm || this.isAccountFormPrepared ? {} : {display: 'none'}
        },
        events() {
            return this.published ? _.map(this.scheduleDates, d => ({
                date_st: d.start,
                date_end: d.end,
            })) : []
        }
    },

    methods: {
        another() {
            this.$store.commit('setGroupClassForce', {})
            this.$store.commit('setTeacherLessonType', null)
            this.$router.push('/teachers/start')
            //this.$emit('update:step', 1, {isEditMode: false})
        },
        preview() {
            this.$emit('update:step', 17)
        },
        back() {
            this.$emit('prev:step')
        },
        submit () {

            //make axios call
            this.published = false
            this.addAnother = false
            this.isLoading = true
            let _this = this
            const initialStep = this.showAccountForm && this.$refs.accountForm.showForm ? this.$refs.accountForm.save() : Promise.resolve(true)
            /*
            initialStep.then(res => {
                console.log(res)
            }).catch(e => {
                console.log(e)
            })
            return
            */
            initialStep.then(res => {
                if(res)
                    return axios.post('/api/classes/', {
                        //user: _this.$store.state.user,
                        profile: _this.$store.state.profile,
                        avatar: _this.$store.state.avatar,
                        categories: _this.$store.state.categoriesSelected,
                        teacherLessonType: _this.$store.state.teacherLessonType,
                        teacherGroupClass: _this.$store.state.teacherGroupClass
                    })
                else {
                    return Promise.resolve({
                        data: {
                            success: false
                        }
                    })
                }
            }).then((res) => {
                console.log('done', res)
                if(res.data && res.data.success) {
                    //_this.$emit('update:step', 11)
                    fbq('trackCustom', 'teacherClassPublish')
                    this.published = true
                    this.addAnother = true
                    this.isBackAvailable = false
                    this.isPublishAvailable = false
                    this.canBook = this.$store.state.teacherGroupClass.canBook
                    this.canPay = this.$store.state.teacherGroupClass.canPay
                    this.isFirstClass = res.data.isFirstClass
                    this.isBankAccount = res.data.isBankAccount
                    const isEditing = this.$store.state.teacherGroupClass.id
                    const isDeactivated = this.$store.state.teacherGroupClass.is_deactivated
                    this.$store.commit('setGroupClassForce', {

                    })
                    /*
                    if(res.data.current_option && res.data.current_option.id) {
                        this.$router.push(`/email_upsell/${res.data.id}`)
                    } else {
                        if(this.canBook) {
                            this.$router.push(`/choose_model/${res.data.id}`)
                        } else {
                            this.$router.push(`/join_as_member/${res.data.id}`)
                        }
                    }
                    */
                    //this.goAway()
                    // insert checkout page after successful publishing
                    if(res.data.isFreeMember || (isEditing && !isDeactivated))
                        return this.$router.push(`/teachers/finish/${res.data.id}`)
                    else
                        return this.$router.push(`/teacher_check/${res.data.id}`)
                    //return this.loadSchedule(res.data.id)

                } else if (res.data && res.data.error_message) {
                    //process errors
                    this.notPublished = true
                    this.notPublishedError = res.data.error_message
                }
            }).catch((e) => {
                console.log('error', e)
                this.notPublished = true
                this.notPublishedError = JSON.stringify(e.response.errors || 'Server error')//'server error, try again later'
            }).then(() => {
                _this.isLoading = false
            })

            //this.$emit('update:step', 12)
        },
        goAway() {
            if(!this.canPay || !this.canBook) {
                this.$router.push('/dashboard/teach/classes')
                return
            }
            if(this.isBankAccount) {
                if(this.isFirstClass) {
                    this.$router.push('/dashboard/teach/classes/first')
                } else {
                    this.$router.push('/dashboard/teach/classes')
                }
            } else {
                if(this.isFirstClass) {
                    this.$router.push('/dashboard/teach/account_take')
                } else {
                    this.$router.push('/dashboard/teach/account_take')
                }
            }
        },
        clear () {

        },
        onAccountDataLoaded(options) {
            this.isAccountFormPrepared = true
        },
        loadClass(id) {
            return axios.get('/api/classes/'+id+'/')
        },
        setSchedule(tclass) {
            this.schedule = _.pick(tclass, [
                'schedule_dates',
                'schedule_excluded',
                'day_select_type',
                'start_date',
                'timezone',
                'until_date',
                'weekdays_schedule',
            ])
            this.schedule.summary = tclass.name
            this.schedule.location = tclass.address ? [
                tclass.address,
                tclass.address_street,
                `${tclass.address_city} ${tclass.address_state}`,
                tclass.address_zip,
            ].join(', ') : tclass.class_type[0].toUpperCase()+tclass.class_type.substr(1)
            this.isGroupClass = !tclass.is_private
        },
        loadSchedule(id) {
            return this.loadClass(id).then((res) => {
                if(!res)
                    return
                this.setSchedule(res.data)
            })
        }
    },
    watch: {
        published(val, oldVal) {
            if(oldVal && !val) {
                //closing, go to dashboard
                this.$router.push('/dashboard/teach/classes')
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>