<template>
    <div class="student-list-item">
        <div class="student-list-item__top">
            <div class="student-list-item__top-content">
                <div class="student-list-item__top-content-left">
                    <div class="student-list-item__top-content-left-avatar" :style="avatarStyle"></div>
                    <div class="student-list-item__top-content-left-text">
                        <div class="student-list-item__top-content-left-title">
                            {{  first_name }} {{  last_name }}
                        </div>
                        <div class="student-list-item__top-content-left-line">
                            <v-icon class="material-icons">email</v-icon>
                            <div class="student-list-item__top-content-left-text">
                                <a :href="`tel:${email}`">{{ email }}</a>
                            </div>
                        </div>
                        <div class="student-list-item__top-content-left-line">
                            <v-icon class="material-icons">phone</v-icon>
                            <div class="student-list-item__top-content-left-text">
                                <a :href="`tel:${phone}`">{{ phone }}</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="student-list-item__top-content-right">
                    <div v-if="skill" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Skills:</div>
                        <div class="student-list-item__top-content-right-text">{{ skill }}</div>
                    </div>
                    <div v-if="interest" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Interests:</div>
                        <div class="student-list-item__top-content-right-text">{{ interest }}</div>
                    </div>
                    <div v-if="level" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Levels:</div>
                        <div class="student-list-item__top-content-right-text">{{ level }}</div>
                    </div>
                    <div v-if="title" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Title:</div>
                        <div class="student-list-item__top-content-right-text">{{ title }}</div>
                    </div>
                    <div v-if="city" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">City:</div>
                        <div class="student-list-item__top-content-right-text">{{ city }}</div>
                    </div>
                    <div v-if="document" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Document:</div>
                        <div class="student-list-item__top-content-right-text">{{ document }}</div>
                    </div>
                    <div v-if="social" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Social:</div>
                        <div class="student-list-item__top-content-right-text">{{ social }}</div>
                    </div>
                    <div v-if="website" class="student-list-item__top-content-right-line">
                        <div class="student-list-item__top-content-right-title">Website:</div>
                        <div class="student-list-item__top-content-right-text">{{ website }}</div>
                    </div>
                </div>
            </div>
            <div class="student-list-item__top-action">
                <v-btn
                    dark
                    @click="startDM"
                >Start DM</v-btn>
            </div>
        </div>
        <div v-if="description" class="student-list-item__bottom">
            <div class="student-list-item__bottom-title">About me:</div>
            <div ref="descrOuter" :class="{ 'student-list-item__bottom-text': true, expanded: isExpanded }">
                <div ref="descrInner" class="description-wrapper">{{ description }}</div>
            </div>
            <div v-if="isExpandAvailable" class="expand-container">
                <v-btn flat icon :class="{ expanded: isExpanded }" @click="onClickExpand">
                    <v-icon>keyboard_arrow_down</v-icon>
                </v-btn>
            </div>
        </div>
    </div>
</template>

<script>
import helperClass from '@/lib/helpers/Class'

export default {
    name: 'dashboard_teach_student_list_item',
    data: () => ({
        isExpanded: false,
        isExpandAvailable: false,
    }),
    props: [
        'id', 'first_name', 'last_name', 'email', 'phone', 'is_company', 
        'company_profile', 'source', 'notes', 'notes2', 'date_joined', 'managed_by', 
        'memberships', 'isMember', 'isCanceledMember', 'isCustomer', 'isRegistered', 
        'isUnregistered', 'isProspect', 'isStudent', 'title', 'media', 'classTitles',
        'orders', 'cost', 'city', 'document', 'social', 'website', 'description', 'level',
        'skill', 'interest',
    ],
    created() {
        
    },
    computed: {
        avatarStyle() {
            return this.media ? `background: url(${helperClass.previewImageSrc(this.media)}), lightgray 50% / contain no-repeat` : '';
        },
    },
    methods: {
        startDM() {

        },
        onClickExpand() {
            this.isExpanded = !this.isExpanded;
        },
    },

    watch: {
        description: {
            immediate: true,
            handler(v) {
                this.$nextTick(() => {
                    if (!this.$refs.descrInner || !this.$refs.descrOuter) return;
                    // console.log(this.$refs.descrInner, this.$refs.descrOuter);
                    if (this.$refs.descrInner.clientHeight > this.$refs.descrOuter.clientHeight) {
                        this.isExpandAvailable = true;
                    } else this.isExpandAvailable = false;
                });
            }
        }
    }
}
</script>
<style lang="scss" scoped>
.student-list-item {
    display: flex;
    width: 100%;
    padding: 18px;
    flex-direction: column;
    align-items: flex-start;
    gap: 21px;
    background: #FFF;
    margin: 3px 0;

    &__top {
        display: flex;
        align-items: flex-start;
        width: 100%;
        justify-content: space-between;
    }
    &__top-content {
        display: flex;
        align-items: flex-start;
        gap: 60px;
    }
    &__top-content-left {
        display: flex;
        align-items: center;
        gap: 17px;
    }
    &__top-content-left-avatar {
        display: flex;
        width: 142.676px;
        flex-direction: column;
        align-items: flex-start;
        gap: 11.529px;
        aspect-ratio: 1;
    }
    &__top-content-left-text {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }
    &__top-content-left-title {
        color: #000;
        font-size: 18px;
        font-family: Poppins;
        font-weight: 600;
        line-height: 22px;
    }
    &__top-content-left-line {
        display: flex;
        align-items: center;
        gap: 9px;
    }
    &__top-content-right {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 3px;
    }
    &__top-content-right-line {
        display: flex;
        align-items: flex-start;
        gap: 9px;
    }
    &__top-content-right-title {
        color: #000;
        font-size: 15px;
        font-family: Poppins;
        font-weight: 500;
        line-height: 22px;
    }
    &__top-content-right-text {
        color: #000;
        font-size: 15px;
        font-family: Poppins;
        line-height: 22px;
    }
    &__top-action {
        display: flex;
        align-items: flex-start;
        gap: 92px;
    }
    &__bottom {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 3px;
    }
    &__bottom-title {
        color: #000;
        font-size: 15px;
        font-family: Poppins;
        font-weight: 500;
        line-height: 22px;
    }
    &__bottom-text {
        color: var(--black, #1C1C1C);
        font-size: 15px;
        font-family: Poppins;
        line-height: 22px;
        text-align: left;
        max-height: 62px;
        overflow: hidden;
        &.expanded {
            max-height: fit-content;
        }
    }
}
.expand-container {
    align-self: center;
    display: flex;
    justify-content: center;
    align-items: center;
    .expanded {
        transform: rotate(180deg);
    }
}
</style>