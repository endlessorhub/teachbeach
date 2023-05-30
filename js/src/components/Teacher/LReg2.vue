<template>
    <v-layout align-top justify-center row wrap>
        <v-flex xs12 text-xs-center>
            <form>
                <v-card class="card">
                    <v-card-title class="headline" primary-title>
                        {{ header }}
                    </v-card-title>
                    <v-card-text>
                        <div class="subheading text-xs-left">{{ subtitle }}</div>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                        <v-btn @click="next">Next</v-btn>
                    </v-card-actions>
                </v-card>
            </form>
        </v-flex>
    </v-layout>
</template>

<script>

export default {
    props: {
        header: {
            type: String,
            default: 'Please select an option',
        },
        subtitle: {
            type: String,
            default: '(don’t worry you can change it later)',
        },
        isClosable: {
            type: Boolean,
            default: false,
        },
    },
    components: {

    },

    validations: {

    },

    data: function () {

        return {
            is_company: true,
            errors: {},
        }
    },

    mounted() {
        if(this.alreadyRegistered) {
            this.$router.push('/teachers/start');
        }
    },

    computed: {
        alreadyRegistered: function () {
            return this.$store.state.user && this.$store.state.user.id;
        },
    },

    methods: {
        next() {
            this.$store.commit('setUser', {
                ...this.$store.state.user,
                is_company: this.is_company,
            });
            this.$router.push('/teachers/profile');
        },
    },
    watch: {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.card {
    margin: 1em auto;
    width: 370px;
}
</style>