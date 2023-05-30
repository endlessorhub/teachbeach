<template>
<div class="choose-model-page">
    <v-container grid-list-md text-xs-center>
        <h3>Choose a plan that fits your business:</h3>
        <h3>Revenue share or membership</h3>

      <v-layout align-center justify-center row wrap style="align-items: stretch;">
          <v-flex xs12 sm5 class="text-xs-center">
            <v-card :class="choosedOption === 'membership' ? 'text-xs-left active' : 'text-xs-left available'" @click="choosedOption = 'membership'">
                <v-card-title class="subheader">
                    Membership
                </v-card-title>

                <v-card-text>
                    <ul>
                        <li>Keep 100% of revenues</li>
                        <li>Students pay card processing</li>
                        <li>Classes distributed free to local media and 42 local online event listings</li>
                        <li>Custom marketing add-ons discounted</li>
                        <li>Live support</li>
                        <li>From $48 month</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs12 sm1 class="text-xs-center or">
              <div>OR</div>
          </v-flex>

          <v-flex xs12 sm5 class="text-xs-center">
            <v-card :class="choosedOption === 'revenue' ? 'text-xs-left active' : 'text-xs-left available'" @click="choosedOption = 'revenue'">
                <v-card-title class="subheader">
                    Revenue Share
                </v-card-title>

                <v-card-text>
                    <ul>
                        <li>Pay a la Carte to submit classes to local media and 42 online event listings</li>
                        <li>Live support</li>
                    </ul>
                </v-card-text>
            </v-card>
          </v-flex>

          <v-flex xs12 class="text-xs-right">
            <v-btn @click="submit" :loading="isLoading" :disabled="isLoading" color="platform-green">GO</v-btn>
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

export default {
    props: {
        class_id: Number,
    },
    mixins: [metadata],
    data: () => ({
        isLoading: false,
        choosedOption: 'membership',
    }),

    created: function () {

    },

    computed: {

    },

    methods: {
        submit(id) {
            console.log('submit', id)
            if(this.choosedOption === 'membership') {
                this.$router.push(this.class_id ? `/join_as_member/${this.class_id}` : '/join_as_member')
            } else {
                this.$router.push(this.class_id ? `/email_upsell/${this.class_id}` : '/email_upsell')
            }
        },
        cancel() {
            console.log('cancel')
        }
    }
}
</script>

<style scoped lang="scss">
.choose-model-page {
    li {
        font-size: 20px;
    }
    h3 {
        font-size: 34px;
        text-align: center;
    }
    .subheader {
        font-size: 24px;
        font-weight: bold;
        padding-bottom: 0;
    }
    .or {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .active {
        background-color: rgba(151, 214, 43, 0.2);
        border: 2px solid rgba(151, 214, 43, 1);
        margin: 0;
        height: 100%;
        font-size: 14px;
    }
    .available {
        cursor: pointer;
        margin: 2px;
        height: 100%;
        font-size: 14px;
    }
}
</style>