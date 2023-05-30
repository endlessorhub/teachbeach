<template>
    <v-card
        class="mx-auto"
        max-width="500"
    >
        <v-card-title class="title font-weight-regular justify-space-between">
          <span>Select student and time slot</span>
        </v-card-title>
        <v-card-text>
            <div class="selected-title">{{ currentTitle }}</div>
            <v-btn
                :disabled="isNextDisabled"
                color="primary"
                depressed
                @click="next"
            >
                {{selectedStep === 3 ? 'Save' : 'Next'}}
            </v-btn>
        <v-window v-model="selectedStep">
          <v-window-item :value="1">
              <SignInStudentStudentList
                v-if="isPrivate"
                :isAvailable="isAvailable"
                :studentsAvailable="studentsAvailable"
                v-model="studentRadio"
              />
              <v-date-picker
                v-else
                v-model="selectedDate"
                :allowedDates="isDateAvailable"
                no-title
              ></v-date-picker>

          </v-window-item>
          <v-window-item :value="2">
              <v-date-picker
                v-if="isPrivate"
                v-model="selectedDate"
                :allowedDates="isPrivateDateAvailable"
                no-title
              ></v-date-picker>
              <SignInStudentStudentList
                v-else
                :isAvailable="isAvailable"
                :studentsAvailable="studentsAvailable"
                v-model="studentRadio"
              />

          </v-window-item>
            <v-window-item :value="3">
              <v-radio-group v-model="selectedTime" class="full-width">
                <v-list
                  two-line
                >
                  <v-list-tile v-for="item in timeSlots" :key="item.start" @click.prevent="item.isAvailable && (selectedTime = item.start)">
                    <v-list-tile-action>
                      <v-radio
                        :value="item.start"
                        :disabled="!item.isAvailable"
                      ></v-radio>
                    </v-list-tile-action>

                    <v-list-tile-content>
                      <v-list-tile-title>{{formatTime(item.start)}} - {{formatTime(item.end)}}</v-list-tile-title>
                      <v-list-tile-sub-title></v-list-tile-sub-title>
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
              </v-radio-group>
          </v-window-item>
        </v-window>

            <v-divider></v-divider>

            <v-card-actions>
              <v-btn
                :disabled="selectedStep === 1"
                flat
                @click="selectedStep--"
              >
                Back
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                :disabled="isNextDisabled"
                color="primary"
                depressed
                @click="next"
              >
                {{selectedStep === 3 ? 'Save' : 'Next'}}
              </v-btn>
            </v-card-actions>

        </v-card-text>
    </v-card>
</template>

<script>

import moment from 'moment'
import classHelper from '@/lib/helpers/Class'
import utils from "@/lib/utils";
import SignInStudentStudentList from './SignInStudentStudentList'

export default {
    name: 'dashboard_component_signinstudent',
    data() {
        return {
            isLoading: false,
            selectedStep: 1,
            selectedDate: null,
            selectedTime: null,
            selectedStudent: null,
        }
    },
    props: [
        'classData',
        'studentsAvailable',
        'value', // {student, date, step}
    ],
    components: {
        SignInStudentStudentList,
    },
    created() {

    },
    computed: {
        duration() {
            return this.selectedStudent && this.selectedStudent.order.data.package.lessonLength && this.selectedStudent.order.data.package.lessonLength.value;
        },
        isNextDisabled() {
            if(this.isPrivate && this.selectedStep === 2 && !this.selectedDate)
                return true
            if(this.isPrivate && this.selectedStep === 1 && !this.selectedStudent)
                return true
            if(!this.isPrivate && this.selectedStep === 1 && !this.selectedDate)
                return true
            if(!this.isPrivate && this.selectedStep === 2 && !this.selectedStudent)
                return true
            if(this.selectedStep === 3 && !this.selectedTime)
                return true
            return false
        },
        isPrivate() {
            return this.classData && this.classData.is_private
        },
        availableDates() {
            if(!this.classData)
                return []
            if(this.classData.is_private) {
                const duration = this.selectedStudent && this.selectedStudent.order.data.package.lessonLength && this.selectedStudent.order.data.package.lessonLength.value
                return this.selectedStudent ? classHelper.getAvailableSchedule(this.classData, 100, duration) : []
            }
            return classHelper.getAvailableSchedule(this.classData, 100)

        },
        timeSlots() {
            return classHelper.getAllTimeSlots(this.selectedDate, this.duration || 30);
            // return this.availableDates && this.availableDates[this.selectedDate] || []
        },
        studentRadio: {
            set(v) {
                this.selectedStudent = (this.studentsAvailable || []).find(s => s.id === v)
            },
            get() {
                return this.selectedStudent && this.selectedStudent.id
            }
        },
        currentTitle() {
            const res = []
            if(this.selectedDate) {
                if(this.selectedTime) {
                    const timeSlot = this.timeSlots.find(v => v.start === this.selectedTime)
                    timeSlot && res.push((new Date(this.selectedDate + ' ' + this.selectedTime + ':00')).toLocaleString('en-us', {
                        month: 'long',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: 'numeric',
                    }) + ' - ' + (new Date(this.selectedDate + ' ' + timeSlot.end + ':00')).toLocaleString('en-us', {
                        hour: 'numeric',
                        minute: 'numeric',
                    }))
                } else
                    res.push((new Date(this.selectedDate)).toLocaleString('en-us', {month: 'long', day: 'numeric'}))
            }
            if(this.selectedStudent) {
                res.push(`${this.selectedStudent.first_name} ${this.selectedStudent.last_name}`)
            }
            return res.join(', ')
        },
    },
    methods: {
        isAvailable(item) {
            return item.num_lessons > item.reserved_lessons
        },
        formatTime(time) {
            return utils.time24HtoAMPM(time)
        },
        isDateAvailable(date) {
            return this.availableDates && this.availableDates[date] && this.availableDates[date].length
        },
        isPrivateDateAvailable(date) {
            return moment(`${date} 23:59:59`) >= new Date()
        },
        next() {
            if(this.selectedStep === 3) {
                this.$emit('change', {
                    date: this.selectedDate,
                    time: this.selectedTime,
                    student: this.selectedStudent,
                })
            } else {
                this.selectedStep++
            }
        }
    },

    watch: {
        value(v) {
            this.selectedStep = v && v.step
            this.selectedDate = v && v.date
            this.selectedTime = v && v.time
            this.selectedStudent = v && v.student
        },
    }
}
</script>
<style lang="scss" scoped>
.selected-title {
    height: 26px;
    margin-top: -26px;
}

</style>
<style lang="scss">
.full-width > .v-input__control {
    width: 100%;
}
</style>