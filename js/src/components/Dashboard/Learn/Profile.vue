<template>
    <div class="client-profile-container">
        <v-layout class="client-profile-layout" align-start justify-start row wrap>
            <v-flex xs12 class="text-xs-center" >
                <div class="title">Profile Set-Up</div>
            </v-flex>
            
            <v-flex xs12 md6 lg3 class="text-xs-left">
                <div class="field-title">Name</div>
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
            <v-flex xs12 md6 lg3 class="text-xs-left">
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
            <v-flex xs12 md6 lg3 class="text-xs-left">
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
                <div class="field-title">About me</div>
                <v-textarea
                    v-model.trim="description"
                    class="text__collab-design"
                    auto-grow
                    outline
                    rows="5"
                ></v-textarea>
            </v-flex>
            <v-flex xs12 class="text-xs-left" >
                <v-select
                    class="select__collab-design"
                    label="Member of"
                    :items="membershipsOptions"
                ></v-select>
            </v-flex>
            <v-flex xs12 md6 lg3 class="text-xs-left">
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
                <div class="field-title">Interest-matching: Select all that apply</div>
                <div class="select-container">
                    <div class="select-in-row">
                        <v-select
                            v-model="interest"
                            :items="interests"
                            label="Interest"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                    <div class="select-in-row">
                        <v-select
                            v-model="skill"
                            :items="skills"
                            label="Skills"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                    <div class="select-in-row">
                        <v-select
                            v-model="level"
                            :items="levels"
                            label="Level"
                            class="select__collab-design"
                            outline
                        ></v-select>
                    </div>
                </div>
            </v-flex>
            <v-flex xs12 class="text-xs-center" >
                <v-btn class="button__collab-design--dark" @click="submit" :loading="isLoadingTeacherMembership" :disabled="isLoadingTeacherMembership">Save</v-btn>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
import axios from 'axios'
import utils from '@/lib/utils.js'
import {mapState, mapActions} from 'vuex';
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
        email: { required, email },
        phone: { required, maxLength: maxLength(20) },
        website: { url },
    },
    components: {
        ImageUploadCrop,
        UploadPopup,
    },
    data: () => ({
        isLoading: false,
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        imageName: '',
        imageUrl: '',
		imageFile: '',
        crop: {},
        memberships: [],
    }),
    created() {
        this.reload()
    },
    computed: {
        emailErrors () {
            const errors = []
            if (!this.$v.email.$dirty) return errors
            !this.$v.email.email && errors.push('Must be valid e-mail')
            !this.$v.email.required && errors.push('E-mail is required')
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
            !this.$v.phone.required && errors.push('Phone is required')
            return errors
        },
        websiteErrors () {
            const errors = []
            if (!this.$v.website.$dirty) return errors
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
    },
    methods: {
        reload() {
            this.isLoading = true
            axios.get('/api/memberships/').then(res => {
                this.memberships = res.data.memberships
            }).catch(e => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
            })
        },
        save() {
            
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
        flex-flow: row wrap;
        gap: 10px;
        .select-in-row {
            flex: 1 0 auto;
            .v-label {
                margin-top: -10px;
            }
        }
    }
}
</style>