<template>
<div class="email-upsell-page">
    <v-container grid-list-md text-xs-center>
        <v-layout align-top justify-center row wrap>
            <v-flex xs1 >
                <v-icon x-large>email</v-icon>
            </v-flex>
            <v-flex xs11 class="text-xs-left">
                <h3>Targeted Email boost:</h3>
                <div class="description-text">Send your class promotion to 20,000 emails with an open rate of 2000 to 4000 and 200 to 400 clicks to your class page for $350.</div>
            </v-flex>
            <v-flex xs12 class="text-xs-right">
                <CreditCards v-if="showCreditCard"
                     :payment-options="{class_id: class_id}"
                     :cancel-btn="true"
                     url="/api/buy_email_boost"
                     successBtnText="Done"
                     @cardAdded="submit"
                     @cancel="cancel" />
                <v-btn v-if="!showCreditCard" @click="cancel" :disabled="isLoading">No, thanks</v-btn>
                <v-btn v-if="!showCreditCard" @click="submit" :loading="isLoading" :disabled="isLoading || !activeOption" color="platform-green">ADD</v-btn>
            </v-flex>
            <v-flex xs12 class="text-xs-right">
              <v-carousel
                :height="gHeight"
              >
                <v-carousel-item
                  v-for="(img, i) in upsellImages"
                  :key="i"
                >
                    <v-img :src="`${img}`" style="margin:auto;"  />
                </v-carousel-item>
              </v-carousel>
            </v-flex>
        </v-layout>
    </v-container>
</div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import utils from '@/lib/utils.js'
import metadata from '@/mixins/metadata'
import CreditCards from '@/components/basic/CreditCards'

export default {
    mixins: [metadata],
    props: {
        class_id: Number,
    },
    components: {
        CreditCards,
    },
    data: () => ({
        isLoading: false,
        showCreditCard: true,
        width: window.innerWidth,
    }),

    created() {
        window.addEventListener('resize', this.updateWidth);
    },

    beforeDestroy() {
        window.removeEventListener('resize', this.updateWidth);
    },

    computed: {
        gHeight() {
            return this.width/2
        },
        activeOption() {
            return this.options.length ? this.options[0] : null
        },
        upsellImages() {
            return [1,2,3].map(n => require(`@/assets/eupsell_${n}.png`))
        },
    },

    methods: {
        submit(id) {
            console.log('submit', id)
            //this.$router.push(`/teacher_checkout/${id}`)
            //this.$router.push(`/teacher_checkout/${this.activeOption.id+100}/${this.class_id}`)
            setTimeout(() => this.$router.push('/dashboard/teach/classes'), 1000)
        },
        cancel() {
            this.$router.push('/dashboard/teach/classes')
        },
        updateWidth() {
            this.width = window.innerWidth
        },
    },
}
</script>

<style lang="scss">
.email-upsell-page {
    h3 {
        font-size: 34px;
    }
    .description-text {
        text-align: left;
        font-size: 20px;
    }
    .v-carousel__prev, .v-carousel__next {
        opacity: 0.7;
        background-color: silver;
        border-radius: 50%;
    }
}

</style>