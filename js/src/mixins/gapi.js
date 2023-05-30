import GoogleCalendarSync from '@/components/bound/GoogleCalendarSync'
import {mapMutations, mapState, mapActions} from 'vuex';

export default {
    components: {
        GoogleCalendarSync,
    },

    mounted() {
        this.getSavedEvents()
    },

    computed: {
        ...mapState({
            externalEvents: state => state.gapi.events,
            timezone: state => state.timezone,
        }),
    },

    methods: {
        ...mapActions({
            getSavedEvents: 'gapi/getSavedEvents',
        }),
    }
}