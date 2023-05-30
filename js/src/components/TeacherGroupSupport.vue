<template>
  <form>
    <h1>{{ title }}</h1>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <v-textarea
                v-model="groupClassDescription"
                auto-grow
                box
                label="What will you do?"
                placeholder="Describe the activities students will do and what knowledge they will learn."
                rows="2"
            ></v-textarea>
            <v-textarea
              v-model="studentsBring"
              :label="studentsBringLabel"
              placeholder="List what students need to bring with them"
              auto-grow
              box
              rows="2"
            ></v-textarea>
            <v-textarea
              v-model="teacherSupply"
              label="What you will supply"
              auto-grow
              box
              placeholder="Describe any amenities or refreshments available for customers"
              rows="2"
            ></v-textarea>
            <v-textarea
                v-model="studentsToKnow"
                auto-grow
                box
                label="What else do they need to know?"
                hint="Be as specific as possible about how to find your meeting place."
                rows="2"
            ></v-textarea>
            <v-textarea
                v-model="groupClassSummary"
                auto-grow
                box
                label="Summary (400 characters)"
                :placeholder="groupClassSummaryPlaceholder"
                rows="2"
                :error-messages="summaryErrors"
                counter
                @input="$v.groupClassSummary.$touch()"
                @blur="$v.groupClassSummary.$touch()"
            ></v-textarea>

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
            ></ImageUploadCrop>
        </v-flex>

      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'

import ImageUploadCrop from '@/components/basic/ImageUploadCrop'

import axios from 'axios'
import { validationMixin } from 'vuelidate'
import { required, maxLength, email, sameAs, minLength, numeric } from 'vuelidate/lib/validators'

export default {
    mixins: [validationMixin],
    validations: {
        groupClassSummary: {maxLength: maxLength(400), required},
    },
    components: {
        ImageUploadCrop
    },
    data: () => ({
        isLoading: false,
        studentsBring: '',
        teacherSupply: '',
        studentsToKnow: '',
        supportFiles: [],
        groupClassDescription: '',
        groupClassSummary: '',
        crop: {},
        imageName: '',
        imageUrl: '',
        imageFile: null,
        isPremiumCommunity: false,
        defaultCommunityStudentsBring: `Regular team meetings
Coaching
Discord group
Private DM with instructors
Exclusive content
`,
    }),

    created: function () {
        if (this.$store.state.teacherGroupClass) {
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity;
            this.studentsBring = this.$store.state.teacherGroupClass.studentsBring || (this.isPremiumCommunity ? this.defaultCommunityStudentsBring : '');
            this.teacherSupply = this.$store.state.teacherGroupClass.teacherSupply;
            this.studentsToKnow = this.$store.state.teacherGroupClass.studentsToKnow;
            this.supportFiles = this.$store.state.teacherGroupClass.supportFiles || [];
            this.groupClassDescription = this.$store.state.teacherGroupClass.groupClassDescription;
            this.groupClassSummary = this.$store.state.teacherGroupClass.groupClassSummary;
        }
    },

    computed: {
        loadedFilesUI() {
            return _.map(this.supportFiles, (f) => {
                return {
                    isImage: true,
                    fileUrl: f.imageUrl
                }
            })
        },
        summaryErrors() {
            const errors = []
            if (!this.$v.groupClassSummary.$dirty) return errors
            !this.$v.groupClassSummary.maxLength && errors.push('Summary must be at most 400 characters long')
            !this.$v.groupClassSummary.required && errors.push('Summary is required field')
            return errors
        },
        title() {
            return this.isPremiumCommunity ? 'Describe your community benefits' : 'Group class';
        },
        studentsBringLabel() {
            return this.isPremiumCommunity ? 'What other benefits will customers receive?' : 'What students will bring'
        },
        groupClassSummaryPlaceholder() {
            return this.isPremiumCommunity ? 'Give your community a short summary that will appear on promotional pages' : 'Give your class a great summary that will show up on listing engines.';
        },
    },

    methods: {
        saveData() {
            this.$store.commit('setGroupClass', {
                studentsBring: this.studentsBring,
                teacherSupply: this.teacherSupply,
                studentsToKnow: this.studentsToKnow,
                supportFiles: this.supportFiles,
                groupClassDescription: this.groupClassDescription,
                groupClassSummary: this.groupClassSummary,
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