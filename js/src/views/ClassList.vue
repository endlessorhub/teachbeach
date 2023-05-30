<template>
  <v-layout align-top justify-center row wrap>
    <v-flex xs12 class="text-xs-left">
        <v-layout align-top justify-center row wrap>
            <v-flex xs12 class="text-xs-left class-list__container">
              <h3 class="class-list__title">{{title}}</h3>
                <div class="class-list__centered">
                    <template v-for="(item, index) in classesListPrepared">
                      <class-list-item
                        v-if="item"
                        v-bind="item"
                        :key="item.key"
                      >
                      </class-list-item>
                      <div v-else class="empty-class-item"></div>
                    </template>
                </div>
            </v-flex>
        </v-layout>
    </v-flex>
  </v-layout>
</template>

<script>
import _ from 'lodash'
import utils from '@/lib/utils.js'
import axios from 'axios'
import metadata from '@/mixins/metadata'
import ClassListItem from '@/components/Classes/ClassListItem'
import classHelper from '@/lib/helpers/Class'

const titles = {
    group: 'Group Events',
    private: 'Private Sessions',
    all: 'All Classes',
}

export default {
    mixins: [metadata],
    props: [

    ],
    components: {
        ClassListItem,
    },
    data: () => ({
        isLoading: false,
        title: 'list of classes',
        items: [],
    }),

    created: function () {
        const class_type = this.$route.params.class_type
        const teacher_id = this.$route.params.teacher_id
        this.title = titles[class_type]
        Promise.all([
            axios.get(`/api/teacher_profile/${teacher_id}/`),
            axios.get(`/api/teacher/${teacher_id}/classes/`),
        ]).then(([{data: teacher}, {data: classes}]) => {
            this.$store.dispatch('syncLogoCompanyProfile', teacher.user.company_profile ? teacher.user.company_profile.id : null)
            this.items = classes
        });
    },

    computed: {
        classesListPrepared() {
            const dateLimit = 5
            const today = new Date()
            let resItems = []
            _.each(_.sortBy(_.filter(this.items, v => {
                if(classHelper.checkExpired(v) || v.is_deactivated)
                    return false
                if(this.$route.params.class_type === 'group' && v.is_private)
                    return false
                if(this.$route.params.class_type === 'private' && !v.is_private)
                    return false
                return true

            }), v => -v.id), (v) => {
                    let res = {
                        id: v.id,
                        key: v.id,
                        title: v.is_private ? v.name+' with '+v.teacher.first_name : v.name,
                        isMasterClass: v.is_master,
                        isEditorPick: false,
                        isPrivate: v.is_private ? true : false,
                        freqDates: '',
                        location: '',
                        teacher: `${v.teacher.first_name} ${v.teacher.last_name}`,
                        price: '',
                        from: '',
                        to: '',
                        avatar: v.master_media || v.teacher.media,
                        description: v.groupClassSummary ? v.groupClassSummary : '',
                        can_enroll: v.day_select_type === 'monthly'
                            && v.schedule_dates
                            && v.schedule_dates.length
                            && _.some(_.map(v.schedule_dates, sd => utils.stringToDate(sd.date) > today))
                            || v.day_select_type === 'weekly'
                            && (!v.until_date || utils.stringToDate(v.until_date) > today)
                    }
                    if (v.class_type === "address") {
                        res.location = `${v.address} ${v.address_street}, ${v.address_zip}`
                    } else if (v.class_type === "online") {
                        res.location = 'online'
                    } else if (v.class_type === 'student_location') {
                        res.location = 'your location'
                    }
                    if (v.is_private) {
                        res.price = utils.formatPrice(v.rate, v.currency)+' /hour'
                    } else {
                        if (v.flexible_dates)
                            res.price = utils.formatPrice(v.drop_in_rate, v.currency)
                        else {
                            let startDate = utils.stringToDate(v.start_date)
                            let untilDate = v.until_date ? utils.stringToDate(v.until_date) : null
                            if (v.standard_packages.length) {
                                res.price = utils.formatPrice(v.standard_packages[0].totalPrice, v.currency)+' workshop'
                            } else if (v.custom_packages.length) {
                                res.price = utils.formatPrice(v.custom_packages[0].totalPrice, v.currency)+' workshop'
                            }

                        }
                    }
                    //calc actual dates
                    let dates = []
                    let counter = 0
                    let month = new Date().getMonth()
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
                    if (v.day_select_type === 'weekly' && v.weekdays_schedule && v.weekdays_schedule.length) {
                        for (let now = new Date(); counter<dateLimit; now.setDate(now.getDate() + 1)) {
                            if (_.find(v.weekdays_schedule, {weekday: now.getDay()})
                            && (!v.schedule_excluded || !v.schedule_excluded.length || v.schedule_excluded.indexOf(utils.dateToString(now)) == -1)) {
                                dates.push(!counter || now.getMonth() !== month ? `${monthDict[now.getMonth()]} ${now.getDate()}` : now.getDate())
                                month = now.getMonth()
                                counter++
                            }
                        }
                    } else if (v.day_select_type === 'monthly' && v.schedule_dates && v.schedule_dates.length) {
                        _.each(v.schedule_dates, (d) => {
                            if (counter >= dateLimit)
                                return
                            let now = utils.stringToDate(d.date)
                            if(now.getTime()+86399000 > new Date().getTime()
                            && (!v.schedule_excluded || !v.schedule_excluded.length || v.schedule_excluded.indexOf(d.date) == -1)) {
                                //dates.push(utils.stringToDate(d))
                                dates.push(!counter || now.getMonth() !== month ? `${monthDict[now.getMonth()]} ${now.getDate()}` : now.getDate())
                                month = now.getMonth()
                                counter++
                            }
                        })
                    }
                    res.freqDates = dates.join(', ')
                    resItems.push(res)

            })
            const minLen = 4
            if(resItems.length < minLen) {
                resItems = [...resItems, ...new Array(minLen-resItems.length)]
            }
            return resItems
        },
    },

    methods: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.small-chip {
    font-size: 12px;
    height: 20px;

}
.class-list {
    &__container {
        display: flex;
        flex-flow: row wrap;
        justify-content: center;
    }
    &__title {
        padding-left: 20px;
        flex: 1 0 100%;
    }
    &__centered {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, max-content));
        grid-gap: 16px;
        justify-content: center;
        padding: 0 0 20px 0;
    }
}
.empty-class-item {
    width: 300px;
}
</style>