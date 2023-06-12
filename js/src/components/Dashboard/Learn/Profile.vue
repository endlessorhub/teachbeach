<template>
    <div class="client-profile-container">
        <v-layout v-if="currentMembership && currentMembershipSetting" class="client-profile-layout" align-start justify-start row wrap>
            <v-flex xs12 class="text-xs-center" >
                <div class="title">Profile Set-Up</div>
            </v-flex>
            
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">First Name</div>
                <v-text-field
                    v-model="firstName"
                    class="text__collab-design"
                    outline
                    :error-messages="firstNameErrors"
                    @input="$v.firstName.$touch()"
                    @blur="$v.firstName.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Last Name</div>
                <v-text-field
                    v-model="lastName"
                    class="text__collab-design"
                    outline
                    :error-messages="lastNameErrors"
                    @input="$v.lastName.$touch()"
                    @blur="$v.lastName.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex v-if="currentMembershipSetting.isEmailAllowed" xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Email Address</div>
                <v-text-field
                    v-model="email"
                    class="text__collab-design"
                    outline
                    :error-messages="emailErrors"
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex v-if="currentMembershipSetting.isPhoneAllowed" xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Phone Number</div>
                <v-text-field
                    v-model="phone"
                    class="text__collab-design"
                    outline
                    :error-messages="phoneErrors"
                    @input="$v.phone.$touch()"
                    @blur="$v.phone.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex v-if="currentMembershipSetting.isUploadAllowed" xs12 md3 class="text-xs-left">
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
            <v-flex v-if="currentMembershipSetting.isAboutAllowed" xs12 md9 class="text-xs-left" >
                <div class="field-title">About me</div>
                <v-textarea
                    v-model.trim="description"
                    class="text__collab-design"
                    auto-grow
                    outline
                    rows="5"
                ></v-textarea>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Title</div>
                <v-text-field
                    v-model="title"
                    class="text__collab-design"
                    outline
                    :error-messages="titleErrors"
                    @input="$v.title.$touch()"
                    @blur="$v.title.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">City</div>
                <v-text-field
                    v-model="city"
                    class="text__collab-design"
                    outline
                    :error-messages="cityErrors"
                    @input="$v.city.$touch()"
                    @blur="$v.city.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Document</div>
                <v-text-field
                    v-model="document"
                    class="text__collab-design"
                    outline
                    :error-messages="documentErrors"
                    @input="$v.document.$touch()"
                    @blur="$v.document.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Social</div>
                <v-text-field
                    v-model="social"
                    class="text__collab-design"
                    outline
                    :error-messages="socialErrors"
                    @input="$v.social.$touch()"
                    @blur="$v.social.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex v-if="currentMembershipSetting.isProjectsAllowed" xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Website</div>
                <v-text-field
                    v-model="website"
                    class="text__collab-design"
                    outline
                    :error-messages="websiteErrors"
                    @input="$v.website.$touch()"
                    @blur="$v.website.$touch()"
                ></v-text-field>
            </v-flex>
            <v-flex xs12 md9 class="text-xs-left" >
                <div class="field-title multifield-title">Select all that apply</div>
                <div class="select-container">
                    <div class="select-in-row">
                        <div class="field-title">Interests</div>
                        <v-select
                            v-model="interest"
                            :items="interests"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                    <div class="select-in-row">
                        <div class="field-title">Skills</div>
                        <v-select
                            v-model="skill"
                            :items="skills"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                    <div class="select-in-row">
                        <div class="field-title">Levels</div>
                        <v-select
                            v-model="level"
                            :items="levels"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                </div>
            </v-flex>
            <v-flex xs12 class="text-xs-center" >
                <v-btn class="button__collab-design--dark" @click="submit" :loading="isLoading" :disabled="isLoading">Save</v-btn>
            </v-flex>
        </v-layout>
        <v-progress-circular v-else-if="isLoading"></v-progress-circular>
        <div v-else></div>
    </div>
</template>

<script>
import axios from 'axios'
import utils from '@/lib/utils.js'
import {mapState, mapActions, mapGetters, mapMutations} from 'vuex';
import { validationMixin } from 'vuelidate'
import { numeric, required, url, maxLength, email } from 'vuelidate/lib/validators'
import ImageUploadCrop from '@/components/basic/ImageUploadCrop'
import UploadPopup from '@/components/basic/UploadPopup'

export default {
    name: 'LearnerProfile',
    mixins: [validationMixin],
    validations: {
        firstName: { required, maxLength: maxLength(64) },
        lastName: { required, maxLength: maxLength(64) },
        email: { email },
        phone: { maxLength: maxLength(20) },
        website: { url },
        title: { maxLength: maxLength(64) },
        city: { maxLength: maxLength(64) },
        document: { maxLength: maxLength(64) },
        social: { maxLength: maxLength(64) },
    },
    components: {
        ImageUploadCrop,
        UploadPopup,
    },
    data: () => ({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        title: '',
        city: '',
        document: '',
        social: '',
        website: '',
        description: '',
        level: '',
        skill: '',
        interest: '',
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
        memberships: [],
        selectedMembership: null,
    }),
    created() {
        this.reload()
        this.firstName = this.user.first_name;
        this.lastName = this.user.last_name;
        this.phone = this.user.phone;
        this.email = this.user.email;
    },
    computed: {
        ...mapGetters('learnerMembership', [
            'isLoading',
            'currentMembership',
            'currentMembershipSetting',
        ]),
        ...mapState(['user']),
        emailErrors () {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isEmailAllowed
                && this.currentMembershipSetting.isEmailRequired
                && !this.email) errors.push('E-mail is required')
            return errors
        },
        firstNameErrors () {
            const errors = []
            if (!this.$v.firstName.$dirty) return errors
            !this.$v.firstName.maxLength && errors.push('Name must be at most 64 characters long')
            !this.$v.firstName.required && errors.push('Name is required.')
            return errors
        },
        lastNameErrors () {
            const errors = []
            if (!this.$v.lastName.$dirty) return errors
            !this.$v.lastName.maxLength && errors.push('Last Name must be at most 64 characters long')
            !this.$v.lastName.required && errors.push('Last Name is required.')
            return errors
        },
        phoneErrors () {
            const errors = []
            if (!this.$v.phone.$dirty) return errors
            !this.$v.phone.maxLength && errors.push('Phone must be at most 20 characters long')
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isPhoneAllowed
                && this.currentMembershipSetting.isPhoneRequired
                && !this.phone) errors.push('Phone is required')
            return errors
        },
        websiteErrors () {
            const errors = []
            if (!this.$v.website.$dirty) return errors
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isProjectsAllowed
                && this.currentMembershipSetting.isProjectsRequired
                && !this.website) errors.push('Website is required')
            !this.$v.website.url && errors.push('Website should be a valid url.')
            return errors
        },
        titleErrors () {
            const errors = []
            if (!this.$v.title.$dirty) return errors
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isTitleAllowed
                && this.currentMembershipSetting.isTitleRequired
                && !this.title) errors.push('Title is required')
            return errors
        },
        cityErrors () {
            const errors = []
            if (!this.$v.city.$dirty) return errors
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isCityAllowed
                && this.currentMembershipSetting.isCityRequired
                && !this.city) errors.push('City is required')
            return errors
        },
        socialErrors () {
            const errors = []
            if (!this.$v.social.$dirty) return errors
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isSocialAllowed
                && this.currentMembershipSetting.isSocialRequired
                && !this.social) errors.push('Social is required')
            return errors
        },
        documentErrors () {
            const errors = []
            if (!this.$v.document.$dirty) return errors
            if (this.currentMembershipSetting 
                && this.currentMembershipSetting.isDocumentAllowed
                && this.currentMembershipSetting.isDocumentRequired
                && !this.document) errors.push('Document is required')
            return errors
        },
        existingMembershipsDict() {
            return (this.$store.state.user.memberships || [])
                .sort((a, b) => a.id - b.id)
                .reduce((acc, m) => ({...acc, [m.membership]: m}), {})
        },
        membershipList() {
            let res = []
            return this.memberships.map((m) => ({
                ...m,
                providerName: m.owner.is_company ? m.owner.company_profile.name : `${m.owner.teacher.first_name} ${m.owner.teacher.last_name}`,
                providerUrl: m.owner.is_company ? `/company_profile/${m.owner.company_profile.id}` : `/teacher_profile/${m.owner.teacher.id}`,
                isMember: !!(this.existingMembershipsDict[m.id] && new Date().getTime() < this.existingMembershipsDict[m.id].current_period_end * 1000),
                isDeactivated: !!(this.existingMembershipsDict[m.id] && this.existingMembershipsDict[m.id].deactivated_at),
                endAt: new Date(this.existingMembershipsDict[m.id] && this.existingMembershipsDict[m.id].current_period_end * 1000).toLocaleString('en-us', {month: 'long', day: 'numeric'}),
                student_membership_id: this.existingMembershipsDict[m.id] && this.existingMembershipsDict[m.id].id,
            })).sort((a, b) => (b.isMember - a.isMember));
        },
        membershipsOptions() {
            return this.memberships.map((m) => ({
                text: m.owner.is_company ? m.owner.company_profile.name : `${m.owner.teacher.first_name} ${m.owner.teacher.last_name}`,
                value: m.id,
            }));
        },
        interests() {
            return this.currentMembershipSetting ? this.currentMembershipSetting.customInterestsField.split(',') || [] : []
        },
        skills() {
            return this.currentMembershipSetting ? this.currentMembershipSetting.customSkillsField.split(',') || [] : []
        },
        levels() {
            return this.currentMembershipSetting ? this.currentMembershipSetting.customLevelsField.split(',') || [] : []
        },
    },
    methods: {
        ...mapMutations(['setUser']),
        ...mapActions('learnerMembership', [
            'loadMemberships',
            'saveMembership',
        ]),
        reload() {
            this.loadMemberships();
        },
        submit () {
            this.$v.$touch()
            console.log('submit')
            if (this.$v.$anyError)
                return
            const data = {
                student_membership_id: this.currentMembership.id,
                firstName: this.firstName,
                lastName: this.lastName,
                email: this.email,
                phone: this.phone,
                title: this.title,
                city: this.city,
                document: this.document,
                social: this.social,
                website: this.website,
                description: this.description,
                level: this.level,
                skill: this.skill,
                interest: this.interest,
            };
            this.saveMembership(data).then(() => {
                const user = {...this.user};
                user.first_name = data.firstName;
                user.last_name = data.lastName;
                user.phone = data.phone;
                user.email = data.email;
                this.setUser(user);
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
    },
    watch: {
        currentMembership: {
            immediate: true,
            handler(val) {
                this.title = val && val.title;
                this.city = val && val.city;
                this.document = val && val.document;
                this.social = val && val.social;
                this.website = val && val.website;
                this.description = val && val.description;
                this.level = val && val.level;
                this.skill = val && val.skill;
                this.interest = val && val.interest;
            },
        },
    },
}
</script>
<style lang="scss">
@import "../../../styles/variables";
.client-profile-layout {
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
    &> div {
        padding: 20px;
    }
    .select-container {
        display: flex;
        flex-flow: row nowrap;
        gap: 10px;
        .select-in-row {
            flex: 0 0 auto;
            .v-label {
                margin-top: -10px;
            }
        }
    }
    .multifield-title {
        height: 0;
        margin-top: -1em;
        margin-bottom: 1em;
    }
}
</style>