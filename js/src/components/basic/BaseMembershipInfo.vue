<template>
    <v-card class="membership-info">
        <v-card-title>
            <div class="headline text-xs-left">
                <router-link class="membership-info__link" :to="`/buy-membership/${id}?return=${$route.path}`">{{ name }}</router-link>
            </div>
        </v-card-title>
        <v-card-text>
            <router-link v-if="media" :to="`/buy-membership/${id}?return=${$route.path}`">
                <v-img
                  :src="media"
                  width="60%"
                >
                </v-img>
            </router-link>
            <div class="membership-info__description">
                <span v-html="descriptionFormatted"></span>
                <router-link :to="`/buy-membership/${id}?return=${$route.path}`">More</router-link>
            </div>
        </v-card-text>
    </v-card>
</template>

<script>

export default {
    name: 'BaseMembershipInfo',
    props: {
        id: {
            type: Number,
        },
        name: {
            type: String,
        },
        media: {
            type: String,
        },
        currency: {
            type: String,
        },
        monthly_rate: {
            type: Number,
        },
        description: {
            type: String,
            default: '',
        },
    },
    data() {
        return {
            descriptionLimit: 200,
        }
    },
    computed: {
        descriptionFormatted() {
            const descr = this.description.length > this.descriptionLimit
                ? this.description
                    .substring(0, this.descriptionLimit)
                    .split(' ')
                    .slice(0, -1)
                    .join(' ')+'...'
                : this.description;
            return '<p>'+descr.replace(/\n/g, '<p>');
        }
    },
    methods: {

    },
}
</script>
<style lang="scss" scoped>
@import "../../styles/_variables.scss";

.membership-info {
    margin: 0 10px 20px 10px;
    &__link {
        text-decoration: none;
        color: #000;
    }
    &__description {
        text-align: left;
        padding: 20px 0;
        & >>> p {
            text-indent: 2em;
        }
    }
}
</style>