<template>
  <form>
    <v-btn @click="submit">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 text-xs-left>
            <v-text-field
              v-model="companyName"
              label="Name of business"
              placeholder="Enter a name"
              required
              @input="$v.companyName.$touch()"
              @blur="$v.companyName.$touch()"
              :error-messages="companyNameErrors"
            ></v-text-field>
            <v-textarea
                v-model="description"
                auto-grow
                box
                label="Why is this a great place to learn?"
                rows="3"
            ></v-textarea>
        </v-flex>
        <v-flex xs12 class="text-xs-left">
            <ImageUploadCrop
                :imageUrl="imageUrl"
                :imageName="imageName"
                :imageFile="imageFile"
                width="400px"
                @change="onFileChanged"
                :aspectRatio="1.25"
                label="Please use your logo for this image"
            ></ImageUploadCrop>
            <v-checkbox
                v-model="replaceLogo"
                label="Show this image instead logo in the page header"
            ></v-checkbox>
        </v-flex>
          <v-flex xs12 class="text-xs-left">
                <ImageUploadCrop
                    :imageUrl="mainImageUrl"
                    :imageName="mainImageName"
                    :imageFile="mainImageFile"
                    width="400px"
                    :aspectRatio="1.25"
                    @change="onMainFileChanged"
                    label="Main image shown on company profile page"
                ></ImageUploadCrop>
            </v-flex>
      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit">Next</v-btn>
  </form>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import { validationMixin } from 'vuelidate'
import { required, maxLength} from 'vuelidate/lib/validators'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'

export default {
    mixins: [validationMixin],
    validations: {
        companyName: { required, maxLength: maxLength(200) },
    },
    components: {
        ImageUploadCrop
    },
    props: ['alreadyRegistered', 'hasAvatar'],

    data: () => ({
        description: '',
        companyName: '',
        replaceLogo: false,
        isLoading: false,
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
        mainImageName: '',
        mainImageUrl: '',
		mainImageFile: '',
        crop2: {},
    }),

    created: function () {
        if (this.$store.state.companyProfile) {
            this.description = this.$store.state.companyProfile.description || ''
            this.companyName = this.$store.state.companyProfile.companyName || ''
            this.replaceLogo = this.$store.state.companyProfile.replaceLogo
            this.imageUrl = this.$store.state.companyProfile.imageUrl || ''
            this.imageName = this.$store.state.companyProfile.imageName || ''
            this.imageFile = this.$store.state.companyProfile.imageFile || ''
            this.mainImageUrl = this.$store.state.companyProfile.mainImageUrl || ''
            this.mainImageName = this.$store.state.companyProfile.mainImageName || ''
            this.mainImageFile = this.$store.state.companyProfile.mainImageFile || ''
        }
    },

    computed: {
        companyNameErrors () {
            const errors = []
            if (!this.$v.companyName.$dirty) return errors
            !this.$v.companyName.required && errors.push('Company Name is required.')
            !this.$v.companyName.maxLength && errors.push('Company Name must be at most 200 characters long')
            return errors
        },
    },

    methods: {
        saveData() {
            this.$store.commit('setCompanyProfile', {
                description: this.description,
                companyName: this.companyName,
                replaceLogo: this.replaceLogo,
                imageName: this.imageName,
                imageUrl: this.imageUrl,
                imageFile: this.imageFile,
                mainImageName: this.mainImageName,
                mainImageUrl: this.mainImageUrl,
                mainImageFile: this.mainImageFile,
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
            this.isLoading = true
            const data = {
                profile: this.$store.state.companyProfile,
                avatar: {
                    uploadPhoto: {
                        imageName: this.imageName,
                        imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                        imageFile: this.imageFile
                    }
                },
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
            axios.post('/api/company_profile/', data).then((res) => {
                //console.log('/api/company_profile/', arguments)
                this.$emit('next:step')
            }).catch((e) => {
                console.log('err!', e)
            }).then(() => {
                this.isLoading = false
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
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>