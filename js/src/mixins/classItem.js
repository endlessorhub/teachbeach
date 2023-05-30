
import _ from 'lodash'
import classHelper from '@/lib/helpers/Class.js'
import utils from '@/lib/utils.js'
import { mapGetters } from 'vuex'

export default {
    data: () => ({
        contactDialog: false,
        sendMessageFormData: {},
        registerDialog: false,
        initAction: '',
        registrationTitle: '',
    }),
    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
        currentClass() {
            // overload this in component
            throw new Error('mixin computed property currentClass should be overloaded in component');
        },
        regMinFormData() {
            return {
                isPrivate: this.currentClass && this.currentClass.is_private,
                class_id: this.currentClass.id,
                alertText: this.currentClass.is_private ? undefined : "You may receive SMS alerts about teacher's first response and lesson reminders"
            }
        },
        isTrialAvailable() {
            return !!this.trialPackage
        },
        trialPackage() {
            return this.isPrivate ?
                _.find(this.currentClass.custom_packages, v => (v.isTrial && v.isPrivate)) :
                _.find(this.currentClass.flexible_dates ? this.currentClass.standard_packages : this.currentClass.custom_packages, p => (p.isTrial && !p.isPrivate))
        },
        trialPackageRate() {
            return this.trialPackage ? Number(this.trialPackage.totalPrice) : null
        },
        canEnroll() {
            return this.canEnrollByClass(this.currentClass)
        },
        avatarUrl() {
            return this.currentClass.teacher && this.currentClass.teacher.media ? this.currentClass.teacher.media : null
        },
    },
    methods: {
        canEnrollByClass(cl) {
            return (cl.can_book || cl.can_book_url) && classHelper.canEnroll(cl)
        },
        closeDialogs() {
            this.contactDialog = false
            this.registerDialog = false
        },
        openSchedule() {
            if(this.isLoggedIn) {
                //console.log('schedule open')
                this.$router.push(`/learners/new_enroll/${this.currentClass.id}/4/0`)
            } else {
                this.registrationTitle = 'Sign up to see schedule'
                this.initAction = 'schedule'
                this.registerDialog = true
            }
        },
        bookClass() {
            if (this.canEnroll) {
                if(this.isLoggedIn) {
                    if(this.currentClass.can_book) {
                        this.$router.push(`/learners/new_enroll/${this.currentClass.id}/4/0`)
                    } else if (this.currentClass.can_book_url) {
                        window.open(utils.prepareUrl(this.currentClass.can_book_url), '_blank')
                    }
                } else {
                    if(!this.currentClass.is_private) {
                        this.registrationTitle = 'Looks like your new here!'
                    } else
                        this.registrationTitle = 'Please create account'
                    this.initAction = 'book'
                    this.registerDialog = true
                }

            }
        },
        openMessageForm() {
            if(this.isLoggedIn) {
                this.sendMessageFormData = {
                    contact: _.assign({entity: 'teacher'}, this.currentClass.teacher),
                    avatar: this.avatarUrl,
                    additional: {classId: this.currentClass.id},
                    showBookBtn: true,
                    includeAllowOther: false,
                }
                this.contactDialog = true
            } else {
                this.registrationTitle = `Sign up to send ${this.currentClass.teacher.first_name} a message`
                this.initAction = 'message'
                this.registerDialog = true
            }
        },
        registerDone(res) {
            this.registerDialog = false
            switch (this.initAction) {
                case 'schedule':
                    this.openSchedule()
                    break;
                case 'book':
                    this.bookClass()
                    break;
                case 'message':
                    this.openMessageForm()
                    break;
            }
        },
        messageDone(res) {
            /*
            if(res.status) {
                this.contactDialog = false
            }
            */
        },
        closeSendMessage() {
            this.contactDialog = false
            this.sendMessageFormData = {}
        }
    }
}