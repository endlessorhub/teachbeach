import Home from './views/Home.vue'
import Teachers from './views/Teachers.vue'
import Register from '@/views/Register.vue'
import Learners from './views/Learners.vue'
import LearnersSearch from './views/LearnersSearch.vue'
import Venues from './views/Venues.vue'
import Classes from './views/Classes.vue'
import ClassList from './views/ClassList.vue'
import TeacherProfile from './views/ProfileTeacher.vue'
import CompanyProfile from './views/ProfileCompany2.vue'
import PasswordReset from './views/PasswordReset.vue'
import Dashboard from './views/Dashboard.vue'
import DashboardInbox from '@/components/Dashboard/Inbox/Index.vue'
import DashboardLearn from '@/components/Dashboard/Learn/Index.vue'
import DashboardLearnProfile from '@/components/Dashboard/Learn/Profile.vue'
import DashboardLearnClasses from '@/components/Dashboard/Learn/Classes.vue'
import DashboardLearnMemberships from '@/components/Dashboard/Learn/Memberships.vue'
import DashboardLearnCalendar from '@/components/Dashboard/Learn/Calendar.vue'
import DashboardLearnAccount from '@/components/Dashboard/Learn/Account.vue'
import DashboardTeach from '@/components/Dashboard/Teach/Index.vue'
import DashboardVenue from '@/components/Dashboard/Venue/Index.vue'
import DashboardTeachProfile from '@/components/Dashboard/Teach/Profile.vue'
import DashboardTeachClasses from '@/components/Dashboard/Teach/Classes.vue'
import DashboardTeachStudentsList from '@/components/Dashboard/Teach/StudentsList.vue'
import DashboardTeachStudentsRefund from '@/components/Dashboard/Teach/StudentsRefund.vue'
import DashboardTeachSchedCalendar from '@/components/Dashboard/Teach/SchedCalendar.vue'
import DashboardTeachSchedList from '@/components/Dashboard/Teach/SchedList.vue'
import DashboardTeachAccountTake from '@/components/Dashboard/Teach/AccountTake.vue'
import DashboardTeachAccountMake from '@/components/Dashboard/Teach/AccountMake.vue'
import DashboardTeachReports from '@/components/Dashboard/Teach/Reports.vue'
import DashboardTeachMembership from '@/components/Dashboard/Teach/Membership.vue'
import DashboardTeachMembershipSetUp from '@/components/Dashboard/Teach/MembershipSetUp.vue'
// import DashboardTeachMembershipDirectory from '@/components/Dashboard/Teach/MembershipDirectory'
import DashboardTeachHosts from '@/components/Dashboard/Teach/Hosts';
import DashboardTeachMembershipDirectory from '@/components/Dashboard/Teach/MembershipDirectory'
import UnauthTeacherConfirmLessons from '@/views/UnauthTeacherConfirmLessons'
import JoinAsMember from '@/views/JoinAsMember'
import TeacherCheckout from '@/views/TeacherCheckout'
import TeacherCheckout2 from '@/views/TeacherCheckout2'
import CompanyGroupClasses from '@/views/CompanyGroupClasses';
import ChooseModel from '@/views/ChooseModel'
import EmailUpsell from '@/views/EmailUpsell'
import CalendarUpsell from '@/views/CalendarUpsell'
import LearnerEnroll from '@/views/LearnerEnroll'
import TeachersPromo from '@/views/TeachersPromo'
import TestAddToCalendar from '@/views/test/AddToCalendar'
import TeacherFinish from '@/components/Teacher/Finish'
import TeacherGroupClassesCalendar from '@/views/TeacherGroupClassesCalendar'
import CompanyGroupClassesCalendar from '@/views/CompanyGroupClassesCalendar'
import PromoPage from '@/views/PromoPage'
import CompanyTeachers from '@/components/Dashboard/Teach/CompanyTeachers'
import DashboardTeachCustomers from '@/components/Dashboard/Teach/Customers'
import LearnerBuyMembership from '@/components/Learner/BuyMembership'
import BuyMembership from '@/views/BuyMembership'
import CompanyMembership from '@/views/CompanyMembership'
import DashboardLearnHistory from '@/components/Dashboard/Learn/History.vue'
import LearnerDiscussionSetup from '@/views/LearnerDiscussionSetup.vue'
import ChatViewAdmin from '@/views/ChatViewAdmin.vue'
import DiscussionViewLearner from '@/views/DiscussionViewLearner.vue'
// import SetUp from '@/views/SetUp.vue'
import DiscussionSetup from '@/views/DiscussionSetup'

// import chatpage3 from '@/views/chatpage3'
import Lreg1 from '@/components/Teacher/LReg1.vue'
import Lreg2 from '@/components/Teacher/LReg2.vue'
import Tprofile from '@/components/Teacher/Profile.vue'
import TeacherDashboard from '@/views/TeacherDashboard.vue'
import MemberView from '@/views/MemberView.vue'
// import DiscussionChatSetup from '@/views/LearnerChatSetup.vue'


import config from '@/config.js'
// import { component } from 'vue/types/umd'

export default [
  
    {
        path: '/',
        name: 'home',
        component: config.companySlug ? CompanyProfile : Home
    },
    {
        path: '/register',
        name: 'register',
        component: Register
    },
    {
        path: '/teachers',
        name: 'teachers',
        component: Teachers
    },
    {
        path: '/teachers/start',
        name: 'teachers_start',
        component: Teachers
    },
    {
        path: '/teachers/class/:id',
        name: 'teachers_class',
        component: Teachers
    },
    {
        path: '/teachers/copy_class/:id',
        name: 'teachers_copy_class',
        component: Teachers
    },
    {
        path: '/teachers/join',
        name: 'teachers_join',
        component: TeachersPromo
    },
 
    {
        path: '/teachers/light-register',
        name: 'teachers_light_reg1',
        component: Lreg1,
    },
    {
        path: '/teachers/company-or-individual',
        name: 'teachers_light_reg2',
        component: Lreg2,
    },
    {
        path: '/teachers/profile',
        name: 'teachers_join_profile',
        component: Tprofile,
    },
    {
        path: '/learners',
        name: 'learners',
        component: LearnersSearch,
    },
    {
        path: '/learners/membership/:class_id',
        name: 'learners_membership',
        component: LearnerBuyMembership,
        meta: { requiresAuth: true },
        props: function (route) {return { class_id: Number(route.params.class_id) }}
    },
    {
        path: '/learners/search/:city/:state/:category?/:subcategory?/:lessontype?',
        name: 'learners_search',
        component: LearnersSearch
    },
    {
        path: '/learners/search/:city/:state/:category?/:subcategory?/:lessontype?/:venue?',
        name: 'learners_search2',
        component: LearnersSearch
    },
    {
        path: '/search/:token',
        name: 'general_search',
        component: LearnersSearch
    },
    {
        path: '/learners/:id/:step',
        name: 'learners_step',
        component: Learners,
    },
    {
        path: '/learners/new_enroll/:id/:step/:order_id',
        name: 'learners_step',
        component: LearnerEnroll,
    },
    {
        path: '/learners/:id/:step/:order_id',
        name: 'learners_step_auth',
        component: Learners,
        meta: { requiresAuth: true },
    },
    {
        path: '/venues',
        name: 'venues',
        component: Venues
    },
    {
        path: '/password_reset/:token/:uidb64/',
        name: 'password_reset',
        component: PasswordReset
    },
    {
        path: '/class/:id',
        name: 'classpage',
        component: Classes
    },

    {
        path: '/teacher_profile/:id',
        name: 'teacher_profile',
        component: TeacherProfile
    },
    {
        path: '/company_profile/:id',
        name: 'company_profile',
        component: CompanyProfile
    },
    {
        path: '/company/:slug',
        name: 'company_profile_slug',
        component: CompanyProfile
    },
    {
        path: '/company_classes/group/:slug',
        name: 'company_classes_group_slug',
        component: CompanyGroupClasses,
    },
    {
        path: '/classes/:class_type/teacher/:teacher_id',
        name: 'teacher_classes',
        component: ClassList
    },
    {
        path: '/unauth_teacher/confirm_lessons/:hash',
        name: 'unauth_teacher_confirm_lessons',
        component: UnauthTeacherConfirmLessons
    },

    {
        path: '/dashboard',
        name: 'dashboard',
        redirect: '/dashboard/teach',
        component: Dashboard,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'teach',
                name: 'dashboard_teach',
                // component: TeacherDashboard,
                component: DashboardTeach,
                redirect: '/dashboard/teach/classes',
                children: [
                    {
                        path: 'profile',
                        name: 'dashboard_teach_profile',
                        component: DashboardTeachProfile,
                    },
                    {
                        path: 'schedule_calendar',
                        name: 'dashboard_teach_schedcal',
                        component: DashboardTeachSchedCalendar,
                    },
                    {
                        path: 'schedule_list',
                        name: 'dashboard_teach_schedlist',
                        component: DashboardTeachSchedList,
                    },
                    {
                        path: 'classes',
                        name: 'dashboard_teach_classes',
                        component: DashboardTeachClasses,
                    },
                    {
                        path: 'classes/:notification',
                        name: 'dashboard_teach_classes_notification',
                        component: DashboardTeachClasses,
                    },
                    {
                        path: 'students_list',
                        name: 'dashboard_teach_students_list',
                        component: DashboardTeachStudentsList,
                    },
                    {
                        path: 'students_refund',
                        name: 'dashboard_teach_students_refund',
                        component: DashboardTeachStudentsRefund,
                    },
                    {
                        path: 'account_take',
                        name: 'dashboard_teach_account_take',
                        component: DashboardTeachAccountTake,
                    },
                    {
                        path: 'account_make',
                        name: 'dashboard_teach_account_make',
                        component: DashboardTeachAccountMake,
                    },
                    {
                        path: 'reports',
                        name: 'dashboard_teach_reports',
                        component: DashboardTeachReports,
                    },
                    {
                        path: 'profile/teachers/:teacher_id?',
                        name: 'dashboard_teach_profile_teachers',
                        component: CompanyTeachers,
                        props: function (route) {return { teacher_id: Number(route.params.teacher_id) }}
                    },
                    {
                        path: 'new_crm',
                        name: 'dashboard_teach_customers',
                        component: DashboardTeachCustomers,
                    },
                    {
                        path: 'membership',
                        name: 'dashboard_teach_membership',
                        component: DashboardTeachMembership,
                    },
                    // {
                    //     path: 'membership-setup',
                    //     name: 'dashboard_teach_membership_setup',
                    //     component: DashboardTeachMembershipSetUp,
                    // },
                    {
                        path: 'membership-directory',
                        name: 'dashboard_teach_membership_directory',
                        component: DashboardTeachMembershipDirectory,
                    },
                    {
                        path: 'hosts',
                        name: 'dashboard_teach_hosts',
                        component: DashboardTeachHosts,
                    },
                ],

            },

            {
                path: '/learn',
                name: 'dashboard_learn',
                // component: Dashboard,
                redirect: '/dashboard/learn/classes',
                component: MemberView,
                children: [
                    
                    {
                        path: 'profile',
                        name: 'dashboard_learn_profile',
                        component: DashboardLearnProfile,
                    },
                    {
                        path: 'calendar',
                        name: 'dashboard_learn_calendar',
                        component: DashboardLearnCalendar,
                    },
                    {
                        path: 'classes',
                        name: 'dashboard_learn_classes',
                        component: DashboardLearnClasses,
                    },
                    {
                        path: 'classes/:notification',
                        name: 'dashboard_learn_classes_notification',
                        component: DashboardLearnClasses,
                    },
                    {
                        path: 'account',
                        name: 'dashboard_learn_account',
                        component: DashboardLearnAccount,
                    },
                    {
                        path: 'memberships',
                        name: 'dashboard_learn_memberships',
                        component: DashboardLearnMemberships,
                    },
                    {
                        path: 'history',
                        name: 'dashboard_learn_history',
                        component: DashboardLearnHistory,
                    },
                 
                ],
            },
          

            // {
            //     path: 'teach',
            //     name: 'dashboard_teach',
            //     component: DashboardLearn,
            //     redirect: '/dashboard/teach/TeacherChatDiscussion',
            //     children: [
            //         {
            //             path: 'TeacherChatDiscussion',
            //             name: 'TeacherChatDiscussion',
            //             component: TeacherChatDiscussion,
            //         },
            //     ]
            //     // {
            //     //     path:'/ChatDiscussion',
            //     //     name:'ChatDiscussion',
            //     //     component: ChatDiscussion
            //     // },
            // }

            {
                path: 'venue',
                name: 'dashboard_venue',
                component: DashboardVenue,
            },
            {
                path: 'inbox',
                name: 'dashboard_inbox',
                component: DashboardInbox,
            },
        ]

    },
    // {
    //     path:'/dashboard/teach',
    //     name:TeacherDashboard,
    //     component: TeacherDashboard
    // },
    {
        path: '/dashboard/teach/ChatView-Admin',
        name: 'ChatViewAdmin',
        component: ChatViewAdmin,
    },
    {
        path:'/dashboard/teach/DiscussionSetup',
        name: 'DiscussionSetup',
        component: DiscussionSetup
    },
    // {
    //     path: '/dashboard/learn/LearnerDiscussionSetup',
    //     name: 'LearnerDiscussionSetup',
    //     component: LearnerDiscussionSetup,
    // },
    // {
    //     path: '/dashboard/learn/DiscussionSetup',
    //     name: 'DiscussionSetup',
    //     component: DiscussionSetup,
    // },
    // {
    //     path: '/dashboard/learn/chat-setup',
    //     name: 'SetUp',
    //     component: SetUp
    // },
    {
        path: '/dashboard/learn/',
        name: 'MemberView',
        component: MemberView
    },
    {
        path:'/dashboard/learn/DiscussionViewLearner',
        name:'DiscussionViewLearner',
        component: DiscussionViewLearner
    },
    // {
    //     path: '/dashboard/learn/DiscussionChatSetup',
    //     name: 'DiscussionChatSetup',
    //     component: DiscussionChatSetup
    // },

    // {
    //     path: '/dashboard/teach/membership-directory',
    //     name: 'dashboard_teach_membership_directory',
    //     component: DashboardTeachMembershipDirectory,
    // },
   

    {
        path: '/join_as_member/:class_id',
        name: 'join_as_member',
        component: JoinAsMember,
        props: function (route) {return { class_id: Number(route.params.class_id) }}
    },
    {
        path: '/join_as_member',
        name: 'join_as_member',
        component: JoinAsMember,
    },
    {
        path: '/teacher_checkout/:option/:class_id',
        name: 'teacher_checkout',
        component: TeacherCheckout,
        props: function (route){
            const option = Number(route.params.option)
            return {
                option,
                class_id: Number(route.params.class_id),
            }
        }
    },
    {
        path: '/teacher_checkout/:option',
        name: 'teacher_checkout',
        component: TeacherCheckout,
        props: function (route) {return { option: Number(route.params.option) }}
    },
    {
        path: '/choose_model/:class_id',
        name: 'choose_model',
        component: ChooseModel,
        props: function (route) {return { class_id: Number(route.params.class_id) }}
    },
    {
        path: '/choose_model',
        name: 'choose_model',
        component: ChooseModel,
    },
    {
        path: '/email_upsell/:class_id',
        name: 'email_upsell',
        component: EmailUpsell,
        props: function (route) {return { class_id: Number(route.params.class_id) }}
    },
    {
        path: '/calendar_upsell/:class_id',
        name: 'calendar_upsell',
        component: CalendarUpsell,
        props: function (route) {return { class_id: Number(route.params.class_id) }}
    },
    {
        path: '/email_upsell',
        name: 'email_upsell',
        component: EmailUpsell,
    },
    {
        path: '/teachers_promo',
        name: 'teachers_promo',
        component: TeachersPromo,
    },
    {
        path: '/teacher_check/:class_id?',
        name: 'teacher_check',
        component: TeacherCheckout2,
    },
    {
        path: '/test_add_to_calendar',
        name: 'test_add_to_calendar',
        component: TestAddToCalendar,
        ignoreSitemap: true,
    },
    {
        path: '/teachers/finish/:class_id?',
        name: 'teachers_finish',
        component: TeacherFinish,
    },
    {
        path: '/teacher_group_calendar/:teacher_id',
        name: 'teacher_group_calendar',
        component: TeacherGroupClassesCalendar,
        props: function (route) {return { teacherId: Number(route.params.teacher_id) }}
    },
    {
        path: '/company_group_calendar/:company_id',
        name: 'company_group_calendar',
        component: CompanyGroupClassesCalendar,
        props: function (route) {return { companyId: Number(route.params.company_id) }}
    },
    {
        path: '/promo',
        name: 'promo_page',
        component: PromoPage,
    },
    {
        path: '/company/membership/:company_id',
        name: 'company_membership',
        component: CompanyMembership,
        meta: { requiresAuth: true },
        props: function (route) {return { company_id: Number(route.params.company_id) }}
    },
    {
        path: '/buy-membership/:id',
        name: 'buy_membership',
        component: BuyMembership,
        meta: { requiresAuth: true },
        props: function (route) {return { id: Number(route.params.id) }}
    },


]
