<template>
    <div class="parent-form">
        <div>
            <h1 class="prof">Profile Setup</h1>
        </div>


        <div class="form">
            <div class="wrapper1">
                <div class="form-group">
                    <label class="first" for="usr"  style="align-self: flex-start;">First Name</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add first name">
                    <small class="form-text text-muted word">8/30</small>
                </div>
                <div class="form-group-2">
                    <label class="first" for="usr"  style="align-self: flex-start;">Last Name</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add last name">
                    <small class="form-text text-muted word">8/30</small>
                </div>
            </div>

            <div class="wrapper1">
                <div class="form-group-3">
                    <label class="first" for="usr"  style="align-self: flex-start;">Email Address</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add email address">
                    <p>
                        <label class="check">
                            <input type="checkbox" value="">
                            Show Email
                        </label>
                    </p>
                </div>
                <div class="form-group-4">
                    <label class="first" for="usr"  style="align-self: flex-start;">Phone Number</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add phone number">
                    <p>
                        <label class="check">
                            <input type="checkbox" value="">
                            Show Number
                        </label>
                    </p>
                </div>
            </div>


            <div class="form-group-5">
                <label class="first" for="comment"  style="align-self: flex-start;">About me</label>
                <textarea class="form-control" rows="5" id="comment" placeholder="Write something about yourself"
                    style="border:1px solid black; padding:0.5rem"></textarea>
            </div>

            <div class="wrapper1">
                <div class="form-group-6">
                    <label class="first" for="usr"  style="align-self: flex-start;">Company</label>
                    <input type="text" class="form-control" style="border:1px solid black; padding:0.5rem" id="usr"
                        placeholder="Add Company Name">
                </div>

                <div class="form-group-7">
                    <label class="first" for="usr" style="align-self: flex-start;">Interest Matching:(Select all the apply)</label>
                    <!-- <input type="text" class="form-control pla-dropdown" id="usr" placeholder="Choose Interest"> -->
                    <select id="interest" name="Interest" style="border:1px solid black; padding:0.5rem">
                        <option value="volvo">interest 1</option>
                        <option value="saab">interest 2</option>
                        <option value="fiat">interest 3</option>
                        <option value="audi">interest 4</option>
                    </select>
                </div>
            </div>


            <div class="wrapper1">
                <div class="form-group-8">
                    <label class="first" for="usr"  style="align-self: flex-start;">Title</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add Company Name">
                </div>



                <div class="form-group-9">
                    <label class="first" for="usr" style="align-self: flex-start;">Skill</label>
                    <!-- <input type="text" class="form-control pla-dropdown" id="usr" placeholder="Choose Skill"> -->
                    <select id="skill" name="skill" style="border:1px solid black; padding:0.5rem">
                        <option value="volvo">skill 1</option>
                        <option value="saab">skill 2</option>
                        <option value="fiat">skill 3</option>
                        <option value="audi">skill 4</option>
                    </select>
                </div>
            </div>

            <div class="wrapper1">
                <div class="form-group-10">
                    <label class="first" for="usr"  style="align-self: flex-start;">Website</label>
                    <input type="text" style="border:1px solid black; padding:0.5rem" class="form-control" id="usr"
                        placeholder="Add Company's website link">
                </div>


                <div class="form-group-11">
                    <label class="first" for="usr"  style="align-self: flex-start;">Level</label>
                    <!-- <input type="text" class="form-control pla-dropdown" id="usr" placeholder="Choose level"> -->
                    <select id="level" name="level" style="border:1px solid black; padding:0.5rem">
                        <option value="volvo">level 1</option>
                        <option value="saab">level 2</option>
                        <option value="fiat">level 3</option>
                        <option value="audi">level 4</option>
                    </select>

                </div>
            </div>


        </div>
    </div>
</template>

<!-- /* form ============================================= */ -->

<style scoped>

.prof{
    font-family: 'poppins';
    font-size: 20px;
    font-weight: 500;
    line-height: 22px;
}

.parent-form {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 1rem;
    font-family: 'poppins';
}


.form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: flex-start;
    width: 70%;
    gap: 2rem;
    flex-wrap: wrap;
}

.wrapper1 {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    /* border: 1px solid saddlebrown; */
}

.form input {
    background-color: transparent;
    border-style: none;
    color: inherit;
    border-bottom: 1px solid;
}

.form textarea {
    background-color: transparent;
    border-style: none;
    color: inherit;
    border-bottom: 1px solid;
    width: 100%;
}


.form-group {
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;

    /* border: 1px solid; */
    /* padding: 1rem; */

}

.form-group-2 {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;



}

.form-group-3 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

}

.form-group-4 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;


}

.form-group-5 {
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: flex-start;

}

.form-group-6 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

}

.form-group-7 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 37%;

}

select{
    width: 100%;
}

.form-group-8 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;


}

.form-group-9 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 37%;


}

.form-group-10 {
    display: flex;
    flex-direction: column;
    align-items: flex-start;


}

.form-group-11 {
    display: flex;
    flex-direction: column;
    width: 37%;

}



.form-control_1 {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 5px 12px;
    gap: 4px;
    width: 696px;
    height: 64px;
    left: 0px;
    top: 0px;
    background: #FFFFFF;
    border-radius: 2px;
}

.check {
    width: 101px;
    height: 22px;
    font-style: normal;
    font-weight: 400;
    font-size: 12px;
    line-height: 22px;
}


.word {
    width: 28px;
    /* height: 22px; */
    /* margin-left: 223px; */
    font-style: normal;
    font-size: 12px;
    line-height: 4px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    color: #8C8C8C;
    -webkit-box-ordinal-group: 2;
    -ms-flex-order: 1;
    order: 1;
    -webkit-box-flex: 0;
    -ms-flex-positive: 0;
    flex-grow: 0;
    text-align: left;
}

.words {
    width: 28px;
    height: 22px;
    margin-left: 258px;
    font-style: normal;
    font-size: 12px;
    line-height: 4px;
    display: flex;
    color: #8C8C8C;
    order: 1;
    flex-grow: 0;
}
</style>

<script>
export default {
    name: 'chatpage3'
}
</script>