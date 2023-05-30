import _ from 'lodash'

let _user = {
    first_name: 'first_name',
    last_name: 'last_name',
    phone: 'phone',
    email: 'email',
}

/* not included:
customDuration
*/
let _class = {
    address: 'teachingAddress',
    address_city: 'teachingCity',
    address_country: 'teachingCountry',
    address_google: 'teachingGooglePlace',
    address_state: 'teachingState',
    address_street: 'teachingStreet',
    address_zip: 'teachingZip',
    can_book: 'canBook',
    can_book_url: 'canBookUrl',
    can_pay: 'canPay',
    class_type: 'whereTeach',
    currency: 'currency',
    day_select_type: 'daySelectType',
    drop_in_rate: 'dropInRate',
    enrolled: 'enrolled',
    experience: 'studentExperienceLevel',
    flexible_dates: 'flexibleDates',
    group_description: 'groupClassDescription',
    group_lesson_length: 'lessonLengthGroup',
    group_number_of_lessons: 'numOfLessonsGroup',
    groupClassSummary: 'groupClassSummary',
    id: 'id',
    instant_booking: 'allowStudentsBookInstantly',
    is_master: null,
    is_private: null,
    is_deactivated: 'is_deactivated',
    lat: 'lat',
    lng: 'lng',
    maxSize: 'maxSize',
    name: 'groupClassName',
    private_class_website: 'privateClassWebsite',
    private_className: 'privateClassName',
    private_lesson_length: 'lessonLengthPrivate',
    private_number_of_lessons: 'numOfLessonsPrivate',
    rate: 'lessonPricePerHour',
    schedule_dates: 'scheduleDates',
    schedule_excluded: 'scheduleDatesExcluded',
    schedule_from: 'scheduleFrom',
    schedule_to: 'scheduleTo',
    show_email: 'showEmail',
    show_phone: 'showPhone',
    show_phone_rule: 'showPhoneRule',
    start_date: 'startDate',
    students_bring: 'studentsBring',
    teacher: null,
    teacher_supplies: 'teacherSupply',
    teaching_country: 'teachingCountry',
    teaching_venue: 'teachingVenue',
    until_date: 'untilDate',
    user_category: null,
    user_subcategory: null,
    venue: 'locationVenue',
    weekdays_schedule: 'weekdaysScheduled',
    what_else: 'studentsToKnow',
    standard_packages: 'standardPackages',
    custom_packages: 'customPackages',
    group_package_type: 'groupPackageType',
    is_price_hidden: 'isPriceHidden',
    is_premium_community: 'isPremiumCommunity',
    zoom_link: 'zoomLink',
}

export default {
    bf: {
        common(data, mapDict) {
            let objToSet = {}
            _.each(mapDict, (fk, bk) => {
                if(fk)
                    objToSet[fk] = data[bk]
            })
            return objToSet
        },
        user(data) {
            return this.common(data, _user)
        },
        teachingClass(data) {
            let res = this.common(data, _class)
            if(res.scheduleDatesExcluded && res.scheduleDatesExcluded.length) {
                res.scheduleDatesExcluded = _.groupBy(res.scheduleDatesExcluded, (v) => (v.split('-')[1]-1))
            }
            if(data.class_media && data.class_media.length) {
                res.supportFiles = _.map(data.class_media, cm => ({
                    imageUrl: cm.class_media,
                    isImage: true,
                    id: cm.id,
                }))
            }
            return res
        },
    },
    fb: {
        common(data, mapDict) {
            let objToSet = {}
            _.each(mapDict, (fk, bk) => {
                if(fk && fk in data)
                    objToSet[bk] = data[fk]
            })
            return objToSet
        },
        user(data) {
            return this.common(data, _user)
        },
        teachingClass(data) {
            let res = this.common(data, _class)
            res.class_media = data.supportFiles ? _.map(data.supportFiles, (v) => ({class_media: v.imageUrl, isRaw: true})) : []
            if(res.schedule_excluded && !_.isArray(res.schedule_excluded)) {
                res.schedule_excluded = _.flatten(_.map(res.schedule_excluded, v => v))
            }
            return res
        },
    }
}