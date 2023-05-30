<template>
    <div class="class-item">
        <div class="class-item__img">
            <v-img v-if="avatar" :src="previewImg" width="100%" height="100%"></v-img>
            <div v-else class="class-item__img-missing">No image</div>
        </div>
        <div class="class-item__content">
            <div class="class-item__content-top-container">
                <div class="class-item__content-top-left">
                    <div class="class-item__content-top-bar">
                        <v-btn dark small color="#9B9B9B" v-if="isExpired" :to="'/teachers/copy_class/'+id">
                            <span class="class-item__text_no_transform">Expired</span> <v-icon right>replay</v-icon>
                        </v-btn>
                        <ActionableOnClick
                            key="paused"
                            v-else-if="isDeactivated"
                            :action="resumeClass"
                            @success="(res) => processActivation(id, res.data)"
                            v-slot="{loading, click}"
                        >
                            <v-btn dark small color="#9B9B9B" @click="click" :loading="loading" :disabled="loading">
                                <span class="class-item__text_no_transform">Paused</span> <v-icon right>play_circle_outline</v-icon>
                            </v-btn>
                        </ActionableOnClick>
                        <ActionableOnClick
                            key="active"
                            v-else
                            :action="pauseClass"
                            @success="(res) => processActivation(id, res.data)"
                            v-slot="{loading, click}"
                        >
                            <v-btn dark small color="#9B9B9B" @click="click" :loading="loading" :disabled="loading">
                                <span class="class-item__text_no_transform">Active</span> <v-icon right>pause_circle_outline</v-icon>
                            </v-btn>
                        </ActionableOnClick>
                        <span class="class-item__content-top-bar-type">{{type}}</span>
                    </div>
                    <div class="class-item__content-title">
                        <router-link :to="`/class/${id}`">{{title}}</router-link>
                        <v-menu bottom left v-if="numEnrolled">
                            <template v-slot:activator="{ on }">
                              <span
                                class="num-enrolled"
                                v-on="on"
                              >({{numEnrolled}})</span>
                            </template>

                            <v-list two-line subheader>
                                <template
                                    v-for="(item, i) in studentList"
                                >
                                    <v-list-tile
                                        v-if="item.student"
                                        :key="item.id"
                                        @click=""
                                    >
                                      <v-list-tile-content>
                                          <v-list-tile-title>{{ item.student.first_name }} {{ item.student.last_name }}</v-list-tile-title>
                                          <v-list-tile-sub-title v-if="item.amount > 1">{{item.amount }} orders</v-list-tile-sub-title>
                                      </v-list-tile-content>
                                    </v-list-tile>
                                    <v-divider v-if="item.type === 'delimiter' && i !== 0">{{item.title}}</v-divider>
                                    <v-subheader :key="item.id" v-if="item.type === 'delimiter'">{{item.title}}</v-subheader>
                                </template>
                            </v-list>
                        </v-menu>
                        <span v-else>({{numEnrolled}})</span>
                    </div>
                    <div class="class-item__content-text">{{description}}</div>
                    <social-share-class
                        :class-id="id"
                        :class-name="name"
                    />
                </div>
                <div class="class-item__actions">
                    <div class="class-item__actions__action">
                        <v-menu offset-y>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              block
                              v-on="on"
                            >
                                <span class="class-item__text_no_transform">Class</span>
                            </v-btn>
                          </template>
                          <v-list>
                            <v-list-tile
                              key="edit"
                              :to="`/teachers/class/${id}`"
                            >
                              <v-list-tile-title>Edit</v-list-tile-title>
                            </v-list-tile>
                            <v-list-tile
                              key="copy"
                              @click="$emit('copy', id)"
                            >
                              <v-list-tile-title>Copy</v-list-tile-title>
                            </v-list-tile>
                          </v-list>
                        </v-menu>
                    </div>
                    <div class="class-item__actions__action">
                        <v-menu offset-y>
                          <template v-slot:activator="{ on }">
                            <v-btn
                              block
                              color="platform-green"
                              v-on="on"
                            >
                                <span class="class-item__text_no_transform">Marketing</span>
                            </v-btn>
                          </template>
                          <v-list>
                            <v-list-tile
                              @click="openBoostForm(id)"
                            >
                              <v-list-tile-title>Submit to calendars</v-list-tile-title>
                            </v-list-tile>
                            <v-list-tile
                              @click="openEmailBoostForm(id)"
                            >
                              <v-list-tile-title>Send email campaign</v-list-tile-title>
                            </v-list-tile>
                          </v-list>
                        </v-menu>
                    </div>
                </div>
            </div>
            <div class="class-item__content-bottom-bar">
                <div v-if="!isDeactivated && !isExpired" key="add" class="class-item__content-bottom-bar-btn">
                    <v-btn color="platform-aqua font-weight-bold" @click="showAddStudentForm($props)"><v-icon left>add</v-icon> <span class="class-item__text_no_transform">Invite new</span></v-btn>
                </div>
                <div v-if="isEnrollStudentsAvailable" key="enroll" class="class-item__content-bottom-bar-btn">
                    <v-btn color="platform-aqua font-weight-bold" @click="showEnrollStudentsForm($props)"><v-icon left>account_circle</v-icon> <span class="class-item__text_no_transform">Sign-in</span></v-btn>
                </div>
                <div key="message" class="class-item__content-bottom-bar-btn">
                    <v-btn color="platform-aqua font-weight-bold" @click="openSendMessageForm(id)"><v-icon left>message</v-icon> <span class="class-item__text_no_transform">Message</span></v-btn>
                </div>
                <div v-if="deleteEnabled" key="delete" class="class-item__content-bottom-bar-btn">
                    <v-btn icon color="platform-aqua font-weight-bold" @click="deleteClass(id)"><v-icon>delete_outline</v-icon></v-btn>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import ActionableOnClick from '@/components/basic/ActionableOnClick'
import SocialShareClass from '@/components/basic/SocialShareClass'
import { mapMutations } from 'vuex'
import classHelpers from '@/lib/helpers/Class'

export default {
    name: 'dashteach_class_list_item',
    components: {
        ActionableOnClick,
        SocialShareClass,
    },
    data: () => ({

    }),
    props: [
        'id',
        'totalAmount',
        'type',
        'chipColor',
        'avatar',
        'name',
        'title',
        'description',
        'editEnabled',
        'deleteEnabled',
        'isPrivate',
        'isExpired',
        'isDeactivated',
        'isBoostAvailable',
        'isBoosted',
        'isEmailAvailable',
        'isEmailBoosted',
        'isLoadidngActivation',
        'isEnrollStudentsAvailable',
        'processActivation',
        'showAddStudentForm',
        'showEnrollStudentsForm',
        'openSendMessageForm',
        'deleteClass',
        'openBoostForm',
        'openEmailBoostForm',
        'students',
    ],
    computed: {
        previewImg() {
            return classHelpers.isPreviewImageSrc(this.avatar) ? this.avatar : classHelpers.previewImageSrc(this.avatar)
        },
        numEnrolled() {
            return this.studentList && this.studentList.filter(s => (s.student && s.student.isActive)).length || 0
        },
        studentList() {
            const reducer = (type) => (acc, s) => {
                const accIndex = acc.findIndex(v => v.student.id === s.id)
                if(accIndex !== -1) {
                    acc[accIndex].amount++
                } else {
                    acc.push({amount: 1, student: s, id: `${type}_${s.id}`})
                }
                return acc
            }
            const sortVal = student => `${student.first_name} ${student.last_name}`
            const sorter = (a, b) => {
                if(sortVal(a) > sortVal(b))
                    return 1
                if(sortVal(a) < sortVal(b))
                    return -1
                return 0
            }
            let list = this.students.filter(s => s.isActive).reduce(reducer('cur'), []).sort(sorter);
            const past = this.students.filter(s => !s.isActive).reduce(reducer('past'), []).sort(sorter);
            if(list.length) {
                list.unshift({type: 'delimiter', title: 'Current students', id: 'cur_del'});
            }
            if(past.length) {
                list.push({type: 'delimiter', title: 'Past students', id: 'past_del'});
                list = [...list, ...past]
            }
            return list
        }
    },
    methods: {
        ...mapMutations([
            'setGlobalError'
        ]),
        pauseClass() {
            return axios.post(`/api/deactivate_class/`, {
                id: this.id,
                deactivate: true,
            })
        },
        resumeClass() {
            return axios.post(`/api/deactivate_class/`, {
                id: this.id,
                deactivate: false,
            })
        },
        reloadData() {

        }
    },
}
</script>
<style lang="scss" scoped>
@mixin multiLineEllipsis($bgColor: white){
    overflow: hidden;
    position: relative;
    text-align: justify;
    margin-right: -1em;
    padding-right: 1em;
    &:before {
        content: '...';
        position: absolute;
        right: 0;
        bottom: 0;
    }
    &:after {
        content: '';
        position: absolute;
        right: 0;
        width: 1em;
        height: 1em;
        margin-top: 0.2em;
        background: $bgColor;
    }
}

.class-item {
    margin: 30px 0;
    height: 244px;
    padding: 0;
    display: flex;
    flex-flow: row nowrap;

    &__text_no_transform {
        text-transform: none;
    }

    &__img {
        flex: 0 0 244px;

        &-missing {
            height: 100%;
            width: 100%;
            background: repeating-radial-gradient(
                circle,
                purple,
                purple 10px,
                #4b026f 10px,
                #4b026f 20px
            );
        }
    }
    &__content {
        flex: 1 1 auto;
        text-align: left;
        padding: 0 30px;
        display: flex;
        flex-flow: column nowrap;
        justify-content: space-between;

        &-top-container {
            display: flex;
            flex-flow: row nowrap;
            overflow: hidden;
        }

        &-top-left {
            flex: 1 1 auto;
            display: flex;
            flex-flow: column nowrap;
        }

        &-top-bar {
            margin: -6px -8px;

            &-type {
                font-weight: 900;
            }
        }

        &-title {
            font-weight: 600;
            font-size: 21px;
            padding-top: 16px;
            padding-bottom: 20px;
        }

        &-text {
            text-overflow: ellipsis;
            overflow: hidden;
            margin-bottom: 10px;
            //@include multiLineEllipsis($bgColor: white)
        }

        &-bottom-bar {
            margin: -6px -8px;
            display: flex;
            flex-flow: row wrap;

            &-btn {

            }
        }
    }
    &__actions {
        flex: 0 0 143px;
    }
}
.class-item__content-top-bar >>> button {
    width: 102px;
}
.class-item__content-title >>> a {
    text-decoration: none;
    color: black;
}
    .num-enrolled {
        cursor: pointer;
        text-decoration: none;
    }
</style>