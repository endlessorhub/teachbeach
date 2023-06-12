<template>
    <v-layout class="company-profile" align-top justify-left row wrap>
        <snack v-model="msg"></snack>
        <v-flex xs12 class="text-xs-center" >
            <div class="title">Collab Set-Up</div>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Collab name</div>
            <v-text-field
                v-model.trim="name"
                :error-messages="nameErrors"
                :counter="30"
                class="text__collab-design"
                outline
                required
                @input="$v.name.$touch()"
                @blur="$v.name.$touch()"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">First Name</div>
            <v-text-field
                v-model.trim="firstName"
                :error-messages="firstNameErrors"
                :counter="30"
                class="text__collab-design"
                outline
                required
                @input="$v.firstName.$touch()"
                @blur="$v.firstName.$touch()"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Last Name</div>
            <v-text-field
                v-model.trim="lastName"
                :error-messages="lastNameErrors"
                :counter="30"
                class="text__collab-design"
                outline
                required
                @input="$v.lastName.$touch()"
                @blur="$v.lastName.$touch()"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Email Address</div>
            <v-text-field
                v-model.trim="email"
                class="text__collab-design"
                outline
                :error-messages="emailErrors"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Phone</div>
            <v-text-field
                v-model.trim="phone"
                :error-messages="phoneErrors"
                class="text__collab-design"
                outline
                required
                @input="$v.phone.$touch()"
                @blur="$v.phone.$touch()"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Collab page headline</div>
            <v-text-field
                v-model="title"
                class="text__collab-design"
                outline
            ></v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">
                Timezone
            </div>
            <div>
                <TimezoneList 
                    v-model="timezone" 
                    class="text__collab-design"
                    outline
                    label=""
                />
                <div class="timezone-checkbox">
                    <v-checkbox
                      v-model="applyTimezoneToClasses"
                      label="Apply to all classes"
                    ></v-checkbox>
                </div>
            </div>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Subdomain</div>
            <v-text-field
                v-model="slug"
                class="text__collab-design subdomain-field"
                outline
            >
                <template v-slot:label>
                    <a :href="subdomain" target="_blank">{{ subdomain }}</a>
                </template>
            </v-text-field>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Upload Logo</div>
            <ImageUploadCrop
                :imageUrl="imageUrl"
                :imageName="imageName"
                :imageFile="imageFile"
                width="90%"
                :aspectRatio="null"
                :is-url-under="true"
                @change="onFileChanged"
            ></ImageUploadCrop>
            <v-checkbox
                v-model="replaceLogo"
                label="Show this logo in the page header"
            ></v-checkbox>
        </v-flex>
        <v-flex xs12 md6 lg3 class="text-xs-left">
            <div class="field-title">Main image</div>
            <ImageUploadCrop
                :imageUrl="mainImageUrl"
                :imageName="mainImageName"
                :imageFile="mainImageFile"
                width="90%"
                :aspectRatio="1.25"
                :is-url-under="true"
                @change="onMainFileChanged"
            ></ImageUploadCrop>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-left">
            <div class="field-title">Promo Description</div>
            <v-textarea
                v-model="description"
                auto-grow
                class="text__collab-design"
                outline
                rows="2"
            ></v-textarea>
        </v-flex>
        <v-flex xs12  class="text-xs-left buttons-container">
            <v-btn class="button__collab-design--light" :disabled="previewBtnDisabled" @click="preview">{{previewBtnText}}</v-btn>
            <v-btn class="button__collab-design--dark" :loading="isLoading" :disabled="isLoading" @click="submit">Save</v-btn>
        </v-flex>



        
        <v-flex xs12 md6 class="text-xs-left">
            <GeoMap v-bind="mapData" height="300px" v-if="lat && lng"/>
        </v-flex>
        <v-flex xs12 md6 class="text-xs-left">
            <v-layout align-top justify-left row wrap>
                <v-flex xs6 class="text-xs-left">
                    <v-menu offset-y>
                      <template v-slot:activator="{ on }">
                        <v-btn
                          v-on="on"
                        >
                          Teachers
                        </v-btn>
                      </template>
                      <v-list>
                          <template v-for="(t, index) in teachers">
                            <v-list-tile
                              :key="t.id"
                              @click="$router.push('profile/teachers/'+t.id)"
                            >
                              <v-list-tile-avatar>
                                <img :src="previewSrc(t.media)">
                              </v-list-tile-avatar>

                              <v-list-tile-content>
                                <v-list-tile-title >{{t.first_name}} {{t.last_name}}</v-list-tile-title>
                                <v-list-tile-sub-title>{{t.phone}}, {{t.email}}</v-list-tile-sub-title>
                              </v-list-tile-content>
                            </v-list-tile>
                            <v-divider
                              v-if="index < teachers.length-1"
                              :key="`divider${index}`"
                            ></v-divider>
                          </template>
                      </v-list>
                    </v-menu>
                </v-flex>
                <v-flex xs6 class="text-xs-left">
                    <v-btn @click="$router.push('profile/teachers/')">Edit teachers</v-btn>
                </v-flex>
                <v-flex xs12 class="text-xs-left">
                    <v-text-field
                        readonly
                        :value="instructorRegistrationUrl"
                        label="Url to instructor registration"
                    >
                        <template v-slot:append>
                            <chip color="success" small v-if="instructorRegistrationUrlCopied">Copied!</chip>
                            <v-icon v-else @click.stop="copyInstructorRegistrationUrl">content_copy</v-icon>
                        </template>
                    </v-text-field>
                </v-flex>
            </v-layout>
            <v-divider />
            <div class="font-weight-bold" style="margin-top: 30px;">Student - Reminders</div>
            <v-checkbox
              v-model="reminderDay"
              hide-details
            >
                <template v-slot:label>
                    Day before <v-icon @click.stop="openReminderInfo('reminderDay')">info</v-icon>
                </template>
            </v-checkbox>
            <v-checkbox
              v-model="reminder10Min"
              hide-details
            >
                <template v-slot:label>
                    10 minutes before <v-icon @click.stop="openReminderInfo('reminder10Min')">info</v-icon>
                </template>
            </v-checkbox>
            <v-checkbox
              v-model="reminderRenew"
              hide-details
            >
                <template v-slot:label>
                    Thx & please renew <v-icon @click.stop="openReminderInfo('reminderRenew')">info</v-icon>
                </template>
            </v-checkbox>
            <v-divider></v-divider>
            <v-text-field
                v-model.trim="homeUrl"
                label="Home Url"
            ></v-text-field>
            <v-text-field
                v-model.trim="memberCenterUrl"
                label="Member Center Url"
            ></v-text-field>
            <v-text-field
                v-model.trim="aboutUsUrl"
                label="About Us Url"
            ></v-text-field>
            <v-text-field
                v-model.trim="memberAccessCode"
                label="Access Code"
            >
                <template v-slot:prepend>
                    <v-icon @click.stop="openReminderInfo('reminderAccessCode')">info</v-icon>
                </template>
            </v-text-field>
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <v-divider ></v-divider>
            
            <template v-if="group_count">
                <v-divider ></v-divider>
                <router-link :to="'/classes/group/company/'+id">Group Events</router-link>
            </template>
            <template v-if="private_count">
                <v-divider ></v-divider>
                <router-link :to="'/classes/private/company/'+id">Private Sessions</router-link>
            </template>
            <template v-if="reviews && reviews.length">
                <v-divider ></v-divider>
                <h3>Reviews</h3>
                <ReviewItem v-for="gc in reviews" v-bind="gc" :key="gc.id"/>
            </template>
            <v-alert
                  :value="errorAlert"
                  type="error"
                  color="platform-error"
                  transition="scale-transition"
            >
                  {{errorText}}
            </v-alert>
            <v-btn color="primary" :loading="isLoading" :disabled="isLoading" @click="submit">Update</v-btn>
        </v-flex>

        <v-dialog
          v-model="reminderInfoDialog"
          width="500"
        >
          <v-card>
            <v-card-title
              class="headline grey lighten-2"
              primary-title
            >
              Reminder text
            </v-card-title>

            <v-card-text>
                <div style="text-align: left;" v-html="reminderInfoText"></div>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                @click="reminderInfoDialog = false"
              >
                Got it
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-layout>

</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'

import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import TimezoneList from './Components/TimezoneList'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'
import helperClass from '@/lib/helpers/Class'
import config from '@/config.js';
const reminderTexts = {
    reminderAccessCode: `If access code is filled in, members automatically receive an email:
This is your access code to the member center:  [access code]`,
    reminderDay: `Teachbeach Reminder: You have [class] with [teacher] scheduled tomorrow at [time] [timezone]. [link]`,
    reminder10Min: `It’s sunny! [class] with [teacher] begins in ten minutes on [date], [time] [timezone].

Powered by TeachBeach`,
    reminderRenew: `Hi [student],

Congrats on completing [class]. You are on a roll!  You are invited to keep learning: [link]

All the best,

[teacher]
[phone]
[email]
Powered by TeachBeach`,
}

export default {
    mixins: [validationMixin],
    name: 'dashboard_teach_company_profile',
    data: () => ({
        isLoading: false,
        //avatarUrl: null,
        title: '',
        name: '',
        firstName: '',
        lastName: '',
        slug: '',
        email: '',
        phone: '',
        replaceLogo: false,
        description: '',
        group_count: 0,
        private_count: 0,
        previewBtnDisabled: false,
        id: null,
        reviews: [],
        timezone: '',
        imageName: '',
        imageUrl: '',
		imageFile: '',
        mainImageName: '',
        mainImageUrl: '',
		mainImageFile: '',
        applyTimezoneToClasses: false,
		errors: {},
        teachers: [],
        crop: {},
        crop2: {},
        errorAlert: false,
        errorText: '',
        msg: '',
        savedData: null,

        reminderDay: true,
        reminder10Min: true,
        reminderRenew: true,
        reminderInfoText: '',
        reminderInfoDialog: false,

        homeUrl: '',
        memberCenterUrl: '',
        aboutUsUrl: '',
        memberAccessCode: '',

        instructorRegistrationUrlCopied: false,
    }),
    validations: {
        name: { required, maxLength: maxLength(30) },
        firstName: { required, maxLength: maxLength(30) },
        lastName: { required, maxLength: maxLength(30) },
        email: { required, email },
        phone: { required, maxLength: maxLength(20) },
    },
    props: [],
    components: {
        ImageUploadCrop,
        TimezoneList,
    },
    created() {
        this.isLoading = true
        axios.all([axios.get('/api/company_profile/'), axios.get('/api/teacher_profile/')])
            .then(axios.spread((cp, tp) => {
                this.isLoading = false
                const profile = cp.data
                this.imageUrl = profile.media
                this.mainImageUrl = helperClass.previewImageSrc(profile.main_media)
                this.title = profile.title || `Welcome to ${profile.name}`
                this.name = profile.name
                this.firstName = profile.user.first_name
                this.lastName = profile.user.last_name
                this.slug = profile.slug
                this.email = profile.user.email
                this.phone = profile.user.phone
                this.description = profile.description
                this.group_count = profile.group_count
                this.private_count = profile.private_count
                this.replaceLogo = profile.replace_logo
                this.timezone = profile.user.timezone
                this.reminderDay = profile.reminder_day
                this.reminder10Min = profile.reminder_10min
                this.reminderRenew = profile.reminder_renew
                this.homeUrl = profile.home_url
                this.memberCenterUrl = profile.member_center_url
                this.aboutUsUrl = profile.about_us_url
                this.memberAccessCode = profile.member_access_code
                this.id = profile.id
                this.teachers = tp.data
                this.savedData = this.getCurrentData()
            }))
    },
    computed: {
        instructorRegistrationUrl() {
            return `${window.location.origin}/teachers/profile?c=${this.id}`;
        },
        urlPrefix() {
            return window.location.origin+'/company/'
        },
        baseUrl() {
            return config.baseUrl;
        },
        subdomain() {
            return this.baseUrl.replace(/(http(|s):\/\/)/, `$1${this.slug}.`).toLowerCase();
        },
        previewBtnText() {
            return this.isNotSavedEdits ? 'Save & Preview' : 'Preview'
        },
        isNotSavedEdits() {
            return this.savedData
                && Object.entries(this.savedData).reduce((acc, [k, v]) => acc || this.currentData[k] !== v, false)
        },
        currentData () {
            return this.getCurrentData()
        },
        emailErrors () {
            const errors = []
            if (this.errors.email) {
                return this.errors.email
            }
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.$v.email.required && errors.push('E-mail is required')
            return errors
        },
        nameErrors () {
            const errors = []
            if (!this.$v.name.$dirty) return errors
            !this.$v.name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.name.required && errors.push('Name is required.')
            return errors
        },
        firstNameErrors () {
            const errors = []
            if (!this.$v.firstName.$dirty) return errors
            !this.$v.firstName.maxLength && errors.push('First Name must be at most 30 characters long')
            !this.$v.firstName.required && errors.push('First Name is required.')
            return errors
        },
        lastNameErrors () {
            const errors = []
            if (!this.$v.lastName.$dirty) return errors
            !this.$v.lastName.maxLength && errors.push('Last Name must be at most 30 characters long')
            !this.$v.lastName.required && errors.push('Last Name is required.')
            return errors
        },
        phoneErrors () {
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            !this.$v.phone.required && errors.push('Phone is required')
            return errors
        },
    },
    methods: {
        copyInstructorRegistrationUrl() {
            navigator.clipboard.writeText(this.instructorRegistrationUrl).then(() => {
                this.instructorRegistrationUrlCopied = true;
                setTimeout(() => {
                    this.instructorRegistrationUrlCopied = false;
                }, 3000);
            }).catch(() => {
                console.error('can\'t write to clipboard')
            });
        },
        previewSrc(src) {
            return helperClass.previewImageSrc(src)
        },
        getCurrentData() {
            return {
                imageUrl: this.imageUrl,
                mainImageUrl: this.mainImageUrl,
                name: this.name,
                firstName: this.firstName,
                lastName: this.lastName,
                title: this.title,
                slug: this.slug,
                email: this.email,
                phone: this.phone,
                description: this.description,
                group_count: this.group_count,
                private_count: this.private_count,
                replaceLogo: this.replaceLogo,
                timezone: this.timezone,
                reminder10Min: this.reminder10Min,
                reminderRenew: this.reminderRenew,
                reminderDay: this.reminderDay,
                homeUrl: this.homeUrl,
                memberCenterUrl: this.memberCenterUrl,
                aboutUsUrl: this.aboutUsUrl,
                memberAccessCode: this.memberAccessCode,
                id: this.id,
            }
        },
        async saveData() {
            this.$v.$touch()
            console.log('submit', this, arguments)
            if (this.$v.$anyError)
                return false
            //make axios call
            this.isLoading = true
            const data = {
                profile: {
                    description: this.description,
                    companyName: this.name,
                    replaceLogo: this.replaceLogo,
                    title: this.title,
                    slug: this.slug,
                    reminder10Min: this.reminder10Min,
                    reminderRenew: this.reminderRenew,
                    reminderDay: this.reminderDay,
                    homeUrl: this.absoluteUrl(this.homeUrl),
                    memberCenterUrl: this.absoluteUrl(this.memberCenterUrl),
                    aboutUsUrl: this.absoluteUrl(this.aboutUsUrl),
                    memberAccessCode: this.memberAccessCode,
                },
                user: {
                    first_name: this.firstName,
                    last_name: this.lastName,
                    email: this.email,
                    phone: this.phone,
                    timezone: this.timezone,
                    timezone_to_classes: this.applyTimezoneToClasses,
                }
            }
            if (this.crop.canvas) {
                data.avatar = {
                    uploadPhoto: {
                        imageName: this.imageName,
                        imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                        imageFile: this.imageFile,
                    },
                }
            }
            if (this.crop2.canvas) {
                data.main_media = {
                    uploadPhoto: {
                        imageName: this.mainImageName,
                        imageUrl: this.crop2.canvas ? this.crop2.canvas.toDataURL() : '',
                        imageFile: this.mainImageFile,
                    },
                }
            }
            try {
                const res = await axios.post('/api/company_profile/', data)
                this.isLoading = false
                return res
            } catch (e) {
                this.isLoading = false
                return e
            }
        },
        submit () {
            this.saveData().then((res) => {
                this.errorAlert = !res.data.success
                if(!res.data.success) {
                    this.errorText = res.data.err
                } else {
                    this.msg = 'Profile was updated'
                    this.$router.push('/dashboard/teach/classes')
                }
            }).catch(() => {
                console.log('err!', arguments)
            })
        },
        onFileChanged(e) {
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
        onMainFileChanged(e) {
            this.mainImageName = e.imageName
            this.mainImageFile = e.imageFile
            this.mainImageUrl = e.imageUrl
            this.crop2 = e.crop
        },
        preview() {
            console.log('preview')
            if(this.isNotSavedEdits) {
                this.saveData().then(() => {
                    this.$router.push(`/company_profile/${this.id}`)
                })
            } else {
                this.$router.push(`/company_profile/${this.id}`)
            }
        },
        openReminderInfo(type) {
            this.reminderInfoText = reminderTexts[type].replace(/(?:\r\n|\r|\n)/g, '<br/>')
            this.reminderInfoDialog = true
        },
    },

    watch: {

    }
}
</script>
<style lang="scss">
.company-profile {
    &> div {
        padding: 20px;
    }
    .subdomain-field .v-label {
        margin-top: 20px;
        pointer-events: all;
    }
    .timezone-checkbox {
        margin-top: -30px;
    }
    .buttons-container > * {
        margin: 0 10px;
    }
}
.title {
    text-align: left;
    font-weight: bold;
}
</style>