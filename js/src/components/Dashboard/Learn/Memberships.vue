<template>
    <v-layout align-center justify-center row wrap>
        <v-flex xs12 class="text-xs-left class-list">
            <h3>Memberships</h3>
        </v-flex>
        <v-flex xs12>
            <v-progress-circular
              v-if="isLoading"
              indeterminate
              color="grey"
            ></v-progress-circular>
        </v-flex>
      <v-flex xs12 class="text-xs-left class-list">
        <v-list three-line class="full-height-list">
          <template v-for="(item, index) in membershipList">
            <v-list-tile
              :key="item.id"
              avatar
              ripple
            >
              <v-list-tile-avatar :tile="true" class="hidden-sm-and-down">
                <img v-if="item.media" :src="item.media">
              </v-list-tile-avatar>
              <v-list-tile-content style="min-height: 96px;">
                <v-list-tile-title>
                    <b>{{item.name}} </b>
                    <router-link :to="item.providerUrl">{{ item.providerName }}</router-link>,
                </v-list-tile-title>

                <v-list-tile-sub-title>
                    <div class="description">{{ item.description }}</div>
                </v-list-tile-sub-title>
              </v-list-tile-content>
              <v-list-tile-action style="min-width: 96px;">
                  <div v-if="item.isMember && !item.isDeactivated" style="text-align: right">
                      <v-chip color="platform-green" text-color="white">
                          <v-avatar>
                            <v-icon>check_circle</v-icon>
                          </v-avatar>
                          Member
                      </v-chip>
                      <div>
                          <v-btn @click="confirmCancelMembership(item.student_membership_id)">Cancel</v-btn>
                      </div>
                  </div>
                  <div  v-else-if="item.isMember && item.isDeactivated" style="text-align: right">
                      <v-chip color="platform-green" text-color="white">
                        Canceled
                      </v-chip>
                      <div>Active until<br/>{{ item.endAt }}</div>
                  </div>
                  <v-btn v-else :to="`/buy-membership/${item.id}?return=${$route.path}`">Buy</v-btn>
              </v-list-tile-action>
            </v-list-tile>
            <v-divider
              v-if="index + 1 < membershipList.length"
            ></v-divider>
          </template>
        </v-list>
      </v-flex>
        <base-confirm-action
            :is-loading="isLoading"
            :is-opened="isCancelConfirmOpened"
            @cancel="onCloseCancel"
            @confirm="onConfirmCancel"
        >
            <div>Your membership will be canceled after current payment period ends: {{ cancelMembershipAfter }}</div>
        </base-confirm-action>
    </v-layout>
</template>

<script>
import axios from 'axios'
import { mapMutations } from 'vuex';
import BaseConfirmAction from '@/components/basic/BaseConfirmAction';

export default {
    name: 'dashboard_learn_memberships',
    components: {
        BaseConfirmAction,
    },
    data: () => ({
        isLoading: false,
        isCancelConfirmOpened: false,
        cancelMembershipAfter: '',
        confirmingCancellationID: null,
        memberships: [],
    }),
    props: [],
    created() {
        this.reload()
    },
    computed: {
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
        }
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
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
        cancelMembership(id) {
            this.isLoading = true
            return axios.post('/api/stripe/cancel_membership/', {
                student_membership_id: id,
            }).then(res => {
                if (!res.data.success) {
                    this.setGlobalError(res.data.error_message);
                    return;
                }
                const memberships = [
                    ...(this.$store.state.user.memberships || []).filter(m => m.id !== id),
                    res.data.student_membership,
                ];
                this.$store.commit('setUser', {
                    ...this.$store.state.user,
                    memberships,
                });
            }).catch(e => {
                console.log(e)
            }).then(() => {
                this.isLoading = false
            })
        },
        confirmCancelMembership(id) {
            this.confirmingCancellationID = id;
            const studentMembership = this.$store.state.user.memberships.find(v => v.id === id);
            this.cancelMembershipAfter = new Date(studentMembership.current_period_end * 1000).toLocaleString('en-us', {month: 'long', day: 'numeric', year: '2-digit'});
            this.isCancelConfirmOpened = true;
        },
        onCloseCancel() {
            this.isCancelConfirmOpened = false;
        },
        onConfirmCancel() {
            this.cancelMembership(this.confirmingCancellationID).then(() => {
                this.isCancelConfirmOpened = false;
                this.confirmingCancellationID = null;
            });
        },
    },

    watch: {

    }
}
</script>
<style lang="scss" scoped>
.action-button {
    padding: 0.5em;
}
</style>