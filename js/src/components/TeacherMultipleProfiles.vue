<template>
    <div class="teacher-multiple-profiles">
        <h1>{{ title }}</h1>
        <MultipleProfiles
            :teachers="teachers"
            :selectedTeacher="currentTeacher"
            :reloadTeachers="reloadTeachers"
            :saveTeacher="saveTeacher"
            v-slot="{saveTeacherLocal}"
        >
            <v-alert
              :value="isError"
              type="error"
              color="platform-error"
              transition="scale-transition"
            >
              Error Image uploading, try another one, smaller size
            </v-alert>
            <v-btn @click="() => {saveTeacherLocal(); back();}" :loading="isLoading">Back</v-btn>
            <v-btn @click="() => {saveTeacherLocal(); submit();}" :loading="isLoading">Next</v-btn>
        </MultipleProfiles>
    </div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import { validationMixin } from 'vuelidate'
import { required, maxLength} from 'vuelidate/lib/validators'

import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import MultipleProfiles from './Teacher/MultipleProfiles'

export default {
    mixins: [validationMixin],
    validations: {
        first_name: { required, maxLength: maxLength(30) },
        last_name: { required, maxLength: maxLength(30) },
    },
    components: {
        ImageUploadCrop,
        MultipleProfiles,
    },
    props: [

    ],

    data: () => ({
        description: '',
        isLoading: false,
        isUpdated: false,
        isError: false,
        imageName: '',
        imageUrl: '',
		imageFile: '',
        teachers: [],
        currentTeacher: null,
        first_name: '',
        last_name: '',
        phone: '',
        email: '',
        crop: {},
        readonly: true,
        ignoreChange: false,
        isPremiumCommunity: false,
    }),

    created: function () {
        if (this.$store.state.profile) {
            this.description = this.$store.state.profile.description || ''
            this.first_name = this.$store.state.profile.first_name || ''
            this.last_name = this.$store.state.profile.last_name || ''
            this.phone = this.$store.state.profile.phone || ''
            this.email = this.$store.state.profile.email || ''
            this.currentTeacher = this.$store.state.profile.id || ''
        }
        if (this.$store.state.avatar && this.$store.state.avatar.uploadPhoto) {
            this.imageName = this.$store.state.avatar.uploadPhoto.imageName || ''
            this.imageUrl = this.$store.state.avatar.uploadPhoto.imageUrl || ''
            this.imageFile = this.$store.state.avatar.uploadPhoto.imageFile || ''
        }
        if (this.$store.state.teacherGroupClass) {
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
        }
        this.readonly = !!this.currentTeacher
        this.reloadTeachers().then(() => {
            const cur = _.find(this.teachers, {id: this.currentTeacher})
            if (!cur || !cur.first_name || !cur.last_name) {
                const notEmpty = _.find(this.teachers, v => v.first_name && v.last_name)
                if(notEmpty) {
                    this.currentTeacher = notEmpty.id
                }
            }
        })
    },

    computed: {
        title() {
            return this.isPremiumCommunity ? 'Who is leading this group?' : 'Who is teaching this class?';
        }
    },

    methods: {

        back() {
            this.$emit('prev:step')
        },
        submit () {
            this.saveTeacher().then((res) => {
                if(res) {
                    if(res.data.id) {
                        this.$store.commit('setTeacherProfile', _.assign({}, this.$store.state.profile, {id: res.data.id}))
                    }
                    this.$emit('next:step')
                }
            }).catch((e) => {
                console.log('err!', e)
            })

        },
        clear () {

        },
        saveTeacher() {

            this.isLoading = true
            this.isUpdated = false
            return new Promise((resolve, reject) => {
                axios.post('/api/teacher_profile/', {
                    profile: this.$store.state.profile,
                    avatar: {
                        uploadPhoto: _.pick(this.$store.state.avatar.uploadPhoto, ['imageName', 'imageUrl']),
                    },
                }).then((res) => {
                    //console.log('/api/company_profile/', arguments)
                    if(res && res.data && res.data.id) {
                        this.$store.commit('setTeacherProfile', _.assign({}, this.$store.state.profile, {id: res.data.id}))
                        this.$store.commit('setTeacher', _.assign({}, this.$store.state.profile, {id: res.data.id}))
                    }
                    resolve(res)
                }).catch((e) => {
                    this.isError = true
                    setTimeout(() => {this.isError = false}, 3000)
                    reject(e)
                }).then(() => {
                    this.isLoading = false
                })
            })

        },
        reloadTeachers() {
            return axios.get('/api/teacher_profile/').then(res => {
                this.teachers = _.sortBy(res.data, v => `${v.first_name} ${v.last_name}`)
                //this.currentTeacher = res.data.length ? res.data[0].id : null
                return res
            })
        },
    },
    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>