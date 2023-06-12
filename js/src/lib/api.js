import axios from 'axios'
import _ from 'lodash'

export default {
    async getUserSettings() {
        return axios.get('/api/user_settings/')
            .then(res => res.data.settings || {})
    },
    async setUserSettings(data) {
        return axios.post('/api/user_settings/', {settings: data})
    },
    async updateUserSettings(data) {
        const settings = await this.getUserSettings()
        const toSave = _.merge({}, settings, data)
        return this.setUserSettings(toSave).catch((e) => {
            return Promise.reject(settings)
        }).then(() => {
            return toSave
        })
    },
    async getCompanyProfile(companyId) {
        return axios.get(`/api/company_profile/${companyId}/`).then(res => res.data)
    },
    async sendTeacherRequest(data) {
        return axios.post(`/api/company_teacher_request/`, data);
    },
    async getTeacherCalendarData(teacherId) {
        return axios.get(`/api/teacher_profile/${teacherId}/`).then(res => res.data)
    },
    async getCompanyCalendarData(companyId) {
        return axios.get(`/api/company_profile/${companyId}/`).then(res => res.data)
    },
    async saveSyncCalendar(providerType, providerId, events) {
        return axios.post('/api/external_calendar/', {
            provider_type: providerType,
            provider_id: providerId,
            events,
        })
    },
    async getSyncCalendar() {
        return axios.get(`/api/external_calendar/`).then(res => res.data)
    },
    async teacherCancelPrivateEnrollments(enrollmentIds, message) {
        return axios.post(`/api/teacher_cancel_private_erollment`, {
            enrollment_ids: enrollmentIds,
            message,
        });
    },
    async getLearnerMemberships() {
        return axios.get(`/api/learner_memberships/`).then(res => res.data)
    },
    async saveLearnerMembership(data) {
        return axios.post(`/api/learner_memberships/`, data).then(res => res.data)
    },
}