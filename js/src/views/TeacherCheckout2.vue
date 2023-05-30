<template>
    <div class="t-wrapper">
        <v-layout align-top justify-center row wrap class="t-container">
            <v-flex xs12 sm6 class="text-xs-left">
                <div class="display-1 font-weight-bold">
                    Yes! Publish on Teachbeach
                </div>
                <ul>
                    <li><span class="t-icon">✓</span>$5 per class per month</li>
                    <li><span class="t-icon">✓</span>Unlimited students</li>
                    <li><span class="t-icon">✓</span>Complete tools for pro trainers</li>
                    <li><span class="t-icon">✓</span>No CC fees</li>
                    <li><span class="t-icon">✓</span>No rev share</li>
                    <li><span class="t-icon">✓</span>Includes scheduling, payments, management, reminders</li>
                    <li><span class="t-icon">✓</span>Marketing support</li>
                    <li><span class="t-icon">✓</span>Live help at <a href="tel:+14088929815">408.892.9815</a>.</li>
                </ul>
            </v-flex>
            <v-divider
              class="hidden-xs-only ver-divider"
              vertical
                inset
            ></v-divider>
            <v-divider
              class="hidden-sm-and-up hor-divider"
              inset

            ></v-divider>
            <v-flex xs12 sm6 class="text-xs-left">
                <div class="display-1 font-weight-bold">
                    Let's do this
                </div>
                <CreditCards
                    :btnText="btnText"
                    :successBtnText="successBtnText"
                    @cardAdded="submit"
                />
            </v-flex>
          </v-layout>
    </div>
</template>

<script>
import CreditCards from '@/components/basic/CreditCards'
import axios from 'axios'
import metadata from '@/mixins/metadata'
import { mapGetters } from 'vuex'

export default {
    mixins: [metadata],
    props: {

    },

    components: {
        CreditCards,
    },

    data: () => ({
        btnText: 'Next',
        successBtnText: 'Great!',
        nextRoute: '/teachers/start',
        unauthRoute: '/teachers_promo',
        timeoutId: false,
        classId: null,
    }),

    created: function () {
        this.classId = Number(this.$route.params.class_id) || null
        if(this.classId) {
            if(this.$route.query.n === 'tc') {
                this.nextRoute = `/dashboard/teach/classes`
            } else
                this.nextRoute = `/teachers/finish/${this.classId}`
        }
        if(!this.isLoggedIn) {
            return this.$router.push(this.unauthRoute)
        }
    },

    computed: {
        ...mapGetters([
            'isLoggedIn',
        ]),
    },

    methods: {
        submit () {
            if(this.timeoutId)
                clearTimeout(this.timeoutId)
            const action = this.classId ? axios.post(`/api/deactivate_class/`, {
                id: this.classId,
                deactivate: false,
            }) : Promise.resolve(true)
            action.then(res => {
                this.timeoutId = setTimeout(() => {
                    this.$router.push(this.nextRoute)
                }, 1000)
            }).catch(e => {
                console.log(e)
            })
        },
    }
}
</script>

<style scoped lang="scss">
    @import "@/styles/_variables.scss";
    .yes {
        font-size: 53px;
        font-weight: 900;
    }
    .separated {
        margin-top: 1em;
    }
    .t-wrapper {
        background-color: $platform-green;
        .t-container {
            padding: 20px;
            border-top-right-radius: 60px;
            border-bottom-left-radius: 60px;
            background-color: white;
            border-bottom: 10px solid $platform-green;
            &> div {
                padding: 0 10px;
            }
            .ver-divider {
                margin: 0px 1px 0px -2px;
            }
            .hor-divider {
                margin: 10px 20px;
            }
        }
    }
    li {
        list-style: none;
        .t-icon {
            margin: 0 5px;
            color: $platform-green;
        }
    }
</style>