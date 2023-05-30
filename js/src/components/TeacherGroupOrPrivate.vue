<template>
  <form>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
    <v-container grid-list-md text-xs-center>
      <v-layout align-top justify-center row wrap>
        <v-flex xs12 class="text-xs-left">
            <h3>Your first sessions will be:</h3>
            <v-radio-group v-model="teacherLessonType" hide-details>
              <v-radio color="primary" label="Private.  Students let you know what they want to learn, one on one." value="private"></v-radio>
              <v-radio color="primary" label="Group or Premium Community. You will set the time/s and location for the meeting/s in advance." value="group"></v-radio>
            </v-radio-group>
            <v-checkbox
              v-if="teacherLessonType === 'group'"
              v-model="isPremiumCommunity"
              hide-details
            >
                <template v-slot:label>
                    Set up a  premium community
                    <info-tooltip activator-event="hover">A premium community is a group associated with one instructor (a coach or team leader)  with  that meets regularly for a defined period  and has other benefits, such as coaching, private messaging and more. Memberships auto renew, and can be used to set discounts for communities, group and private sessions. </info-tooltip>
                </template>
            </v-checkbox>
            <v-checkbox
              v-model="shouldCreateMembership"
              :label="membershipOptionLabel"
              hide-details
            ></v-checkbox>
            <div style="width: 200px;">
            <v-text-field
              v-model="promoCode"
              label="Promo code"
              outline
            ></v-text-field>
            </div>
        </v-flex>

      </v-layout>
    </v-container>
    <v-btn @click="back">Back</v-btn>
    <v-btn @click="submit" :loading="isLoading" :disabled="isLoading">Next</v-btn>
  </form>
</template>

<script>
import { mapGetters } from 'vuex'
import InfoTooltip from '@/components/basic/InfoTooltip'

export default {
    props: ['hasAvatar'],
    components: {
        InfoTooltip,
    },
    data: () => ({
        isLoading: false,
        teacherLessonType: 'group',
        shouldCreateMembership: false,
        isPremiumCommunity: false,
        promoCode: '',
    }),

    created: function () {
        let _this = this
        if (this.$store.state.teacherLessonType) {
            this.teacherLessonType = _this.$store.state.teacherLessonType
        }
        this.shouldCreateMembership = _this.$store.state.teacherCreateMembership
        if (this.$store.state.teacherGroupClass) {
            this.isPremiumCommunity = this.$store.state.teacherGroupClass.isPremiumCommunity
        }
    },

    computed: {
        ...mapGetters([
            'haveMembership',
        ]),
        membershipOptionLabel() {
            return this.haveMembership ? 'Edit membership' : 'Add membership first?'
        },
    },

    methods: {
        back() {
            this.save()
            this.$emit('prev:step')
        },
        submit () {
            this.save()
            this.$emit('next:step')
        },
        save() {
            this.$store.commit('setTeacherLessonType', this.teacherLessonType)
            this.$store.commit('setCreateMembership', this.shouldCreateMembership)
            this.$store.commit('setGroupClass', {
                isPremiumCommunity: this.isPremiumCommunity,
            });
        },
        clear () {

        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>