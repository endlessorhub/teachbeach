<template>
    <v-layout align-top justify-left row wrap>
        <snack v-model="msg"></snack>
      <v-flex xs12 class="text-xs-left">
        <v-btn :disabled="previewBtnDisabled" @click="preview">{{previewBtnText}}</v-btn>
      </v-flex>
        <v-flex xs12 class="text-xs-left">
          <div class="bio">
            <v-flex xs11 md6  class="text-xs-left">
              <ImageUploadCrop
                :imageUrl="imageUrl"
                :imageName="imageName"
                :imageFile="imageFile"
                width="90%"
                :aspectRatio="1.25"
                @change="onFileChanged"
            ></ImageUploadCrop>
            </v-flex>
          <v-flex xs12 class="text-xs-left" style="display: flex;">
            <TimezoneList v-model="timezone" />
            <v-checkbox
                v-model="applyTimezoneToClasses"
                label="Apply to all classes"
            ></v-checkbox>
          </v-flex>
            <v-flex xs12  class="text-xs-left">
            <v-text-field
              v-model.trim="first_name"
              :error-messages="firstNameErrors"
              :counter="30"
              label="First Name"
              required
              @input="$v.first_name.$touch()"
              @blur="$v.first_name.$touch()"
            ></v-text-field>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
            <v-text-field
              v-model.trim="last_name"
              :error-messages="lastNameErrors"
              :counter="30"
              label="Last Name"
              required
              @input="$v.last_name.$touch()"
              @blur="$v.last_name.$touch()"
            ></v-text-field>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
            <v-text-field
              v-model.trim="email"
              label="Email Address"
              :error-messages="emailErrors"
            ></v-text-field>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
            <v-text-field
              v-model.trim="phone"
              :error-messages="phoneErrors"
              label="Phone Number"
              required
              @input="$v.phone.$touch()"
              @blur="$v.phone.$touch()"
            ></v-text-field>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
              <v-divider ></v-divider>
            </v-flex>
            <v-flex xs12  class="text-xs-left">
              <v-textarea
                v-model="description"
                auto-grow
                box
                label="What makes you stand-out as a teacher and how are you uniquely qualified?"
                rows="2"
              ></v-textarea>
            </v-flex>
            <v-flex xs12 class="text-xs-left">
                <v-combobox
                  v-model="areasOfSpeciality"
                  :items="specialties"
                  label="Areas of speciality"
                  multiple
                  chips
                ></v-combobox>
            </v-flex>
          </div>
          <v-flex v-if="group_count" xs12 class="text-xs-left">
            <v-divider ></v-divider>
            <router-link :to="'/classes/group/teacher/'+id">Group Events</router-link>
          </v-flex>
          <v-flex v-if="private_count" xs12 class="text-xs-left">
            <v-divider ></v-divider>
            <router-link :to="'/classes/private/teacher/'+id">Private Sessions</router-link>
          </v-flex>
          <v-flex v-if="reviews && reviews.length" xs12 md12 class="text-xs-left">
            <v-divider ></v-divider>
            <h3>Reviews</h3>
            <ReviewItem v-for="gc in reviews" v-bind="gc" :key="gc.id"/>
          </v-flex>

          <v-flex xs12  class="text-xs-left">
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
        </v-flex>
    </v-layout>

</template>

<script>
// @ is an alias to /src
import _ from 'lodash'
import axios from 'axios'

import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import Snack from '@/components/basic/Snack'
import TimezoneList from './Components/TimezoneList'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],
    name: 'dashboard_teach_profile',
    data: () => ({
        isLoading: false,
        //avatarUrl: null,
        first_name: '',
        last_name: '',
        phone: '',
        email: '',
        bio: '',
        timezone: '',
        specialties: [],
        group_count: 0,
        private_count: 0,
        id: null,
        areasOfSpeciality: [],
        reviews: [],
        imageName: '',
        imageUrl: '',
		imageFile: '',
        applyTimezoneToClasses: false,
		errors: {},
        crop: {},
        errorAlert: false,
        errorText: '',
        msg: '',
        previewBtnDisabled: false,
        savedData: null,
    }),
    validations: {
        first_name: { required, maxLength: maxLength(30) },
        last_name: { required, maxLength: maxLength(30) },
        email: { required, email },
        phone: { required, maxLength: maxLength(20) },
    },
    props: [],
    components: {
        ImageUploadCrop,
        Snack,
        TimezoneList,
    },
    created() {
        this.isLoading = true
        axios.get('/api/teacher_profile/').then(res => {
            this.isLoading = false
            if(!res.data.length)
                return
            const profile = res.data[0]
            this.imageUrl = profile.media
            this.first_name = profile.first_name
            this.last_name = profile.last_name
            this.phone = profile.user.phone
            this.email = profile.user.email
            this.description = profile.description
            this.areasOfSpeciality = profile.areas_of_specialty || []
            this.timezone = profile.user.timezone
            this.group_count = profile.group_count
            this.private_count = profile.private_count
            this.id = profile.id
            this.savedData = this.getCurrentData()
        })
    },
    computed: {
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
        firstNameErrors () {
            const errors = []
            if (!this.$v.first_name.$dirty) return errors
            !this.$v.first_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.first_name.required && errors.push('Name is required.')
            return errors
        },
        lastNameErrors () {
            const errors = []
            if (!this.$v.last_name.$dirty) return errors
            !this.$v.last_name.maxLength && errors.push('Name must be at most 30 characters long')
            !this.$v.last_name.required && errors.push('Name is required.')
            return errors
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
        phoneErrors () {
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            !this.$v.phone.required && errors.push('Phone is required')
            return errors
        },
    },
    methods: {
        async saveData() {
            this.$v.$touch()
            console.log('submit', this, arguments)
            if (this.$v.$anyError)
                return
            //make axios call
            this.isLoading = true
            const data = {
                profile: {
                    description: this.description,
                    areasOfSpeciality: this.areasOfSpeciality
                },
                user: {
                    first_name: this.first_name,
                    last_name: this.last_name,
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
            try {
                const res = await axios.post('/api/teacher_profile/', data)
                this.isLoading = false
                return res
            } catch (e) {
                this.isLoading = false
                return e
            }
        },
        getCurrentData() {
            return {
                imageUrl: this.imageUrl,
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                phone: this.phone,
                description: this.description,
                group_count: this.group_count,
                private_count: this.private_count,
                areasOfSpeciality: this.areasOfSpeciality,
                timezone: this.timezone,
                id: this.id,
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
            }).catch((e) => {
                console.log('err!', e)

            })
        },
        onFileChanged(e) {
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
        preview() {
            console.log('preview')
            if(this.isNotSavedEdits) {
                this.saveData().then(() => {
                    this.$router.push(`/teacher_profile/${this.id}`)
                })
            } else {
                this.$router.push(`/teacher_profile/${this.id}`)
            }
        },
    },

    watch: {

    }
}
</script>
<style lang="scss">

</style>