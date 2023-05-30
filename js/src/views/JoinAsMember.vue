<template>
<div class="join-as-member-page">
    <v-container grid-list-md text-xs-center>
        <v-layout align-center justify-center row wrap>
          <v-flex xs1>
              <v-icon x-large>fas fa-rocket</v-icon>
          </v-flex>
          <v-flex xs11>
            <div v-if="currentOption.id">
                <h3>Free until July</h3>
                <ul style="text-align: left;">
                    <li>
                        Your current plan is <b>{{currentOptionName}}</b>
                    </li>
                    <li>
                        Please upgrade your membership to submit more classes to 42 local media and event listings.
                    </li>
                </ul>
            </div>
            <div v-else-if="canBook">
                <h3>Boost classes free until July, no credit card required! Save hours, get free promotion!</h3>
                <ul style="text-align: left;">
                    <li>
                        Select # of Classes to boost, click next
                    </li>
                    <li>
                        Click on the green rocket to select which classes to boost
                    </li>
                    <li>
                        Teachbeach submits your classes to 42 local media and online event Calendars (see a partial list below)
                    </li>
                </ul>
            </div>
            <div v-else>
                <h3>Boost classes free until July, no credit card required! Save hours, get free promotion!</h3>
                <ul style="text-align: left;">
                    <li>
                        Select # of Classes to boost, click next
                    </li>
                    <li>
                        Click on the green rocket to select which classes to boost
                    </li>
                    <li>
                        Teachbeach submits your classes to 42 local media and online event Calendars (see a partial list below)
                    </li>
                </ul>
            </div>
          </v-flex>
        </v-layout>

      <v-layout v-if="optionsPrepared.length" align-center justify-center row wrap>
          <v-flex v-for="option in optionsPrepared" xs12 sm4 class="text-xs-center shrinked" :key="option.id">
            <v-card :class="option.cardClass" @click="chooseOption(option.id)">
                <v-card-title class="subheader">
                    {{option.title}}
                </v-card-title>

                <v-card-text>
                    <div class="line1">{{option.line1}}</div>
                    <div class="line2">{{option.line2}}</div>
                </v-card-text>

            </v-card>
          </v-flex>
          <v-flex xs12 class="text-xs-left shrinked">
            <v-checkbox
              v-model="choosedOption"
              :value="singleId"
              :label="singleOptionName"
            ></v-checkbox>
          </v-flex>
          <v-flex xs12 sm6 class="text-xs-center shrinked">
            <v-btn @click="cancel" :loading="isLoading" :disabled="isLoading">No, thanks</v-btn>
          </v-flex>
          <v-flex xs12 sm6 class="text-xs-center shrinked">
            <v-btn @click="submit(choosedOption)" :loading="isLoading" :disabled="isLoading || !choosedOption" color="platform-green">GO</v-btn>
          </v-flex>
          <v-flex xs12 sm6 class="text-xs-right shrinked">
            Concierge program
          </v-flex>
      </v-layout>
        <PromotionLogos></PromotionLogos>
    </v-container>
</div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'

import utils from '@/lib/utils.js'
import PromotionLogos from '@/components/basic/PromotionLogos'
import metadata from '@/mixins/metadata'

export default {
    props: {
        class_id: Number,
    },

    mixins: [metadata],

    components: {
        PromotionLogos
    },

    data: () => ({
        isLoading: false,
        options: [],
        canBook: true,
        choosedOption: 2,
        currentOption: {},
        singleId: 4,
    }),

    created: function () {
        this.isLoading = true
        axios.get('/api/buy_membership').then(res => {
            console.log(res.data)
            this.options = res.data.available_options
            this.isLoading = false
            this.canBook = res.data.can_book
            this.currentOption = res.data.current_option || {}
            if(this.currentOption.option_id) {
                this.choosedOption = _.first(_.sortBy(_.filter(this.options, ['is_available', 'is_monthly']), o => Number(o.num_classes))).id
            }
        })
    },

    computed: {
        currentOptionName() {
            return this.currentOption.option_id ? _.find(this.options, {id: this.currentOption.option_id}).name : ''
        },
        optionsPrepared() {
            return _.sortBy(_.map(_.filter(this.options, v => (v.id !== this.singleId)), v => {
                const promoId = 2
                return {
                    id: v.id,
                    is_available: v.is_available,
                    title: v.name,
                    line1: `${utils.formatPrice(v.amount, 'usd')} ${v.is_monthly ? 'month' : ''}`,
                    line2: `Yes! Launch ${v.num_classes} classes by submitting them to 42 local media and online engines.`,
                    cardClass: `${v.id === promoId ? 'above' : ''} ${this.choosedOption === v.id ? 'active' : 'available'} ${!v.is_available ? 'disabled' : ''}`,
                }
            }), 'order')
        },
        singleOptionName() {
            if(!this.class_id) {
                return 'Just one class for $99'
            }
            return 'Just this class for $99'
        }
    },

    methods: {
        submit(id) {
            console.log('submit', id)
            if(this.class_id) {
                this.$router.push(`/teacher_checkout/${id}/${this.class_id}`)
            } else {
                this.$router.push(`/teacher_checkout/${id}`)
            }

        },
        cancel() {
            console.log('cancel')
        },
        chooseOption(id) {
            if(this.currentOption.option_id === id)
                return
            this.choosedOption = id
        }
    }
}
</script>

<style scoped lang="scss">
.join-as-member-page {
    li {
        font-size: 20px;
    }
    h3 {
        font-size: 34px;
        text-align: center;
    }
    .shrinked {
        padding: 0 !important;
    }
    .above{
        padding: 20px 0 !important;
        margin: 20px 0 !important;
        z-index: 1;
    }
    .subheader {
        font-size: 24px;
        font-weight: bold;
        padding-bottom: 0;
    }
    .line1 {
        font-size: 20px;
        font-weight: bold;
        text-align: left;
    }
    .line2 {
        font-size: 20px;
        text-align: left;
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
        border: 2px solid rgba(0, 0, 0, 0);
        margin: 0;
        height: 100%;
        font-size: 14px;
    }
    .disabled {
        background-color: rgba(200, 200, 200, 0.1);
        border: 2px solid rgba(0, 0, 0, 0);
        color: grey;
        margin: 0;
        height: 100%;
        font-size: 14px;
        cursor: default;
    }
}
</style>