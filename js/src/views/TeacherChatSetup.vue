<template>
    <div class="chat-setup-main">
        <div class="header-selection">
            <h2>Discussion Setup</h2>
        </div>

        <div class="chat-setup-select-option">
            <label for="switchA1" class="switch-item">
                <input v-model="chatSetupOptions.is_community" type="checkbox" name="" id="switchA1" class="control">
                <span class="label"></span>
            </label>
            <h2>Community Discussion</h2>
        </div>
        <div class="setup-intro">
            <div class="eventchat-para">
                <p>A forum for members to post and discuss any topic of interest</p>
            </div>
        </div>

        <div class="setupfield1"
            style="flex-direction: row; gap: 1rem; align-items: center; justify-content: space-between;">
            <div class="setupfield1-member">
                <input v-model="chatSetupOptions.community.participants" type="radio" id="html" name="community" value="members">
                  <label for="html" style="margin-left: 5px;">Members Only Access</label>
            </div>
            <div class="setupfield1-contact">
                  <input v-model="chatSetupOptions.community.participants" type="radio" id="css" name="community" value="contacts" >
                  <label for="css" style="margin-left: 5px;">All Contact Access</label>
            </div>
        </div>

        <div class="setup-image">
            <div class="setup-image-label">
                <label for="">Main images</label>
                <div class="image-box">
                        <input type="file" id="community_thumbnail" accept="image/png, image/gif, image/jpeg"  class="hidden"  @change="fileInput($event,'community_thumbnail')" />
                        <label for="community_thumbnail">
                        <svg v-if="!community_thumbnail" width="17" height="16" viewBox="0 0 17 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M5.99996 0.166504L4.47496 1.83317H1.83329C0.916626 1.83317 0.166626 2.58317 0.166626 3.49984V13.4998C0.166626 14.4165 0.916626 15.1665 1.83329 15.1665H15.1666C16.0833 15.1665 16.8333 14.4165 16.8333 13.4998V3.49984C16.8333 2.58317 16.0833 1.83317 15.1666 1.83317H12.525L11 0.166504H5.99996ZM8.49996 12.6665C6.19996 12.6665 4.33329 10.7998 4.33329 8.49984C4.33329 6.19984 6.19996 4.33317 8.49996 4.33317C10.8 4.33317 12.6666 6.19984 12.6666 8.49984C12.6666 10.7998 10.8 12.6665 8.49996 12.6665Z"
                            fill="black" fill-opacity="0.45" />
                        </svg>
                        <img :src="community_thumbnail" width="100%"/>
                    </label>

                    

                </div>

            </div>

            <div class="setup-image-desc">
                <label for="">Description</label>
                <div class="image-desc">
                    <textarea v-model="chatSetupOptions.community.description" name="" id="" cols="55" rows="3" placeholder="Add Description"
                        style="height: 100%;"></textarea>
                </div>

            </div>

        </div>

        <div class="breaker"></div>

        <div class="eventchat-container">
<!-- Event  -->
            <div class="eventchat-selector">
                <label for="switchA1" class="switch-item">
                    <input v-model="chatSetupOptions.is_event" type="checkbox" name="" id="switchA1" class="control">
                    <span class="label"></span>
                </label>
            </div>

            <div class="eventchat-content">
                <h2>Event Discussion</h2>
                <div class="eventchat-para">
                    <p>This forum will activate whenever an event is posted</p>
                </div>

            </div>

        </div>

        <div class="setupfield1"
            style="flex-direction: row; gap: 1rem; align-items: center; justify-content: space-between;">
            <div class="setupfield1-member">
                <input v-model="chatSetupOptions.event.participants" type="radio" id="html" name="event" value="participants">
                  <label for="html" style="margin-left: 5px;">Participants-only access</label>
            </div>
            <div class="setupfield1-contact">
                  <input v-model="chatSetupOptions.event.participants" type="radio" id="css" name="event" value="members">
                  <label for="css" style="margin-left: 5px;">All Members Access</label>
            </div>
        </div>

        <div class="breaker"></div>


        <div class="eventchat-container">
            <div class="eventchat-selector">
                <label for="switchA1" class="switch-item">
                    <input v-model="chatSetupOptions.is_topic" type="checkbox" name="" id="switchA1" class="control">
                    <span class="label"></span>
                </label>
            </div>

            <div class="eventchat-content">
                <h2>Discussion Topic</h2>
            </div>
        </div>
        <div class="eventchat-para">
            <p>Add any topic for the group to discuss. Pin an image and message about the topic and kick off the discussion
                with
                a post.</p>
        </div>


        <div class="setupfield1"
            style="flex-direction: row; gap: 1rem; align-items: center; justify-content: space-between;">
            <div class="setupfield1-member">
                <input v-model="chatSetupOptions.topic.participants" type="radio" id="html" name="topic" value="members">
                  <label for="html" style="margin-left: 5px;">Members-only access</label>
            </div>
            <div class="setupfield1-contact">
                  <input v-model="chatSetupOptions.topic.participants" type="radio" id="css" name="topic" value="contacts">
                  <label for="css" style="margin-left: 5px;">All Contacts Access</label>
            </div>
        </div>

        <h2>Discussion Chat</h2>

        <div class="setupfield2">
            <label for="">Add Discussion Topic</label>
            <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                <option>Add Discussion Topic </option>
                <option>Add Discussion Topic </option>
                <option>Add Discussion Topic </option>
                <option>Add Discussion Topic </option>
            </select>
        </div>


        <div class="setup-image">
            <div class="setup-image-label">
                <label for="">Main images</label>
                <div class="image-box">
                    <input type="file" id="topic_thumbnail" accept="image/png, image/gif, image/jpeg"  class="hidden"  @change="fileInput($event, 'topic_thumbnail')" />
                    <label for="topic_thumbnail">
                    <svg v-if="!topic_thumbnail" width="17" height="16" viewBox="0 0 17 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M5.99996 0.166504L4.47496 1.83317H1.83329C0.916626 1.83317 0.166626 2.58317 0.166626 3.49984V13.4998C0.166626 14.4165 0.916626 15.1665 1.83329 15.1665H15.1666C16.0833 15.1665 16.8333 14.4165 16.8333 13.4998V3.49984C16.8333 2.58317 16.0833 1.83317 15.1666 1.83317H12.525L11 0.166504H5.99996ZM8.49996 12.6665C6.19996 12.6665 4.33329 10.7998 4.33329 8.49984C4.33329 6.19984 6.19996 4.33317 8.49996 4.33317C10.8 4.33317 12.6666 6.19984 12.6666 8.49984C12.6666 10.7998 10.8 12.6665 8.49996 12.6665Z"
                            fill="black" fill-opacity="0.45" />
                    </svg>
                    <img :src="topic_thumbnail" width="100%"/>
                    </label>
                </div>

            </div>

            <div class="setup-image-desc">
                <label for="">Description</label>
                <div class="image-desc">
                    <textarea v-model="chatSetupOptions.topic.description" name="" id="" cols="55" rows="3" placeholder="Add Description"
                        style="height: 100%;"></textarea>
                </div>

            </div>
        </div>

        <div class="breaker"></div>

        <div class="setup-buttons">
            <button class="setup-buttons-1">Preview</button>
            <button @click="setupDiscussion()" class="setup-buttons-2">Save</button>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex';


export default {
    name: 'TeacherChatSetup',
    data() {
        return {
            activeItem: 'Community',
            chatSetupOptions: {
                'is_community':false,
                'is_event': false,
                'is_topic': false,
                'community': {},
                'topic': {},
                'event': {}
            },
            community_thumbnail: null,
            topic_thumbnail: null,
        };
    },
    methods: {
        ...mapActions('chatDiscussion',['discussionSetup','initiateChat','setDiscussionId','emptyChats']),
        show(val) {
            this.activeItem = val;
        },
        async setupDiscussion() {
            //initializing form data
            let setupOptions = new FormData()

            //setting values with in formData
            setupOptions.append('is_community', this.chatSetupOptions.is_community)
            setupOptions.append('is_event', this.chatSetupOptions.is_event)
            setupOptions.append('is_topic', this.chatSetupOptions.is_topic)

            if (this.chatSetupOptions.is_community) {
                setupOptions.append('community_post', JSON.stringify(this.chatSetupOptions.community))
                if(this.chatSetupOptions.community_thumbnail)
                setupOptions.append('community_thumbnail',this.chatSetupOptions.community_thumbnail['0'])
            }
            else if (this.chatSetupOptions.is_event) {
                setupOptions.append('event_discussion', JSON.stringify(this.chatSetupOptions.event))
            }
            else if (this.chatSetupOptions.is_topic) {
                setupOptions.append('topic_post', JSON.stringify(this.chatSetupOptions.topic))
                if (this.chatSetupOptions.topic_thumbnail)
                setupOptions.append('topic_thumbnail', this.chatSetupOptions.topic_thumbnail['0'])
            }

            // requesting backend
            this.discussionSetup(setupOptions).then(async(res) => {
                if (res.status === 201) {
                    
                    //setting discussion Id
                    await this.setDiscussionId(res.data.discussion_id)

                    //clear all fields
                    this.clearInputs()

                    //clear all the chats
                    this.emptyChats()
                    
                     //redirect discussion when request is successfull 
                     this.$router.push({name:'TeacherChatDiscussion'})
                }
            })
            
        },
        clearInputs() {
            this.chatSetupOptions.is_community = false
            this.chatSetupOptions.community = {}
            this.chatSetupOptions.is_event = false
            this.chatSetupOptions.event = {}
            this.chatSetupOptions.is_topic = false
            this.chatSetupOptions.topic = {}
            this.chatSetupOptions.community_thumbnail = null
            this.chatSetupOptions.topic_thumbnail = null
            this.community_thumbnail = null
            this.topic_thumbnail= null

            
        },

        fileInput(e, type) { 
            if (e.target.files.length>0) {
                this.chatSetupOptions[type] = e.target.files
                switch (type) {
                    case 'community_thumbnail':
                        this.community_thumbnail = window.URL.createObjectURL(this.chatSetupOptions[type]['0'])
                        break;
                    case 'topic_thumbnail':
                        this.topic_thumbnail = window.URL.createObjectURL(this.chatSetupOptions[type]['0'])
                        break;
                }
            }
         }


    }
}
</script>



<!-- /* CHAT SETUP STYLING ============================================== */ -->

<style scoped>
.header-selection {
    display: flex;
    width: 60%;
    justify-content: space-between;
}

.selector-options {
    width: 40%;
}

.selector-options ul {
    display: flex;
    gap: 1rem;

}

.selector-options ul li {
    list-style-type: none;
}

.selector-options ul li:hover {
    color: #434343;
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-underline-offset: 6px;
    cursor: pointer;
}


p {
    font-size: 15px;
    margin-bottom: 0;
    text-align: left;
    width: 100%;

}

h2 {
    margin-bottom: 0px;
}

.eventchat-para {
    width: 561px;
}

.chat-setup-main h2 {
    font-size: 20px;
    font-weight: 500;
    line-height: 22px;
    font-family: 'poppins';

}


.chat-setup-main {
    display: flex;
    width: 100%;
    justify-content: flex-start;
    /* height: 100vh; */
    flex-direction: column;
    gap: 2rem;
    font-family: 'poppins';

}



.setup-intro {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.switch-item {
    display: block;
}

.switch-item .control[type='checkbox'] {
    appearance: none;
    position: relative;
    width: 52px;
    height: 34px;
    padding: 3px;
    border-radius: 34px;
    background-color: #aaa;
    vertical-align: middle;
    transition: all .3s cubic-bezier(.4, 0, .1, 1.4);
}

.switch-item .control[type='checkbox']:after {
    content: '';
    position: relative;
    display: block;
    left: 0;
    width: 60.9%;
    height: 100%;
    border-radius: 28px;
    background-color: #fff;
    transition: left .3s cubic-bezier(0.175, 0.885, 0.32, 1.275), padding .3s ease, margin .3s ease;
    box-sizing: content-box;
}

.switch-item .control[type='checkbox']:active:after {
    padding-right: 8px;
}

.switch-item .control[type='checkbox']:checked {
    /* background-color: royalblue; */
    background-color: rgb(52, 199, 89);
    ;
}

.switch-item .control[type='checkbox']:checked:after {
    left: 39.1%;
}

.switch-item .control[type='checkbox']:checked:active:after {
    margin-left: -8px;
}

.switch-item .control[type='checkbox']:disabled {
    opacity: .3;
}

.switch-item .control[type='checkbox']:disabled:active:after {
    padding-right: 0;
    margin-left: 0;
}



.chat-setup-select-option {
    display: flex;
    flex-direction: row;
    /* border: 1px solid red; */
    gap: 2rem;
    align-items: center;
    width: 100%;
}

.inputfields-setup {
    display: flex;
    flex-direction: row;
    width: 50%;
    justify-content: space-between;
}

.setupfield1 {
    display: flex;
    flex-direction: row;
    width: 30%;
    align-items: flex-start;
    justify-content: space-between;
}

.setupfield2 {
    display: flex;
    align-items: flex-start;
    width: 50%;
    justify-content: space-between;
    /* align-items: center; */
    flex-direction: column;
    gap: 0.5rem;
}

.breaker {
    display: flex;
    width: 42%;
    justify-content: center;
    align-items: center;
    border: 1px solid gray;
    opacity: 0.1;

}

.community-setup {
    display: flex;
    flex-direction: row;
    width: 55%;
    justify-content: space-between;
}

.chat-setup-main select {
    border-bottom: 1px solid black;
}

label {
    font-size: 14px;
    line-height: 22px;
    font-weight: 400;
}

.setup-image {
    display: flex;
    flex-direction: row;
    /* border: 1px solid; */
    gap: 2rem;
    width: 30%;
    justify-content: space-between;
    height: 115px;

}

.setup-image-label {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}

.setup-image-desc {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
    /* border: 1px solid saddlebrown; */
}

.image-desc {
    width: 100%;
    border: 1px solid #D9D9D9;
    height: 99px;

}

.image-box {
    width: 99px;
    height: 99px;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #D9D9D9;
}

svg:hover {
    cursor: pointer;
}

.eventchat-container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    width: 50%;
    justify-content: flex-start;
    /* height: 115px; */
}

.eventchat-content {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

}

input[type="checkbox"]:checked {
    color: blue;
}

input[type="radio"]:checked {
    background-color: blue;
}

.setup-buttons {
    display: flex;
    flex-direction: row;
    width: 39%;
    justify-content: flex-end;
    align-items: center;
    gap: 1rem;
}

.setup-buttons-1 {
    height: 39.6px;
    width: 114px;
    border: 0.8px solid #434343;
    color: #434343;

}

.setup-buttons-2 {
    height: 40px;
    width: 114px;
    border: 1px solid #595959;
    background: #595959;
    color: #FFFFFF;
}

.setup-buttons-1:hover {
    border: 0.8px solid #377DD6;
    color: #377DD6;
    cursor: pointer;
}

.setup-buttons-2:hover {
    border: 0.8px solid #377DD6;
    color: #FFFFFF;
    background: #377DD6;
    cursor: pointer;
}

/* label{
     display: block;
      margin-bottom: 10px;
  } */

input[type=radio] {
    appearance: none;
    background-color: #fff;
    width: 15px;
    height: 15px;
    border: 2px solid #ccc;
    border-radius: 2px;
    display: inline-grid;
    place-content: center;
}

input[type=radio]::before {
    content: "";
    width: 10px;
    height: 10px;
    transform: scale(0);
    transform-origin: bottom left;
    background-color: #fff;
    clip-path: polygon(13% 50%, 34% 66%, 81% 2%, 100% 18%, 39% 100%, 0 71%);
}

input[type=radio]:checked::before {
    transform: scale(1);
}

input[type=radio]:checked {
    background-color: #0075FF;
    border: 2px solid #0075FF;
}

li.active {
    text-decoration: underline;
    color: #434343;
    text-decoration: underline;
    text-decoration-thickness: 3px;
    text-underline-offset: 6px;
    cursor: pointer;
}

li:hover {
    cursor: pointer;
}

::file-selector-button,.hidden {
  display: none;
}

/* .file-input{
    background: url('data:image/svg+xml,<svg width="17" height="16" viewBox="0 0 17 16" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M5.99996 0.166504L4.47496 1.83317H1.83329C0.916626 1.83317 0.166626 2.58317 0.166626 3.49984V13.4998C0.166626 14.4165 0.916626 15.1665 1.83329 15.1665H15.1666C16.0833 15.1665 16.8333 14.4165 16.8333 13.4998V3.49984C16.8333 2.58317 16.0833 1.83317 15.1666 1.83317H12.525L11 0.166504H5.99996ZM8.49996 12.6665C6.19996 12.6665 4.33329 10.7998 4.33329 8.49984C4.33329 6.19984 6.19996 4.33317 8.49996 4.33317C10.8 4.33317 12.6666 6.19984 12.6666 8.49984C12.6666 10.7998 10.8 12.6665 8.49996 12.6665Z" fill="black" fill-opacity="0.45" /> </svg>') no-repeat;
} */
</style>