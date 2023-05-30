import moment from 'moment'
import fbmap from '@/lib/fbmap.js'
import utils from '@/lib/utils.js'
import _ from 'lodash'
import humanizeDuration from 'humanize-duration'

const res = {
    subscriptionLengths: {
        'quarter': 'quarterly',
        'half_year': 'for six months',
        'year': 'annually',
    },
    subscriptionLengthMap: {
        'quarter': {
            'week|1': 13,
            'month|1': 3,
        },
        'half_year': {
            'week|1': 26,
            'month|1': 6,
        },
        'year': {
            'week|1': 52,
            'month|1': 12,
        },
    },
    subscriptionLengthReverseMap: null,
    processReverse() {
        this.subscriptionLengthReverseMap = {}
        _.each(this.subscriptionLengthMap, (periods, name) => {
            _.each(periods, (num, period) => {
                if(!this.subscriptionLengthReverseMap[num])
                    this.subscriptionLengthReverseMap[num] = {}
                this.subscriptionLengthReverseMap[num][period] = name
            })
        })
    },
    subscriptionLengthsList() {
        return _.sortBy(_.map(this.subscriptionLengths, (v, k) => ({
            value: k,
            text: v,
        })), v => this.subscriptionLengthMap[v.value]['week|1'])
    },
    normalize(classData) {
        return 'address_city' in  classData ? classData : fbmap.fb(classData)
    },
    getSubscriptionLengthName(p) {
        if(!p.numberOfIntervals || !p.period) {
            return '-invalid_package-'
        }
        if(!this.subscriptionLengthReverseMap) {
            this.processReverse()
        }
        if(!this.subscriptionLengthReverseMap[p.numberOfIntervals])
            return '-'
        return this.subscriptionLengths[this.subscriptionLengthReverseMap[p.numberOfIntervals][p.period]]
    },
    // mode = regular, isMember, addMembership
    packageFormatter(p, mode = 'regular') {
        let additional = ''
        if (mode === 'addMembership' && p.memberTotalPrice) {
            additional = `, Member rate ${utils.formatPrice(p.memberTotalPrice, p.currency || 'usd')}`
        }
        if (p.type === 'limitedSubscription') {
            `${utils.formatPrice(p.pricePerInterval, p.currency || 'usd')} ${p.interval}ly ${p.numberOfIntervals} time${p.numberOfIntervals > 1 ? 's' : ''}`
        }
        if(!p.isPrivate) {
            if (mode === 'isMember' && (p.memberTotalPrice || p.memberTotalPrice === '0' || p.memberTotalPrice === 0)) {
                return `Member Rate: ${utils.formatPrice(p.memberTotalPrice, p.currency || 'usd')} ${Number(p.memberTotalPrice) ? 'for' : ''}  ${p.numberOfLessons} ${p.isTrial ? 'trial' : ''} lesson${p.numberOfLessons == 1 ? '' : 's'}`
            }
            return `${utils.formatPrice(p.totalPrice, p.currency || 'usd')} ${Number(p.totalPrice) ? 'for' : ''}  ${p.numberOfLessons} ${p.isTrial ? 'trial' : ''} lesson${p.numberOfLessons == 1 ? '' : 's'}${additional}`
        }
        if(p.isSubscription) {
            if (mode === 'isMember' && (p.memberTotalPrice || p.memberTotalPrice === '0' || p.memberTotalPrice === 0)) {
                return `${utils.formatPrice(p.memberTotalPrice, p.currency || 'usd')} ${this.packagePeriodName(p.period)}, for ${p.classesPerInterval} class${p.classesPerInterval > 1 ? 'es' : ''} per ${this.packagePeriodNameSingle(p.period)} ${this.getSubscriptionLengthName(p)} subscription`
            }
            return `${utils.formatPrice(p.rateBilled, p.currency || 'usd')} ${this.packagePeriodName(p.period)}, for ${p.classesPerInterval} class${p.classesPerInterval > 1 ? 'es' : ''} per ${this.packagePeriodNameSingle(p.period)} ${this.getSubscriptionLengthName(p)} subscription${additional}`
            //return `Subscription ${p.classesPerYear} lessons per year for ${utils.formatPrice(p.rateBilled, classData.currency || 'usd')} ${this.packagePeriodName(p.period)}`
        }
        //const now = moment()
        //const TimeHumanReadable = moment().add(p.lessonLength.value * p.numberOfLessons, 'm').to(now, true)
        const TimeHumanReadable = this.humanizeDurationMinutes(p.lessonLength.value * p.numberOfLessons)
        if(!Number(p.totalPrice)) {
            return `${p.numberOfLessons} free${p.isTrial ? ' trial ' : ' '}lesson${p.numberOfLessons > 1 ? 's' : ''}, ${TimeHumanReadable}`
        }
        if (mode === 'isMember' && (p.memberTotalPrice || p.memberTotalPrice === '0' || p.memberTotalPrice === 0)) {
            return `${utils.formatPrice(p.memberTotalPrice, p.currency || 'usd')} ${Number(p.memberTotalPrice) ? 'for' : ''} ${p.numberOfLessons} ${p.isTrial ? 'trial' : ''} time${p.numberOfLessons == 1 ? '' : 's'}, ${TimeHumanReadable} total`
        }
        return `${utils.formatPrice(p.totalPrice, p.currency || 'usd')} ${Number(p.totalPrice) ? 'for' : ''} ${p.numberOfLessons} ${p.isTrial ? 'trial' : ''} time${p.numberOfLessons == 1 ? '' : 's'}, ${TimeHumanReadable} total${additional}`
    },
    price(classData, detailed = false) {
        classData = this.normalize(classData)
        if (classData.is_price_hidden) {
            return ''
        }
        if(classData.is_private) {
            const packages = _.filter(classData.custom_packages, 'isPrivate')
            if (Number(classData.rate)) {
                packages.push({
                    numberOfLessons: 1,
                    totalPrice: Number(classData.rate),
                    lessonLength: {value: 60, text: 'one hour'},
                    perLesson: Number(classData.rate),
                    isDropIn: true,
                })
            }
            const minimalPackage = _.minBy(packages, p => (p.isSubscription ? Number(p.rateBilled) : Number(p.totalPrice)))
            if(!minimalPackage)
                return '-'

            const formatter = (p) => this.packageFormatter(p)

            return detailed ? _.map(packages, formatter) : formatter(minimalPackage)

            //return this.currencyLogo+Number(this.rate || this.drop_in_rate || 0).toFixed(2)
        } else {
            let packages = []
            const formatter = p => this.packageFormatter(p)
            if (classData.flexible_dates) {
                packages = _.uniqBy(classData.standard_packages, v => `${v.numberOfLessons}-${v.perLesson}-${v.totalPrice}`)
            } else {
                packages = _.filter(classData.custom_packages, p => !p.isPrivate)
            }
            if (Number(classData.drop_in_rate)) {
                packages.push({
                    numberOfLessons: 1,
                    totalPrice: Number(classData.drop_in_rate),
                    lessonLength: {value: 60, text: 'one hour'},
                    perLesson: Number(classData.drop_in_rate),
                    isDropIn: true,
                })
            }
            packages = _.sortBy(packages, v => Number(v.totalPrice))
            if (detailed) {
                return _.map(packages, formatter)
            }
            const firstPackage = _.first(packages)

            return firstPackage ? formatter(firstPackage) : '-'
        }
    },
    sortByPriceValue(classData) {
        let res = []
        classData = this.normalize(classData)
        if(classData.is_private) {
            if (Number(classData.rate)) {
                res.push(Number(classData.rate))
            }
            _.each(classData.custom_packages, v => {
                if(v.isPrivate)
                    res.push(Number(v.totalPrice))
            })
        } else {
            if(Number(classData.drop_in_rate)) {
                res.push(Number(classData.drop_in_rate))
            }
            if (classData.flexible_dates) {
                _.each(_.uniqBy(classData.standard_packages, v => `${v.numberOfLessons}-${v.perLesson}-${v.totalPrice}`), v => {
                    res.push(Number(v.totalPrice))
                })
            } else {
                _.each(classData.custom_packages, v => {
                    if(!v.isPrivate)
                        res.push(Number(v.totalPrice))
                })
            }
        }
        return _.min(res)
    },
    canEnroll(classData) {
        const today = moment()
        classData = this.normalize(classData)
        if(classData.day_select_type !== 'weekly' && (!classData.schedule_dates || !classData.schedule_dates.length))
            return false
        const isStarted = classData.day_select_type === 'weekly' ?
            today.diff(moment(classData.start_date, 'YYYY-MM-DD')) > 0 :
            today.diff(moment(_.sortBy(classData.schedule_dates, 'date')[0].date, 'YYYY-MM-DD')) > 0
        // workshop has already begun
        if (!classData.is_private && isStarted && !classData.flexible_dates && !classData.drop_in_rate)
            return false
        // workshop reached max students limit
        if (!classData.is_private
            && !classData.flexible_dates
            && classData.maxSize) {
            const peopleBought = classData.orders
                .filter(o => !o.data.package.isDropIn && o.data.package.numberOfLessons > 1)
                .reduce((acc, o) => acc+Number(o.data.persons), 0)
            if(peopleBought >= classData.maxSize) {
                return false
            }
        }
        /*
        just skip for now, implement complex check using dates
        if (classData.maxSize && classData.enrolled.length >= classData.maxSize) {
            return false
        }
        */
        if (classData.is_deactivated) {
            return false
        }
        return true
    },
    personsText(customPackage) {
        if (customPackage.minPersons === customPackage.maxPersons) {
            return `${customPackage.minPersons} person${customPackage.minPersons === 1 ? '' : 's'}`
        } else {
            return `from ${customPackage.minPersons} up to ${customPackage.maxPersons} persons`
        }
    },
    humanizeDurationMinutes(minutes) {
        return humanizeDuration(minutes * 60 * 1000, { units: ['h', 'm'] })
    },
    location(classData) {
        if(classData.class_type === 'student_location') {
            return 'Student’s location'
        }
        if(classData.class_type === 'online') {
            return 'Online'
        }
        if(classData.class_type === 'other') {
            return 'TBA'
        }
        if(classData.class_type === 'custom') {
            return 'We’ll work it out'
        }
        return classData.address+' '+classData.address_street+', '+classData.address_city+' '+classData.address_zip
    },
    priceDescription(classData) {
        classData = this.normalize(classData)
        if (classData.is_price_hidden) {
            return ''
        }
        if(classData.is_private) {
            const packages = _.filter(classData.custom_packages, 'isPrivate')
            if (Number(classData.rate)) {
                packages.push({
                    numberOfLessons: 1,
                    totalPrice: Number(classData.rate),
                    lessonLength: {value: 60, text: 'one hour'},
                    perLesson: Number(classData.rate),
                    memberPerLesson: 0,
                    memberTotalPrice: 0,
                    isDropIn: true,
                })
            }
            const minimalPackage = _.minBy(packages, p => (p.isSubscription ? Number(p.rateBilled) : Number(p.totalPrice)))
            if(minimalPackage.isSubscription) {
                return {
                    text: this.packageFormatter(minimalPackage),
                    memberPrice: minimalPackage.memberTotalPrice || minimalPackage.memberTotalPrice === 0 ? utils.formatPrice(minimalPackage.memberTotalPrice, classData.currency || 'usd') : null,
                }
            }
            const TimeHumanReadable = this.humanizeDurationMinutes(minimalPackage.lessonLength.value * minimalPackage.numberOfLessons)
            let description = ''
            if(minimalPackage.isDropIn)
                description = ', (Drop in)'
            if(minimalPackage.isTrial)
                description = ', (Trial)'
            if(minimalPackage.description)
                description = `, ${minimalPackage.description}`
            if(!Number(minimalPackage.totalPrice)) {
                return {
                    text: `${minimalPackage.numberOfLessons} free${minimalPackage.isTrial ? ' trial ' : ' '}lesson${minimalPackage.numberOfLessons > 1 ? 's' : ''}, ${TimeHumanReadable}`,
                    memberPrice: minimalPackage.memberTotalPrice || minimalPackage.memberTotalPrice === 0 ? utils.formatPrice(minimalPackage.memberTotalPrice, classData.currency || 'usd') : null,
                }
            }
            return {
                text: `${packages.length > 1 ? 'From ' : ''}${utils.formatPrice(minimalPackage.totalPrice, classData.currency)} ${Number(minimalPackage.totalPrice) ? 'for' : ''} ${TimeHumanReadable}, ${minimalPackage.numberOfLessons} time${minimalPackage.numberOfLessons > 1 ? 's' : ''}${description}`,
                memberPrice: minimalPackage.memberTotalPrice ? utils.formatPrice(minimalPackage.memberTotalPrice, classData.currency || 'usd') : null,
            }
        } else {
            if (classData.is_premium_community) {
                return classData.custom_packages.filter(p => p.type === 'limitedSubscription').map(p => ({
                    text: `${utils.formatPrice(p.pricePerInterval, classData.currency || 'usd')} ${p.interval}ly ${p.numberOfIntervals} time${p.numberOfIntervals > 1 ? 's' : ''}`,
                    memberPrice: '',
                }))
            }
            let packages = []
            const formatter = p => `${utils.formatPrice(p.totalPrice, classData.currency || 'usd')} ${Number(p.totalPrice) ? 'for' : ''}  ${p.numberOfLessons} ${p.isTrial ? 'trial' : ''} lesson${p.numberOfLessons == 1 ? '' : 's'}`
            if (classData.flexible_dates) {
                packages = _.uniqBy(classData.standard_packages, v => `${v.numberOfLessons}-${v.perLesson}-${v.totalPrice}`)
            } else {
                packages = _.filter(classData.custom_packages, p => !p.isPrivate)
            }
            packages = _.sortBy(packages, v => Number(v.totalPrice))
            return _.map(packages, (p) => ({
                text: formatter(p),
                memberPrice: p.memberTotalPrice ? utils.formatPrice(p.memberTotalPrice, classData.currency || 'usd') : null,
            }))
        }

    },
    previewImageSrc(src) {
        if(!src)
            return null
        const reg = /(\.[^\.]+)$/
        // png used on backend
        return reg.test(src) ? src.replace(/(\.[^\.]+)$/, '.thumbnail300$1') : `${src}.thumbnail300.png`
    },
    isPreviewImageSrc(src) {
        return /\.thumbnail300/.test(src)
    },
    classPackages(classData) {
        if(classData.is_private) {
            const packages = _.filter(classData.custom_packages, 'isPrivate')
            if (Number(classData.rate)) {
                packages.push({
                    numberOfLessons: 1,
                    totalPrice: Number(classData.rate),
                    lessonLength: {value: 60, text: 'one hour'},
                    perLesson: Number(classData.rate),
                    isDropIn: true,
                    memberPerLesson: 0,
                    memberTotalPrice: 0,
                    description: `Drop in for ${utils.formatPrice(classData.rate, classData.currency)} (one hour)`,
                })
            }
            return packages
        } else {
            let packages = []
            if (classData.flexible_dates) {
                if (classData.is_premium_community) {
                    packages = classData.custom_packages.filter(p => p.type === 'limitedSubscription')
                } else {
                    packages = _.uniqBy(classData.standard_packages, v => `${v.numberOfLessons}-${v.perLesson}-${v.totalPrice}`)
                }
            } else {
                packages = _.filter(classData.custom_packages, p => !p.isPrivate)
            }
            if (Number(classData.drop_in_rate)) {
                packages.push({
                    numberOfLessons: 1,
                    totalPrice: Number(classData.drop_in_rate),
                    lessonLength: {value: 60, text: 'one hour'},
                    perLesson: Number(classData.drop_in_rate),
                    memberPerLesson: 0,
                    memberTotalPrice: 0,
                    isDropIn: true,
                    description: `Drop in for ${utils.formatPrice(classData.drop_in_rate, classData.currency)} (one hour)`,
                })
            }
            return packages
        }
    },
    packagePeriodName(id) {
        const periodDict = {
            'week|1': 'weekly',
            'month|1': 'monthly',
            'week|2': 'every other week',
        }
        return periodDict[id]
    },
    packagePeriodNameSingle(id) {
        const periodDict = {
            'week|1': 'week',
            'month|1': 'month',
            'week|2': 'every other week',
        }
        return periodDict[id]
    },
    title(classData) {
        return `${classData.is_private ? classData.private_className : classData.name}`
    },
    getAvailableSchedule(classData, limit = 100, duration = 60) {
        let start = new Date()
        if(classData.day_select_type === 'weekly') {
            const excludedDict = (classData.schedule_excluded || []).reduce((acc, c) => ({...acc, [c]: true}), {})
            start = Math.max(start, moment(classData.start_date).toDate())
            let current = new Date(start)
            const end = classData.until_date ? moment(classData.until_date).toDate() : null
            const res = {}
            while((!end || current < end) && Object.keys(res).length < limit) {
                for (let weekday of classData.weekdays_schedule) {
                    current.setDate(current.getDate()-(current.getDay()-weekday.weekday))
                    const key = moment(current).format('YYYY-MM-DD')
                    if(excludedDict[key] || (end && current > end) || start > current)
                        continue
                    if(!res[key]) {
                        res[key] = this.getTimeslotsForDate(classData, key, duration)
                    }
                    //res[key].push({date: key, ...weekday})
                }
                current.setDate(current.getDate()+7)
            }
            return res
        } else {
            return classData.schedule_dates.filter(d => moment(`${d.date} ${d.start}`).toDate() > start).reduce((acc, d) => {
                if(!acc[d.date]) {
                    acc[d.date] = this.getTimeslotsForDate(classData, d.date, duration)
                }
                return acc
            }, {})
        }
    },
    getAllTimeSlots(date, duration) {
        const res = []
        let endTime = moment('23:30', 'HH:mm').add(30, 'm').subtract(duration, 'm')
        for (let curTime = moment('06:00', 'HH:mm'); endTime.diff(curTime) >= 0; curTime.add(duration, 'm')) {
            const end = moment(curTime).add(duration, 'm')
            res.push({
                date,
                start: curTime.format('HH:mm'),
                end: end.format('HH:mm'),
                isAvailable: true,
            })
        }
        return res
    },
    getTimeslotsForDate(classData, date, duration) {
        if(classData.is_private) {
            const res = []
            const dateObj = moment(date).toDate()
            let day = classData.weekdays_schedule.find(v => v.weekday === dateObj.getDay())
            let endTime = moment(day.end, 'HH:mm').subtract(this.duration, 'm')
            for (let curTime = moment(day.start, 'HH:mm'); endTime.diff(curTime) >= 0; curTime.add(duration, 'm')) {
                const end = moment(curTime).add(duration, 'm')
                const isAvailable = !classData.enrolled.filter(v => v.date === date && v.status === "approved").some((v, k) => {
                    const timeTo = moment(v.time_to, 'HH:mm')
                    const timeFrom = moment(v.time_from, 'HH:mm')
                    return (curTime < timeTo && end >= timeTo || end > timeFrom && curTime <= timeFrom || curTime >= timeFrom && end <= timeTo)
                })
                res.push({
                    date,
                    start: curTime.format('HH:mm'),
                    end: end.format('HH:mm'),
                    isAvailable,
                })
            }
            return res
        } else {
            const dateItem = classData.schedule_dates.find(v => v.date === date)
            let isAvailable = true
            if(classData.maxSize
                && classData.enrolled.filter(v => (v.date === date && v.status === "approved")).length >= classData.maxSize) {
                isAvailable = false
            }
            return [{...dateItem, isAvailable}]
        }
    },
    /**
     * split orders to lists: current, past
     * @param {array}   orders                      array of orders
     * @param {object}  orders.class                object representing class of order
     * @param {array}   orders.class.enrolled       array representing enrollments of class
     *
     * @return object {current: Array, past: Array}
     */
    groupOrdersByStatus(orders) {
        return orders.reduce((acc, o) => {
            if(o.is_subscription && new Date(this.current_period_end*1000) < new Date() && new Date(this.current_period_start*1000) > new Date()) {
                acc.current.push(o)
            } else if (!o.is_subscription) {
                if(o.class.day_select_type === 'monthly') {
                    // monthly
                    if(!o.class.schedule_dates.some(d => moment(`${d.date} ${d.start}`).diff(new Date()) > 0)) {
                        acc.past.push(o)
                    } else if (o.reserved_lessons < o.num_lessons) {
                        acc.current.push(o)
                    } else if(o.class.enrolled.some(en => (en.order_id === o.id && moment(`${en.date} ${en.time_from}`).diff(new Date()) > 0))) {
                        // checked if one of enrollments is in the future
                        acc.current.push(o)
                    } else {
                        acc.past.push(o)
                    }
                } else {
                    // weekly
                    if(o.class.until_date && moment(o.class.until_date).diff(new Date()) < 0) {
                        acc.past.push(o)
                    } else if (o.reserved_lessons < o.num_lessons) {
                        acc.current.push(o)
                    } else if(o.class.enrolled.some(en => (en.order_id === o.id && moment(`${en.date} ${en.time_from}`).diff(new Date()) > 0))) {
                        // checked if one of enrollments is in the future
                        acc.current.push(o)
                    } else {
                        acc.past.push(o)
                    }
                }
            } else {
                acc.past.push(o)
            }
            return acc
        }, {
            current: [],
            past: [],
        })
    },
    /**
     *
     * @param {object} cl       class object
     * @param {Date} start      start date
     * @param {Date} end        end date
     *
     * @return object {current: Array, past: Array}
     */
    getWeeklyClassDates(cl, start, end) {
        if(!start) {
            start = moment(cl.start_date).toDate()
        }
        if(!end) {
            // 60 days from today
            end = cl.until_date ? moment(cl.until_date).toDate() : moment(Date.now()+3600*24*60*1000).toDate()
        }
        let days = moment(end).diff(start, 'days')
        const res = []
        const excluded = (cl.schedule_excluded || []).reduce((acc, d) => ({...acc, [d]: true}), {})
        const weekdays = cl.weekdays_schedule.reduce((acc, d) => ({...acc, [d.weekday]: true}), {})
        for (let sm = moment(start);sm.diff(end) <= 0;sm.add(1, 'days')) {
            if(weekdays[sm.day()] && !excluded[sm.format('YYYY-MM-DD')]) {
                // good to add
                res.push(sm.format('YYYY-MM-DD'))
            }
        }
        return res
    },
    /**
     *
     * @param {array} classes
     *
     * @return object {current: Array, past: Array}
     */
    groupClassesByAvailability(classes) {
        return classes.filter(c => !c.is_deactivated).reduce((acc, c) => {
            if(c.day_select_type === 'monthly') {
                if(c.schedule_dates.some(d => moment(`${d.date} ${d.start}`).diff(new Date()) > 0))
                    acc.current.push(c)
                else
                    acc.past.push(c)
            } else {
                if(!c.until_date) {
                    // ongoing
                    acc.current.push(c)
                } else if (this.getWeeklyClassDates(c, new Date()).length) {
                    acc.current.push(c)
                } else {
                    acc.past.push(c)
                }
            }
            return acc
        }, {
            current: [],
            past: [],
        })
    },

    checkExpired: classRow => {
        if(classRow.day_select_type === 'monthly') {
            return !_.some(_.map(classRow.schedule_dates, v => utils.isTimeInFuture(`${v.date} ${v.start}:00`, classRow.timezone)))
        } else {
            return classRow.until_date && !utils.isTimeInFuture(`${classRow.until_date} 23:30:00`, classRow.timezone)
        }
    },

    isUpcoming(classRow) {
        if(classRow.day_select_type === 'monthly') {
            return _.every(_.map(classRow.schedule_dates, v => utils.isTimeInFuture(`${v.date} ${v.start}:00`, classRow.timezone)))
        } else {
            const lastDates = this.getWeeklyClassDates(classRow, moment(classRow.start_date).toDate(), new Date());
            return !lastDates.length;
        }
    }
}

res.processReverse()

export default res