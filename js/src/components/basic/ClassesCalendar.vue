<template>
  <v-layout align-center justify-center row wrap class="teacher-calendar">
            <v-flex sm4 xs12 class="text-sm-left text-xs-center">
              <v-btn @click="$refs.calendar.prev()">
                <v-icon dark left>
                  keyboard_arrow_left
                </v-icon>
                Prev
              </v-btn>
            </v-flex>
            <v-flex sm4 xs12 class="text-xs-center">
              {{yearMonth}}
            </v-flex>
            <v-flex
              sm4
              xs12
              class="text-sm-right text-xs-center"
            >
              <v-btn @click="$refs.calendar.next()">
                Next
                <v-icon
                  right
                  dark
                >
                  keyboard_arrow_right
                </v-icon>
              </v-btn>
            </v-flex>

            <v-flex xs12>
              <v-sheet height="600">
                <v-calendar
                  ref="calendar"
                  v-model="start"
                  :type="type"
                  :end="end"
                  color="primary"
                >
                    <template v-slot:day="{ date }">
                        <template v-for="event in calendarEvents[date]">
                          <v-menu
                            v-if="event.items"
                            :key="event.key"
                            v-model="event.open"
                            full-width
                            offset-y
                            top
                            :close-on-content-click="true"
                            :close-on-click="true"
                          >
                            <template v-slot:activator="{ on }">
                              <div
                                v-ripple
                                v-on="on"
                                class="lesson-event"
                              >
                                  {{event.name}}
                              </div>
                            </template>

                                <div style="background: white;">
                                    <div
                                        v-for="(item, index) in event.items"
                                        :key="item.key"
                                        v-ripple
                                        class="lesson-event"
                                        @click="$router.push(`/class/${item.id}`)"
                                    >
                                          {{item.name}}
                                    </div>
                                </div>

                          </v-menu>
                            <div
                                v-else
                                :key="event.key"
                                v-ripple
                                class="lesson-event"
                                @click="$router.push(`/class/${event.id}`)"
                            >
                                  {{event.name}}
                            </div>
                        </template>
                    </template>
                </v-calendar>
              </v-sheet>
            </v-flex>
    </v-layout>
</template>

<script>
import api from '@/lib/api'
import utils from '@/lib/utils'
import moment from 'moment'

export default {
    props: {
        teacherId: {
            type: Number,
        },
        classes: {
            type: Object,
            default: [],
        }
    },
    data: () => ({
        cellEventsLimit: 3,
        type: 'month',
        start: utils.dateToString(new Date()),
        end: utils.dateToString(new Date()),
        typeOptions: [
            { text: 'Day', value: 'day' },
            { text: '4 Day', value: '4day' },
            { text: 'Week', value: 'week' },
            { text: 'Month', value: 'month' },
        ],
    }),
    name: 'classes_calendar',
    computed: {
        dateEvents() {
            const res = {}
            this.classes.forEach(c => {
                c.schedule_dates.forEach(sd => {
                    if(!res[sd.date])
                        res[sd.date] = []
                    res[sd.date].push(Object.assign({
                        id: c.id,
                        key: `${sd.date} ${sd.start}`,
                        name: c.name,
                        datetime: moment(`${sd.date} ${sd.start}`)
                    }, sd))
                })
            })
            console.log(res)
            return res
        },
        calendarEvents() {
            return Object.entries(this.dateEvents).reduce((acc, [datetime, events]) => {
                const sorted = events.sort((a, b) => (a.datetime - b.datetime))
                if(events.length > this.cellEventsLimit) {
                    acc[datetime] = sorted.slice(0, this.cellEventsLimit-1)
                    acc[datetime].push({
                        id: 'multiple',
                        key: `${datetime}_additional`,
                        name: `+${events.length-this.cellEventsLimit} lessons`,
                        items: sorted,
                    })
                } else
                    acc[datetime] = sorted
                return acc
            }, {})
        },
        yearMonth() {
            return utils.stringToDate(this.start).toLocaleString('en-us', {month: 'long'})
        }
    },
}
</script>
<style scoped lang="scss">
.lesson-event {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-radius: 2px;
    color: #000000;
    width: 100%;
    font-size: 12px;
    padding: 3px;
    cursor: pointer;
    margin-bottom: 1px;
    background-color: rgba(31, 190, 215, 0.1);
    border: 1px solid rgba(31, 190, 215, 1);
}
</style>