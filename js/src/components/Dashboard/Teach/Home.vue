<template>
    <content>
        <div class="dashboard-content-outer-div">
            <div class="main-card-header"><img src="../../../assets/left-border.svg" />View collaborations</div>
            <div class="cards-outer-div">
                <div class="card" @click="$router.push('/dashboard/teach/students_list')">
                    <img src="../../../assets/card_members.png" />
                    <div class="heading">Members (300)</div>
                </div>
                <div class="card" @click="$router.push('/dashboard/teach/classes?services')">
                    <img src="../../../assets/card_dm.png" />
                    <div class="heading">Services (5)</div>
                </div>
                <div class="card" @click="$router.push('/dashboard/teach/classes?events')">
                    <img src="../../../assets/card_discussion.png" />
                    <div class="heading">Events &amp; Classes</div>
                </div>
                <div class="card" @click="$router.push('/dashboard/teach/teacher-chat-discussion')">
                    <img src="../../../assets/card_events.png" />
                    <div class="heading">Discussions</div>
                </div>
            </div>
        </div>
    </content>
</template>


<style lang="scss" scoped>
.dashboard-content-outer-div {
    margin: 40px 48px;
    padding: 32px;
    background-color: white;
    border-radius: 10px;
    border: 1px solid #E9E9E9;
    min-height: 80vh;

    .main-card-header {
        font-weight: 900;
        font-size: 32px;
        line-height: 37px;
        color: var(--dark);

        img {
            margin-right: 8px;
        }
    }

    .cards-outer-div {
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        flex-wrap: wrap;
        gap: 48px;
        margin-top: 40px;

        .card {
            cursor: pointer;
            flex: 1;
            width: 100%;
            background: #FFFFFF;
            box-shadow: 0px 2.02179px 10.1089px rgba(65, 72, 86, 0.15);
            border-radius: 20.2179px;
            text-align: center;

            img {
                width: 100%;
                height: 100%;
            }

            .heading {
                font-weight: 900;
                font-size: 24px;
                line-height: 28px;
                color: var(--dark);
                padding: 20px;
                margin-top: -9px;
            }
        }
    }
}

@media(max-width:1560px) {
    .dashboard-content-outer-div {
        margin: 16px 16px;
        padding: 24px;
    }

    .dashboard-content-outer-div .cards-outer-div {
        gap: 20px;
    }

    .dashboard-content-outer-div .cards-outer-div .card .heading {
        font-size: 24px;
        padding: 32px 10px;
    }
}

@media(max-width:1280px) {
    .dashboard-content-outer-div .cards-outer-div .card .heading {
        font-size: 18px;
        padding: 20px 12px;
    }
}

@media(max-width:1024.99px) {
    .dashboard-content-outer-div .cards-outer-div {
        justify-content: space-around;
    }

    .dashboard-content-outer-div .cards-outer-div .card {
        width: 45%;
        flex: unset;
    }
}

@media(max-width:768px) {
    .dashboard-content-outer-div .cards-outer-div .card {
        width: 70%;
        flex: unset;
    }
}

@media(max-width:575px) {
    .dashboard-content-outer-div .cards-outer-div .card {
        width: 95%;
        flex: unset;
    }
}
</style>