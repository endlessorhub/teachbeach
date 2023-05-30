import _ from 'lodash'
import moment from 'moment'

const currencies = [
    {id: 'usd', label: 'US Dollar', logo: '$'},
    {id: 'mxn', label: 'Mexican Peso', logo: 'Mex$'},
]
const currencyDict = _.keyBy(currencies, 'id')

const weekdays = {
    short: [],
    long: [],
}
let tmpDate = new Date()
for (let i=1;i<=7;i++) {
    tmpDate.setDate(i)
    weekdays.long[tmpDate.getDay()] = tmpDate.toLocaleString('en-us', {  weekday: 'long' })
    weekdays.short[tmpDate.getDay()] = tmpDate.toLocaleString('en-us', {  weekday: 'short' })
}

export default {

    getWeekday(weekdayNum, type = 'short') {
        return weekdays[type] ? weekdays[type][weekdayNum] : undefined
    },

    getCurrencyList() {
        return currencies
    },

    getCurrencyLogo(id) {
        return currencyDict[id] ? currencyDict[id].logo : '$'
    },
    time24HtoAMPM(time) {
        if (!time)
            return ''
        const hhmm = time.split(':')
        let ampm = Number(hhmm[0]) < 12 || Number(hhmm[0]) == 24 ? 'am' : 'pm'
        const h = hhmm[0]%12 || 12
        return h+':'+hhmm[1]+' '+ampm
    },
    timeAMPMto24H(time) {
        if (!time)
            return ''
        const parsed = time.match(/(\d{1,2})\:(\d{2}).?(pm|am)/i)
        if(parsed[2] == '00' && parsed[3].toLowerCase() == 'am' && parsed[1] == '12') {
            return '24:00'
        }
        let add = parsed[3].toLowerCase() == 'am' || parsed[1] == '12' ? 0 : 12
        let hour = add+Number(parsed[1])
        hour = hour < 10 ? '0'+String(hour) : String(hour)

        return hour+':'+parsed[2]
    },
    daysInMonth(y, m) {
        return 32 - new Date(y, m, 32).getDate()
    },
    dateToString(date) {
        return date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
    },
    stringToDate(str) {
        const parts = str.split('-')
        return new Date(parts[0], parts[1]-1, parts[2])
    },
    getDatesForPeriod(periodStart, periodEnd, weekdaysScheduled, startDateStr, untilDateStr) {
        const dayCount = Math.round((this.stringToDate(periodEnd)-this.stringToDate(periodStart))/86400000)+1
        const weekdayDict = _.keyBy(weekdaysScheduled, v => v.weekday)
        const untilDate = untilDateStr ? new Date(untilDateStr.split('-')[0], untilDateStr.split('-')[1]-1, untilDateStr.split('-')[2]) : null
        const startDate = startDateStr ? new Date(startDateStr.split('-')[0], startDateStr.split('-')[1]-1, startDateStr.split('-')[2]) : null
        let res = []
        let date = this.stringToDate(periodStart)
        for (let d=0; d<dayCount; d++) {
            const str = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
            if (weekdayDict[date.getDay()] && (!untilDate || untilDate >= date) && (startDate && startDate <= date)) {
                res.push(str)
            }
            date.setDate(date.getDate()+1)
        }
        return res
    },
    getDatesForMonth(y, m, weekdaysScheduled, startDateStr, untilDateStr) {
        const dayCount = this.daysInMonth(y, m)
        const weekdayDict = _.keyBy(weekdaysScheduled, v => v.weekday)
        const untilDate = untilDateStr ? new Date(untilDateStr.split('-')[0], untilDateStr.split('-')[1]-1, untilDateStr.split('-')[2]) : null
        const startDate = startDateStr ? new Date(startDateStr.split('-')[0], startDateStr.split('-')[1]-1, startDateStr.split('-')[2]) : null
        let res = []
        for (let d=1; d<=dayCount; d++) {
            const date = new Date(y, m, d)
            const str = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2)
            if (weekdayDict[date.getDay()] && (!untilDate || untilDate >= date) && (startDate && startDate <= date)) {
                res.push(str)
            }
        }
        return res
    },
    getCalendarDatesForMonth(y, m, weekdaysScheduled, startDateStr, untilDateStr, scheduleDatesExcluded) {
        const excludedDict = scheduleDatesExcluded && scheduleDatesExcluded.length ? _.keyBy(scheduleDatesExcluded, v => v) : {}
        return _.filter(this.getDatesForMonth(y, m, weekdaysScheduled, startDateStr, untilDateStr), v => !excludedDict[v])
    },
    getCalendarDatesForPeriod(periodStart, periodEnd, weekdaysScheduled, startDateStr, untilDateStr, scheduleDatesExcluded) {
        const excludedDict = scheduleDatesExcluded && scheduleDatesExcluded.length ? _.keyBy(scheduleDatesExcluded, v => v) : {}
        return _.filter(this.getDatesForPeriod(periodStart, periodEnd, weekdaysScheduled, startDateStr, untilDateStr), v => !excludedDict[v])
    },
    checkSequence(allValsSorted, checkVals) {
        const indexDict = _.reduce(allValsSorted, (res, val, index) => {
            res[val] = index
            return res
        }, {})
        const sortedValIndexes = _.map(checkVals, v => indexDict[v]).sort()
        for (let i=0; i<sortedValIndexes.length-1;i++) {
            if(sortedValIndexes[i+1] - sortedValIndexes[i] != 1) {
                return false
            }
        }
        return true
    },
    formatTextToHtml(text) {
        return text ? _.map(text.split(/[\n\r]/), substr => {
            return substr ? `<p style="text-indent: 1em;">${substr}</p>` : ' '
        }).join('') : ''
    },
    formatPrice(val, currency_id) {
        if(!Number(val))
            return 'Free'
        return this.getCurrencyLogo(currency_id || 'usd')+String(Math.round(val ? val : 0))
    },
    formatDatesSchedule(arr, isShort = false) {
        const groups = _.groupBy(_.sortBy(arr, 'date'), v => this.stringToDate(v.date).getDay()+'|'+v.start+'|'+v.end)
        return _.map(Object.keys(groups), (k) => {
            const v = groups[k]
            const vals = k.split('|')
            if(v.length === 1) {
                return {
                    dateStr: this.stringToDate(v[0].date).toLocaleString('en-us', {weekday: 'long'})+' '
                        +this.time24HtoAMPM(v[0].start)+' to '+this.time24HtoAMPM(v[0].end)+', '
                        +this.stringToDate(v[0].date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'}),
                    items: v
                }
            }
            return {
                dateStr: 'selected ' + this.stringToDate(v[0].date).toLocaleString('en-us', {weekday: 'long'})+'s, '
                    +this.time24HtoAMPM(v[0].start)+' to '+this.time24HtoAMPM(v[0].end)+', '
                    +'from '+this.stringToDate(v[0].date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})+' to '
                    +`${this.stringToDate(v[v.length-1].date).toLocaleString('en-us', {month: 'long', day: 'numeric', year: 'numeric'})}.`
                    +(isShort ? '' : ` ${v.length} classes`),
                items: v,
            }

        })
    },
    disabledHoursFromTime(timestr, isBefore) {
        let res = []
        let x = timestr.split(':')[0]-0
        let start = isBefore ? 0 : 23
        while (x != start) {
            res.push(start)
            isBefore ? start++ : start--
        }
        return () => res
    },
    disabledMinutesFromTime(timestr, isBefore) {
        let disabledHours = this.disabledHoursFromTime(timestr, isBefore)()
        let allMinutes = _.map(Array(60), (v, i) => i)
        return (hour) => {
            if(disabledHours.indexOf(hour) != -1)
                return allMinutes
            if(hour != timestr.split(':')[0]-0) {
                return []
            }
            let res = []
            let x = timestr.split(':')[1]-0
            let start = isBefore ? 0 : 59
            while (x != start) {
                res.push(start)
                isBefore ? start++ : start--
            }
            return res
        }
    },
    prepareUrl(url) {
        url = url.trim()
        if(!/^http(s?):\/\//.test(url)) {
            url = `http://${url}`
        }
        return url
    },
    formatMinutes(minutes) {
        const hours = Math.floor(minutes/60)
        const restMins = minutes % 60
        const res = []
        if(hours)
            res.push(`${hours} hour${hours > 1 ? 's' : ''}`)
        if(restMins)
            res.push(`${restMins} minutes`)
        return res.join(', ')
    },
    isTimeInFuture(timestr, timezone) {
        return (timezone ? moment.tz(timestr, timezone) : moment(timestr)).diff(new Date()) > 0
    },
    getAvailableTimesForPeriod(startTime, endTime, classData) {
        const available = []
        let dateStart = moment(startTime).add(-1, 'd')
        let dateEnd = moment(endTime).add(1, 'd')
        for (let curTime = moment(dateStart).tz(classData.timezone); curTime.diff(dateEnd) <= 0; curTime.add(1, 'd')) {
            const weekday = curTime.day()
            if(classData.schedule_excluded && classData.schedule_excluded.find(v => v === curTime.format('YYYY-MM-DD')))
                continue
            const daySchedule = classData.weekdays_schedule.find(v => v.weekday === weekday);
            if(daySchedule) {
                const start = moment.tz(`${curTime.format('YYYY-MM-DD')} ${daySchedule.start}`, classData.timezone);
                const end = moment.tz(`${curTime.format('YYYY-MM-DD')} ${daySchedule.end}`, classData.timezone);
                if(start.diff(endTime) < 0 && end.diff(startTime) > 0)
                    available.push({
                        date: curTime.format('YYYY-MM-DD'),
                        weekday,
                        start: (dateStart.diff(start) > 0 ? dateStart : start).format('HH:mm'),
                        end: (dateEnd.diff(end) < 0 ? dateEnd : end).format('HH:mm'),
                    });
            }
        }
        return available
    },
    useMemberPrice:(mode, v) => (mode === 'isMember' && (v.memberTotalPrice === '0' || Number(v.memberTotalPrice) || v.memberPricePerInterval === 0 || v.memberPricePerInterval === '0' || Number(v.memberPricePerInterval))),
}