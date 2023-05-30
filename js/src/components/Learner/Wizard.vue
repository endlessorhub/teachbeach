<template>
  <v-stepper v-if="dataReady" v-model="step" class="flex xs11 learner-city-category" style="box-shadow: none;">
    <v-stepper-header style="display: none;">
      <v-stepper-step :complete="step > 1" step="1"><div class="text-xs-center">Choose<br/>a category</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 2" step="2"><div class="text-xs-center">Create<br/>needs</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 3" step="3"><div class="text-xs-center">Create<br/>contact</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 4" step="4"><div class="text-xs-center">Create<br/>duration</div></v-stepper-step>
      <v-divider></v-divider>
      <v-stepper-step :complete="step > 5" step="5"><div class="text-xs-center">Create<br/>num lessons</div></v-stepper-step>
        <v-divider></v-divider>
      <v-stepper-step :complete="step > 6" step="6"><div class="text-xs-center">Create<br/>num lessons</div></v-stepper-step>
        <v-divider></v-divider>
      <v-stepper-step :complete="step > 7" step="7"><div class="text-xs-center">Create<br/>num lessons</div></v-stepper-step>
        <v-divider></v-divider>
      <v-stepper-step :complete="step > 8" step="8"><div class="text-xs-center">Create<br/>num lessons</div></v-stepper-step>
    </v-stepper-header>

    <v-stepper-items>
      <v-stepper-content step="1">

      </v-stepper-content>

      <v-stepper-content step="2">
        <h1 v-if="isPrivate && step === 2">{{teacherName}}'s schedule</h1>
        <!--Needs v-if="isPrivate && step == 2" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-on:back:to:start="backToStart"/-->
          <PrivateFinalReverse v-if="learnerChoice && isPrivate && step === 2"
              v-on:update:step="updateStep"
              v-on:next:step="nextStep"
              v-on:prev:step="prevStep"
              v-bind:class-data="learnerChoice"
          />
      </v-stepper-content>

      <v-stepper-content step="3">
        <h1 v-if="!isPrivate">Looks like you are new here! <a href="javascript:void(0);" @click="openLoginForm">Login if not</a></h1>
        <h1 v-if="isPrivate">What’s  a good way for {{teacherName}} to contact you? <a href="javascript:void(0);" @click="openLoginForm">Or login</a></h1>
        <Contact v-if="step == 3" v-on:update:step="updateStep" v-on:prev:step="prevStep" v-bind:isPrivate="isPrivate" v-on:openLoginForm="openLoginForm"/>
      </v-stepper-content>

      <v-stepper-content step="4">
        <h1 v-if="isPrivate">How long would you like to meet with {{teacherName}}?</h1>
        <h1 v-else>{{className}}</h1>
        <PrivatePackage v-if="isPrivate && step === 4" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:step="step"/>
        <Schedule v-bind:step="step" v-else-if="learnerChoice && step === 4" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind="learnerChoice" v-on:back:to:start="backToStart"/>
      </v-stepper-content>

      <v-stepper-content step="5">
        <h1 v-if="isPrivate">How many people are you bringing?</h1>
        <PrivatePersons v-if="isPrivate && step === 5" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:step="step" v-bind:duration="duration" v-bind="learnerChoice"/>
        <h1 v-if="!isPrivate && isWorkshop">How many people are you bringing?</h1>
        <GroupPersons v-if="!isPrivate && step === 5 && isWorkshop" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:step="step" v-bind="learnerChoice"/>
      </v-stepper-content>

      <v-stepper-content step="6">
        <Checkout3 v-bind:step="step" v-if="learnerChoice && step === 6" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:classData="learnerChoice"/>
      </v-stepper-content>

      <v-stepper-content step="7">
        <h1 v-if="isPrivate">Request a time to meet {{teacherName}} For  {{className}}</h1>
        <PrivateFinal v-if="learnerChoice && isPrivate && step === 7"
          v-on:update:step="updateStep"
          v-on:next:step="nextStep"
          v-on:prev:step="prevStep"
          v-bind:duration="duration"
          v-bind:num-lessons="numLessons"
          v-bind:order-id="order_id"
          v-bind:classData="learnerChoice"
          v-bind:orderData="orderData"
        />
        <ChooseClasses v-if="learnerChoice && step === 7 && !isPrivate"
           v-on:update:step="updateStep"
           v-on:next:step="nextStep"
           v-on:prev:step="prevStep"
           v-bind="learnerChoice"
           v-bind:package="package"
           v-bind:learnerData="learnerData"
           v-bind:order-id="order_id"
        />
      </v-stepper-content>

      <v-stepper-content step="8">
        <h1>Congratulations!</h1>
        <Confirmation v-if="learnerChoice && step === 8" v-on:update:step="updateStep" v-on:next:step="nextStep" v-on:prev:step="prevStep" v-bind:classData="learnerChoice"/>
      </v-stepper-content>


    </v-stepper-items>
  </v-stepper>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import Needs from '@/components/Learner/Needs.vue'
import Contact from '@/components/Learner/ContactMinimal.vue'
import Checkout3 from '@/components/Learner/Checkout3.vue'
import Confirmation from '@/components/Learner/Confirmation.vue'
import Schedule from '@/components/Learner/Schedule.vue'
import PrivateFinal from '@/components/Learner/PrivateFinal.vue'
import PrivateFinalReverse from '@/components/Learner/PrivateFinalReverse.vue'
import ChooseClasses from '@/components/Learner/ChooseClasses.vue'
import PrivatePackage from "@/components/Learner/PrivatePackage";
import PrivatePersons from "@/components/Learner/PrivatePersons";
import GroupPersons from "@/components/Learner/GroupPersons";

let prevRoute = null

export default {
    props: [
        'initialStep',
        'initialId',
        'initialOrderId',
    ],
    components: {
        GroupPersons,
        PrivatePersons,
        PrivatePackage,
        Needs,
        Contact,
        Checkout3,
        Confirmation,
        Schedule,
        PrivateFinal,
        ChooseClasses,
        PrivateFinalReverse,
    },
    data () {
        return {
            dataReady: false,
            order_id: null,
            orderData: null,
        }
    },
    created() {
        //this.loadInitialData()
        if(this.$route.query.email || this.$route.query.name || this.$route.query.phone) {
            //prefill user(student) data
            this.$store.commit('setStudentName', this.$route.query.name)
            this.$store.commit('setStudentPhone', this.$route.query.phone)
            this.$store.commit('setStudentEmail', this.$route.query.email)
        }
    },
    mounted() {
        if(!this.classId)
            return
        if(this.classId && !this.$store.state.learnerChoice || this.$store.state.learnerChoice.id !== this.classId || !this.orderData && this.initialOrderId) {
            this.loadInitialData().then((res) => {
                let step = this.step-1
                if (!this.order_id) {
                    // if no order id that means no order data loaded, so not set, fallback to first step
                    step = Math.min(3, step)
                }
                step = this.getNextStep(step)
                if(step !== this.step) {
                    // shift step due to some conditions
                    this.$router.push(`/learners/${this.classId}/${step}`+(this.order_id ? `/${this.order_id}` : ''))
                }
                this.dataReady = true
            })
        } else {
            let step = this.step-1
            step = this.getNextStep(step)
            if(step !== this.step) {
                // shift step due to some conditions
                this.$router.push(`/learners/${this.classId}/${step}`+(this.order_id ? `/${this.order_id}` : ''))
            }
            this.dataReady = true
        }

        /*
        this.$nextTick(() => {
            if(this.initialId) {
                if (!this.$store.state.learnerChoice || this.$store.state.learnerChoice.id != this.initialId || !this.orderData && this.initialOrderId) {
                    this.loadInitialData().then((res) => {
                        console.log('promise3', res)
                        if(this.initialStep) {
                            let step = this.initialStep-1
                            if (!this.order_id) {
                                // if no order id that means no order data loaded, so not set, fallback to first step
                                step = Math.min(3, step)
                            }
                            this.step = step
                            this.stepRoute = step
                            this.nextStep()
                        }
                    })
                } else {
                    this.classData = this.$store.state.learnerChoice
                    if(this.initialOrderId) {
                        this.order_id = this.initialOrderId
                        if(this.$store.state.learnerData) {
                            this.isPrivate = this.$store.state.learnerChoice.is_private
                            this.className = this.isPrivate ? this.$store.state.learnerChoice.private_className : this.$store.state.learnerChoice.name
                            if(this.$store.state.learnerData.package && this.$store.state.learnerData.package.lessonLength)
                                this.duration = this.$store.state.learnerData.package.lessonLength.value
                            if(this.$store.state.learnerData && this.$store.state.learnerData.numLessons)
                                this.numLessons = this.$store.state.learnerData.numLessons
                            this.package = this.$store.state.learnerData.package
                        }
                    }
                    if(this.initialStep) {
                        this.step = this.initialStep-1
                        this.stepRoute = this.initialStep-1
                        this.nextStep()
                    }
                }
            }
        })
        */
    },
    computed: {
        ...mapState(['learnerChoice', 'learnerData', 'user']),
        isPrivate() {
            return this.learnerChoice && this.learnerChoice.is_private
        },
        package() {
            return this.learnerData && this.learnerData.package
        },
        isWorkshop() {
            return this.learnerChoice && !this.learnerChoice.flexible_dates && !this.isPrivate
        },
        className() {
            return this.learnerChoice && (this.isPrivate ? this.learnerChoice.private_className : this.learnerChoice.name)
        },
        alreadyRegistered() {
            return this.user && !!Object.keys(this.user).length
        },
        teacherName() {
            return this.learnerChoice && this.learnerChoice.teacher.first_name
        },
        step() {
            return Number(this.initialStep) || 2
        },
        classId() {
            return Number(this.initialId)
        },
        duration() {
            return this.package && this.package.lessonLength && this.package.lessonLength.value
        },
        numLessons() {
            return Number(this.orderData && this.orderData.num_lessons) || 0
        }
    },
    watch: {
        step(val, oldVal) {
            if(this.learnerChoice && this.step >= 2) {
                this.updateCompanyProfile()
            }
        },
        learnerChoice(v) {
            if(v && this.step >= 2) {
                 this.updateCompanyProfile()
            }
        },
        user(v) {
            // go to login if user has changed
            if(Number(this.initialStep) === 3)
                this.nextStep()
            else
                this.$router.push(`/learners/${this.classId}/3`)
        }
    },
    methods: {
        updateCompanyProfile() {
            this.$store.dispatch('syncLogoCompanyProfile', this.learnerChoice.teacher.user.company_profile ? this.learnerChoice.teacher.user.company_profile.id : null);
        },
        openLoginForm() {
            this.$store.commit('setLoginFormOpened', {register: 'close'})
            //this.$emit('openLoginForm', {register: 'close'})
        },
        loadInitialData() {
            this.isLoading = true
            return axios.get('/api/classes/'+this.initialId+'/').then((res) => {
                console.log('done', res)
                //this.classData = res.data
                this.$store.commit('setLearnerChoice', res.data)
                if(this.initialOrderId) {
                    this.order_id = this.initialOrderId
                    return this.reloadOrder()
                }
                return false
            }).then((res) => {
                console.log('promise2', res)
                return true
            }).catch((e) => {
                console.log(e)

            }).then(() => {
                this.isLoading = false
            })
        },

        reloadOrder() {
            return axios.get('/api/orders/'+this.order_id+'/').then(res => {
                this.orderData = res.data

                const dataToSet = {
                    id: res.data.data.id,
                    package: this.package,
                    learnerNeeds: res.data.data.learnerNeeds,
                }
                if('package' in res.data.data)
                    dataToSet.package = res.data.data.package
                if('persons' in res.data.data)
                    dataToSet.persons = res.data.data.persons
                if('learnerNeeds' in res.data.data)
                    dataToSet.learnerNeeds = res.data.data.learnerNeeds
                if (res.data.order_enrolled && res.data.order_enrolled.length) {
                    dataToSet.selectedLessons = res.data.order_enrolled
                        .filter(v => v.status !== 'rejected')
                        .map(v => `${v.date}_${v.time_from}-${v.time_to}`)
                }
                this.$store.commit('setLearnerData', dataToSet)
                return true
            })
        },
        getNextStep(step) {
            let add = 0
            //back to registration if not registered yet (for group classes)
            if(!this.alreadyRegistered && step > 2) {
                step = 2
            }

            if(step+add === 1 && !this.isPrivate) {
                add++
            }
            if(step+add === 2 && this.alreadyRegistered) {
                add++
            }
            if(step+add === 4 && this.isPrivate && this.package && this.package.minPersons === this.package.maxPersons) {
                this.$store.commit('mergeLearnerData', {persons: this.package.minPersons})
                add++
            } else if(step+add === 4 && (!this.isPrivate || this.package && this.package.isSubscription) && !this.isWorkshop) {
                add++
            }
            return step+add+1
        },
        getPrevStep(step) {
            let add = 0
            if(step-add === 6 && (!this.isPrivate || this.package && this.package.isSubscription) && !this.isWorkshop) {
                add++
            } else if(step-add === 6 && this.isPrivate && this.package && this.package.minPersons === this.package.maxPersons) {
                add++
            }
            if(step-add === 4 && this.alreadyRegistered) {
                add++
            }
            if(step-add === 3 && !this.isPrivate) {
                add++
            }
            return step-(add+1)
        },
        nextStep: function (data) {
            if(data) {
                if(data.order_id) {
                    this.order_id = data.order_id
                    return this.reloadOrder().then(() => {
                        this.$router.push(`/learners/${this.classId}/${this.step+1}/${data.order_id}`)
                    })
                }
            }
            let step = this.getNextStep(this.step)
            if(step !== this.step) {
                return this.$router.push(`/learners/${this.classId}/${step}${this.order_id ? `/${this.order_id}` : ''}`)
            }
        },
        prevStep: function (data) {
            if(data) {
                if(data.order_id) {
                    this.order_id = data.order_id
                }
            }
            let step = this.getPrevStep(this.step)
            if(step !== this.step) {
                return this.$router.push(`/learners/${this.classId}/${step}${this.order_id ? `/${this.order_id}` : ''}`)
            }
        },
        backToStart() {
            let route = '/'
            if(prevRoute && prevRoute.name !== 'learners_step') {
                route = prevRoute.fullPath
            } else if (this.learnerChoice) {
                route = `/class/${this.learnerChoice.id}`
            }
            this.stepRoute = 1
            this.$router.push(route)
        },
        syncRouter(path) {
            if(path !== this.$router.currentRoute.fullPath)
                this.$router.push({path})
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.learner-city-category .v-stepper__content {
    padding: 0;
}
</style>