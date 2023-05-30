
<template>
    <div class="membership-setup-container">
        <v-layout class="membership-section-layout" align-start justify-start row wrap>
            <v-flex xs12 class="text-xs-center" >
                <div class="title">Membership Set-Up</div>
            </v-flex>
            <v-flex xs12 md3 class="text-xs-left">
                <div class="field-title">Main image</div>
                <image-upload-crop
                    :imageUrl="imageUrl"
                    :imageName="imageName"
                    :imageFile="imageFile"
                    width="100%"
                    :aspectRatio="1.25"
                    @change="onFileChanged"
                />
            </v-flex>
            <v-flex xs12 md9 class="text-xs-left" >
                <div class="field-title">Headline</div>
                <v-text-field
                    v-model="name"
                    class="text__collab-design"
                    outline
                    :error-messages="nameErrors"
                    @input="$v.name.$touch()"
                    @blur="$v.name.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 class="text-xs-left" >
                <div class="field-title">Description</div>
                <v-textarea
                    v-model.trim="description"
                    class="text__collab-design"
                    auto-grow
                    outline
                    rows="5"
                ></v-textarea>
            </v-flex>
            <v-flex xs12 class="text-xs-left" >
                <div class="field-group-title">Price</div>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left" >
                <div class="field-title">Week</div>
                <v-text-field
                    v-model="weekly_rate"
                    class="text__collab-design"
                    outline
                    :error-messages="weeklyRateErrors"
                    @input="$v.weekly_rate.$touch()"
                    @blur="$v.weekly_rate.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left" >
                <div class="field-title">Month</div>
                <v-text-field
                    v-model="monthly_rate"
                    class="text__collab-design"
                    outline
                    :error-messages="monthlyRateErrors"
                    @input="$v.monthly_rate.$touch()"
                    @blur="$v.monthly_rate.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left" >
                <div class="field-title">Year</div>
                <v-text-field
                    v-model="yearly_rate"
                    class="text__collab-design"
                    outline
                    :error-messages="yearlyRateErrors"
                    @input="$v.yearly_rate.$touch()"
                    @blur="$v.yearly_rate.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left" >
                <div class="field-title">Currency</div>
                <v-select
                    v-model="currency"
                    :items="currencies"
                    class="select__collab-design"
                    outline
                    item-text="label"
                    item-value="id"
                ></v-select>
            </v-flex>
            <v-flex xs12 class="text-xs-center" >
                <v-btn class="button__collab-design--dark" @click="submit" :loading="isLoadingTeacherMembership" :disabled="isLoadingTeacherMembership">Save</v-btn>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
import utils from '@/lib/utils.js'
import {mapState, mapActions} from 'vuex';
import { validationMixin } from 'vuelidate'
import { numeric, required } from 'vuelidate/lib/validators'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import UploadPopup from '@/components/basic/UploadPopup'

export default {
    name: 'DashboardTeachMembershipSetUp',
    mixins: [validationMixin],
    validations: {
        weekly_rate: {numeric},
        monthly_rate: {numeric},
        yearly_rate: {numeric},
        name: {required},
    },
    components: {
        ImageUploadCrop,
        UploadPopup,
    },
    data: () => ({
        currency: 'usd',
        currencies: utils.getCurrencyList(),
        weekly_rate: null,
        monthly_rate: null,
        yearly_rate: null,
        name: '',
        description: '',
        isDirectoryEnabled: false,
        isDMEnabled: false,
        isChatEnabled: false,
        isUploadAllowed: false,
        isUploadRequired: false,
        isAboutAllowed: false,
        isAboutRequired: false,
        isTitleAllowed: false,
        isTitleRequired: false,
        isCityAllowed: false,
        isCityRequired: false,
        isProjectsAllowed: false,
        isProjectsRequired: false,
        isSocialAllowed: false,
        isSocialRequired: false,
        isPhoneAllowed: false,
        isPhoneRequired: false,
        isEmailAllowed: false,
        isEmailRequired: false,
        isDocumentAllowed: false,
        isDocumentRequired: false,
        customInterestsField: '',
        customSkillsField: '',
        customLevelsField: '',
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
                this.isDirectoryEnabled = this.teacherMembership.isDirectoryEnabled
                this.isDMEnabled = this.teacherMembership.isDMEnabled
                this.isChatEnabled = this.teacherMembership.isChatEnabled
                this.isUploadAllowed = this.teacherMembership.isUploadAllowed
                this.isUploadRequired = this.teacherMembership.isUploadRequired
                this.isAboutAllowed = this.teacherMembership.isAboutAllowed
                this.isAboutRequired = this.teacherMembership.isAboutRequired
                this.isTitleAllowed = this.teacherMembership.isTitleAllowed
                this.isTitleRequired = this.teacherMembership.isTitleRequired
                this.isCityAllowed = this.teacherMembership.isCityAllowed
                this.isCityRequired = this.teacherMembership.isCityRequired
                this.isProjectsAllowed = this.teacherMembership.isProjectsAllowed
                this.isProjectsRequired = this.teacherMembership.isProjectsRequired
                this.isSocialAllowed = this.teacherMembership.isSocialAllowed
                this.isSocialRequired = this.teacherMembership.isSocialRequired
                this.isPhoneAllowed = this.teacherMembership.isPhoneAllowed
                this.isPhoneRequired = this.teacherMembership.isPhoneRequired
                this.isEmailAllowed = this.teacherMembership.isEmailAllowed
                this.isEmailRequired = this.teacherMembership.isEmailRequired
                this.isDocumentAllowed = this.teacherMembership.isDocumentAllowed
                this.isDocumentRequired = this.teacherMembership.isDocumentRequired
                this.customInterestsField = this.teacherMembership.customInterestsField
                this.customSkillsField = this.teacherMembership.customSkillsField
                this.customLevelsField = this.teacherMembership.customLevelsField
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
                isDirectoryEnabled: this.isDirectoryEnabled,
                isDMEnabled: this.isDMEnabled,
                isChatEnabled: this.isChatEnabled,
                isUploadAllowed: this.isUploadAllowed,
                isUploadRequired: this.isUploadRequired,
                isAboutAllowed: this.isAboutAllowed,
                isAboutRequired: this.isAboutRequired,
                isTitleAllowed: this.isTitleAllowed,
                isTitleRequired: this.isTitleRequired,
                isCityAllowed: this.isCityAllowed,
                isCityRequired: this.isCityRequired,
                isProjectsAllowed: this.isProjectsAllowed,
                isProjectsRequired: this.isProjectsRequired,
                isSocialAllowed: this.isSocialAllowed,
                isSocialRequired: this.isSocialRequired,
                isPhoneAllowed: this.isPhoneAllowed,
                isPhoneRequired: this.isPhoneRequired,
                isEmailAllowed: this.isEmailAllowed,
                isEmailRequired: this.isEmailRequired,
                isDocumentAllowed: this.isDocumentAllowed,
                isDocumentRequired: this.isDocumentRequired,
                customInterestsField: this.customInterestsField,
                customSkillsField: this.customSkillsField,
                customLevelsField: this.customLevelsField,
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
        submit () {
            this.$v.$touch()
            console.log('submit')
            if (this.$v.$anyError)
                return
            this.save().then(() => {
                console.log('saved');
            }).catch((err) => {
                console.log('error', err);
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
        onUploadSuccess() {
            console.log('uploaded');
        },
    },
}
</script>
<style lang="scss">
@import "../../../styles/variables";
.membership-section-layout {
    .field-group-title {
        font-weight: 500;
        font-size: 20px;
        line-height: 25px;
    }
    .field-title {
        font-weight: 500;
        font-size: 16px;
        line-height: 22px;
    }
    margin-bottom: 3px;
    &> div {
        padding: 20px;
    }
    .checkbox-row {
        display: flex;
        flex-flow: row nowrap;
        align-items: flex-end;
        .add-cell {
            flex: 0 0 90px;
        }
        .require-cell {
            flex: 0 0 90px;
        }
        .label-cell {
            flex: 1 0 auto;
        }
    }
    .enablement-container {
        display: flex;
        flex-flow: row nowrap;
        .switch-item {
            flex: 0 0 150px;
            display: flex;
            flex-flow: row nowrap;
            align-items: center;
            .switch-label {
                padding-right: 1em;
            }
        }
    }
    .custom-field-row {
        display: flex;
        flex-flow: row nowrap;
        align-items: center;
        padding: 8px 0;
        .custom-field-name {
            flex: 0 0 120px;
        }
        .custom-field-label {
            height: 32px;
            background: #FFFFFF;
            border: 1px solid #D9D9D9;
            box-shadow: 0px 2px 0px rgba(0, 0, 0, 0.016);
            border-radius: 2px;
            display: flex;
            flex-flow: row nowrap;
            align-items: center;
            justify-content: center;
        }
        .custom-field-value {
            padding-left: 15px;
            flex: 1 0 auto;
        }
    }
}
.vert-divider {
    position: absolute;
    height: 3px;
    left: 0;
    right: 0;
    background-color: white;
}
.upload-options-container {
    display: flex;
    flex-flow: row nowrap;
    justify-content: flex-start;
    .upload-option {
        padding-right: 40px;
    }
}
</style>