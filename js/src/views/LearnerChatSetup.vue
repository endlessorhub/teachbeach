<template>
    <div class="chat-setup-main">
        <div class="header-selection">
            <div class="setup-intro">
                <h2>Discussion Setup</h2>
                <p>Select how your members will connect on your website</p>
            </div>
            <div class="selector-options">
                <ul>
                    <li :class="{ 'active': activeItem === 'Community' }" @click="show('Community')">Community</li>
                    <li :class="{ 'active': activeItem === 'By event' }" @click="show('By event')">By event</li>
                    <li :class="{ 'active': activeItem === 'By Topic' }" @click="show('By Topic')">By Topic</li>
                </ul>
            </div>
        </div>


        <div class="chat-setup-select-option">
            <label for="switchA1" class="switch-item">
                <input type="checkbox" name="" id="switchA1" class="control" checked>
                <span class="label"></span>
            </label>
            <label>
                <input type="radio" name="" />
                Members only
            </label>
        </div>


        <div class="inputfields-setup">
            <div class="setupfield1">
                <label for="">Topic</label>
                <select placeholder="select topic" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Topic 1</option>
                    <option>topic 1</option>
                    <option>topic 1</option>
                    <option>topic 1</option>
                </select>
            </div>

            <div class="setupfield2">
                <label for="">Add co-host (optional)</label>
                <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                </select>
            </div>
        </div>

        <div class="breaker"></div>

        <div class="chat-setup-select-option">
            <label for="switchA1" class="switch-item">
                <input type="checkbox" name="" id="switchA1" class="control">
                <span class="label"></span>
            </label>
            <label>
                <input type="radio" name="" />
                All Concerns
            </label>
        </div>

        <div class="inputfields-setup">
            <div class="setupfield1">
                <label for="">Topic</label>
                <select placeholder="select topic" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Topic 1</option>
                    <option>topic 1</option>
                    <option>topic 1</option>
                    <option>topic 1</option>
                </select>
            </div>

            <div class="setupfield2">
                <label for="">Add co-host (optional)</label>
                <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                    <option>Add co-host</option>
                </select>
            </div>
        </div>

        <div class="breaker"></div>

        <h2>Community Discussion</h2>

        <div class="community-setup" style="align-items: center;">
            <div class="setup-radio-btns" style="display: flex; flex-direction: column;">
                <div class="setup-radiobtns_selector"
                    style="display: flex; flex-direction: row; align-items: center; gap: 1rem;">
                    <input type="radio" id="html" name="fav_language" value="Members">
                      <label for="html">Members Only</label>
                </div>
                <div class="setup-radiobtns_selector"
                    style="display: flex; flex-direction: row; align-items: center; gap: 1rem;">
                    <input type="radio" id="css" name="fav_language" value="All">
                      <label for="html">All</label>
                </div>  
            </div>

            <div class="setupfield2" >
                <label for="">Add Discussion moderator (optional)</label>
                <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Add Discussion moderator </option>
                    <option>Add Discussion moderator </option>
                    <option>Add Discussion moderator </option>
                    <option>Add Discussion moderator </option>
                </select>
            </div>
        </div>

        <div class="breaker"></div>

        <h2>Discussion</h2>

        <div class="setupfield1">
            <label for="">Add Discussion Topic</label>
            <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                <option>Add Discussion Topic 1</option>
                <option>Add Discussion Topic 2</option>
                <option>Add Discussion Topic 3</option>
                <option>Add Discussion Topic 4</option>
            </select>
        </div>




    </div>
</template>

<script>

export default {
    name: 'TeacherChatSetup',
    data() {
        return {
            activeItem: 'Community'
        };
    },
    methods: {
        show(val) {
            this.activeItem = val;
        }


    }
}
</script>



<!-- /* CHAT SETUP STYLING ============================================== */ -->

<style scoped>
h2 {
    margin-bottom: 0px;
}

.header-selection {
    display: flex;
    width: 75%;
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
    background-color: rgb(52, 199, 89);
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
}

.inputfields-setup {
    display: flex;
    flex-direction: row;
    width: 50%;
    justify-content: space-between;
}

.setupfield1 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.setupfield2 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

}

.breaker {
    display: flex;
    width: 60%;
    justify-content: center;
    align-items: center;
    border: 1px solid gray;
    opacity: 0.1;

}

.community-setup {
    display: flex;
    flex-direction: row;
    width: 50%;
    justify-content: space-between;
}

.chat-setup-main select {
    border-bottom: 1px solid black;
}


input[type="checkbox"]:checked {
    color: blue;
}


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

li:hover{
    cursor: pointer;
}



</style>