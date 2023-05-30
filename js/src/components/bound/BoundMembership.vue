<template>
    <v-layout align-start justify-start row wrap>
        <v-flex xs12 class="text-xs-center" >
            <v-btn v-if="isBackBtnVisible" @click="back">{{backBtnText}}</v-btn>
            <v-btn v-if="isSubmitBtnDuplicated" @click="submit" :loading="isLoadingTeacherMembership" :disabled="isLoadingTeacherMembership">{{submitBtnText}}</v-btn>
            <v-btn v-if="teacherMembership" @click="preview">Preview</v-btn>
        </v-flex>
        <v-flex xs4 class="text-xs-left">
            <v-select
                v-model="currency"
                :items="currencies"
                label="Currency"
                item-text="label"
                item-value="id"
            ></v-select>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <div style="width: 300px;">
                <image-upload-crop
                    :imageUrl="imageUrl"
                    :imageName="imageName"
                    :imageFile="imageFile"
                    width="100%"
                    :aspectRatio="1.25"
                    @change="onFileChanged"
                />
            </div>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <div style="width: 300px;">
              <v-text-field
                v-model="name"
                label="Name"
                :error-messages="nameErrors"
                @input="$v.name.$touch()"
                @blur="$v.name.$touch()"
              ></v-text-field>
            </div>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <div style="width: 300px;">
              <v-text-field
                v-model="weekly_rate"
                label="Weekly Rate"
                outline
                :error-messages="weeklyRateErrors"
                @input="$v.weekly_rate.$touch()"
                @blur="$v.weekly_rate.$touch()"
              ></v-text-field>
            </div>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <div style="width: 300px;">
              <v-text-field
                v-model="monthly_rate"
                label="Monthly Rate"
                outline
                :error-messages="monthlyRateErrors"
                @input="$v.monthly_rate.$touch()"
                @blur="$v.monthly_rate.$touch()"
              ></v-text-field>
            </div>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <div style="width: 300px;">
              <v-text-field
                v-model="yearly_rate"
                label="Yearly Rate"
                outline
                :error-messages="yearlyRateErrors"
                @input="$v.yearly_rate.$touch()"
                @blur="$v.yearly_rate.$touch()"
              ></v-text-field>
            </div>
        </v-flex>
        <v-flex xs12 class="text-xs-left" >
            <v-textarea
                v-model.trim="description"
                label="Description of benefits"
                auto-grow
                box
                rows="5"
            ></v-textarea>
        </v-flex>
        <v-flex xs12 class="text-xs-center" >
            <v-btn @click="back">{{cancelBtnText}}</v-btn>
            <v-btn @click="submit" :loading="isLoadingTeacherMembership" :disabled="isLoadingTeacherMembership">{{submitBtnText}}</v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
import utils from '@/lib/utils.js'
import {mapState, mapActions} from 'vuex';
import { validationMixin } from 'vuelidate'
import { numeric, required } from 'vuelidate/lib/validators'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'

export default {
    name: 'TeacherMembership',
    mixins: [validationMixin],
    validations: {
        weekly_rate: {numeric},
        monthly_rate: {numeric},
        yearly_rate: {numeric},
        name: {required},
    },
    components: {
        ImageUploadCrop,
    },
    props: {
        cancelBtnText: {
            type: String,
            default: 'Back',
        },
        submitBtnText: {
            type: String,
            default: 'Next',
        },
        isBackBtnVisible: {
            type: Boolean,
            default: false,
        },
        isSubmitBtnDuplicated: {
            type: Boolean,
            default: false,
        },
        backBtnText: {
            type: String,
            default: 'Back',
        },
        backBtnUrl: {
            type: String,
            default: '/',
        },
    },
    data: () => ({
        currency: 'usd',
        currencies: utils.getCurrencyList(),
        weekly_rate: null,
        monthly_rate: null,
        yearly_rate: null,
        name: '',
        description: '',
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
    }),
    created() {
        this.reload()
    },
    computed: {
        ...mapState([
            'teacherMembership',
            'isLoadingTeacherMembership'
        ]),
        weeklyRateErrors() {
            const errors = []
            if (!this.$v.weekly_rate.$dirty) return errors
            !this.$v.weekly_rate.numeric && errors.push('Please use numbers only')
            return errors
        },
        monthlyRateErrors() {
            const errors = []
            if (!this.$v.monthly_rate.$dirty) return errors
            !this.$v.monthly_rate.numeric && errors.push('Please use numbers only')
            return errors
        },
        yearlyRateErrors() {
            const errors = []
            if (!this.$v.yearly_rate.$dirty) return errors
            !this.$v.yearly_rate.numeric && errors.push('Please use numbers only')
            !this.weekly_rate && !this.monthly_rate && !this.yearly_rate && errors.push('at least one rate is required')
            return errors
        },
        nameErrors() {
            const errors = []
            if (!this.$v.name.$dirty) return errors
            !this.$v.name.required && errors.push('Name is required')
            return errors
        },
    },
    methods: {
        reload() {
            this.$store.dispatch('loadTeacherMembership').then(() => {
                if(!this.teacherMembership)
                    return
                this.currency = this.teacherMembership.currency
                this.weekly_rate = Math.round(this.teacherMembership.weekly_rate)
                this.monthly_rate = Math.round(this.teacherMembership.monthly_rate)
                this.yearly_rate = Math.round(this.teacherMembership.yearly_rate)
                this.description = this.teacherMembership.description
                this.name = this.teacherMembership.name
                this.imageUrl = this.teacherMembership.media
            })
        },
        save() {
            const data = {
                currency: this.currency,
                weekly_rate: Math.abs(this.weekly_rate),
                monthly_rate: Math.abs(this.monthly_rate),
                yearly_rate: Math.abs(this.yearly_rate),
                description: this.description,
                name: this.name,
            }
            if (this.crop.canvas) {
                data.picture = {
                    uploadPhoto: {
                        imageName: this.imageName,
                        imageUrl: this.crop.canvas ? this.crop.canvas.toDataURL() : '',
                        imageFile: this.imageFile,
                    },
                }
            }
            return this.$store.dispatch('saveTeacherMembership', data)
        },
        back() {
            this.$emit('cancel')
        },
        submit () {
            this.$v.$touch()
            if (this.$v.$anyError)
                return
            this.save().then(() => {
                this.$emit('saved')
            }).catch((err) => {
                this.$emit('error', err)
            })
        },
        onFileChanged(e) {
            this.imageName = e.imageName
            this.imageFile = e.imageFile
            this.imageUrl = e.imageUrl
            this.crop = e.crop
        },
        preview() {
            this.$router.push(`/buy-membership/${this.teacherMembership.id}?preview`);
        },
    },
}
</script>
<style lang="scss">
@import "../../styles/_variables.scss";

</style>