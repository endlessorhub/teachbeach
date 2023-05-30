<template>
  <form>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <h3>This summary will show up in your published listing. Don´t worry, you can add more than one type of class, such as one for beginners, one for experts, different technigues, etc. later.</h3>
            <v-text-field
              v-model="privateClassName"
              label="Name your lessons"
              placeholder="Come up with a name for this type of lesson here."
              :error-messages="nameErrors"
              @input="$v.privateClassName.$touch()"
              @blur="$v.privateClassName.$touch()"
            ></v-text-field>
            <v-textarea
                v-model="groupClassSummary"
                auto-grow
                box
                label="Summary (400 characters)"
                placeholder="Describe"
                rows="2"
                :error-messages="summaryErrors"
                counter
                @input="$v.groupClassSummary.$touch()"
                @blur="$v.groupClassSummary.$touch()"
            ></v-textarea>
            <div>
                This is a longer description of your class that can include the summary and will show up on the class profile page.
            </div>
            <v-textarea
                v-model="groupClassDescription"
                auto-grow
                box
                label="What will you do?"
                placeholder="Describe the activities students will do and what knowledge they will learn."
                rows="2"
            ></v-textarea>
            <v-text-field
              v-model="privateClassWebsite"
              label="Website (optional)"
              placeholder="http://..."
            ></v-text-field>
            <div v-for="(file, i) in loadedFilesUI">
                <img :src="file.fileUrl" width="400" v-if="file.isImage"/>
                <v-btn class="remove-photo-btn" flat icon @click="onDeleteFile(i)"><v-icon>cancel</v-icon></v-btn>
            </div>
            <ImageUploadCrop
                :imageUrl="imageUrl"
                :imageName="imageName"
                :imageFile="imageFile"
                width="400px"
                @change="onFileChanged"
                label="Upload image"
                :confirmable="true"
                :aspectRatio="1.25"
                ref="imageUploader"
            ></ImageUploadCrop>
        </v-flex>
        <v-flex xs12 sm6>
            <v-checkbox color="primary" v-model="showEmail" label="Show Email on the Class Page" hide-details></v-checkbox>
        </v-flex>
        <v-flex xs12 sm6>
            <ShowPhoneRule v-model="showPhoneRule" />
            <v-checkbox color="primary" v-model="showPhone" label="Show Phone on the Class Page" hide-details></v-checkbox>
        </v-flex>
      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import ShowPhoneRule from './Teacher/ShowPhoneRule'

import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength, numeric } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],
    validations: {
        privateClassName: {required, maxLength: maxLength(140)},
        groupClassSummary: {required, maxLength: maxLength(400)},
    },
    components: {
        ImageUploadCrop,
        ShowPhoneRule,
    },
    data: () => ({
        isLoading: false,
        studentExperienceLevel: [],
        privateClassName: '',
        privateClassWebsite: '',
        groupClassSummary: '',
        groupClassDescription: '',
        supportFiles: [],
        imageName: '',
        imageUrl: '',
        imageFile: null,
        fileLoadedAutoNext: false,
        showEmail: false,
        showPhone: false,
        showPhoneRule: 'text',
    }),

    created: function () {
        let _this = this
        if (this.$store.state.teacherGroupClass) {
            this.privateClassName = _this.$store.state.teacherGroupClass.privateClassName
            this.privateClassWebsite = _this.$store.state.teacherGroupClass.privateClassWebsite
            this.groupClassSummary = _this.$store.state.teacherGroupClass.groupClassSummary
            this.groupClassDescription = _this.$store.state.teacherGroupClass.groupClassDescription
            this.supportFiles = _this.$store.state.teacherGroupClass.supportFiles || []
            if('showEmail' in this.$store.state.teacherGroupClass) {
                this.showEmail = this.$store.state.teacherGroupClass.showEmail
            }
            if('showPhone' in this.$store.state.teacherGroupClass) {
                this.showPhone = this.$store.state.teacherGroupClass.showPhone
            }
            if('showPhoneRule' in this.$store.state.teacherGroupClass) {
                this.showPhoneRule = this.$store.state.teacherGroupClass.showPhoneRule
            }
        }

    },

    computed: {
        nameErrors() {
            const errors = []
            if (!this.$v.privateClassName.$dirty) return errors
            !this.$v.privateClassName.required && errors.push('Class name is required')
            !this.$v.privateClassName.maxLength && errors.push('Class name must be at most 140 characters long')
            return errors
        },
        summaryErrors() {
            const errors = []
            if (!this.$v.groupClassSummary.$dirty) return errors
            !this.$v.groupClassSummary.required && errors.push('Summary is required')
            !this.$v.groupClassSummary.maxLength && errors.push('Summary must be at most 400 characters long')
            return errors
        },
        loadedFilesUI() {
            return _.map(this.supportFiles, (f) => {
                return {
                    isImage: true,
                    fileUrl: f.imageUrl
                }
            })
        },
    },

    methods: {
        saveData() {
            this.$store.commit('setGroupClass', {
                studentExperienceLevel: this.studentExperienceLevel,
                privateClassName: this.privateClassName,
                privateClassWebsite: this.privateClassWebsite,
                groupClassSummary: this.groupClassSummary,
                groupClassDescription: this.groupClassDescription,
                supportFiles: this.supportFiles,
                showEmail: this.showEmail,
                showPhone: this.showPhone,
                showPhoneRule: this.showPhoneRule,
            })
        },
        back() {
            this.saveData()
            this.$emit('prev:step')
        },
        submit () {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            if (this.$refs.imageUploader.isEditing) {
                //auto confirm image crop/upload
                this.fileLoadedAutoNext = true
                this.$refs.imageUploader.confirmFile()
                return
            }
            this.saveData()
            this.$emit('next:step')
        },
        clear () {

        },
        onFileChanged(e) {
            this.supportFiles.push({
                imageName: e.imageName,
                imageUrl: e.crop.canvas ? e.crop.canvas.toDataURL() : e.imageUrl,
                imageFile: e.imageFile,
            })
            this.imageName = ''
            this.imageUrl = ''
            this.imageFile = null
            if (this.fileLoadedAutoNext) {
                this.fileLoadedAutoNext = false
                this.submit()
            }
        },
        onDeleteFile(i) {
            this.supportFiles.splice(i, 1)
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>