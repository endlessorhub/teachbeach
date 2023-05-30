<template>
    <div class="chat-setup-main">
        <div class="setup-intro">
            <h2>Chat Setup</h2>
            <p>Select how your members will connect on your website</p>
        </div>


        <div class="chat-setup-select-option">
            <label for="switchA1" class="switch-item">
                <input type="checkbox" name="" id="switchA1" class="control" checked>
                <span class="label"></span>
            </label>
            <label>
                <input type="checkbox" name="checkbox" />
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
                <input type="checkbox" name="checkbox" />
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

        <h2>Community Chat</h2>

        <div class="community-setup" style="align-items: center;">
            <div class="setupfield1" style="flex-direction: row; gap: 1rem; align-items: center; justify-content: space-between;">
                <!-- <label>
                    <input type="checkbox" name="checkbox" />
                    Members only
                </label>
                <label>
                    <input type="checkbox" name="checkbox" />
                    All
                </label> -->
                <input type="radio" id="html" name="fav_language" value="HTML">
                  <label for="html">Members only</label>
                  <input type="radio" id="css" name="fav_language" value="CSS">
                  <label for="css">All</label>
            </div>

            <div class="setupfield2">
                <label for="">Add chat moderator (optional)</label>
                <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                    <option>Add chat moderator </option>
                    <option>Add chat moderator </option>
                    <option>Add chat moderator </option>
                    <option>Add chat moderator </option>
                </select>
            </div>
        </div>

        <div class="breaker"></div>

        <h2>Event Chat</h2>

        <div class="setupfield1">
            <label for="">Add chat Topic</label>
            <select placeholder="Add co-host" style="border: 1px solid black; padding:0.5rem; width: 200px;">
                <option>Add chat Topic </option>
                <option>Add chat Topic </option>
                <option>Add chat Topic </option>
                <option>Add chat Topic </option>
            </select>
        </div>




    </div>
</template>

<script>

export default {
    name: 'SetUp',
}
</script>


<!-- /* CHAT SETUP STYLING ============================================== */ -->
<style scoped>
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
    background-color: royalblue;
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
    width: 55%;
    justify-content: space-between;
}

.chat-setup-main select {
    border-bottom: 1px solid black;
}
</style>